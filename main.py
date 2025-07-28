import os
import sys
import copy
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
If asked by the user to execute a Python file, run the script without arguments unless arguments are explicitly provided.
Any references to the calculator refer to the calculator program, which is run with main.py in the calculator folder. 
Execute the functions in your plan accordingly.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def call_function(function_call_part, verbose=False):
    try:
        if verbose:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")
        args_dict = copy.deepcopy(function_call_part.args)
        args_dict["working_directory"] = "./calculator"
        #print(args_dict)
        function_result = ""
        match (function_call_part.name):
            case "get_files_info":
                function_result = get_files_info(**args_dict)
            case "get_file_content":
                function_result = get_file_content(**args_dict)
            case "write_file":
                function_result = write_file(**args_dict)
            case "run_python_file":
                function_result = run_python_file(**args_dict)
            case _:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )
    except Exception as e:
        print(f"Error: {e}")
        
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

def main():
    if len(sys.argv) < 2:
        print("no prompt provided")
        sys.exit(1)
    messages = [
            types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
            ]
    for i in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
                )
            )
    
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        has_function_calls = False
        func_results = []
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'function_call'):
                    if part.function_call != None:
                        #print(f"{part.function_call}")
                        has_function_calls = True
                        func_result = call_function(part.function_call, True)
                        if not func_result.parts[0].function_response.response:
                            raise Exception("Error: invalid function response format")
                        if "--verbose" in sys.argv:
                            print(f"-> {func_result.parts[0].function_response.response["result"]}")
                        function_response_part = types.Part.from_function_response(
                            name=part.function_call.name,
                            response={"result": func_result},
                        )
                        func_results.append(function_response_part)
        if func_results:
            tool_message = types.Content(role='tool', parts=func_results)
            messages.append(tool_message)
        

        if not has_function_calls:
            print(f"Final Response:\n{response.text}")
            break
    
    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
