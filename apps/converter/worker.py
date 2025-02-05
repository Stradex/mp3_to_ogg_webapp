# Convert files from 
import time
from ffmpeg import FFmpeg
import os
import time
import string
import random

dirname = os.path.dirname(__file__)
upload_folder = os.path.join(dirname, 'uploaded/')
converted_folder = os.path.join(dirname, 'converted/')

def file_already_converted(file_path):
    file_name = os.path.basename(file_path)
    file_data = os.path.splitext(file_name)
    file_basename = file_data[0]

    return os.path.isfile(converted_folder + file_basename + '.ogg')
def convert_to_ogg(file_path):
    file_name = os.path.basename(file_path)
    file_data = os.path.splitext(file_name)
    file_basename = file_data[0]
    ffmpeg = (
        FFmpeg()
        .input(file_path)
        .output(converted_folder + file_basename + ".ogg")
    )

    ffmpeg.execute()

def uploadFileToBucket(file_path):
    print("Uploading to bucket...")

def processFiles():
    print("[DEBUG] Processing files...")
    filesUploaded = [f for f in os.listdir(upload_folder) if os.path.isfile(upload_folder + f)]
    for file in filesUploaded:
        if file_already_converted(file):
            continue
        print(file)
        convert_to_ogg(upload_folder + file)
        uploadFileToBucket(converted_folder + file)

def main():
    while(True):
        processFiles()
        time.sleep(5)

main()
