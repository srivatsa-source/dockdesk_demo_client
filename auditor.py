import os
import sys
import json
import google.generativeai as genai
import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)

# --- CONFIGURATION ---

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = 'gemini-flash-latest'
GROQ_MODEL = 'mixtral-8x7b-32768'  # or another available model

def get_gemini_response(system_prompt):
    if not GEMINI_API_KEY:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        print(f"{Fore.YELLOW}Gemini failed: {e}")
        return None

def get_groq_response(system_prompt):
    if not GROQ_API_KEY:
        return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are DockDesk, a strict Code Auditor."},
            {"role": "user", "content": system_prompt}
        ],
        "max_tokens": 2048
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"{Fore.YELLOW}Groq failed: {e}")
        return None

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File {filepath} not found.")
        sys.exit(1)

def write_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"{Fore.GREEN}✔ File updated successfully: {filepath}")

def run_audit(code_path, doc_path):
    print(f"{Fore.CYAN}--- DockDesk AI (Auto-Fix Mode) ---")
    print(f"{Fore.YELLOW}Model:{Style.RESET_ALL} {MODEL_NAME}")
    
    code_content = read_file(code_path)
    doc_content = read_file(doc_path)

    # UPDATED PROMPT: Asks for the FULL corrected document content
    system_prompt = f"""
    You are DockDesk, a strict Code Auditor.
    1. Compare the Code vs Documentation.
    2. If they contradict, return STATUS: FAIL.
    3. If FAIL, rewrite the ENTIRE documentation to match the code.
    
    DATA:
    --- DOCS ({doc_path}) ---
    {doc_content}
    --- CODE ({code_path}) ---
    {code_content}

    OUTPUT JSON ONLY:
    {{
        "status": "FAIL" or "PASS",
        "risk_level": "HIGH" or "LOW",
        "impact": "Short explanation of the business risk.",
        "full_corrected_doc": "The ENTIRE content of the documentation file with the fix applied (not just the snippet)."
    }}
    """

    print(f"{Fore.CYAN}🚀 Analyzing Knowledge Integrity...{Style.RESET_ALL}")
    

    # Try Gemini first, then Groq
    result_text = get_gemini_response(system_prompt)
    if not result_text:
        print(f"{Fore.YELLOW}Falling back to Groq...")
        result_text = get_groq_response(system_prompt)
    if not result_text:
        print(f"{Fore.RED}💥 Both Gemini and Groq failed. No API response.")
        sys.exit(1)

    try:
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(result_text)

        print("\n" + "="*40)
        
        if data["status"] == "FAIL":
            # 1. SHOW THE PROBLEM
            print(f"{Fore.RED}❌ KNOWLEDGE DRIFT DETECTED")
            print(f"{Fore.YELLOW}📉 Hallucination Risk: {Fore.RED}{data['risk_level']}" )
            print(f"{Fore.WHITE}⚠️ Business Impact: {data['impact']}")
            print("-" * 40)
            
            # 2. SHOW THE PROPOSED FIX (First 200 chars preview)
            print(f"{Fore.CYAN}ℹ️  Proposed Change Preview:")
            print(f"{Fore.CYAN}{data['full_corrected_doc'][:200]}...") 
            print("-" * 40)

            # 3. ASK TO APPLY
            user_input = input(f"{Fore.MAGENTA}[?] Apply this fix to {doc_path} now? (y/n): {Style.RESET_ALL}")
            
            if user_input.lower() == 'y':
                write_file(doc_path, data['full_corrected_doc'])
                print(f"{Fore.GREEN}✅ FIXED! Knowledge Base is now in sync with Code.")
                sys.exit(0)
            else:
                print(f"{Fore.YELLOW}Action skipped. Docs remain broken.")
                sys.exit(1)
        else:
            print(f"{Fore.GREEN}✅ KNOWLEDGE INTEGRITY VERIFIED")

    except Exception as e:
        print(f"\n{Fore.RED}💥 AI Error:")
        print(f"{Fore.YELLOW}{e}")

if __name__ == "__main__":
    run_audit("auth.py", "README.md")