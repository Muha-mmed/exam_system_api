from fastapi import FastAPI
from authentication.views import auth
from exam.views import exam_routes
app = FastAPI()

app.include_router(auth)
app.include_router(exam_routes)