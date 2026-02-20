# main.py
from fastapi import HTTPException
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

# 🌟 핵심 1: DB에 테이블들을 실제로 생성하는 마법의 주문! (서버 켤 때 알아서 도면 보고 테이블을 만듭니다)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🌟 핵심 2: DB 창구 직원(세션)을 배정해주는 함수
def get_db():
    db = SessionLocal() # 직원 한 명 부르기
    try:
        yield db        # 손님(API)에게 직원 연결
    finally:
        db.close()      # 업무 끝나면 직원 퇴근(연결 종료)

# --- [1. Create (생성)] ---
@app.post("/diaries", response_model=schemas.DiaryResponse)
def create_diary(diary: schemas.DiaryCreate, db: Session = Depends(get_db)):
    # 1. Pydantic 스키마(택배 상자)에 담긴 내용으로 SQLAlchemy 모델(DB 도면) 만들기
    new_diary = models.Post(title=diary.title, content=diary.content)
    
    # 2. DB에 데이터 밀어 넣고 저장! (fake_db.append 대신 이거 씁니다)
    db.add(new_diary)
    db.commit()          # "진짜로 저장해!" (도장 쾅)
    db.refresh(new_diary) # DB가 만들어준 id 번호를 새로고침해서 가져옴
    
    return new_diary

# --- [2. Read (조회)] ---
@app.get("/diaries")
def read_all_diaries(db: Session = Depends(get_db)):
    # DB에 가서 Post(게시글) 테이블에 있는 데이터를 전부(.all()) 가져와라!
    diaries = db.query(models.Post).all()
    return diaries

# --- [3. Update (수정)] ---
@app.patch("/diaries/{diary_id}")
def update_diary(diary_id: int, diary_update: schemas.DiaryCreate, db: Session = Depends(get_db)):
    # 1. DB 직원에게 "Post 테이블에서 id가 diary_id랑 똑같은 거 첫 번째 놈(.first()) 좀 찾아와!" 라고 시킵니다.
    db_diary = db.query(models.Post).filter(models.Post.id == diary_id).first()
    
    # 2. 찾아봤는데 없으면 에러 던지기
    if db_diary is None:
        raise HTTPException(status_code=404, detail="수정할 일기가 없습니다.")
        
    # 3. 찾았다면 파이썬 객체의 내용을 싹 바꿔치기
    db_diary.title = diary_update.title
    db_diary.content = diary_update.content
    
    # 4. DB에 "바뀐 내용 진짜로 저장해!" 도장 쾅
    db.commit()
    db.refresh(db_diary)
    
    return db_diary

# --- [4. Delete (삭제)] ---
@app.delete("/diaries/{diary_id}")
def delete_diary(diary_id: int, db: Session = Depends(get_db)):
    # 1. 일단 지울 일기가 DB에 있는지부터 찾습니다.
    db_diary = db.query(models.Post).filter(models.Post.id == diary_id).first()
    
    if db_diary is None:
        raise HTTPException(status_code=404, detail="삭제할 일기가 없습니다.")
        
    # 2. DB 직원에게 "이거 완전 삭제해!" 라고 지시
    db.delete(db_diary)
    db.commit() # 지운 상태로 도장 쾅
    
    return {"message": f"{diary_id}번 일기가 영구 삭제되었습니다."}