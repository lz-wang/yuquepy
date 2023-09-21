"""
References: https://www.yuque.com/yuque/developer/user
"""
from typing import Optional

from pydantic import BaseModel


class UserBaseInfo(BaseModel):
    type: str

    id: int
    login: str
    name: str

    description: Optional[str] = None
    avatar_url: str

    followers_count: int
    following_count: int

    created_at: str
    updated_at: str
    _serializer: str


class UserCreatorInfo(UserBaseInfo):
    books_count: int
    public_books_count: int


class UserDetailInfo(BaseModel):
    type: str

    id: int
    space_id: int
    account_id: int
    login: str
    name: str
    avatar_url: str

    books_count: int
    public_books_count: int
    followers_count: int
    following_count: int

    public: int
    description: Optional[str] = None
    created_at: str
    updated_at: str
    _serializer: str
