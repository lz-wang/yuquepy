"""
References: https://www.yuque.com/yuque/developer/doc
"""
from typing import Optional, Any, Union

from pydantic import BaseModel

from .repo import RepoBaseInfo
from .user import UserBaseInfo, UserCreatorInfo


class DocBaseInfo(BaseModel):
    id: int
    slug: str
    title: str

    book_id: int  # 仓库编号，就是 repo_id
    book: Any  # 仓库信息，就是 repo 信息

    user_id: int
    last_editor_id: int
    last_editor: UserBaseInfo

    public: int  # 是否公开 [1 - 公开, 0 - 私密]
    status: int  # 状态 [1 - 正常, 0 - 草稿]
    view_status: int
    read_status: int

    word_count: int
    likes_count: int
    read_count: int
    comments_count: int

    cover: Optional[Any] = None
    description: Optional[str] = None
    custom_description: Optional[Any] = None
    draft_version: int
    format: str  # 描述了正文的格式 [asl, markdown]

    published_at: Optional[str] = None
    first_published_at: Optional[str] = None
    content_updated_at: str
    created_at: str
    updated_at: str
    _serializer: str


class DocData(BaseModel):
    id: int
    slug: str
    title: str

    book_id: int  # 仓库编号，就是 repo_id
    book: Union[RepoBaseInfo, None]  # 仓库信息，就是 repo 信息

    user_id: int
    creator: Union[UserCreatorInfo, None]

    format: str  # 描述了正文的格式 [asl, markdown]
    body: str  # 正文 Markdown 源代码
    body_draft: str  # 草稿 Markdown 源代码
    body_html: Optional[str] = None  # 转换过后的正文 HTML
    body_lake: Optional[str] = None  # 语雀 lake 格式的文档内容
    body_draft_lake: Optional[str] = None  # 语雀 lake 格式的文档内容

    public: int  # 是否公开 [1 - 公开, 0 - 私密]
    status: int  # 状态 [1 - 正常, 0 - 草稿]
    view_status: int
    read_status: int

    word_count: int
    likes_count: Optional[int] = None
    comments_count: Optional[int] = None

    cover: Optional[Any] = None
    description: Optional[str] = None
    custom_description: Optional[Any] = None
    hits: Optional[int] = None

    published_at: Optional[str] = None
    first_published_at: Optional[str] = None
    content_updated_at: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str] = None
    _serializer: str


class DocPermission(BaseModel):
    update: bool
    destroy: bool


class DocDetailInfo(BaseModel):
    abilities: DocPermission
    data: DocData
