# scripts/analyze_log.py
import os
import sys
import openai

def analyze_log_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        log = f.read()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY is not set in the environment.", file=sys.stderr)
        sys.exit(2)

    openai.api_key = api_key

    prompt = (
        "You are an expert CI build engineer. Summarize the main reason the build failed from the log "
        "and provide 3 actionable fixes (ordered). If you cannot determine, provide 3 debugging steps.\n\n"
        "Build log:\n" + log
    )

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful CI/CD assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=600
        )
        text = resp["choices"][0]["message"]["content"].strip()
        print("\n=== AI Analysis ===\n")
        print(text)
    except Exception as e:
        print("LLM call failed:", str(e), file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_log.py <path-to-log>", file=sys.stderr)
        sys.exit(1)
    analyze_log_file(sys.argv[1])
