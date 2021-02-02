from typing import List, Optional

from fastapi import FastAPI, Query

app = FastAPI()

@app.get('/')
async def root():
    return {'Server status':'Online'}

# @app.get("/items/")
# async def read_items(q: Optional[List[str]] = Query(None)):
#     query_items = {"q": q}
#     return query_items

# @app.get("/items/")
# async def read_items(q: str = Query("fixedquery", min_length=3)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results