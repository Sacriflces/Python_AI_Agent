from os.path import commonpath, isfile
from utility import get_abs_paths
from config import MAX_PROMPT_SIZE
from google.genai import types

def get_file_content(working_directory, file_path):
    #Check to see if the file is within the working directory
    abs_working_directory, abs_file_path = get_abs_paths(working_directory, file_path)

    if commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    #Check to see if the file argument is a file
    if not isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        file_content = ""
        #Read contents into a string
        with open(abs_file_path) as f:
            file_content = f.read(MAX_PROMPT_SIZE)
        if len(file_content) == MAX_PROMPT_SIZE:
            file_content +=  f'[...File "{file_path}" truncated at {MAX_PROMPT_SIZE} characters]'
        return file_content
    except Exception as ex:
        return f'Error: reading file "{file_path}" - {ex}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the file content of the specified file path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to retrieve contents from.",
            )
        }
    )
)