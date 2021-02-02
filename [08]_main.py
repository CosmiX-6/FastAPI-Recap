from fastapi import FastAPI, Form


app = FastAPI(title='Forms',version='v0.0.1')

@app.get('/')
async def root():
    return 'Welcome! Form is ready'

@app.post('/language/')
async def lang(name:str = Form(...),type:str = Form(...)):
    return {'name':name,'type':type}