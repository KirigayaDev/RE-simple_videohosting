import uvicorn

from fastapi import FastAPI

from healthcheck import router as health_router
from rabbitmq_app.router import router

app = FastAPI()

app.include_router(health_router)
app.include_router(router)


def main():
    uvicorn.run("main:app",
                host='0.0.0.0',
                port=8010,
                reload=False,
                ssl_keyfile="/channel_actions/certs/server.key",
                ssl_certfile="/channel_actions/certs/server.crt",
                ssl_ca_certs="/channel_actions/certs/rootCA.crt")


if __name__ == '__main__':
    main()
