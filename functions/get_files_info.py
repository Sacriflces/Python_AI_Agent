import os
from os.path import commonpath, isdir
from utility import get_abs_paths

def get_files_info(working_directory, directory=None):
    #Check to see if the directory is within the working directory
    abs_working_directory, target_dir = get_abs_paths(working_directory, directory)

    if commonpath([abs_working_directory, target_dir]) != abs_working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #Check to see if the directory argument is a directory:
    if not isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        #Get directory contents and return a string representation.
        entry_reps = []
        with os.scandir(target_dir) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    entry_reps.append(f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}")
        return "\n".join(entry_reps)
    except Exception as ex:
        return f"Error listing files: {ex}"
