from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import asyncio
import os
import time
import string
import random
from dotenv import load_dotenv
load_dotenv() 
from s3 import *

def main():
    if os.getenv('STORAGE_LOCAL') != 'true':
        start_s3_connection()

app = FastAPI()
main()

def get_local_file_status(file_id):
    files_found = [entry for entry in os.listdir('uploaded') if entry.startswith(file_id) and entry.endswith('.mp3') and os.path.isfile('uploaded/' + entry)]
    if not files_found:
        return { "status": "MISSING", "description": "File was not found!" }
    
    file_path = files_found[0]
    file_name = os.path.basename(file_path)
    file_data = os.path.splitext(file_name)
    file_basename = file_data[0]

    if os.path.isfile('converted/' + file_basename + '.ogg'):
        return { "status": "CONVERTED", "description": "File already converted to OGG." }

    return { "status": "PROCESSING", "description": "File still being processed." }

def get_remote_file_status(file_id):
    uploaded_file = list(filter(lambda f: os.path.basename(f).startswith(file_id) and os.path.basename(f).endswith('.mp3'), s3_get_uploaded_files()))
    converted_file = list(filter(lambda f: os.path.basename(f).startswith(file_id) and os.path.basename(f).endswith('.ogg'), s3_get_converted_files()))

    print("[DEBUG] converted file")
    print(converted_file)
    print("[DEBUG] uploaded file")
    print(uploaded_file)

    if not uploaded_file:
        return { "status": "MISSING", "description": "File was not found!" }
    elif converted_file:
        return { "status": "CONVERTED", "description": "File already converted to OGG." }

    return { "status": "PROCESSING", "description": "File still being processed." }

def get_file_status(file_id):
    if os.getenv('STORAGE_LOCAL') == 'true':
        return get_local_file_status(file_id)
    return get_remote_file_status(file_id) 

def save_file_locally(upload_file_name, file):
    hasErrors = False
    try:
        contents = file.file.read()
        with open("uploaded/" + upload_file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        hasErrors = True
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()

    return hasErrors

def download_file_locally(file_id):
    files_found = [entry for entry in os.listdir('converted') if entry.startswith(file_id) and entry.endswith('.ogg') and os.path.isfile('converted/' + entry)]

    if not files_found:
        return {
            "message": f"File {file_id} does not exists.",
            "status": "ERROR",
            "id": file_id
        }
    full_file_path = 'converted/' + files_found[0]
    
    return FileResponse(full_file_path)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/{file_id}")
def convert(file_id, file: UploadFile):
    upload_file_name = file_id + file.filename  
    hasErrors = False

    if os.getenv('STORAGE_LOCAL') == 'true':
        hasErrors = save_file_locally(upload_file_name, file)

    if hasErrors:
        return {
            "message": f"File {file.filename} was not uploaded!.",
            "status": "ERROR",
            "id": file_id
        }
    else: 
        return {
            "message": f"File {file.filename} uploaded correctly.",
            "status": "OK",
            "id": file_id
        }

@app.get("/status/{file_id}")
async def status(file_id):
    return get_file_status(file_id)

#et
@app.get("/download/{file_id}")
async def download(file_id):
    if os.getenv('STORAGE_LOCAL') == 'true':
        return download_file_locally(file_id)

    return {
        "message": f"Not allowed to download files from here. Download from S3 BUCKET.",
        "status": "ERROR",
        "id": file_id
    }
