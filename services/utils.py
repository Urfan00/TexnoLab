

import os

def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


