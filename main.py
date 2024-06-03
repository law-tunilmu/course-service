import supabase

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from supabase.client import AsyncClient

from app import schemas
from app.exceptions import invalid_request_handler
from app.validators import validate_course
from app.dependencies import supa, supa_async, CloudinaryUpload, get_current_utc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_exception_handler(
    RequestValidationError,
    handler=invalid_request_handler
)

COURSE_TABLE_NAME = 'course'
COURSE_SORT_KEYS = ["id", "title", "creator", "price"]
SELECT_COLUMNS = ", ".join(schemas.Course.model_fields.keys())

@app.get("/course/list")
async def list_courses(page: int = 0, page_size : int = 5, order_by : str = "id", is_descending: bool = False,
                       supa_client: AsyncClient=Depends(supa_async)) -> list[schemas.Course]:
    try:
        query = supa_client.table(COURSE_TABLE_NAME).select(SELECT_COLUMNS)
        if order_by and order_by.lower() in COURSE_SORT_KEYS:
            query = query.order(column=order_by, desc=is_descending)
        result = await query.limit(page_size).offset(page * page_size).execute()
        return result.data
    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/course/detail/{course_id}")
async def get_course(course_id: int, supa_client: AsyncClient=Depends(supa_async)) -> schemas.Course:
    try:
        result = await supa_client.table(COURSE_TABLE_NAME).select(SELECT_COLUMNS) \
                        .eq("id", course_id).maybe_single().execute()
        
        if not result:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Item is not found"
                )

        return result.data
    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/course/created_by")
async def get_created_course(mentor: str, page: int = 0, page_size: int = 5, 
                            supa_client: AsyncClient=Depends(supa_async)) -> list[schemas.Course]:
    try:
        result = await supa_client.table(COURSE_TABLE_NAME) \
                        .select(SELECT_COLUMNS).eq("creator", mentor) \
                        .limit(page_size).offset(page * page_size).execute()
        return result.data
    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/course/search")
async def search_courses(query: str, page: int = 0, page_size: int = 5, 
                        supa_client: AsyncClient=Depends(supa_async)) -> list[schemas.Course]:
    try:
        result = await supa_client.table(COURSE_TABLE_NAME).select(SELECT_COLUMNS) \
                        .limit(page_size).offset(page * page_size) \
                        .text_search("tfs", query, options={"type": "web_search"}).execute()
        return result.data
    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/course/create")
def create_course(  course: schemas.CourseCreate,
                    supa_client: supabase.Client=Depends(supa),
                    cl_client: CloudinaryUpload=Depends(CloudinaryUpload)
                 ) -> schemas.Course:
    validate_course(course)
    courseInDB = course.model_dump(exclude=set(["picture"]))

    picture_url = ""
    if course.picture:
        picture_url = cl_client.upload(course.picture)
    courseInDB["picture_url"] = picture_url

    utc_now = get_current_utc()
    courseInDB['created_at'] = utc_now
    courseInDB['last_update_at'] = utc_now

    try:
        result = supa_client.table(COURSE_TABLE_NAME) \
                    .insert(courseInDB).execute()
        
        return result.data[0]
    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.put("/course/edit")
def edit_course(    course: schemas.CourseEdit,
                    supa_client: supabase.Client=Depends(supa),
                    cl_client: CloudinaryUpload=Depends(CloudinaryUpload)
                 ) -> schemas.Course:
    
    validate_course(course)

    courseInDB = course.model_dump(exclude=set(["picture"]))
    
    if course.picture:
        courseInDB['picture_url'] = cl_client.upload(course.picture)

    courseInDB['last_update_at'] = get_current_utc()

    try:
        result = supa_client.table(COURSE_TABLE_NAME).update(courseInDB) \
                    .eq("id", course.id).execute()

        return result.data[0]
    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.delete("/course/delete")
def delete_course( id: int, supa_client: supabase.Client=Depends(supa), 
                    cl_client: CloudinaryUpload=Depends(CloudinaryUpload)
                ) -> schemas.Course :
    try:
        result = supa_client.table(COURSE_TABLE_NAME) \
                    .delete().eq("id", id).execute()

        course_deleted = result.data[0]

        if course_deleted['picture_url']:
            cl_client.delete(course_deleted['picture_url'])
            course_deleted["picture_url"] = ""

        return course_deleted

    except supabase.PostgrestAPIError:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)