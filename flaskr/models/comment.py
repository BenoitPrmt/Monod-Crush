from datetime import datetime
from typing import Optional, Literal


class Comment:
    """ Comment class """

    id: int
    message: str
    author_id: int
    status: Literal['pending', 'approved', 'rejected']
    anonymous: bool
    created: datetime
    reports: Optional[int]
    last_updated: Optional[datetime]
    liked: Optional[int]
