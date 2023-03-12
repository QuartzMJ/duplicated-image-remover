import os
import re
import argparse

def reformat(filepath,path_ending):
    
    filename = os.path.basename(filepath)
    pattern = r"^[0-9]*"
    filename = re.sub(pattern,"", filename)
    pattern = r"boys?|girls?"
    filename = re.sub(pattern,"", filename)
    pattern = r"\b[a-zA-Z0-9]{1,2}\b"
    filename = re.sub(pattern,"", filename)

    pattern_left = "%28"
    pattern_right = "%29"
    filename = re.sub(pattern_left,"(", filename)
    filename = re.sub(pattern_right,")", filename)

    temp_path = filepath
    parent_node = ""
    while parent_node != path_ending:
        temp_path = os.path.dirname(temp_path)
        parent_node = os.path.basename(temp_path)
        filename = parent_node + " " + filename
        print(parent_node)
    
    words = filename.split()
    unique_words = []

    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    
    filename = " ".join(unique_words)

    dir_path = os.path.dirname(filepath)
    new_filepath = os.path.join(dir_path,filename)
    rename_file(filepath,new_filepath,0)
    
    return new_filepath;
   

def rename_file(filepath, new_filepath,count):
    if(count == 0):
        candidte_path = new_filepath
    else:
        candidte_path = new_filepath[0:-4] + str(count) + new_filepath[-4:]
    try:
        os.rename(filepath, candidte_path)
        print("Renaming!")
    except:
        count += 1
        rename_file(filepath,new_filepath,count)


def findFiles(base):
    for subdir, dirs, files in os.walk(base):
        for file in files:
            file_path = os.path.join(subdir, file)
            yield file_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str,help="Path to observe")
    args = parser.parse_args()
    path = args.path
    path_root = os.path.basename(path)
    count = 1
    for file_path in findFiles(path):
        reformat(file_path,path_root);
        print(count)
        count += 1
    
if __name__ == '__main__':
    main()
