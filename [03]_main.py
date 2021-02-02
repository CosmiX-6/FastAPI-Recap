''' Response Model '''
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# --- Pydantic BaseModel --------
class PackageIn(BaseModel):
    secret_id : int
    name : str
    number : int
    value : Optional[bool] = None

# --- Pydantic BaseModel --------
class Package(BaseModel):
    name : str
    number : int
    value : Optional[bool] = None

app = FastAPI()


# Response Model -------------------------------------
# url : 127.0.0.1/docs
@app.post('/package/',response_model=Package, response_model_exclude={'number','value'})
async def make_package(package:PackageIn):
    return package