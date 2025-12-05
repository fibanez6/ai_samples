#!/bin/bash
set -e

# Claude Code Review Script
# Usage: ./claude-review.sh <diff_file> <output_file>

DIFF_FILE="${1:-diff.txt}"
OUTPUT_FILE="${2:-review.md}"

if [ ! -f "$DIFF_FILE" ]; then
  echo "Error: Diff file not found: $DIFF_FILE"
  exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Error: ANTHROPIC_API_KEY environment variable is not set"
  exit 1
fi

echo "Reading diff from $DIFF_FILE..."
DIFF_CONTENT=$(cat "$DIFF_FILE")

# Escape the diff content for JSON
DIFF_JSON=$(jq -Rs . <<< "$DIFF_CONTENT")

# Create the review prompt
PROMPT="You are a senior code reviewer. Review the following code changes and provide:

1. **Summary of Changes**: Brief overview of what was modified
2. **Potential Issues**: Bugs, logic errors, or problematic code patterns
3. **Security Concerns**: Any security vulnerabilities or risks
4. **Performance**: Suggestions for optimization
5. **Best Practices**: Code quality and maintainability improvements

For specific issues, use this format:
\`📁 filename.ext:line_number - Issue description\`

Code changes:
\`\`\`diff
$DIFF_CONTENT
\`\`\`

Provide your review in clear, actionable markdown format."

# Prepare API request payload
REQUEST_PAYLOAD=$(jq -n \
  --arg model "claude-sonnet-4-20250514" \
  --argjson max_tokens 4096 \
  --arg prompt "$PROMPT" \
  '{
    model: $model,
    max_tokens: $max_tokens,
    messages: [{
      role: "user",
      content: $prompt
    }]
  }')

echo "Calling Claude API..."

# Call Claude API
RESPONSE=$(curl -s -w "\n%{http_code}" \
  https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d "$REQUEST_PAYLOAD")

# Extract HTTP status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "Error: API request failed with status code $HTTP_CODE"
  echo "Response: $RESPONSE_BODY"
  exit 1
fi

# Extract review text from response
REVIEW=$(echo "$RESPONSE_BODY" | jq -r '.content[0].text // "Error: Unable to extract review text"')

if [ "$REVIEW" = "null" ] || [ -z "$REVIEW" ]; then
  echo "Error: Failed to extract review from API response"
  echo "Response: $RESPONSE_BODY"
  exit 1
fi

# Save review to output file
echo "$REVIEW" > "$OUTPUT_FILE"
echo "Review saved to $OUTPUT_FILE"

# Also output to stdout for GitHub Actions
echo "REVIEW_CONTENT<<EOFMARKER"
echo "$REVIEW"
echo "EOFMARKER"