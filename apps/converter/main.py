from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import asyncio
import os
import time
import string
import random
from dotenv import load_dotenv
load_dotenv() 

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
	return { "status": "ERROR", "description": "S3 bucket not configured yet." }

def get_file_status(file_id):
	if os.getenv('STORAGE_LOCAL') == 'true':
		return get_local_file_status(file_id)
	return get_remote_file_status(file_id) 

def upload_file_to_s3(upload_file_name, file):
	print("[DEBUG] S3 upload not implemented yet");
	return False

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

def download_file_from_s3(file_id):
	return {
		"message": f"File {file_id} does not exists.",
		"status": "ERROR",
		"id": file_id
	}

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.post("/upload/{file_id}")
def convert(file_id, file: UploadFile):
	upload_file_name = file_id + file.filename  
	hasErrors = False

	if os.getenv('STORAGE_LOCAL') == 'true':
		hasErrors = save_file_locally(upload_file_name, file)
	else:
		hasErrors = upload_file_to_s3(upload_file_name, file)

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

@app.get("/download/{file_id}")
async def download(file_id):
	if os.getenv('STORAGE_LOCAL') == 'true':
		return download_file_locally(file_id)
	else:
		return download_file_from_s3(file_id)
