import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        directory = os.path.join(working_directory, directory)
        abs_work_directory = os.path.abs(working_directory)
        abs_directory = os.path.abs(directory)
        if not abs_directory.startswith(abs_work_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'
        result = ""
        dir_list = os.listdir(directory)
        for item in dir_list:
            item_path = os.path.join(directory, item)
            result += " - " + item + ": file size=" + str(os.path.getsize(item_path)) + " bytes, is_dir=" + str(os.path.isdir(item_path)) + "\n"

        return result
    
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)