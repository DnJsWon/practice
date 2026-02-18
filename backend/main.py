# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

# 우리가 만든 파일들 불러오기
from database import get_db
import models
import schemas

app = FastAPI()

# 비밀번호 암호화 도구 (bcrypt 알고리즘)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
async def mainpage():
    return {"message": "Hello World", "status": "Server is running!"}

# 1. 회원가입 API
@app.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    
    # [Step 1] 이메일 중복 체크
    # DB에서 같은 이메일이 있는지 조회합니다.
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    # [Step 2] 비밀번호 암호화
    # 사용자가 입력한 "1234"를 "$2b$12$..." 같은 외계어로 바꿉니다.
    hashed_pw = pwd_context.hash(user.password)

    # [Step 3] DB 저장용 객체 생성 (Entity)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        nickname=user.nickname,
        role="user"
    )

    # [Step 4] 저장 및 확정
    db.add(new_user)      # 메모리에 추가
    await db.commit()     # DB에 진짜 저장
    await db.refresh(new_user) # 저장된 데이터(ID 등) 다시 가져오기

    return new_user

# 2. 게시글 작성 API (테스트용)
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    
    # 지금은 로그인 기능이 없으니, 무조건 1번 유저가 쓴다고 가정합니다.
    # (주의: DB에 id=1인 유저가 먼저 있어야 에러가 안 납니다!)
    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=1 
    )
    
    db.add(new_post)
    await db.commit()
    
    return {"message": "게시글 작성 성공"}