import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


    if api_key is None:
        raise RuntimeError ("GEMINI_API_KEY not found in environment variables")

    client = genai.Client(api_key = api_key)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages, 
            config=types.GenerateContentConfig(
                tools = [available_functions],
                system_instruction=system_prompt
                )
        )
    except Exception as e:
        print (f'Error: RuntimeError: API request failed: {e}')

    #if response.usage_metadata == None:
    #    raise RuntimeError ("Failed API request")
    if args.verbose:
        user_prompt = args.user_prompt
        print(f"User prompt: {user_prompt}")

        if response.usage_metadata is not None:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            
    #If there are function calls in response, print them
    if response.function_calls:
        for function_call in response.function_calls:
            print (f"Calling function: {function_call.name}({function_call.args})")
    #Otherwise, print as normal
    elif response.text:
        print(f"Response: {response.text}")
    else:
        print("No response text returned.")



if __name__ == "__main__":
    main()