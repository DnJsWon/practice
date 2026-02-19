import schemas
from fastapi import FastAPI, HTTPException
import schemas # 만들어둔 양식 가져오기

app = FastAPI()

fake_db = []
post_id_counter = 1

@app.get("/")
def mainpage():
    return {"message": "Hello World", "status": "fakeDB로 연습"}

@app.post("/post", response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate):
    global post_id_counter

    new_post = {
        "id": post_id_counter,
        "title": post.title,
        "content": post.content
    }

    fake_db.append(new_post)

    post_id_counter += 1

    return new_post

@app.get("/posts")
def get_posts():
    return fake_db

@app.patch("/posts/{post_id}")
def update_post(post_id: int, post_update: schemas.PostCreate):
    for item in fake_db:
        if item["id"] == post_id:
            item["title"] = post_update.title
            item["content"] = post_update.content
            return item
    
    raise HTTPException(status_code=404, detail="수정할 게시글이 없습니다.")

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == post_id:
            del fake_db[i]
            return {"message": f"{post_id}번 게시글 삭제 완료"}
    
    raise HTTPException(status_code=404, detail="삭제할 게시글이 없습니다.")

# ==========================================
# 🚀 파라미터 3대장 테스트 구역
# ==========================================

# 1. Path Parameter 테스트
# 주소의 일부분을 변수처럼 쏙 빼온다.
@app.get("/test/path/{user_name}")
def test_path(user_name: str):
    return {"message": f"환영합니다. {user_name}님! (경로 파라미터 확인)"}

# 2. Query Parameter 테스트
# 주소 끝에 ?와 &를 붙여서 욥션을 전달합니다. page는 안 적으면 기본값 1입니다.
@app.get("/test/query")
def test_query(keyword: str, page: int = 1):
    return{
        "message": f"검색어 '{keyword}의 {page}페이지 결과를 가져옵니다. (쿼리 파라미터 확인)'"
    }

# 3. Request Body (요청 본문) 테스트
# 브라우저 주소창으로 테스트 불가 /docs 등을 통해서 사용
@app.post("/test/body")
def test_body(data: schemas.PostCreate):
    return{
        "message": "숨겨진 박스(Body)로 데이터가 잘 도착했습니다!",
        "받은_제목": data.title,
        "받은_내용": data.content
    }