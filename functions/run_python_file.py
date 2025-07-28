import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_file_path = os.path.join(working_directory, file_path)
        abs_work_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_file_path)
        #print(abs_work_directory + " " + abs_file_path)
        
        if not abs_file_path.startswith(abs_work_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        args_list = ["python3", abs_file_path]
        if args != []:
            args_list.extend(args)
        completed_process = subprocess.run(args_list, cwd=abs_work_directory,capture_output=True, text=True, timeout=30)
                
        output = "STDOUT:"
        if completed_process.stdout == "":
            output += "No output produced.\n"
        else:
            output = "STDOUT:" + completed_process.stdout + "\nSTDERR:"
        if completed_process.stderr == "":
            output += "No output produced.\n"
        else:
            output += completed_process.stderr + "\n"
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"
        return output



    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python script with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the script relative to the working directory. The script must end with a .py file extnsion.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="An optional list of arguments to pass to the Python script.",
            ),
            
        },
    ),
)