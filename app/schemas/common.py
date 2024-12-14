from enum import Enum
from typing import List

from pydantic import BaseModel


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class PaginationMetadata(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    items_per_page: int


class PaginatedResponse(BaseModel):
    data: List
    metadata: PaginationMetadata
