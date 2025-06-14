from os.path import commonpath, isfile, exists, dirname
from os import mkdir
from utility import get_abs_paths

def write_file(working_directory, file_path, content):
    #Check to see if the directory is within the working directory
    abs_working_directory, abs_file_path = get_abs_paths(working_directory, file_path)
    
    if commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    basename =dirname(abs_file_path)
    if not exists(basename):
        mkdir(basename)
        
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as ex:
        return f'Error: writing file "{file_path}" - {ex}'

