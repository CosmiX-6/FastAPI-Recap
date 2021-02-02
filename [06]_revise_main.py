from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class ModelName(BaseModel):
    item_name:str
    description: Optional[str] = None
    price:float
    tax:Optional[float] = None

app = FastAPI()

@app.post('/item/')
async def model_name(model:ModelName):
    model_dict=model.dict()
    if model.tax:
        price_with_tax = model.price * model.tax
        model_dict.update({'Price TDS':price_with_tax})
    return model_dict
