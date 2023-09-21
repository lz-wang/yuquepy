"""
References: https://www.yuque.com/yuque/developer/group
"""
from typing import Optional, Any

from pydantic import BaseModel


class GroupData(BaseModel):
    type: Optional[str] = 'Group'

    id: int
    login: str
    name: str
    avatar_url: str

    owner_id: Optional[int] = None
    space_id: Optional[int] = None
    organization_id: Optional[int] = None

    books_count: int
    public_books_count: int
    topics_count: int
    public_topics_count: int
    members_count: int

    public: int
    description: Optional[str] = None
    created_at: str
    updated_at: str

    grains_sum: Optional[int] = None
    _serializer: str


class UserInGroup(BaseModel):
    type: str

    id: int
    login: str
    name: str
    avatar_url: str

    followers_count: int
    following_count: int

    description: Optional[str] = None
    created_at: str
    updated_at: str
    _serializer: str


class GroupUserData(BaseModel):
    id: int
    group_id: int
    user_id: int
    role: int
    visibility: int
    status: int
    user: Optional[UserInGroup] = None
    group: Any
    created_at: str
    updated_at: str
    _serializer: str


class GroupUserPermission(BaseModel):
    create: bool
    update: bool
    destroy: bool


class GroupRepoPermission(BaseModel):
    create: bool
    update: bool
    destroy: bool


class GroupPermission(BaseModel):
    read: bool
    update: bool
    destroy: bool
    group_user: GroupUserPermission
    repo: GroupRepoPermission


class GroupMeta(BaseModel):
    topic_enable: int


class GroupDetailInfo(BaseModel):
    abilities: GroupPermission
    meta: GroupMeta
    data: GroupData
