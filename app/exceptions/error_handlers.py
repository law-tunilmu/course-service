"""
4xx error handlers
"""
from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError

def invalid_request_handler(request: Request, exc: RequestValidationError):
    detail_dict: dict[str, str] = exc.errors()[0]
    field_name = " ".join(detail_dict['loc'])
    message = f'{field_name} is missing'
    
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )