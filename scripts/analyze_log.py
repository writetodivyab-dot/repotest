from openai import OpenAI
import os
import sys

def analyze_log(log_file):
    """Reads a Jenkins build log, sends it to the OpenAI API, and prints a human-readable analysis."""
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Analyze the following Jenkins build log. Identify the root cause of the failure, 
    summarize it in plain English, and suggest 1–2 possible fixes:

    {log_content}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a CI/CD assistant that helps diagnose build failures."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )

    print("\n=== 🤖 AI Build Log Analysis ===\n")
    print(response.choices[0].message.content)
    print("\n===============================\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_log.py <log_file>")
        sys.exit(1)

    analyze_log(sys.argv[1])
