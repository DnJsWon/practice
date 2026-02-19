from pydantic import BaseModel

# 1. 사용자가 글을 쓸 때 서버로 보낼 양식
# (사용자는 글 번호(id)를 정할 수 없으니 제목과 내용만 받습니다.)
class PostCreate(BaseModel):
    title: str
    content: str

# 2. 서버가 사용자에게 보여줄 게시글 양식
# (서버가 번호(id)를 부여해서 같이 보여줍니다.)
class PostResponse(BaseModel):
    id: int
    title: str
    content: str