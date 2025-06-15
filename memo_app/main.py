# FastAPIを使ったメモ帳アプリケーション
# このファイルは、メモの作成・読み取り・更新・削除ができるWebAPIを提供します

# 必要なライブラリをインポートします
from fastapi import FastAPI, HTTPException, Depends  # FastAPI: Webフレームワーク、HTTPException: エラー処理、Depends: 依存性注入
from fastapi.middleware.cors import CORSMiddleware  # CORS: 異なるドメインからのアクセスを許可
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text  # SQLAlchemy: データベース操作用ライブラリ
from sqlalchemy.orm import declarative_base, sessionmaker, Session  # データベースモデルとセッション管理用
from pydantic import BaseModel  # データ検証用の基底クラス
from datetime import datetime  # 日時を扱うためのクラス
from typing import List, Optional  # 型ヒント用（リストやオプショナル値の型定義）

# FastAPIアプリケーションのインスタンスを作成
# title: APIのタイトル、version: APIのバージョン
app = FastAPI(title="メモ帳アプリ", version="1.0.0")

# CORS（Cross-Origin Resource Sharing）の設定
# 異なるドメインやポートからのアクセスを許可します
# 例：フロントエンドが http://localhost:3000 で、APIが http://localhost:8000 の場合
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # すべてのオリジンを許可（開発用。本番環境では特定のドメインのみ許可すべき）
    allow_credentials=True,    # クッキーを含むリクエストを許可
    allow_methods=["*"],       # すべてのHTTPメソッド（GET, POST, PUT, DELETE等）を許可
    allow_headers=["*"],       # すべてのヘッダーを許可
)

# データベースの接続URL
# SQLiteを使用（ファイルベースの軽量データベース）
# "sqlite:///./memo_app.db" は現在のディレクトリにmemo_app.dbファイルを作成
SQLALCHEMY_DATABASE_URL = "sqlite:///./memo_app.db"

# データベースエンジンの作成
# エンジンはデータベースとの接続を管理します
# check_same_thread=False: SQLiteで複数スレッドからのアクセスを許可
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# セッションファクトリーの作成
# セッションはデータベースとのやり取りを管理する単位
# autocommit=False: 自動コミットを無効化（明示的にcommit()を呼ぶ必要がある）
# autoflush=False: 自動フラッシュを無効化（明示的にflush()を呼ぶ必要がある）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# すべてのデータベースモデルの基底クラス
# このクラスを継承してテーブルを定義します
Base = declarative_base()


# データベースのテーブル定義（SQLAlchemyのモデル）
# このクラスが「memos」テーブルの構造を定義します
class Memo(Base):
    __tablename__ = "memos"  # データベース上のテーブル名

    # id: 主キー（各メモを一意に識別する番号）
    # primary_key=True: この列が主キーであることを示す
    # index=True: 検索を高速化するためのインデックスを作成
    id = Column(Integer, primary_key=True, index=True)
    
    # title: メモのタイトル（最大100文字）
    # nullable=False: NULL値を許可しない（必須項目）
    title = Column(String(100), nullable=False)
    
    # content: メモの本文（文字数制限なし）
    content = Column(Text, nullable=False)
    
    # created_at: 作成日時（自動的に現在時刻が設定される）
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # updated_at: 更新日時（作成時と更新時に自動的に現在時刻が設定される）
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# データベースにテーブルを作成
# 上で定義したMemoクラスに基づいて、実際のテーブルを作成します
# すでにテーブルが存在する場合は何もしません
Base.metadata.create_all(bind=engine)


# Pydanticモデルの定義（APIのリクエスト/レスポンスの型定義）
# これらのクラスは、APIで送受信するデータの形式を定義します

# メモの基本構造（titleとcontentを持つ）
class MemoBase(BaseModel):
    title: str      # タイトル（文字列型）
    content: str    # 本文（文字列型）


# メモ作成時のリクエストボディの型
# MemoBaseを継承しているので、titleとcontentが必須
class MemoCreate(MemoBase):
    pass  # 追加のフィールドは不要なのでpassと書く


# メモ更新時のリクエストボディの型
# Optional[str] = None により、フィールドは省略可能（部分更新が可能）
class MemoUpdate(BaseModel):
    title: Optional[str] = None    # タイトル（省略可能）
    content: Optional[str] = None  # 本文（省略可能）


# メモ取得時のレスポンスの型
# MemoBaseに加えて、id、created_at、updated_atも含む
class MemoResponse(MemoBase):
    id: int                # メモのID
    created_at: datetime   # 作成日時
    updated_at: datetime   # 更新日時

    class Config:
        # SQLAlchemyのモデルから自動的に値を読み取れるようにする設定
        from_attributes = True


# データベースセッションを取得する関数
# FastAPIの依存性注入システムで使用されます
# この関数により、各リクエストで新しいデータベースセッションが作成され、
# リクエスト終了時に自動的にクローズされます
def get_db():
    db = SessionLocal()  # 新しいセッションを作成
    try:
        yield db         # セッションを提供（yieldは値を返しつつ、処理を一時停止）
    finally:
        db.close()       # 処理が終わったらセッションを閉じる


