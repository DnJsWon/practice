# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 1. 환경 변수(.env) 불러오기
load_dotenv()

# 2. DB 주소 가져오기 (아까 .env 파일에 적어둔 그 주소입니다!)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. 엔진 생성 (파이썬과 PostgreSQL을 연결하는 진짜 케이블 선)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. 세션 생성기 (DB에 접속해서 일할 '창구 직원'을 만들어내는 기계)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base 클래스 (아까 models.py에서 도면 그릴 때 썼던 그 찰흙 판입니다!)
Base = declarative_base()