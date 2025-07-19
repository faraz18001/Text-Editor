                        #---File-Mangement-Fucntions---#
files_dir = './files'
def new_file(name: str):
    file_path = f'{files_dir}/{name}'
    with open(file_path, 'w') as f:
        f.write(' ')
