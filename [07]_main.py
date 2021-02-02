from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from typing import Optional, List
from pydantic import BaseModel

'''
what's new ?
from fastapi.exceptions import HTTPException
from typing import List
app = FastAPI(title='Todo APi')
raise HTTPException(404,detail='Invalid ID')
'''

class Todo(BaseModel):

    name : str
    due_date : str
    description : str

app = FastAPI(title='Todo APi')


''' --- fake database ----------------------- '''
store_db = []



''' ---- root page -------------------------- '''
@app.get('/')
async def root():
    return {'Hello':'Todo'}



''' ----- create, read, update, delete ------ '''

@app.post('/todo/c/')
async def create(todo:Todo):
    store_db.append(todo)
    return todo

@app.get('/todo/ra/',response_model=List[Todo])
async def read_all():
    return store_db

@app.get('/todo/r/{todo_id}')
async def read(todo_id:int):
    try:
        return store_db[todo_id]
    except:
        raise HTTPException(404,detail='Invalid ID')

@app.put('/todo/u/{todo_id}')
async def update(todo_id:int,todo:Todo):
    try:
        store_db[todo_id]=todo
        return store_db[todo_id]
    except:
        raise HTTPException(400,'Failed to update.')

@app.delete('/todo/d/{todo_id}')
async def delete(todo_id:int):
    try:
        temp = store_db[todo_id]
        store_db.pop(todo_id)
        return temp
    except:
        raise HTTPException(500, detail='REG Failed to delete')