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
        model='claude-opus-4-5',
        max_tokens=1024,
        tools=[{'type': 'web_search_20250305', 'name': 'web_search'}],
        messages=[{'role': 'user', 'content': prompt}]
    )
    for block in message.content:
        if block.type == 'text':
            return block.text
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
    prompt = (
        'Please search the web and find the top five stories '
        'this morning on federal funding cuts or freezes. '
        'For each story, give me the headline, a two or three '
        'sentence summary, and the source.'
    )
    print('Asking Claude...')
    result = ask_claude(prompt)
    print('Sending email...')
    send_email(
        subject='Daily Briefing: Federal Funding Cuts',
        body=result
    )


main()
