import os
import random

def choice_file_to_del(origin):
    file_dir = random.choice(os.listdir(origin))
    return file_dir
def del_file(direc):
    if os.path.exists(direc):
        if os.path.isfile(direc):
            os.remove(direc)
        else:
            os.rmdir(direc)
