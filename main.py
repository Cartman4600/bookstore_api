from fastapi import FastAPI
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

app = FastAPI(title       = "Bookstore/Coffee_Shop-API",
              description = "Provides bookstore and coffee_shop database control",
              version     = "0.8.0"
             )

# bookstore routes
from routers.bookstore import books, ebooks, movies, summary, bookstore_logs
app.include_router(books.router,   prefix = "/bookstore/books",   tags = ["Books"])
app.include_router(ebooks.router,  prefix = "/bookstore/ebooks",  tags = ["Ebooks"])
app.include_router(movies.router,  prefix = "/bookstore/movies",  tags = ["Movies"])
app.include_router(summary.router, prefix = "/bookstore/summary", tags = ["Summary"])
app.include_router(bookstore_logs.router, prefix = "/bookstore/logs", tags = ["Bookstore logs"])

# coffee_shop routes
from routers.coffee_shop import americano, apple_spritzer, backstock, latte, lemonade, coffee_shop_logs
app.include_router(backstock.router,  prefix = "/coffee_shop/backstock",  tags = ["Backstock"])
app.include_router(latte.router,      prefix = "/coffee_shop/latte",      tags = ["Latte"])
app.include_router(americano.router,  prefix = "/coffee_shop/americano",  tags = ["Americano"])
app.include_router(lemonade.router,   prefix = "/coffee_shop/lemonade",   tags = ["Lemonade"])
app.include_router(apple_spritzer.router,   prefix = "/coffee_shop/apple_spritzer",  tags = ["Apple spritzer"])
app.include_router(coffee_shop_logs.router, prefix = "/coffee_shop/logs", tags = ["Coffee shop logs"])

# app starten
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
                host         = "127.0.0.1",
                port         = 5000,
                reload       = True,
                # Falls keine ssl Zertifikate zur Hand auskommentieren:
                ssl_certfile = ROOT_DIR / 'data' / 'secret' / 'cert.pem',
                ssl_keyfile  = ROOT_DIR / 'data' / 'secret' / 'key.pem'
                )

# uvicorn myapi:app --host 127.0.0.1 --port 5000 --reload