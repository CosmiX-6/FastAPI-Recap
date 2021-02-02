''' Example Upgrade / Pydantic BaseModel ''''

from typing import Optional
from fastapi import FastAPI

from pydantic import BaseModel

# --- Pydantic BaseModel --------
class Package(BaseModel):
    name : str
    number : int
    description : Optional[str] = None

# --- Pydantic BaseModel --------
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

app = FastAPI()

# url : 127.0.0.1/
@app.get('/')
async def hello_world():
    return {'Hello':'World'}

# BaseModel Response -------------------------------------
# url : 127.0.0.1/docs
@app.post('/package/{priority}')
async def make_package(priority : int,package : Package,value : bool):
    return {'priority':priority,**package.dict(),'value':value}

# url : 127.0.0.1/docs
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}