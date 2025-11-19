import json

from sqlalchemy import RowMapping
from starlette import status
from starlette.responses import JSONResponse
from datetime import datetime


class TodoResponse(JSONResponse):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.content = {
            "status": "TODO",
            "message": "API尚未实现"
        }
        super().__init__(status_code=self.status_code, content=self.content)

class OKResponse(JSONResponse):
    def __init__(self, content):
        self.status_code = status.HTTP_200_OK
        self.content = content
        super().__init__(status_code=self.status_code, content=self.content)

    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=True,
            indent=None,
            separators=(",", ":"),
            default=lambda x: {i: x[i] if not isinstance(x[i], datetime) else x[i].isoformat() for i in x},
        ).encode("utf-8")

class ErrorResponse(JSONResponse):
    def __init__(self, error):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.content = str(error)
        super().__init__(status_code=self.status_code, content=self.content)
