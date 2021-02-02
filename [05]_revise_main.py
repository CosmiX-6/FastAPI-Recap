from fastapi import FastAPI
from typing import Optional

app = FastAPI()

#------------- PATH PARAM -----------------------------
# url : http://127.0.0.1/component/int_value
@app.get('/component/{component_id}') #path parameters
async def component(component_id:int):
    return {'component_id':component_id}

# url : http://127.0.0.1/files//new_link.com/path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


#------------- QUERY PARAM -----------------------------
#url : http://127.0.0.1/items/                     <<< Here value of both skip and limit reamins default as in fucntion arg.
#url : http://124.0.0.1/items/?skip=14&limit=15    <<< Here value of both skip and limit get changed in function arg.
#url : http://127.0.0.1/items/?skip=20             <<< Here value of both skip get changed in function arg and limit remains default.
fake_items_db = [{"item_name 1": "Foo"}, {"item_name 2": "Bar"}, {"item_name 3": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#url : http://127.0.0.1:8000/items/cosmix&q=2&value=true
@app.get("/items/{item_id}")
async def read_items(item_id:str,q:Optional[str] = None,value:bool = True):
    items={'item_name':item_id}
    if q:
        items.update({'q':q})
    else:
        items.update({'message':'There no more info available here'})
    return items