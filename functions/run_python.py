from os.path import commonpath, isfile, exists, dirname
from os import mkdir
from utility import get_abs_paths
from config import TIMEOUT
import subprocess    

def run_python_file(working_directory, file_path, args=None):
    #Check to see if the directory is within the working directory
    abs_working_directory, abs_file_path = get_abs_paths(working_directory, file_path)

    if commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        process_results = subprocess.run(
            commands, 
            cwd=abs_working_directory, 
            capture_output=True, 
            timeout=TIMEOUT, 
            text=True)

        formatted_output_arr = []
        if process_results.stdout:
            formatted_output_arr.append(f"STDOUT: {process_results.stdout}")
        if process_results.stderr:
            formatted_output_arr.append(f"STDERR: {process_results.stderr}")
        if process_results.returncode != 0:
            formatted_output_arr.append(f"Process exited with code {process_results.returncode}")
        
        return "\n".join(formatted_output_arr) if formatted_output_arr else "No output produced."
    except Exception as ex:
        return f"Error: executing Python file: {ex}"