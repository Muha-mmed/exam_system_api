from fastapi import FastAPI
from authentication.views import auth
app = FastAPI()

app.include_router(auth)