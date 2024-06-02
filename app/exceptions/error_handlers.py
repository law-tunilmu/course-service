"""
4xx error handlers
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .course_exceptions import CourseException

def course_exception_handler(request: Request, exc: CourseException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "description": exc.description
        }
    )

def invalid_request_handler(request: Request, exc: RequestValidationError):
    detail_dict: dict[str, str] = exc.errors()[0]
    field_name = " ".join(detail_dict['loc'])
    message = f'{field_name} is missing'
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = {
            "description": message
        }
    )