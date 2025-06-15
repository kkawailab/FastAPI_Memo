# 🚀 FastAPI 完全ガイド

FastAPIは、Pythonで高速かつモダンなWeb APIを構築するためのフレームワークです。本リポジトリでは、FastAPIの基本から実践的な使い方まで、包括的なガイドと実装例を提供します。

## 📋 目次

1. [FastAPIとは](#fastapi-とは)
2. [なぜFastAPIを選ぶのか](#なぜ-fastapi-を選ぶのか)
3. [FastAPIの特徴](#fastapi-の特徴)
4. [クイックスタート](#クイックスタート)
5. [基本概念](#基本概念)
6. [高度な機能](#高度な機能)
7. [ベストプラクティス](#ベストプラクティス)
8. [実装例](#実装例)
9. [デプロイメント](#デプロイメント)
10. [トラブルシューティング](#トラブルシューティング)
11. [リソース](#リソース)

## 🌟 FastAPI とは

FastAPIは、Python 3.7+ の標準的な型ヒントに基づいて、APIを構築するためのモダンで高速（高パフォーマンス）なWebフレームワークです。

### 主な特徴
- **高速**: NodeJSやGo並みの非常に高いパフォーマンス（StarletteとPydanticのおかげ）
- **高速な開発**: 開発速度を約200〜300%向上
- **少ないバグ**: 開発者起因のバグを約40%削減
- **直感的**: 優れたエディタサポート、自動補完
- **簡単**: 使いやすく、学習時間が短い
- **短い**: コードの重複を最小限に抑制
- **堅牢**: 本番環境に対応したコードを自動生成
- **標準準拠**: APIのオープンスタンダード（OpenAPI、JSON Schema）に完全準拠

## 🤔 なぜ FastAPI を選ぶのか

### 1. **型安全性**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return item
```
Pythonの型ヒントを使用することで、自動的にリクエストの検証とドキュメント生成が行われます。

### 2. **自動ドキュメント生成**
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI schema: `/openapi.json`

### 3. **非同期処理のサポート**
```python
@app.get("/async-endpoint/")
async def read_async():
    # 非同期処理を簡単に実装
    await some_async_function()
    return {"message": "非同期処理完了"}
```

### 4. **依存性注入システム**
```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## ⚡ FastAPI の特徴

### 1. **Pydantic による自動バリデーション**
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: Optional[int] = Field(None, ge=0, le=150)
    created_at: datetime

    @validator('email')
    def email_must_be_valid(cls, v):
        if '@example.com' in v:
            raise ValueError('example.comのメールアドレスは使用できません')
        return v
```

### 2. **セキュリティと認証**
```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if not is_valid_token(token):
        raise HTTPException(status_code=403, detail="無効なトークンです")
    return token

@app.get("/protected/")
def protected_route(token: str = Depends(verify_token)):
    return {"message": "認証成功", "token": token}
```

### 3. **WebSocket サポート**
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"メッセージ: {data}")
```

### 4. **バックグラウンドタスク**
```python
from fastapi import BackgroundTasks

def send_email_notification(email: str, message: str):
    # メール送信処理
    pass

@app.post("/send-notification/")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_notification, email, "通知メッセージ")
    return {"message": "通知をバックグラウンドで送信中"}
```

## 🚀 クイックスタート

### 必要な環境
- Python 3.7以上
- pip（Pythonパッケージマネージャー）

### インストール
```bash
# FastAPIとASGIサーバーをインストール
pip install fastapi uvicorn[standard]

# 追加の依存関係（推奨）
pip install python-multipart  # ファイルアップロード用
pip install jinja2  # HTMLテンプレート用
pip install python-jose[cryptography]  # JWT認証用
```

### 最初のアプリケーション
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### サーバーの起動
```bash
uvicorn main:app --reload
```

## 📚 基本概念

### 1. **パスパラメータ**
```python
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
```

### 2. **クエリパラメータ**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### 3. **リクエストボディ**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### 4. **レスポンスモデル**
```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str

class UserOut(BaseModel):
    username: str
    email: str

@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    # パスワードは返さない
    return user
```

### 5. **HTTPステータスコード**
```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    # 削除処理
    return None
```

## 🔧 高度な機能

### 1. **ミドルウェア**
```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 2. **CORS（Cross-Origin Resource Sharing）**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. **依存性注入の高度な使い方**
```python
from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret-api-key":
        raise HTTPException(status_code=403, detail="無効なAPIキー")
    return x_api_key

@app.get("/protected-items/", dependencies=[Depends(verify_api_key)])
def read_protected_items():
    return {"items": ["secret-item-1", "secret-item-2"]}
```

### 4. **ファイルアップロード**
```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

### 5. **データベース統合（SQLAlchemy）**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 💡 ベストプラクティス

### 1. **プロジェクト構造**
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   ├── models/
│   ├── schemas/
│   ├── crud/
│   └── db/
├── tests/
├── alembic/
├── requirements.txt
└── .env
```

### 2. **環境設定**
```python
# core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. **エラーハンドリング**
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": f"不正な値: {exc}"},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
```

### 4. **ロギング**
```python
import logging
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### 5. **テスト**
```python
# test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "テストアイテム", "price": 100.0},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "テストアイテム"
```

## 📝 実装例

### サンプルアプリケーション: メモ帳API

本リポジトリには、FastAPIを使用した実践的なメモ帳アプリケーションの実装例が含まれています。

📁 **[memo_app - FastAPIメモ帳アプリケーション](./memo_app/)**

このサンプルアプリケーションでは以下を学べます：
- RESTful APIの設計と実装
- SQLAlchemyを使用したデータベース操作
- Pydanticモデルによるデータ検証
- CRUD操作の実装
- 検索機能の実装
- エラーハンドリング
- CORSの設定

詳細なドキュメントは[memo_app/README.md](./memo_app/README.md)をご覧ください。

## 🚢 デプロイメント

### 1. **Docker**
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. **Gunicorn + Uvicorn**
```bash
# 本番環境用の起動コマンド
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. **環境変数の管理**
```python
# .env ファイル
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
ENVIRONMENT=production
```

### 4. **HTTPS/SSL**
```python
# Nginx設定例
server {
    listen 443 ssl;
    server_name api.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
    }
}
```

## 🔍 トラブルシューティング

### よくある問題と解決策

#### 1. **"RuntimeError: This event loop is already running"**
```python
# 解決策: nest_asyncio を使用
import nest_asyncio
nest_asyncio.apply()
```

#### 2. **CORS エラー**
```python
# すべてのオリジンを許可（開発環境のみ）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. **大きなファイルアップロードの問題**
```python
# ファイルサイズ制限の設定
from fastapi import UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # チャンク単位で読み込む
    contents = b""
    while chunk := await file.read(1024 * 1024):  # 1MB chunks
        contents += chunk
    return {"filename": file.filename, "size": len(contents)}
```

#### 4. **循環参照の問題**
```python
# 解決策: 遅延インポートまたは TYPE_CHECKING を使用
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
```

## 📚 リソース

### 公式ドキュメント
- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [FastAPI 日本語ドキュメント](https://fastapi.tiangolo.com/ja/)
- [Pydantic ドキュメント](https://pydantic-docs.helpmanual.io/)
- [Starlette ドキュメント](https://www.starlette.io/)

### チュートリアル
- [FastAPI チュートリアル](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI 高度なユーザーガイド](https://fastapi.tiangolo.com/advanced/)

### コミュニティ
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [FastAPI Gitter](https://gitter.im/tiangolo/fastapi)
- [Stack Overflow - FastAPI](https://stackoverflow.com/questions/tagged/fastapi)

### 関連ツール
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [pytest](https://docs.pytest.org/)
- [httpx](https://www.python-httpx.org/)

## 🤝 貢献

プルリクエストを歓迎します！大きな変更を行う場合は、まずissueを作成して変更内容について議論してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

FastAPIを使用した開発についてご質問がある場合は、Issueを作成してください。ハッピーコーディング! 🚀