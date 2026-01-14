import os, subprocess

def run_python_file(working_directory, file_path, args=None):

    #Define working directory and target file
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    #check for file path issues
    try:
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    except ValueError:
        return (f"Error: Issue with commonpath")
    
    #check if file is in permitted directory
    if not valid_target_file:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
   
    #if file path exists and points to regular file
    if not os.path.isfile(target_file):
        return(f'Error: "{file_path}" does not exist or is not a regular file')
    
    #If file name doesn't end with .py
    if not target_file.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file')

    command = ["python", target_file]
    if args:
        command.extend(*args)

    #Run Subprocess
    try:
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out'
    except OSError as e:
        return f'Error: Failed to execute "{file_path}": {e}'
    
    #Try output
    try:
        output_parts=[]

        if result.returncode != 0:
            output_parts.append(f'"Process exited with code {result.returncode}"')
        #check stdout and stderr
        stdout = result.stdout or ""
        stderr = result.stderr or ""

        if not stdout.strip() and not stderr.strip():
            output_parts.append("No output produced")
        else:
            if stdout.strip():
                output_parts.append("STDOUT:")
                output_parts.append(stdout.rstrip())

            if stderr.strip():
                output_parts.append("STDERR:")
                output_parts.append(stderr.rstrip())
    except Exception as e:
        return(f"Error: executing Python file: {e}")
    
    return "\n".join(output_parts)
