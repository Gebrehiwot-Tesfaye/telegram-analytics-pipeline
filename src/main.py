from fastapi import FastAPI, Query
from typing import List
from .schemas import MediaReport, ChannelActivity, MessageSearchResult, ChannelOverview,Message
from .crud import get_top_media, get_channel_activity, search_messages, get_top_questions, get_channel_overview
from pydantic import BaseModel

app = FastAPI()

class TopQuestion(BaseModel):
    text: str
    count: int

@app.get("/api/reports/top-media", response_model=List[MediaReport])
def top_media(limit: int = Query(10, gt=0)):
    return get_top_media(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity)
def channel_activity(channel_name: str):
    return get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search_messages_endpoint(query: str):
    return search_messages(query)

@app.get("/api/channels", response_model=List[str])
def get_channels():
    from .crud import list_channels
    return list_channels()

@app.get("/api/reports/top-questions", response_model=List[TopQuestion])
def top_questions(limit: int = 10):
    return get_top_questions(limit)

@app.get("/api/channels/overview", response_model=List[ChannelOverview])
def channel_overview():
    return get_channel_overview()

@app.get("/api/messages", response_model=List[Message])
def get_all_messages():
    from .crud import get_all_messages
    return get_all_messages()