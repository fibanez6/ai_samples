import os
import subprocess
import sys
from typing import List

from openai import OpenAI


def get_changed_files() -> List[str]:
    """Get list of changed files between HEAD and HEAD~1."""
    try:
        # Check if it's a shallow clone, if so we might fail to find HEAD~1
        # In GitHub Actions, usually fetch-depth: 0 or 2 is needed.
        cmd = ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
        return [f for f in files if f.endswith(".py") and os.path.exists(f)]
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def review_and_improve_file(client: OpenAI, file_path: str):
    """Read file, send to Claude, write back improvements."""
    print(f"Reviewing {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""You are an expert Python developer and code reviewer.
    Current file: {file_path}
    
    Review the following Python code. Your goal is to improve it by:
    1. Fixing any potential bugs.
    2. Improving readability and variable naming.
    3. Adding type hints if missing.
    4. Adding docstrings (Google style).
    5. Ensuring it follows PEP 8.
    
    IMPORTANT: You must output ONLY the full, valid Python code. 
    Do not output markdown code blocks (```python ... ```). 
    Do not output any explanation text before or after the code.
    Just the raw code.
    
    Code to review:
    {content}
    """

    try:
        response = client.chat.completions.create(
            model="Claude-3.5-Sonnet",
            messages=[
                {
                    "role": "system",
                    "content": "You are a code optimization engine. You output only raw python code.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=4096,  # Adjust if needed, GitHub Models might have different limits
        )

        improved_code = response.choices[0].message.content.strip()

        # Simple safeguard: check if it looks like python
        if improved_code.startswith("```python"):
            improved_code = improved_code.split("\n", 1)[1]
        if improved_code.endswith("```"):
            improved_code = improved_code.rsplit("\n", 1)[0]

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(improved_code)

        print(f"Successfully updated {file_path}")

    except Exception as e:
        print(f"Failed to review {file_path}: {e}")


def main():
    api_key = os.environ.get("GITHUB_TOKEN")
    if not api_key:
        print("GITHUB_TOKEN not found in environment variables.")
        sys.exit(1)

    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=api_key,
    )

    changed_files = get_changed_files()
    if not changed_files:
        print("No Python files changed.")
        return

    print(f"Found {len(changed_files)} changed Python files: {changed_files}")

    for file_path in changed_files:
        review_and_improve_file(client, file_path)


if __name__ == "__main__":
    main()
