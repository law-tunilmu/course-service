import os
import datetime

import cloudinary.uploader
import cloudinary
import dotenv

from supabase.client import AsyncClient, Client
from supabase.lib.client_options import ClientOptions

async def supa_async() -> AsyncClient:
    dotenv.load_dotenv()
    supa_client = AsyncClient(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    if not os.environ.get('PRODUCTION', False):
        supa_client.rest_url = os.environ['SUPABASE_URL']
        
        schema = os.environ.get("SUPABSE_SCHEMA", "public")
        supa_client.options = ClientOptions(schema=schema)

    return supa_client

def supa() -> Client:
    dotenv.load_dotenv()
    supa_client = Client(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    if not os.environ.get('PRODUCTION', False):
        supa_client.rest_url = os.environ['SUPABASE_URL']
        
        schema = os.environ.get("SUPABSE_SCHEMA", "public")
        supa_client.options = ClientOptions(schema=schema)

    return supa_client

def get_current_utc() -> str:
    utc_now = datetime.datetime.now(datetime.UTC)
    utc_now_str = str(utc_now).split(".")[0] # strip away miliseconds precision
    return utc_now_str

class CloudinaryUpload:
    def __init__(self) -> None:
        dotenv.load_dotenv()
    
    def upload(self, file_as_base64: str) -> str:
        result = cloudinary.uploader.unsigned_upload(
            file_as_base64,
            cloud_name=os.environ["CL_CLOUDNAME"],
            api_key=os.environ["CL_APIKEY"],
            api_secret=os.environ["CL_APISECRET"],
            upload_preset=os.environ["CL_PRESET"]
        )
        return result['secure_url']

    def delete(self, cl_url: str) -> None:
        public_id = cl_url.split("/")[-1]
        cloudinary.uploader.destroy(
            public_id,
            cloud_name=os.environ["CL_CLOUDNAME"],
            api_key=os.environ["CL_APIKEY"],
            api_secret=os.environ["CL_APISECRET"],
            upload_preset=os.environ["CL_PRESET"]
        )