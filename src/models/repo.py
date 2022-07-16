"""
References: https://www.yuque.com/yuque/developer/repo
"""
from typing import Optional, Any, Union

from pydantic import BaseModel

from .user import UserBaseInfo


class RepoBaseInfo(BaseModel):
    type: str

    id: int
    slug: str  # 仓库路径
    name: str  # 仓库名称
    namespace: str  # 仓库完整路径 user.login/book.slug

    user_id: int
    user: UserBaseInfo
    creator_id: int

    items_count: int
    likes_count: int
    watches_count: int

    public: int  # 公开状态 [1 - 公开, 0 - 私密]
    description: Union[str, None]
    created_at: str
    updated_at: str
    content_updated_at: str
    _serializer: str


class RepoData(BaseModel):
    type: str

    id: int
    slug: str  # 仓库路径
    name: str  # 仓库名称
    namespace: Optional[str]

    user_id: int
    user: Union[UserBaseInfo, None]
    creator_id: Union[int, None]

    items_count: int
    likes_count: int
    watches_count: int

    toc: Optional[str]
    toc_yml: Optional[str]

    public: int  # 公开状态 [1 - 公开, 0 - 私密]
    description: str
    pinned_at: Optional[Any]
    achieved_at: Optional[Any]
    created_at: str
    updated_at: str
    content_updated_at: Optional[str]
    _serializer: str


class RepoDocPermission(BaseModel):
    create: bool


class RepoPermission(BaseModel):
    update: bool
    destroy: bool
    doc: RepoDocPermission


class RepoDetailInfo(BaseModel):
    abilities: RepoPermission
    data: RepoData
