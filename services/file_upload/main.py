import uvicorn

from fastapi import FastAPI

from healthcheck import router as health_router
from file_upload.router import router as file_upload_router
from rabbitmq_app.router import router as rabbit_router


from configurations import development_mode_settings

app = FastAPI(docs_url="/docs" if development_mode_settings.development_mode else None,
              redoc_url="/redoc" if development_mode_settings.development_mode else None)

app.include_router(file_upload_router)
app.include_router(health_router)
app.include_router(rabbit_router)


def main():
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=8030,
                reload=False,
                ssl_keyfile="/file_upload/certs/server.key",
                ssl_certfile="/file_upload/certs/server.crt",
                ssl_ca_certs="/file_upload/certs/rootCA.crt")


if __name__ == '__main__':
    main()
