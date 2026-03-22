import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# —————————————————————

# CONFIGURATION

# These values are pulled from GitHub Secrets automatically

# when the script runs. Never put real values here directly.

# —————————————————————

ANTHROPIC_API_KEY = os.environ[“ANTHROPIC_API_KEY”]
GMAIL_ADDRESS = os.environ[“GMAIL_ADDRESS”]
GMAIL_APP_PASSWORD = os.environ[“GMAIL_APP_PASSWORD”]

# The email address you want to send the briefing TO.

# For now this is you, so it’s the same as your Gmail address.

RECIPIENT_EMAIL = os.environ[“GMAIL_ADDRESS”]

# —————————————————————

# STEP 1: ASK CLAUDE

# This function sends your prompt to the Claude API

# and returns Claude’s response as a string.

# —————————————————————

def ask_claude(prompt):
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

```
message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Claude's response comes back as a list of content blocks.
# We find the text block and return it.
for block in message.content:
    if block.type == "text":
        return block.text

return "No response received from Claude."
```

# —————————————————————

# STEP 2: SEND THE EMAIL

# This function takes a subject line and body text,

# and sends it from your Gmail to your Gmail.

# —————————————————————

def send_email(subject, body):
# Build the email structure
msg = MIMEMultipart()
msg[“From”] = GMAIL_ADDRESS
msg[“To”] = RECIPIENT_EMAIL
msg[“Subject”] = subject

```
# Attach the body as plain text
msg.attach(MIMEText(body, "plain"))

# Connect to Gmail's outgoing mail server and send
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

print("Email sent successfully.")
```

# —————————————————————

# STEP 3: RUN EVERYTHING

# This is the main function that ties it all together.

# —————————————————————

def main():
prompt = (
“Please search the web and find the top five stories “
“this morning on federal funding cuts or freezes. “
“For each story, give me the headline, a two or three “
“sentence summary, and the source.”
)

```
print("Asking Claude...")
result = ask_claude(prompt)

print("Sending email...")
send_email(
    subject="Daily Briefing: Federal Funding Cuts",
    body=result
)
```

# This line means “run main() when this script is executed directly”

if **name** == “**main**”:
main()
