from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# url : 127.0.0.1/
@app.get('/')
async def hello_world():
    return {'Hello':'World'}

# Path Parameters -------------------------------------
# url : 127.0.0.1/component/3
@app.get('/component/{component_id}') #path parameters
async def component(component_id:int):
    return {'component_id':component_id}

# Query Parameters -------------------------------------
# url : 127.0.0.1/component/?number=3&text=cosmix git
@app.get('/component/') #query parameter
async def read_component(number : int,text : str):
    return {'number':number,'text':text}