# ルートエンドポイント（トップページ）
# HTTPメソッド: GET
# パス: /
# 用途: APIが正常に動作していることを確認するための簡単なメッセージを返す
@app.get("/")
def read_root():
    return {"message": "メモ帳アプリへようこそ！"}


# メモ作成エンドポイント
# HTTPメソッド: POST
# パス: /memos/
# 用途: 新しいメモをデータベースに保存する
# response_model: レスポンスの型をMemoResponseに指定
@app.post("/memos/", response_model=MemoResponse)
def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    # 受け取ったデータからデータベースモデルのインスタンスを作成
    db_memo = Memo(title=memo.title, content=memo.content)
    
    # データベースセッションに新しいメモを追加
    db.add(db_memo)
    
    # 変更をデータベースに保存（コミット）
    db.commit()
    
    # データベースから最新のデータを取得（IDや作成日時などが自動設定される）
    db.refresh(db_memo)
    
    # 作成したメモを返す
    return db_memo


# メモ一覧取得エンドポイント
# HTTPメソッド: GET
# パス: /memos/
# 用途: 保存されているメモの一覧を取得する
# response_model: MemoResponseのリストを返すことを指定
@app.get("/memos/", response_model=List[MemoResponse])
def read_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # skip: 最初の何件をスキップするか（ページネーション用）
    # limit: 最大何件取得するか（デフォルト100件）
    # 例: skip=20, limit=10 の場合、21件目から30件目を取得
    
    # データベースからメモを取得
    # offset(skip): 指定した件数をスキップ
    # limit(limit): 指定した件数まで取得
    # all(): すべての結果を取得
    memos = db.query(Memo).offset(skip).limit(limit).all()
    return memos


# 特定のメモ取得エンドポイント
# HTTPメソッド: GET
# パス: /memos/{memo_id}
# 用途: 指定されたIDのメモを取得する
# {memo_id}: パスパラメータ（URLの一部として指定）
@app.get("/memos/{memo_id}", response_model=MemoResponse)
def read_memo(memo_id: int, db: Session = Depends(get_db)):
    # 指定されたIDのメモをデータベースから検索
    # filter(): 検索条件を指定
    # first(): 最初の1件を取得（該当なしの場合はNone）
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    
    # メモが見つからない場合は404エラーを返す
    if memo is None:
        raise HTTPException(status_code=404, detail="メモが見つかりません")
    
    return memo


# メモ更新エンドポイント
# HTTPメソッド: PUT
# パス: /memos/{memo_id}
# 用途: 指定されたIDのメモを更新する
@app.put("/memos/{memo_id}", response_model=MemoResponse)
def update_memo(memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    # 更新対象のメモをデータベースから取得
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    
    # メモが見つからない場合は404エラーを返す
    if db_memo is None:
        raise HTTPException(status_code=404, detail="メモが見つかりません")
    
    # 部分更新の実装
    # リクエストに含まれるフィールドのみを更新（Noneでないもののみ）
    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None:
        db_memo.content = memo.content
    
    # 更新日時を現在時刻に設定
    db_memo.updated_at = datetime.utcnow()
    
    # 変更をデータベースに保存
    db.commit()
    
    # 最新のデータを取得
    db.refresh(db_memo)
    
    return db_memo


# メモ削除エンドポイント
# HTTPメソッド: DELETE
# パス: /memos/{memo_id}
# 用途: 指定されたIDのメモを削除する
@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    # 削除対象のメモをデータベースから取得
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    
    # メモが見つからない場合は404エラーを返す
    if db_memo is None:
        raise HTTPException(status_code=404, detail="メモが見つかりません")
    
    # データベースからメモを削除
    db.delete(db_memo)
    
    # 変更をデータベースに保存
    db.commit()
    
    # 削除完了メッセージを返す
    return {"message": "メモが削除されました"}


# メモ検索エンドポイント
# HTTPメソッド: GET
# パス: /memos/search/
# 用途: キーワードでメモを検索する
# 注意: このパスは /memos/{memo_id} より前に定義する必要がある
#      （そうしないと "search" がmemo_idとして解釈されてしまう）
@app.get("/memos/search/", response_model=List[MemoResponse])
def search_memos(q: str, db: Session = Depends(get_db)):
    # q: 検索キーワード（クエリパラメータとして受け取る）
    # 例: /memos/search/?q=買い物
    
    # タイトルまたは本文に検索キーワードを含むメモを検索
    # contains(): 部分一致検索（大文字小文字を区別）
    # |: OR条件（タイトルか本文のどちらかに含まれていればOK）
    memos = db.query(Memo).filter(
        (Memo.title.contains(q)) | (Memo.content.contains(q))
    ).all()
    
    return memos