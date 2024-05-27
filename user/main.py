from fastapi import FastAPI

from user.views import router

app = FastAPI()

app.include_router(router)