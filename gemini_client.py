import google.generativeai as genai
from config import load_config 

def prompt1(text):
    cfg = load_config()
    api_key = cfg.get("api_key", "")

    if not api_key:
        return None, "No API key configured."
    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt_template = cfg.get("prompt_template1", "")
        prompt = prompt_template + " " + text

        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        error_message = str(e)
        if "API_KEY_INVALID" in error_message:
            return None, "Invalid API key. Please check your settings."
        if "RATE_LIMIT" in error_message:
            return None, "Rate limit exceeded. Please try again later."
        return None, f"An error occurred: {error_message}"
    
def prompt2(text):
    cfg = load_config()
    api_key = cfg.get("api_key", "")
    if not api_key:
        return None, "No API key configured."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3-flash-preview")
        prompt_template = cfg.get("prompt_template2", "")
        prompt = prompt_template + " " + text
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        error_message = str(e)
        if "API_KEY_INVALID" in error_message:
            return None, "Invalid API key. Please check your settings."
        if "RATE_LIMIT" in error_message:
            return None, "Rate limit exceeded. Please try again later."
        return None, f"An error occurred: {error_message}"
    