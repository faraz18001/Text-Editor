import os
                        #---File-Mangement-Fucntions---#
"""
new_file()
open_file()
save_file()
save_as_file()
close_file()
exit_application()
"""

files_dir = './files'
def new_file(name: str):
    file_path = f'{files_dir}/{name}'
    with open(file_path, 'w') as f:
        f.write(' ')



def open_file(filename: str):
    file_path = f'{files_dir}/{filename}'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read()
    else:
        raise FileNotFoundError(f"File '{filename}' not found in {files_dir}")
        
        

