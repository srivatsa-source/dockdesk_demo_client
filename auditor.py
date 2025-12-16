import os
import sys
import json
import google.generativeai as genai
from colorama import Fore, Style, init

# Initialize color output for the terminal demo
init(autoreset=True)

# --- CONFIGURATION ---
# Make sure to set your env variable: export GEMINI_API_KEY="your_key"
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(f"{Fore.RED}Error: GEMINI_API_KEY not found in environment variables.")
    print(f"{Fore.YELLOW}Tip: Run $env:GEMINI_API_KEY='your_key' (Windows) or export GEMINI_API_KEY='your_key' (Mac/Linux)")
    sys.exit(1)

genai.configure(api_key=api_key)

# We use Flash for speed (simulating a fast CI/CD check)
model = genai.GenerativeModel('gemini-2.0-flash')

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Could not find {filepath}")
        sys.exit(1)

def run_audit(code_path, doc_path):
    print(f"{Fore.CYAN}--- DockDesk AI Knowledge Guardrail ---")
    print(f"{Fore.YELLOW}Target:{Style.RESET_ALL} Preventing Knowledge Decay in {doc_path}")
    
    code_content = read_file(code_path)
    doc_content = read_file(doc_path)

    # --- UPGRADED PROMPT FOR CEO DEMO ---
    system_prompt = f"""
    You are DockDesk, a Knowledge Integrity Agent for Atomicwork.
    
    1. ANALYZE: Compare the Code Logic ({code_path}) vs. Documentation ({doc_path}).
    2. DETECT: Find contradictions that would cause an AI Support Agent to hallucinate/fail.
    3. FIX: If a contradiction exists, REWRITE the specific section of the documentation to match the code.

    DATA:
    --- DOCS ({doc_path}) ---
    {doc_content}
    --- CODE ({code_path}) ---
    {code_content}

    OUTPUT FORMAT (Strict JSON):
    {{
        "status": "FAIL" or "PASS",
        "risk_level": "HIGH" or "LOW",
        "impact": "One sentence explaining why an AI Agent would give wrong answers based on the old docs.",
        "suggested_fix": "The exact Markdown text to replace the outdated section."
    }}
    """

    print(f"{Fore.CYAN}🤖 Simulating Atomicwork Knowledge Scan...{Style.RESET_ALL}")
    
    try:
        response = model.generate_content(system_prompt)
        result = response.text.strip()
        
        # Clean up JSON formatting for terminal display
        if result.startswith("```json"):
            result = result.replace("```json", "").replace("```", "")
        if result.startswith("```"):
            result = result.replace("```", "")
        
        data = json.loads(result)

        print("\n" + "="*40)
        
        if data["status"] == "FAIL":
            print(f"{Fore.RED}❌ KNOWLEDGE DRIFT DETECTED")
            print(f"{Fore.YELLOW}📉 Hallucination Risk: {Fore.RED}{data['risk_level']}")
            print(f"{Fore.WHITE}⚠️ Business Impact: {data['impact']}")
            print("-" * 40)
            print(f"{Fore.GREEN}✨ DockDesk Auto-Fix Suggestion:")
            print(f"{Fore.CYAN}{data['suggested_fix']}")
            print("-" * 40)
            sys.exit(1)
        else:
            print(f"{Fore.GREEN}✅ KNOWLEDGE INTEGRITY VERIFIED")
            print(f"{Fore.WHITE}Docs and Code are perfectly aligned.")
            sys.exit(0)

    except Exception as e:
        print(f"{Fore.RED}Error parsing AI response: {e}")
        print(f"Raw Output: {response.text}")

if __name__ == "__main__":
    # Pointing to the specific files we are about to create
    run_audit("auth.py", "README.md")