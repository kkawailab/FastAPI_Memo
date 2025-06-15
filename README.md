# FastAPI

FastAPIは、Pythonの標準的な型ヒントに基づいてAPIを構築するための、モダンで高速（高パフォーマンス）なWebフレームワークです。

## 主な特徴

### 高速
- **非常に高いパフォーマンス**: NodeJSやGoと同等のパフォーマンスを実現（StarletteとPydanticのおかげ）
- **最速のPythonフレームワークの1つ**

### 高速な開発
- **開発速度の向上**: 機能開発速度を約200％〜300％向上
- **バグの削減**: 開発者起因のエラーを約40％削減
- **直感的**: 優れたエディタサポート、自動補完機能が充実
- **簡単**: 使いやすく学びやすい設計、ドキュメントを読む時間を最小限に
- **短いコード**: コードの重複を最小限に抑え、各パラメータ宣言から複数の機能を提供

### 堅牢性
- **本番環境対応**: 自動的に対話型のAPIドキュメントを生成
- **標準ベース**: APIのオープンスタンダードに基づく：OpenAPI（以前のSwagger）とJSON Schema

## インストール

```bash
pip install fastapi
```

また、本番環境ではASGIサーバーが必要です：

```bash
pip install "uvicorn[standard]"
```

## 基本的な使い方

### シンプルな例

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### 実践的なサンプル

実際のアプリケーション例として、FastAPIを使用したメモアプリのサンプルをご覧ください：

- [FastAPIメモアプリのサンプル](./memo-app/README.md)

### サーバーの起動

```bash
uvicorn main:app --reload
```

## 型ヒントの活用

FastAPIは、Pythonの型ヒントを最大限に活用します：

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

## 自動ドキュメント

FastAPIは自動的に以下のドキュメントを生成します：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 主要な機能

### 1. リクエストの検証
- パスパラメータ、クエリパラメータ、リクエストボディの自動検証
- Pydanticを使用した強力なデータ検証

### 2. 依存性注入
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

### 3. セキュリティ
- OAuth2、JWT、HTTPベーシック認証などのサポート
- CORSの簡単な設定

### 4. 非同期サポート
```python
@app.get("/async-items/")
async def read_items():
    results = await some_async_function()
    return results
```

### 5. WebSocket
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```

## ベストプラクティス

### 1. プロジェクト構造
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── models/
│       ├── __init__.py
│       └── item.py
├── tests/
└── requirements.txt
```

### 2. 環境変数の管理
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. エラーハンドリング
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

## パフォーマンスの最適化

### 1. 非同期処理の活用
- I/Oバウンドな処理には`async/await`を使用
- CPUバウンドな処理にはバックグラウンドタスクを使用

### 2. キャッシング
```python
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@app.get("/cached-data/")
@cache(expire=60)
async def get_cached_data():
    return expensive_computation()
```

### 3. データベース接続の最適化
- コネクションプーリングの使用
- 適切なインデックスの設定

## テスト

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

## デプロイメント

### Docker
```dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 本番環境での考慮事項
- Gunicornを使用したワーカープロセスの管理
- HTTPSの設定（Let's Encryptなど）
- ロードバランシング
- モニタリングとロギング

## 関連リソース

- [公式ドキュメント](https://fastapi.tiangolo.com/)
- [GitHub リポジトリ](https://github.com/tiangolo/fastapi)
- [チュートリアル](https://fastapi.tiangolo.com/tutorial/)
- [コミュニティ](https://fastapi.tiangolo.com/community/)

## まとめ

FastAPIは、現代的なPython Webアプリケーション開発において、開発効率とパフォーマンスの両方を追求できる優れたフレームワークです。型ヒントを活用した自動検証、自動ドキュメント生成、高いパフォーマンスなど、多くの利点を提供します。