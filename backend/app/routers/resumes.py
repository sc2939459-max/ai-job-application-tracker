import re

import uuid

import mimetypes
import os
import tempfile

from pathlib import Path



from fastapi import (

    APIRouter,

    Depends,

    HTTPException,

    UploadFile,

    File,

    Form,

)

from fastapi.responses import FileResponse, Response

from sqlalchemy.orm import Session

from vercel.blob import AsyncBlobClient, BlobClient



from ..database import get_db

from ..deps import get_current_user



from ..models import (

    ResumeVersion,

    ResumeAnalysis,

    MatchAnalysis,

    JobApplication,

)



from ..schemas import (

    ResumeCreate,

    ResumeOut,

)



from ..services.resume_parser import (

    extract_text_from_pdf,

)





# ============================================================

# ROUTER

# ============================================================



router = APIRouter(

    prefix="/resumes",

    tags=["Resumes"],

)




