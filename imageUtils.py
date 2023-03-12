import os
import hashlib

def findFiles(base):
    for subdir, dirs, files in os.walk(base):
        for file in files:
            file_path = os.path.join(subdir, file)
            yield file_path

def calculate_md5(filename):
    with open(filename, "rb") as f:
        # Read the file in chunks to avoid loading large files into memory all at once
        md5 = hashlib.md5()
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()

def calculate_size(file_path):
    return os.path.getsize(file_path)

def process_file(file_path):
    file_md5 = calculate_md5(file_path)
    file_size = calculate_size(file_path)
    file_name = os.path.basename(file_path)
    dir_path = os.path.dirname(file_path)
    return file_name,dir_path,file_size,file_md5