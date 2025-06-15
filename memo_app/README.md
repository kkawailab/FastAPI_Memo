# 📝 メモ帳アプリ

FastAPIを使用したシンプルなメモ帳アプリケーションです。

## 📋 目次

1. [アプリケーション概要](#-アプリケーション概要)
2. [このアプリについて](#-このアプリについて)
3. [主な機能](#-機能)
4. [セットアップ](#-セットアップ)
5. [利用方法](#-利用方法)
6. [API仕様](#-api-エンドポイント)
7. [具体的な使用例](#-使用例)
8. [プロジェクト構造](#-プロジェクト構造)
9. [技術スタック](#-技術スタック)
10. [今後の改良のヒント](#-今後の改良のヒント)

## 🌟 アプリケーション概要

このメモ帳アプリは、日々の思いつきやタスク、アイデアを簡単に保存・管理できるWeb APIアプリケーションです。シンプルながら実用的な機能を備えており、プログラミング学習の教材としても最適です。

### なぜこのアプリを作ったのか？

- **学習用途**: FastAPIの基本的な使い方を学べる
- **実用性**: 実際に使えるメモ管理システム
- **拡張性**: 機能追加が容易な設計

### このアプリでできること

1. **メモの管理**: 作成、表示、編集、削除の基本操作
2. **検索機能**: キーワードでメモを素早く見つける
3. **API連携**: 他のアプリケーションと連携可能

## 🎯 このアプリについて

このアプリケーションは、Pythonの最新Webフレームワーク「FastAPI」を使って作られたREST APIです。
メモの保存・管理ができるシンプルな機能を提供しています。

### 初心者の方へ
- **REST API**とは: Webサービス同士がデータをやり取りするための仕組みです
- **FastAPI**とは: Pythonで高速なWebAPIを簡単に作れるフレームワークです
- **SQLite**とは: ファイル一つで動作する軽量なデータベースです

## ✨ 機能

- **メモの作成、読み取り、更新、削除（CRUD）**
  - Create（作成）: 新しいメモを保存
  - Read（読み取り）: 保存したメモを表示
  - Update（更新）: メモの内容を変更
  - Delete（削除）: 不要なメモを削除
- **メモの検索機能**: キーワードでメモを検索
- **SQLiteデータベースを使用したデータ永続化**: アプリを終了してもデータが残る
- **CORS対応**: 異なるドメインからのアクセスが可能（フロントエンドとの連携用）

## 📦 セットアップ

### 前提条件
- Python 3.8以上がインストールされていること
- pip（Pythonのパッケージ管理ツール）が使えること

### 手順

1. **プロジェクトディレクトリに移動**：
```bash
cd memo_app
```

2. **依存関係のインストール**：
```bash
# requirements.txtに記載されたパッケージをまとめてインストール
pip install -r requirements.txt
```

3. **アプリケーションの起動**：
```bash
# 開発サーバーを起動（--reloadオプションでコード変更時に自動再起動）
uvicorn main:app --reload
```

4. **ブラウザで以下のURLにアクセス**：
- **API本体**: http://localhost:8000
  - ウェルカムメッセージが表示されます
- **対話的APIドキュメント（Swagger UI）**: http://localhost:8000/docs
  - ブラウザ上で直接APIを試せる便利なツール
  - 各エンドポイントの詳細な説明付き
- **代替APIドキュメント（ReDoc）**: http://localhost:8000/redoc
  - より読みやすい形式のドキュメント

## 🚀 利用方法

### 基本的な使い方

1. **Swagger UIを使った操作（推奨）**
   - http://localhost:8000/docs にアクセス
   - 各エンドポイントの「Try it out」ボタンをクリック
   - パラメータを入力して「Execute」をクリック

2. **コマンドラインからの操作**
   - curlコマンドを使用（後述の使用例を参照）

3. **プログラムからの利用**
   ```python
   import requests
   
   # メモを作成
   response = requests.post(
       "http://localhost:8000/memos/",
       json={"title": "テストメモ", "content": "これはテストです"}
   )
   print(response.json())
   ```

### 典型的な使用シナリオ

1. **日記として使う**
   - 毎日の出来事をメモとして保存
   - 日付をタイトルに含めて管理

2. **タスク管理**
   - TODOリストとして活用
   - 完了したタスクは削除または更新

3. **アイデアメモ**
   - 思いついたアイデアをすぐに保存
   - キーワード検索で後から見つけやすい

## 🔌 API エンドポイント

### 基本的なエンドポイント

| HTTPメソッド | パス | 説明 |
|------------|------|------|
| GET | `/` | ウェルカムメッセージを表示 |
| POST | `/memos/` | 新しいメモを作成 |
| GET | `/memos/` | すべてのメモを取得（ページネーション対応） |
| GET | `/memos/{memo_id}` | 特定のメモを取得 |
| PUT | `/memos/{memo_id}` | メモを更新（部分更新可能） |
| DELETE | `/memos/{memo_id}` | メモを削除 |
| GET | `/memos/search/?q={query}` | メモを検索 |

### 詳細説明

- **ページネーション**: `/memos/?skip=0&limit=10` のように指定可能
- **部分更新**: PUTメソッドではタイトルまたは本文の片方だけの更新も可能
- **検索**: タイトルと本文の両方から部分一致で検索

## 💡 使用例

### 1. メモの作成
```bash
# curlコマンドを使ってPOSTリクエストを送信
curl -X POST "http://localhost:8000/memos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "買い物リスト", "content": "牛乳、パン、卵"}'

# レスポンス例:
# {
#   "id": 1,
#   "title": "買い物リスト",
#   "content": "牛乳、パン、卵",
#   "created_at": "2025-01-15T10:30:00",
#   "updated_at": "2025-01-15T10:30:00"
# }
```

### 2. すべてのメモを取得
```bash
# 保存されているすべてのメモを取得
curl "http://localhost:8000/memos/"

# ページネーションを使用する場合
curl "http://localhost:8000/memos/?skip=0&limit=5"  # 最初の5件を取得
```

### 3. 特定のメモを取得
```bash
# ID=1のメモを取得
curl "http://localhost:8000/memos/1"
```

### 4. メモの更新
```bash
# タイトルと本文の両方を更新
curl -X PUT "http://localhost:8000/memos/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "買い物リスト（更新）", "content": "牛乳、パン、卵、バター"}'

# タイトルのみ更新（部分更新）
curl -X PUT "http://localhost:8000/memos/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "買い物リスト（今日）"}'
```

### 5. メモの削除
```bash
# ID=1のメモを削除
curl -X DELETE "http://localhost:8000/memos/1"

# レスポンス例:
# {"message": "メモが削除されました"}
```

### 6. メモの検索
```bash
# "買い物"というキーワードで検索
curl "http://localhost:8000/memos/search/?q=買い物"

# URLエンコーディングが必要な場合（日本語など）
curl "http://localhost:8000/memos/search/?q=%E8%B2%B7%E3%81%84%E7%89%A9"
```

## 🏗️ プロジェクト構造

```
memo_app/
├── main.py              # メインアプリケーションファイル
├── requirements.txt     # Python依存関係のリスト
├── README.md           # このファイル
├── CLAUDE.md           # Claude Code用の設定ファイル
└── memo_app.db         # SQLiteデータベースファイル（自動生成）
```

## 🔧 技術スタック

- **FastAPI**: 高速でモダンなPython Webフレームワーク
- **SQLAlchemy**: Python用のORM（オブジェクト関係マッピング）
- **Pydantic**: データ検証とシリアライゼーション
- **SQLite**: 軽量なファイルベースのデータベース
- **Uvicorn**: ASGI準拠の高速Webサーバー

## 📝 開発のヒント

1. **データベースの確認**: `memo_app.db`ファイルがSQLiteデータベースです
2. **APIテスト**: http://localhost:8000/docs でSwagger UIを使うと簡単にテストできます
3. **エラー処理**: 存在しないメモIDを指定すると404エラーが返されます
4. **日本語対応**: タイトルや本文に日本語を使用できます

## 🎯 今後の改良のヒント

### 📌 初級レベルの改良

1. **メモのカテゴリー機能**
   ```python
   # Memoモデルにカテゴリーフィールドを追加
   category = Column(String(50), nullable=True)
   ```
   - カテゴリー別にメモを整理
   - カテゴリーでフィルタリングする機能

2. **メモの重要度設定**
   - 優先度（高・中・低）を設定できる機能
   - 重要なメモを上位に表示

3. **文字数制限の追加**
   - タイトルや本文の最大文字数を設定
   - バリデーションの強化

### 📊 中級レベルの改良

1. **ユーザー認証機能**
   ```python
   # JWT認証の実装例
   from fastapi.security import HTTPBearer
   from jose import jwt
   ```
   - ユーザーごとにメモを管理
   - ログイン/ログアウト機能
   - パスワードのハッシュ化

2. **タグ機能**
   - 複数のタグをメモに付けられる
   - タグによる検索機能
   - タグクラウドの表示

3. **ページネーションの改良**
   - 総ページ数の表示
   - 前後のページへのリンク
   - ページサイズの動的変更

4. **データのエクスポート/インポート**
   ```python
   @app.get("/memos/export/csv")
   def export_memos_csv():
       # CSVファイルとしてエクスポート
   ```
   - CSV、JSON形式でのエクスポート
   - バックアップ機能

### 🚀 上級レベルの改良

1. **リアルタイム同期**
   - WebSocketを使用したリアルタイム更新
   - 複数デバイス間での同期

2. **全文検索エンジン**
   ```python
   # Elasticsearchとの連携例
   from elasticsearch import Elasticsearch
   ```
   - より高度な検索機能
   - 検索結果のスコアリング

3. **マイクロサービス化**
   - 認証サービスの分離
   - メモサービスの分離
   - APIゲートウェイの実装

4. **AI機能の統合**
   - メモの自動要約
   - 関連メモの推薦
   - 自動タグ付け

### 🛠️ インフラ・運用面の改良

1. **データベースの変更**
   ```python
   # PostgreSQLへの移行例
   SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
   ```
   - PostgreSQL、MySQLへの移行
   - データベースのレプリケーション

2. **Docker化**
   ```dockerfile
   # Dockerfile例
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
   ```

3. **CI/CDパイプライン**
   - GitHub Actionsでの自動テスト
   - 自動デプロイメント

4. **監視・ロギング**
   - Prometheusでのメトリクス収集
   - ELKスタックでのログ管理

### 💡 学習のためのヒント

1. **テストを書く**
   ```python
   # pytest使用例
   def test_create_memo():
       response = client.post("/memos/", json={...})
       assert response.status_code == 200
   ```

2. **ドキュメントの充実**
   - APIドキュメントの詳細化
   - 使用例の追加

3. **パフォーマンス改善**
   - インデックスの最適化
   - キャッシュの実装
   - 非同期処理の活用

これらの改良を段階的に実装することで、FastAPIの理解を深めながら、より実用的なアプリケーションに成長させることができます。