import base64
import binascii
from fastapi import status, HTTPException

from .schemas import CourseCreate 

PICTURE_SIZE=5 # in mb

# performs non-null checks
def validate_course(course: CourseCreate) -> None:
    
    if course.price < 0:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "Price field must NOT be negative"
        )
        
    if course.picture:
        try:
            _, bodyImage = course.picture.split(",")
            picture_byte: bytes = base64.b64decode(bodyImage)

            if len(picture_byte) * 8 > PICTURE_SIZE * 1_000_000:
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail = f"Picture must be less than {PICTURE_SIZE}mb"
                )
            
        except binascii.Error:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                description = "Picture field must be encoded as a base64"
            )