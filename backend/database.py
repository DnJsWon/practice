# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings # 방금 만든 config에서 주소를 가져옵니다.

# 1. 엔진 생성 (비동기 방식)
# echo=True: 실행되는 SQL을 터미널에 보여줍니다 (개발할 때 좋음)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. 세션 공장 (SessionLocal)
# DB 연결 세션을 찍어내는 공장입니다.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. 모델들의 부모 클래스
# models.py에서 테이블 만들 때 얘를 상속받습니다.
Base = declarative_base()

# 4. 의존성 주입 함수 (Dependency Injection)
# API 요청이 올 때 세션을 빌려주고, 끝나면 반드시 닫습니다.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()