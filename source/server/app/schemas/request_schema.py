# [ Server ] request_schema.py
# source/server/app/schemas/request_schema.py

from pydantic import BaseModel, HttpUrl

class UrlDetectRequest(BaseModel):
    url: HttpUrl
