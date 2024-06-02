import sys
import base64
import binascii
from fastapi import status

from .schemas import CourseCreate 
from .exceptions import CourseException

PICTURE_SIZE=5 # in mb

# performs non-null checks
def validate_course(course: CourseCreate) -> None:
    
    if course.price < 0:
        raise CourseException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            description = "Price field must NOT be negative"
        )
        
    if course.picture:
        try:
            _, bodyImage = course.picture.split(",")
            picture_byte: bytes = base64.b64decode(bodyImage)

            if len(picture_byte) * 8 > PICTURE_SIZE * 1_000_000:
                raise CourseException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description = f"Picture must be less than {PICTURE_SIZE}mb"
                )
            
        except binascii.Error:
            raise CourseException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                description = "Picture field must be encoded as a base64"
            )