from starlette import status
from starlette.responses import JSONResponse


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