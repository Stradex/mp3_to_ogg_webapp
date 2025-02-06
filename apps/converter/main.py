from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import asyncio
import os
import time
import string
import random

def get_file_status(file_id):
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

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/{file_id}")
def convert(file_id, file: UploadFile):
    upload_file_name = file_id + file.filename  
    try:
        contents = file.file.read()
        with open("uploaded/" + upload_file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        file.file.close()
    return {
        "message": f"File {file.filename} uploaded correctly.",
        "status": "OK",
        "id": file_id
    }

@app.get("/status/{file_id}")
async def status(file_id):
    return get_file_status(file_id)

@app.get("/download/{file_id}")
async def download(file_id):
    files_found = [entry for entry in os.listdir('converted') if entry.startswith(file_id) and entry.endswith('.ogg') and os.path.isfile('converted/' + entry)]

    if not files_found:
        return {
        "message": f"File {file_id} does not exists.",
        "status": "ERROR",
        "id": file_id
    }
    full_file_path = 'converted/' + files_found[0]
    
    return FileResponse(full_file_path)
