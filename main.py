from enum import Enum
from fastapi import FastAPI, HTTPException, Depends, Query, Form
from pydantic import BaseModel, Field, conlist
from typing import Optional, List
import databases
import sqlalchemy
from datetime import datetime



db_url = 'sqlite:///../DB_store/STORE_2/store.db'

metadata = sqlalchemy.MetaData()

database = databases.Database(db_url)

Song = sqlalchemy.Table(
    "Song",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("name",sqlalchemy.String(100)),
    sqlalchemy.Column("duration",sqlalchemy.Integer),
    sqlalchemy.Column("upload_time",sqlalchemy.DateTime())
)
Podcast = sqlalchemy.Table(
    "Podcast",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("name",sqlalchemy.String(5)),
    sqlalchemy.Column("duration",sqlalchemy.Integer),
    sqlalchemy.Column("upload_time",sqlalchemy.DateTime()),
    sqlalchemy.Column("host",sqlalchemy.String(100)),
    sqlalchemy.Column("participants",sqlalchemy.types.JSON(10))
)
Audiobook = sqlalchemy.Table(
    "Audiobook",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("title",sqlalchemy.String(100)),
    sqlalchemy.Column("author",sqlalchemy.String(100)),
    sqlalchemy.Column("narrator",sqlalchemy.String(100)),
    sqlalchemy.Column("duration",sqlalchemy.Integer),
    sqlalchemy.Column("upload_time",sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(
    db_url,connect_args={'check_same_thread':False}
)
metadata.create_all(engine)

class FileType(str,Enum):
    song = 'Song'
    podcast = 'Podcast'
    audiobook = 'Audiobook'

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/')
async def root():
    return {'Server status':'Online'}

class SONGIn(BaseModel):
    name : str = Field(...)
    duration : int = Field(...)

class SONG(BaseModel):
    id : int
    name : str
    duration : int
    upload_time : datetime

class PODCASTIn(BaseModel):
    name : str = Field(...)
    duration : int = Field(...)
    host : str = Field(...)
    participants : Optional[conlist(str, max_items=10)] = Field(None)

class PODCAST(BaseModel):
    id : int
    name : str
    duration : int
    upload_time : datetime
    host : str
    participants : Optional[conlist(str, max_items=10)] = Field(None)

class AUDIOBOOKIn(BaseModel):
    title : str = Field(...)
    author : str = Field(...)
    narrator : str = Field(...)
    duration : int = Field(...)

class AUDIOBOOK(BaseModel):
    id : int
    title : str
    author : str
    narrator : str
    duration : int
    upload_time : datetime


''' # NEED MORE WORK HERE
@app.post('/test/{string}', response_model=SONG or PODCAST or AUDIOBOOK)
async def create(string:FileType):
    if string == FileType.song:
        create_song()
    elif string == FileType.podcast:
        create_podcast()
    elif string == FileType.audiobook:
        create_audiobook()
    else:
        raise HTTPException(status_code=404,details='Invalid')
'''

@app.post('/create/1',response_model=SONG)
async def create_song(s:SONGIn = Depends()):
    query = Song.insert().values(
        name =  s.name,
        duration = s.duration,
        upload_time = datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = Song.select().where(Song.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.post('/create/1',response_model=PODCAST)
async def create_podcast(p:PODCASTIn = Depends()):
    query = Podcast.insert().values(
        name =  p.name,
        duration = p.duration,
        upload_time = datetime.utcnow(),
        host = p.host,
        participants = p.participants
    )
    record_id = await database.execute(query)
    query = Podcast.select().where(Podcast.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.post('/create/1',response_model=AUDIOBOOK)
async def create_audiobook(a:AUDIOBOOKIn = Depends()):
    query = Audiobook.insert().values(
        title =  a.title,
        author = a.author,
        narrator = a.narrator,
        duration = a.duration,
        upload_time = datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = Audiobook.select().where(Audiobook.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}