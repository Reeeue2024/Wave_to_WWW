# [ Server ] request_schema.py

from pydantic import BaseModel, HttpUrl

class UrlDetectRequest(BaseModel):
    url: HttpUrl
