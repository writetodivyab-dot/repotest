from openai import OpenAI
import os
import sys

def analyze_log(log_file, output_file="build_logs/ai_analysis.txt"):
    """Reads a Jenkins build log, sends it to the OpenAI API, and saves a human-readable analysis."""
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

    analysis = response.choices[0].message.content.strip()

    print("\n=== 🤖 AI Build Log Analysis ===\n")
    print(analysis)
    print("\n===============================\n")

    # Save analysis to file for Jenkins artifact
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(analysis)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_log.py <log_file>")
        sys.exit(1)
    analyze_log(sys.argv[1])
