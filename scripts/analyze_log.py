from openai import OpenAI
import os
import sys

def analyze_log(log_file, output_file=None):
    """Reads a Jenkins build log, sends it to OpenAI, prints and saves the analysis."""
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Analyze this Jenkins build log. Identify the root cause of failure,
    summarize it clearly for developers, and suggest specific fixes:

    {log_content}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a CI/CD assistant that diagnoses build failures and suggests fixes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )

    analysis = response.choices[0].message.content.strip()

    # 🎨 Colored console output
    print("\033[93m\n=== 🤖 AI Build Log Analysis ===\033[0m\n")
    print(f"\033[91m{analysis}\033[0m")
    print("\033[93m\n===============================\033[0m\n")

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(analysis)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_log.py <log_file> [output_file]")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    analyze_log(log_file, output_file)
