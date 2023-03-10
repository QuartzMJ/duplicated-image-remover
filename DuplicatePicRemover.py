import hashlib
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import sys


def calculate_md5(filename):
    with open(filename, "rb") as f:
        # Read the file in chunks to avoid loading large files into memory all at once
        md5 = hashlib.md5()
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()

def select_folder():
    path = filedialog.askdirectory()
       

# Example usage:
md5 = calculate_md5("path/to/file.txt")
print(md5)