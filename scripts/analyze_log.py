from openai import OpenAI
import os
import sys
import re

# Known error patterns
KNOWN_ERRORS = {
    r"ModuleNotFoundError: No module named '(\w+)'": "Missing Python module: {}",
    r"ImportError: cannot import name '(\w+)'": "Import error: {}",
    r"SyntaxError: (.+)": "Syntax error: {}",
    r"Exception: (.+)": "General exception: {}"
}

def analyze_log(log_file, output_file=None):
    """Analyze Jenkins build log, detect known issues, and call OpenAI."""
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Analyze this Jenkins build log. Identify the root cause of failure,
    summarize clearly, and suggest specific fixes:

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

    # Detect known issues
    alerts = []
    for pattern, message in KNOWN_ERRORS.items():
        match = re.search(pattern, log_content)
        if match:
            alerts.append(message.format(*match.groups()))

    # Colored console output
    print("\033[93m\n=== 🤖 AI Build Log Analysis ===\033[0m\n")
    if alerts:
        print("\033[91m⚠️ Known Issues Detected:\033[0m")
        for alert in alerts:
            print(f"\033[91m- {alert}\033[0m")
        print("\033[91m------------------------------\033[0m")
    print(f"\033[94m{analysis}\033[0m")
    print("\033[93m\n===============================\033[0m\n")

    # Save to file
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            if alerts:
                f.write("Known Issues:\n")
                for alert in alerts:
                    f.write(f"- {alert}\n")
                f.write("\n")
            f.write(analysis)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_log.py <log_file> [output_file]")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    analyze_log(log_file, output_file)
