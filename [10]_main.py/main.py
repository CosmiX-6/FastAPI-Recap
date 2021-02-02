from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates('templates')
app =FastAPI()

@app.get('/todo/{id}',response_class=HTMLResponse)
async def test(request:Request,id:int):
    return templates.TemplateResponse("index.html",{'request':request,'t_id':id})