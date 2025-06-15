# FastAPIメモ帳アプリケーション

FastAPIとSQLAlchemyを使用したシンプルなメモ帳アプリケーションです。RESTful APIとモダンなWebクライアントインターフェースを提供します。

## 📋 機能

### APIエンドポイント
- **メモの作成** - 新しいメモを作成
- **メモの一覧表示** - すべてのメモを取得（ページネーション対応）
- **メモの個別取得** - 特定のメモを取得
- **メモの更新** - 既存のメモを編集（部分更新対応）
- **メモの削除** - メモを削除
- **メモの検索** - タイトルや内容でメモを検索

### Webクライアント
- レスポンシブデザイン（デスクトップ・モバイル対応）
- リアルタイムでのメモの作成・編集・削除
- 検索機能
- モーダルウィンドウでの編集
- 作成日時・更新日時の表示

## 🚀 クイックスタート

### 必要な環境
- Python 3.7以上
- pip（Pythonパッケージマネージャー）

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/FastAPI_Memo.git
cd FastAPI_Memo
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

### 起動方法

1. FastAPIサーバーを起動
```bash
cd memo_app
uvicorn main:app --reload
```

2. Webクライアントにアクセス
- ブラウザで `memo_app/index.html` を直接開く
- または、HTTPサーバーを使用:
```bash
cd memo_app
python -m http.server 8080
```
その後、ブラウザで `http://localhost:8080` にアクセス

## 📁 プロジェクト構造

```
FastAPI_Memo/
├── README.md              # このファイル
├── requirements.txt       # Python依存関係
└── memo_app/
    ├── main.py           # FastAPI アプリケーション
    ├── memo_app.db       # SQLite データベース（自動生成）
    ├── index.html        # Webクライアント - HTML
    ├── style.css         # Webクライアント - スタイル
    ├── app.js            # Webクライアント - JavaScript
    └── CLAUDE.md         # 開発ガイドライン
```

## 🔧 技術スタック

### バックエンド
- **FastAPI** - 高速なWebフレームワーク
- **SQLAlchemy** - ORMライブラリ
- **SQLite** - 軽量データベース
- **Pydantic** - データ検証
- **Uvicorn** - ASGIサーバー

### フロントエンド
- **HTML5** - 構造
- **CSS3** - スタイリング（レスポンシブデザイン）
- **Vanilla JavaScript** - インタラクティブ機能
- **Fetch API** - APIとの通信

## 📚 API仕様

### エンドポイント一覧

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| GET | `/` | ウェルカムメッセージ |
| GET | `/memos/` | メモ一覧を取得 |
| POST | `/memos/` | 新しいメモを作成 |
| GET | `/memos/{memo_id}` | 特定のメモを取得 |
| PUT | `/memos/{memo_id}` | メモを更新 |
| DELETE | `/memos/{memo_id}` | メモを削除 |
| GET | `/memos/search/?q={query}` | メモを検索 |

### APIドキュメント
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### リクエスト/レスポンス例

#### メモの作成
```bash
curl -X POST "http://localhost:8000/memos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "買い物リスト",
    "content": "牛乳、パン、卵"
  }'
```

#### レスポンス
```json
{
  "id": 1,
  "title": "買い物リスト",
  "content": "牛乳、パン、卵",
  "created_at": "2024-01-20T10:30:00",
  "updated_at": "2024-01-20T10:30:00"
}
```

## 💾 データベース

### スキーマ

**memosテーブル**
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INTEGER | 主キー（自動採番） |
| title | VARCHAR(100) | メモのタイトル |
| content | TEXT | メモの内容 |
| created_at | DATETIME | 作成日時 |
| updated_at | DATETIME | 更新日時 |

## 🛠️ 開発

### 環境設定
```bash
# 仮想環境の作成（推奨）
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 開発サーバーの起動
```bash
# ホットリロード有効
uvicorn main:app --reload --port 8000
```

### データベースのリセット
```bash
# SQLiteデータベースファイルを削除
rm memo_app.db
# サーバーを再起動すると自動的に再作成されます
```

## 🔒 セキュリティに関する注意

現在の設定は開発環境用です。本番環境では以下の変更を推奨します：

1. **CORS設定の制限**
   - `allow_origins=["*"]` を特定のドメインに制限
   
2. **認証の実装**
   - JWT認証やOAuth2の導入
   
3. **環境変数の使用**
   - データベースURLなどの設定を環境変数化
   
4. **HTTPS の使用**
   - SSL/TLS証明書の設定

## 📝 今後の機能拡張案

- [ ] ユーザー認証・認可
- [ ] メモのカテゴリー分け
- [ ] タグ機能
- [ ] メモの共有機能
- [ ] ファイル添付
- [ ] マークダウン対応
- [ ] エクスポート機能（PDF、テキストファイル）
- [ ] ダークモード
- [ ] 多言語対応

## 🤝 貢献

プルリクエストを歓迎します！大きな変更を行う場合は、まずissueを作成して変更内容について議論してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🙏 謝辞

- FastAPIコミュニティ
- SQLAlchemyチーム
- すべてのコントリビューター

---

質問や提案がある場合は、Issueを作成してください。