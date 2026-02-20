# models.py
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base # 나중에 database.py에서 만들 Base(뼈대)를 가져옵니다.

# 1. 유저 테이블
class User(Base):
    __tablename__ = "users" # 실제 DB에 생성될 테이블 이름

    id = Column(Integer, primary_key=True, index=True) # SERIAL PRIMARY KEY
    email = Column(String(100), unique=True, nullable=False) # UNIQUE NOT NULL
    hashed_password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    role = Column(String(20), default="user", nullable=False) # DEFAULT 'user'
    is_admin = Column(Boolean, default=False)
    profile_image_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # DEFAULT CURRENT_TIMESTAMP
    is_active = Column(Boolean, default=True)

    # 파이썬에서 편하게 쓰기 위한 연결선 (DB 테이블엔 안 생김)
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")


# 2. 게시글 테이블
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    # 외래키: users 테이블의 id를 참조, 유저 삭제 시 게시글도 동시 삭제(CASCADE)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 연결선
    owner = relationship("User", back_populates="posts")
    images = relationship("PostImage", back_populates="post")
    comments = relationship("Comment", back_populates="post")


# 3. 사진 관리 테이블
class PostImage(Base):
    __tablename__ = "post_images"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    image_url = Column(Text, nullable=False)
    file_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 연결선
    post = relationship("Post", back_populates="images")


# 4. 댓글 테이블
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 연결선
    post = relationship("Post", back_populates="comments")
    owner = relationship("User", back_populates="comments")


# 5. 좋아요(추천) 테이블
class PostLike(Base):
    __tablename__ = "post_likes"

    # 복합키 (user_id와 post_id 두 개를 합쳐서 하나의 Primary Key로 사용)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())