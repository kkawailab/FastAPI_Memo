# 📝 FastAPIメモ帳アプリケーション

高性能WebフレームワークFastAPIを使用した、実践的なメモ帳アプリケーションです。このアプリケーションは、REST APIの設計からデータベース操作まで、Webアプリケーション開発の基本を学べる教材として設計されています。

🔗 **FastAPIについての詳細は [FastAPI完全ガイド](../README.md) をご覧ください。**

## 📋 目次

1. [アプリケーション概要](#-アプリケーション概要)
2. [アーキテクチャ](#-アーキテクチャ)
3. [機能詳細](#-機能詳細)
4. [API仕様](#-api仕様)
5. [データモデル](#-データモデル)
6. [セットアップガイド](#-セットアップガイド)
7. [使用方法](#-使用方法)
8. [Webクライアント](#-webクライアント)
9. [開発ガイド](#-開発ガイド)
10. [テスト方法](#-テスト方法)
11. [デプロイメント](#-デプロイメント)
12. [カスタマイズ例](#-カスタマイズ例)
13. [トラブルシューティング](#-トラブルシューティング)
14. [今後の拡張案](#-今後の拡張案)

## 🌟 アプリケーション概要

このメモ帳アプリケーションは、日常的なメモ管理のニーズに応える実用的なWebアプリケーションです。シンプルながら拡張性の高い設計により、学習用途から実際の業務まで幅広く活用できます。

### 主な特徴

- **RESTful API**: 業界標準のREST設計原則に従った実装
- **リアルタイムレスポンス**: FastAPIの高速性を活かした快適な操作性
- **データ永続化**: SQLiteによる確実なデータ保存
- **型安全**: Pydanticによる厳密なデータ検証
- **自動ドキュメント**: Swagger UIによる対話的なAPI探索
- **モダンなWebUI**: レスポンシブデザインの直感的なインターフェース

### このアプリで学べること

1. **FastAPIの基礎**
   - ルーティングとエンドポイント設計
   - リクエスト/レスポンスの処理
   - エラーハンドリング
   - ミドルウェアの使用

2. **データベース操作**
   - SQLAlchemy ORMの使用方法
   - CRUD操作の実装
   - データベースセッション管理
   - マイグレーション戦略

3. **API設計**
   - RESTful原則の実践
   - HTTPステータスコードの適切な使用
   - ページネーションの実装
   - 検索機能の設計

4. **Webアプリケーション開発**
   - フロントエンドとバックエンドの連携
   - CORS設定
   - 非同期JavaScript（Fetch API）
   - レスポンシブデザイン

## 🏗️ アーキテクチャ

### システム構成図

```
┌─────────────────────────────────────────────────────────┐
│                     Webブラウザ                          │
│  ┌─────────────────┐    ┌──────────────────────────┐  │
│  │   index.html    │    │  Swagger UI / ReDoc      │  │
│  │   style.css     │    │  (API Documentation)     │  │
│  │   app.js        │    └──────────────────────────┘  │
│  └─────────────────┘                                   │
└────────────────────┬───────────────────────────────────┘
                     │ HTTP/HTTPS
                     │ (CORS enabled)
┌────────────────────▼───────────────────────────────────┐
│                  FastAPI Application                    │
│  ┌─────────────────────────────────────────────────┐  │
│  │               API Endpoints                      │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────────┐  │  │
│  │  │  POST   │ │   GET   │ │  PUT/DELETE     │  │  │
│  │  │ /memos/ │ │ /memos/ │ │ /memos/{id}    │  │  │
│  │  └─────────┘ └─────────┘ └─────────────────┘  │  │
│  └─────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────┐  │
│  │            Pydantic Models                       │  │
│  │  ┌───────────┐ ┌────────────┐ ┌─────────────┐ │  │
│  │  │MemoCreate │ │MemoUpdate  │ │MemoResponse │ │  │
│  │  └───────────┘ └────────────┘ └─────────────┘ │  │
│  └─────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────┐  │
│  │             SQLAlchemy ORM                       │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │          Memo Model                      │   │  │
│  │  │  - id: Integer (Primary Key)            │   │  │
│  │  │  - title: String(100)                   │   │  │
│  │  │  - content: Text                        │   │  │
│  │  │  - created_at: DateTime                 │   │  │
│  │  │  - updated_at: DateTime                 │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                  SQLite Database                        │
│                   memo_app.db                          │
└────────────────────────────────────────────────────────┘
```

### レイヤー構造

1. **プレゼンテーション層**
   - HTML/CSS/JavaScript によるWebクライアント
   - Swagger UI / ReDoc によるAPIドキュメント

2. **API層**
   - FastAPIによるHTTPエンドポイント
   - リクエスト/レスポンスの処理
   - バリデーションとエラーハンドリング

3. **ビジネスロジック層**
   - CRUD操作の実装
   - 検索ロジック
   - データ変換処理

4. **データアクセス層**
   - SQLAlchemy ORM
   - データベースセッション管理
   - クエリ最適化

5. **データ永続化層**
   - SQLiteデータベース
   - 自動マイグレーション

## ✨ 機能詳細

### 1. メモの作成（Create）

新しいメモを作成する機能です。

**特徴:**
- タイトルと本文の入力
- 自動的なタイムスタンプ付与
- 入力検証（タイトルは必須、最大100文字）
- 作成成功時に完全なメモ情報を返却

**使用例:**
```python
# Python での使用例
import requests

response = requests.post(
    "http://localhost:8000/memos/",
    json={
        "title": "会議メモ",
        "content": "明日の会議は10時から。資料の準備を忘れずに。"
    }
)
memo = response.json()
print(f"作成されたメモID: {memo['id']}")
```

### 2. メモの一覧表示（Read - List）

保存されているすべてのメモを取得します。

**特徴:**
- ページネーション対応（skip/limit パラメータ）
- 作成日時の降順でソート
- 大量データにも対応

**使用例:**
```bash
# 最初の10件を取得
curl "http://localhost:8000/memos/?skip=0&limit=10"

# 11件目から20件目を取得
curl "http://localhost:8000/memos/?skip=10&limit=10"
```

### 3. メモの個別取得（Read - Detail）

特定のメモの詳細情報を取得します。

**特徴:**
- IDによる高速検索
- 存在しないIDの場合は404エラー
- 完全なメモ情報の取得

### 4. メモの更新（Update）

既存のメモを編集します。

**特徴:**
- 部分更新対応（タイトルのみ、本文のみの更新が可能）
- 更新日時の自動更新
- 楽観的ロック非対応（将来の拡張ポイント）

**使用例:**
```python
# タイトルのみを更新
response = requests.put(
    "http://localhost:8000/memos/1",
    json={"title": "会議メモ（更新済み）"}
)

# 本文のみを更新
response = requests.put(
    "http://localhost:8000/memos/1",
    json={"content": "会議は11時に変更になりました。"}
)
```

### 5. メモの削除（Delete）

不要なメモを削除します。

**特徴:**
- 物理削除（データベースから完全に削除）
- 削除確認メッセージの返却
- 存在しないIDの場合は404エラー

### 6. メモの検索

キーワードによるメモの検索機能です。

**特徴:**
- タイトルと本文の両方から検索
- 部分一致検索
- 大文字小文字を区別
- 検索結果は作成日時の降順

**使用例:**
```bash
# "会議"を含むメモを検索
curl "http://localhost:8000/memos/search/?q=会議"

# URLエンコードが必要な場合
curl "http://localhost:8000/memos/search/?q=%E4%BC%9A%E8%AD%B0"
```

## 📡 API仕様

### エンドポイント一覧

| メソッド | エンドポイント | 説明 | リクエストボディ | クエリパラメータ |
|---------|---------------|------|-----------------|-----------------|
| GET | `/` | ウェルカムメッセージ | - | - |
| POST | `/memos/` | メモ作成 | `MemoCreate` | - |
| GET | `/memos/` | メモ一覧取得 | - | `skip`, `limit` |
| GET | `/memos/{memo_id}` | メモ個別取得 | - | - |
| PUT | `/memos/{memo_id}` | メモ更新 | `MemoUpdate` | - |
| DELETE | `/memos/{memo_id}` | メモ削除 | - | - |
| GET | `/memos/search/` | メモ検索 | - | `q` |

### リクエスト/レスポンス仕様

#### MemoCreate (リクエストボディ)
```json
{
  "title": "string",      // 必須、1-100文字
  "content": "string"     // オプション、デフォルト空文字
}
```

#### MemoUpdate (リクエストボディ)
```json
{
  "title": "string",      // オプション、1-100文字
  "content": "string"     // オプション
}
```

#### MemoResponse (レスポンス)
```json
{
  "id": 1,
  "title": "メモのタイトル",
  "content": "メモの内容",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

### HTTPステータスコード

| コード | 説明 | 使用場面 |
|--------|------|----------|
| 200 | OK | 正常な取得、更新、削除 |
| 201 | Created | メモの作成成功 |
| 400 | Bad Request | 不正なリクエスト |
| 404 | Not Found | 存在しないメモへのアクセス |
| 422 | Unprocessable Entity | バリデーションエラー |
| 500 | Internal Server Error | サーバーエラー |

## 💾 データモデル

### Memoテーブル

```sql
CREATE TABLE memos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### SQLAlchemyモデル

```python
class Memo(Base):
    __tablename__ = "memos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Pydanticスキーマ

```python
# 基底スキーマ
class MemoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = ""

# 作成用スキーマ
class MemoCreate(MemoBase):
    pass

# 更新用スキーマ
class MemoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None

# レスポンス用スキーマ
class MemoResponse(MemoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

## 🚀 セットアップガイド

### 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）
- Git（オプション）

### 手順

1. **リポジトリのクローン（Gitを使用する場合）**
```bash
git clone https://github.com/yourusername/FastAPI_Memo.git
cd FastAPI_Memo/memo_app
```

2. **仮想環境の作成（推奨）**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **アプリケーションの起動**
```bash
uvicorn main:app --reload
```

5. **動作確認**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 使用方法

### 1. Swagger UIを使った操作

最も簡単な方法は、Swagger UIを使用することです。

1. ブラウザで http://localhost:8000/docs にアクセス
2. 使いたいエンドポイントをクリック
3. "Try it out" ボタンをクリック
4. パラメータを入力
5. "Execute" ボタンをクリック

### 2. curlコマンドを使った操作

```bash
# メモの作成
curl -X POST "http://localhost:8000/memos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "テストメモ", "content": "これはテストです"}'

# メモ一覧の取得
curl "http://localhost:8000/memos/"

# 特定のメモの取得
curl "http://localhost:8000/memos/1"

# メモの更新
curl -X PUT "http://localhost:8000/memos/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "更新されたメモ"}'

# メモの削除
curl -X DELETE "http://localhost:8000/memos/1"

# メモの検索
curl "http://localhost:8000/memos/search/?q=テスト"
```

### 3. Pythonスクリプトから使用

```python
import requests
import json

# APIのベースURL
BASE_URL = "http://localhost:8000"

# メモの作成
def create_memo(title, content=""):
    response = requests.post(
        f"{BASE_URL}/memos/",
        json={"title": title, "content": content}
    )
    return response.json()

# メモの一覧取得
def get_memos(skip=0, limit=10):
    response = requests.get(
        f"{BASE_URL}/memos/",
        params={"skip": skip, "limit": limit}
    )
    return response.json()

# メモの検索
def search_memos(query):
    response = requests.get(
        f"{BASE_URL}/memos/search/",
        params={"q": query}
    )
    return response.json()

# 使用例
if __name__ == "__main__":
    # 新しいメモを作成
    memo = create_memo("Pythonからのメモ", "APIを使って作成しました")
    print(f"作成されたメモ: {memo}")
    
    # メモ一覧を取得
    memos = get_memos()
    print(f"メモ一覧: {len(memos)}件")
    
    # メモを検索
    results = search_memos("Python")
    print(f"検索結果: {len(results)}件")
```

## 🌐 Webクライアント

### 概要

本アプリケーションには、モダンなWebクライアントが付属しています。

### 機能

- **レスポンシブデザイン**: PC、タブレット、スマートフォンに対応
- **リアルタイム更新**: APIとの即座な同期
- **直感的なUI**: ドラッグ＆ドロップ非対応だが使いやすいインターフェース
- **モーダル編集**: ポップアップウィンドウでの編集
- **検索機能**: インクリメンタルサーチ非対応だが高速検索

### ファイル構成

```
memo_app/
├── index.html    # メインHTMLファイル
├── style.css     # スタイルシート
└── app.js        # JavaScriptロジック
```

### 起動方法

1. **直接ファイルを開く方法**
```bash
# ファイルエクスプローラーで index.html をダブルクリック
```

2. **HTTPサーバーを使う方法**
```bash
# Python標準のHTTPサーバー
cd memo_app
python -m http.server 8080

# Node.jsのhttp-server
npx http-server -p 8080
```

### カスタマイズポイント

1. **デザインの変更** (style.css)
```css
/* カラースキームの変更 */
:root {
    --primary-color: #007bff;  /* メインカラー */
    --secondary-color: #6c757d; /* サブカラー */
    --background-color: #f8f9fa; /* 背景色 */
}
```

2. **API URLの変更** (app.js)
```javascript
// 本番環境のURLに変更
const API_URL = 'https://api.example.com';
```

## 🔧 開発ガイド

### コード規約

1. **命名規則**
   - 関数名: snake_case（例: `get_memo_by_id`）
   - クラス名: PascalCase（例: `MemoResponse`）
   - 定数: UPPER_SNAKE_CASE（例: `DATABASE_URL`）

2. **インポート順序**
   ```python
   # 標準ライブラリ
   from datetime import datetime
   from typing import List, Optional
   
   # サードパーティライブラリ
   from fastapi import FastAPI, HTTPException
   from sqlalchemy import create_engine
   
   # ローカルモジュール
   from .models import Memo
   ```

3. **エラーハンドリング**
   ```python
   # 明示的なエラーメッセージ
   if not memo:
       raise HTTPException(
           status_code=404,
           detail=f"ID {memo_id} のメモが見つかりません"
       )
   ```

### デバッグ方法

1. **ログの追加**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/memos/")
def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    logger.debug(f"Creating memo: {memo.title}")
    # ... 処理 ...
```

2. **デバッガーの使用**
```python
# pdbを使用
import pdb

def some_function():
    pdb.set_trace()  # ここでブレークポイント
    # ... 処理 ...
```

3. **SQLクエリの確認**
```python
# SQLAlchemyのクエリログを有効化
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  # SQLログを出力
)
```

## 🧪 テスト方法

### 単体テストの作成

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_memo():
    """メモ作成のテスト"""
    response = client.post(
        "/memos/",
        json={"title": "テストメモ", "content": "テスト内容"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "テストメモ"
    assert "id" in data

def test_get_memo():
    """メモ取得のテスト"""
    # まずメモを作成
    create_response = client.post(
        "/memos/",
        json={"title": "取得テスト", "content": "内容"}
    )
    memo_id = create_response.json()["id"]
    
    # 作成したメモを取得
    response = client.get(f"/memos/{memo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == memo_id
    assert data["title"] == "取得テスト"

def test_update_memo():
    """メモ更新のテスト"""
    # メモを作成
    create_response = client.post(
        "/memos/",
        json={"title": "更新前", "content": "古い内容"}
    )
    memo_id = create_response.json()["id"]
    
    # メモを更新
    response = client.put(
        f"/memos/{memo_id}",
        json={"title": "更新後"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新後"
    assert data["content"] == "古い内容"  # contentは変更していない

def test_delete_memo():
    """メモ削除のテスト"""
    # メモを作成
    create_response = client.post(
        "/memos/",
        json={"title": "削除テスト", "content": "削除される"}
    )
    memo_id = create_response.json()["id"]
    
    # メモを削除
    response = client.delete(f"/memos/{memo_id}")
    assert response.status_code == 200
    
    # 削除されたことを確認
    get_response = client.get(f"/memos/{memo_id}")
    assert get_response.status_code == 404

def test_search_memos():
    """メモ検索のテスト"""
    # テスト用のメモを作成
    client.post("/memos/", json={"title": "Python入門", "content": "基礎から学ぶ"})
    client.post("/memos/", json={"title": "JavaScript", "content": "Webフロントエンド"})
    
    # 検索実行
    response = client.get("/memos/search/?q=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Python" in memo["title"] for memo in data)
```

### テストの実行

```bash
# pytestのインストール
pip install pytest

# テストの実行
pytest test_main.py -v

# カバレッジレポート付きで実行
pip install pytest-cov
pytest test_main.py --cov=main --cov-report=html
```

## 🚢 デプロイメント

### 1. Docker を使用したデプロイ

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# ポート公開
EXPOSE 8000

# アプリケーション起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./memo_app.db:/app/memo_app.db
    environment:
      - DATABASE_URL=sqlite:///./memo_app.db
```

### 2. Heroku へのデプロイ

```python
# Procfile
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}
```

```txt
# runtime.txt
python-3.9.16
```

### 3. AWS Lambda + API Gateway

```python
# lambda_handler.py
from mangum import Mangum
from main import app

handler = Mangum(app)
```

### 4. 本番環境の設定

```python
# production_config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key")
    allowed_origins: list = ["https://yourdomain.com"]
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 🎨 カスタマイズ例

### 1. 認証機能の追加

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証に失敗しました",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# 保護されたエンドポイント
@app.post("/memos/", dependencies=[Depends(verify_credentials)])
def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    # ... 既存の処理 ...
```

### 2. カテゴリー機能の追加

```python
# モデルの拡張
class Memo(Base):
    __tablename__ = "memos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False, default="")
    category = Column(String(50), nullable=True)  # カテゴリー追加
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# スキーマの更新
class MemoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = ""
    category: Optional[str] = Field(None, max_length=50)

# カテゴリー別取得エンドポイント
@app.get("/memos/category/{category}", response_model=List[MemoResponse])
def get_memos_by_category(category: str, db: Session = Depends(get_db)):
    memos = db.query(Memo).filter(Memo.category == category).all()
    return memos
```

### 3. ファイル添付機能

```python
from fastapi import File, UploadFile
import shutil
import uuid

@app.post("/memos/{memo_id}/attachment")
async def upload_attachment(
    memo_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # メモの存在確認
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not memo:
        raise HTTPException(status_code=404, detail="メモが見つかりません")
    
    # ファイルを保存
    file_id = str(uuid.uuid4())
    file_path = f"attachments/{memo_id}/{file_id}_{file.filename}"
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "file_id": file_id}
```

### 4. リアルタイム通知（WebSocket）

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        del self.active_connections[client_id]
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # メッセージ処理
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# メモ作成時に通知を送信
@app.post("/memos/")
async def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    # ... メモ作成処理 ...
    
    # WebSocket経由で通知
    await manager.broadcast({
        "type": "memo_created",
        "memo": memo_dict
    })
    
    return db_memo
```

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. ポート8000が既に使用されている

**エラーメッセージ:**
```
ERROR: [Errno 48] Address already in use
```

**解決方法:**
```bash
# 別のポートで起動
uvicorn main:app --reload --port 8001

# または、使用中のプロセスを終了
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 2. データベースファイルのアクセス権限エラー

**エラーメッセージ:**
```
sqlite3.OperationalError: unable to open database file
```

**解決方法:**
```bash
# ファイルの権限を変更
chmod 666 memo_app.db

# または、ディレクトリの権限を変更
chmod 755 .
```

#### 3. 依存関係のインストールエラー

**解決方法:**
```bash
# pipをアップグレード
pip install --upgrade pip

# 仮想環境を再作成
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 4. CORS エラー

**エラーメッセージ:**
```
Access to fetch at 'http://localhost:8000/memos/' from origin 'http://localhost:8080' has been blocked by CORS policy
```

**解決方法:**
```python
# main.py でCORS設定を確認
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # クライアントのURLを追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 5. 日本語の文字化け

**解決方法:**
```python
# レスポンスヘッダーに文字エンコーディングを指定
from fastapi.responses import JSONResponse

@app.get("/")
def read_root():
    return JSONResponse(
        content={"message": "FastAPIメモアプリケーションへようこそ！"},
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
```

## 🚀 今後の拡張案

### 基本的な機能拡張

1. **タグ機能**
   - 複数タグの付与
   - タグによるフィルタリング
   - タグクラウド表示

2. **全文検索**
   - Elasticsearchとの統合
   - 検索結果のハイライト
   - 関連メモの提案

3. **マルチユーザー対応**
   - ユーザー認証（JWT）
   - ユーザーごとのメモ管理
   - 共有機能

4. **リッチテキストエディタ**
   - Markdownサポート
   - 画像の埋め込み
   - コードハイライト

### 高度な機能拡張

1. **AI機能の統合**
   ```python
   @app.post("/memos/{memo_id}/summarize")
   async def summarize_memo(memo_id: int, db: Session = Depends(get_db)):
       memo = get_memo_by_id(db, memo_id)
       summary = await ai_service.summarize(memo.content)
       return {"summary": summary}
   ```

2. **音声入力対応**
   ```python
   @app.post("/memos/voice")
   async def create_memo_from_voice(
       audio: UploadFile = File(...),
       db: Session = Depends(get_db)
   ):
       text = await speech_to_text(audio)
       memo = create_memo(db, title="音声メモ", content=text)
       return memo
   ```

3. **バージョン管理**
   ```python
   class MemoVersion(Base):
       __tablename__ = "memo_versions"
       
       id = Column(Integer, primary_key=True)
       memo_id = Column(Integer, ForeignKey("memos.id"))
       version = Column(Integer)
       title = Column(String(100))
       content = Column(Text)
       created_at = Column(DateTime, default=datetime.utcnow)
   ```

4. **GraphQL API**
   ```python
   import strawberry
   from strawberry.fastapi import GraphQLRouter
   
   @strawberry.type
   class Memo:
       id: int
       title: str
       content: str
       created_at: datetime
   
   @strawberry.type
   class Query:
       @strawberry.field
       def memos(self) -> List[Memo]:
           # GraphQLクエリの実装
           pass
   
   schema = strawberry.Schema(query=Query)
   graphql_app = GraphQLRouter(schema)
   app.include_router(graphql_app, prefix="/graphql")
   ```

### パフォーマンス最適化

1. **キャッシング**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.decorator import cache
   
   @app.get("/memos/")
   @cache(expire=60)  # 60秒間キャッシュ
   async def get_memos(skip: int = 0, limit: int = 10):
       # ... 既存の処理 ...
   ```

2. **非同期処理の活用**
   ```python
   import asyncio
   from motor.motor_asyncio import AsyncIOMotorClient
   
   # 非同期データベースクライアント
   client = AsyncIOMotorClient("mongodb://localhost:27017")
   db = client.memo_database
   
   @app.get("/memos/")
   async def get_memos():
       memos = await db.memos.find().to_list(100)
       return memos
   ```

3. **CDNとの統合**
   - 静的ファイルのCDN配信
   - 画像の最適化とキャッシング
   - グローバル配信の高速化

## 📚 参考資料

### 公式ドキュメント
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [Pydantic公式ドキュメント](https://pydantic-docs.helpmanual.io/)

### チュートリアル
- [FastAPIチュートリアル（日本語）](https://fastapi.tiangolo.com/ja/tutorial/)
- [Real Python - FastAPI入門](https://realpython.com/fastapi-python-web-apis/)

### 関連技術
- [Uvicorn - ASGIサーバー](https://www.uvicorn.org/)
- [Starlette - ASGIフレームワーク](https://www.starlette.io/)
- [httpx - HTTPクライアント](https://www.python-httpx.org/)

### コミュニティ
- [FastAPI GitHub Discussions](https://github.com/tiangolo/fastapi/discussions)
- [FastAPI Discord](https://discord.gg/VQjSZaeJmf)
- [Stack Overflow - fastapi tag](https://stackoverflow.com/questions/tagged/fastapi)

---

このメモ帳アプリケーションを通じて、FastAPIの基本から応用まで幅広く学ぶことができます。ぜひカスタマイズして、自分だけのアプリケーションを作ってみてください！

ご質問やご提案がありましたら、GitHubのIssueでお知らせください。