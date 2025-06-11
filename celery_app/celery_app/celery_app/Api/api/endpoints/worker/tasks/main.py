from fastapi import FastAPI
from api.endpoints import terraform

app = FastAPI()

app.include_router(terraform.router, prefix="/terraform", tags=["Terraform"])
