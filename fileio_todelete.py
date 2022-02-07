
'''
FILE: FILE IO

flattens nested subdirectories
'''

import os
import shutil

def move(destination):
    all_files = []
    first_loop_pass = True
    for root, _dirs, files in os.walk(destination):
        if first_loop_pass:
            first_loop_pass = False
            continue
        for filename in files:
            all_files.append(os.path.join(root, filename))
            print(all_files)
    for filename in all_files:
        shutil.move(filename, destination)

