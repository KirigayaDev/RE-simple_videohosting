import uvicorn

from fastapi import FastAPI

from healthcheck import router as health_router
from rabbitmq_app.router import router as rabbit_router

from configurations import development_mode_settings

app = FastAPI(docs_url="/docs" if development_mode_settings.development_mode else None,
              redoc_url="/redoc" if development_mode_settings.development_mode else None)

app.include_router(health_router)
app.include_router(rabbit_router)


def main():
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=8010,
                reload=False,
                ssl_keyfile="/channel_actions/certs/channel_actions/server.key",
                ssl_certfile="/channel_actions/certs/channel_actions/server.crt",
                ssl_ca_certs="/channel_actions/certs/channel_actions/rootCA.crt")


if __name__ == '__main__':
    main()
