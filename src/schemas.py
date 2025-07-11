from pydantic import BaseModel

class MediaReport(BaseModel):
    media_path: str
    mentions: int

class ChannelActivity(BaseModel):
    channel_name: str
    post_count: int
    last_post_date: str | None
    image_count: int
    reply_count: int

class MessageSearchResult(BaseModel):
    message_id: str
    channel_name: str
    content: str
    date: str
    media: bool
    channel_url: str | None = None
    sender_id: int | None = None
    is_reply: bool | None = None
    image_path: str | None = None  # Add this field if your table has it

class ChannelOverview(BaseModel):
    channel_name: str
    message_count: int
    media_post_count: int
    reply_count: int

class Message(BaseModel):
    id: int
    date: str
    text: str
    media: bool
    channel_name: str
    channel_url: str | None = None
    sender_id: int | None = None
    is_reply: bool | None = None