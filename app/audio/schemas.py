from typing import Optional, List

from pydantic import BaseModel

from app.repository.schemas import SBaseListResponse


class SAudioResponse(BaseModel):
    id: int
    filename: Optional[str]
    file: str


class SAudioListResponse(SBaseListResponse):
    data: List[SAudioResponse]