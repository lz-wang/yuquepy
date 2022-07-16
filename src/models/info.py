from typing import Optional

from pydantic import BaseModel

REPO_TYPES = ['Book', 'Thread', 'Design', 'Resource']

DOC_FORMATS = ['markdown', 'lake', 'html']


class ErrorInfo(BaseModel):
    message: str
    code: Optional[str]
    status: Optional[int]
