import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']
GMAIL_ADDRESS = os.environ['GMAIL_ADDRESS']
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
RECIPIENT_EMAIL = os.environ['GMAIL_ADDRESS']


def ask_claude(prompt):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model='claude-haiku-4-5',
        max_tokens=8192,
        tools=[{'type': 'web_search_20250305', 'name': 'web_search'}],
        messages=[{'role': 'user', 'content': prompt}]
    )

    # Diagnostic logging so we can see what came back in the Actions log
    print(f'Stop reason: {message.stop_reason}')
    print(f'Number of content blocks: {len(message.content)}')
    for i, block in enumerate(message.content):
        print(f'Block {i}: type={block.type}')
        if block.type == 'text':
            print(f'  Text length: {len(block.text)} chars')
            print(f'  First 200 chars: {block.text[:200]}')

    # Join all text blocks
    text_blocks = []
    for block in message.content:
        if block.type == 'text' and block.text.strip():
            text_blocks.append(block.text.strip())

    print(f'Total text blocks collected: {len(text_blocks)}')

    if text_blocks:
        result = '\n\n'.join(text_blocks)
        print(f'Total result length: {len(result)} chars')
        return result
    return 'No response received from Claude.'


def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
    print('Email sent successfully.')


def main():
    prompt = 'Please give me a detailed daily briefing on developments in ancient history and archaeology. Cover two stories. For each story provide: a clear headline, the background context needed to understand the issue, what specifically happened or was announced, and any notable reactions or next steps. Each story should be substantial -- aim for three to five full paragraphs. Use clear headers to separate each story.'
    print('Asking Claude...')
    result = ask_claude(prompt)
    print('Sending email...')
    send_email(
        subject='Daily Briefing: History!',
        body=result
    )


main()
