import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.join(working_directory, file_path)
        abs_work_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_file_path)
        if not abs_file_path.startswith(abs_work_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite the contents of a specific file with a given string. The file location is constrained to the working directory. If the file doesn't exist, create the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string of content to be written to the file.",
            ),
        },
    ),
)