from enum import Enum
from fastapi import FastAPI

class ModelName(str,Enum):
    ford='fortuner'
    maruti='benz'
    tata='taycoon'

app = FastAPI()

@app.get('/test/{string}')
async def function_1(string:ModelName):
    if string == ModelName.ford:
        return {'company':string,'model':ModelName.ford,'message':'Testcase 1 passed !'}
    if string.value == 'taycoon':
        return {'company':string,'model':ModelName.tata,'message':'Testcase 2 passed !!'}
    else:
        return {'company':string,'model':ModelName.maruti,'message':'Testcase 3 passed !!'}