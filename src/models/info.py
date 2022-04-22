from pydantic import BaseModel
from typing import Optional

REPO_TYPES = ['Book', 'Thread', 'Design', 'Resource']

DOC_FORMATS = ['markdown', 'lake', 'html']


class ErrorInfo(BaseModel):
    message: str
    code: Optional[str]
    status: Optional[int]
