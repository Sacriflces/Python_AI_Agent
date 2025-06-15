import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("A prompt is needed!")
        exit(1)
    
    user_prompt = " ".join(args)

    if verbose:
        print(f"user prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    agent_feedback_loop(client, messages, verbose)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[
            available_functions],
            system_instruction=system_prompt),
        )
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    return response
        


def agent_feedback_loop(client, messages, verbose):
    for _ in range(20):
        response = generate_content(client, messages, verbose)
        if not response.function_calls:
            print(response.text)
            return
        function_call_results = call_functions(response.function_calls, verbose)
        for candidate in response.candidates:
            messages.append(candidate.content)
        for function_call_result in function_call_results:
            messages.append(types.Content(role="tool", parts=function_call_result))

def call_functions(function_calls, verbose):
    results = []
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Error: No response from function call.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response['result']}")
        results.append(function_call_result.parts[0])
    return results

if __name__ == "__main__":
    main()
