from fastapi import FastAPI, HTTPException
from models import Todo, Todo_Pydantic, TodoIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel

class Message(BaseModel):
    message : str

app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World!  Welcome, to ORM'

@app.post('/todo',response_model=Todo_Pydantic)
async def create(todo:TodoIn_Pydantic):
    obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(obj)

@app.get('/todo/{todo_id}',response_model=Todo_Pydantic,responses={404:{'models':HTTPNotFoundError}})
async def read_one(todo_id:int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))

@app.put('/todo/{todo_id}',response_model=Todo_Pydantic,responses={404:{'models':HTTPNotFoundError}})
async def update(todo_id:int,todo:TodoIn_Pydantic):
    await Todo.filter(id=todo_id).update(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))

@app.delete('/todo/{todo_id}',responses={404:{'model':HTTPNotFoundError}})
async def delete(todo_id:int):
    delete_obj = await Todo.filter(id=todo_id).delete()
    if not delete_obj:
        raise HTTPException(404,detail='Not Found')
    else:
        return Message(message='Successfully Deleted')

register_tortoise(
   app,
   db_url='sqlite://../../DB_store/store.db',
   modules={'models':['models']},
   generate_schemas=True,
   add_exception_handlers=True,
)