import uvicorn

from fastapi import FastAPI

from healthcheck import router as health_router
from auth.router import router as auth_router

app = FastAPI()

app.include_router(health_router)
app.include_router(auth_router)


def main():
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=8000,
                reload=False,
                ssl_keyfile="/auth_service/certs/server.key",
                ssl_certfile="/auth_service/certs/server.crt",
                ssl_ca_certs="/auth_service/certs/rootCA.crt")


if __name__ == '__main__':
    main()
