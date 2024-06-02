from typing import Optional
from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    description: Optional[str]
    creator: str
    price: float

class CourseCreate(CourseBase):
    picture: str    # base64 encoded

    class Config:
        from_attributes = True

class CourseEdit(CourseBase):
    id: int
    picture: str    # base64 encoded

    class Config:
        from_attributes = True

class Course(CourseBase):
    id: int
    picture_url: str
    created_at: str
    last_update_at: str

    class Config:
        from_attributes = True
