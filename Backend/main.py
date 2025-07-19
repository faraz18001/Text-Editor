import os
                    #---File-Mangement-Fucntions---#
"""
new_file()-done
open_file()-done
save_file()-done
save_as_file()-waiting for ui
close_file()-waiting for ui
exit_application()-wating for ui
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



written_text='faraz'       #Leaving this for now becuase the text will come from front-end
def save_file(filename:str):
    file = open(f'{filename}','w')
    file.write(f'{written_text}')
    file.close()



def close_file(filename:str):
    pass
    #will implement this later when the ui is created

def exit_appilcataion():
    pass# will implement this when the ui is created
