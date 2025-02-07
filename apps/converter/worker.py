# Convert files from 
import time
from ffmpeg import FFmpeg
import os
import time
import string
import random
from dotenv import load_dotenv
from s3 import *
load_dotenv() 

dirname = os.path.dirname(__file__)
upload_folder = os.path.join(dirname, 'upload/')
converted_folder = os.path.join(dirname, 'converted/')
tmp_upload_folder = os.path.join(dirname, 'tmp/upload/')
tmp_converted_folder = os.path.join(dirname, 'tmp/converted/')
all_files_converted = []

def file_already_converted(file_path):
    global all_files_converted
    file_name = os.path.basename(file_path)
    file_data = os.path.splitext(file_name)
    file_basename = file_data[0]
    converted_name = file_basename + '.ogg'
    if os.getenv('STORAGE_LOCAL') == 'true':
        return os.path.isfile(converted_folder + converted_name)
    else:
        return converted_name in all_files_converted

def convert_to_ogg(file_path):
    file_name = os.path.basename(file_path)
    file_data = os.path.splitext(file_name)
    file_basename = file_data[0]
    input_file=""
    output_file=""

    if os.getenv('STORAGE_LOCAL') != 'true':
        s3_download_file(file_path, tmp_upload_folder + file_name)
        input_file = tmp_upload_folder + file_name
        output_file = tmp_upload_folder + file_basename + ".ogg" 
    else:
        input_file = file_path
        output_file = converted_folder + file_basename + ".ogg" 

    ffmpeg = (
        FFmpeg()
        .input(input_file)
        .output(output_file)
    )
    ffmpeg.execute()

    return output_file

def processLocalFiles():
    print("[DEBUG] Processing local files")
    filesUploaded = [f for f in os.listdir(upload_folder) if os.path.isfile(upload_folder + f)]
    for file in filesUploaded:
        if file_already_converted(file):
            continue
        print(file)
        convert_to_ogg(upload_folder + file)
        print("File will be stored locally")

def processRemoteFiles():
    global all_files_converted
    filesUploaded = s3_get_uploaded_files()
    all_files_converted = s3_get_converted_files()
    print("[DEBUG] processing remote files")
    print(filesUploaded)
    for file in filesUploaded:
        if file_already_converted(file):
            continue
        print("[DEBUG] Converting file: " + file)
        converted_file = convert_to_ogg("upload/" + file)
        print("[DEBUG] Uploading file: " + converted_file)
        s3_upload_file(converted_file, "converted/" + os.path.basename(converted_file))

def processFiles():
    if os.getenv('STORAGE_LOCAL') == 'true':
        processLocalFiles()
    else:
        processRemoteFiles()
 
def main():
    if os.getenv('STORAGE_LOCAL') != 'true':
        start_s3_connection()
    while(True):
        processFiles()
        time.sleep(5)

main()
