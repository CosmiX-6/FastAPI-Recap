from fastapi import FastAPI, HTTPException, Request
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from pydantic import BaseModel
from models import Student, Student_Pydantic, StudentIn_Pydantic
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

class Message(BaseModel):
    message : str

templates = Jinja2Templates('templates')

app = FastAPI(title='Student ORM')

@app.get('/')
async def root():
    return {'Server status':'Online'}

@app.post('/student',response_model=Student_Pydantic)
async def create(student:StudentIn_Pydantic):
    obj = await Student.create(**student.dict(exclude_unset=True))
    return await Student_Pydantic.from_tortoise_orm(obj)

@app.get('/student/{student_id}',response_model=Student_Pydantic,responses={404:{'model':HTTPNotFoundError}})
async def read_all(student_id:int):
     return await Student_Pydantic.from_queryset_single(Student.get(id=student_id))

@app.get('/display/{student_id}',response_class=HTMLResponse)
async def display_one(request:Request,student_id:int):
    z = await read_all(student_id)
    return templates.TemplateResponse("index.html",{'request':request,'s_id':z.id,'s_name':z.name,'s_email':z.email,'s_pass':z.password,'s_join':z.joined_date})

@app.put('/student/{student_id}',response_model=Student_Pydantic,responses={404:{'model':HTTPNotFoundError}})
async def update(student_id:int,student:StudentIn_Pydantic):
    await Student.filter(id=student_id).update(**student.dict(exclude_unset=True))
    return await Student_Pydantic.from_queryset_single(Student.get(id=student_id))

@app.delete('/student/{student_id}')
async def delete(student_id:int):
    delete_obj = await Student.filter(id=student_id).delete()
    if not delete_obj:
        raise HTTPException(404,detail='Invalid ID!')
    else:
        return Message(message='Successfully deleted')


register_tortoise(
    app,
    db_url='sqlite://../store.db',
    modules={'models':['models']},
    generate_schemas=True,
    add_exception_handlers=True
)