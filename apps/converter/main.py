from fastapi import FastAPI, File, UploadFile, HTTPException
import asyncio
import os
import time
import string
import random

def current_milli_time():
    return round(time.time() * 1000)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return str(current_milli_time()) + ''.join(random.choice(chars) for _ in range(size))

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

@app.post("/upload")
def convert(file: UploadFile):
    file_id = id_generator()
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
