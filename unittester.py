from typing import Optional, List

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    return q