# schemas.py
from pydantic import BaseModel

# 1. 회원가입할 때 (받는 데이터)
class UserCreate(BaseModel):
    email: str
    password: str
    nickname: str

# 2. 유저 정보 보여줄 때 (보내는 데이터)
# 비밀번호는 절대 보내면 안 되니까 뺍니다.
class UserResponse(BaseModel):
    id: int
    email: str
    nickname: str
    
    class Config:
        from_attributes = True # DB 모델을 Pydantic 모델로 변환 허용

# 3. 글 쓸 때 (받는 데이터)
class PostCreate(BaseModel):
    title: str
    content: str