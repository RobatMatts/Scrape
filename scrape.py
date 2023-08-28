import requests
import re

# URLs
source_url = "https://biotechresearchreport.com/disclaimer/"
webhook_url = "https://discord.com/api/webhooks/1144016412185202738/f7txAsKyss6Gcqkjf4GpPx6-8TajNALmUM0IZ3Wk8pvqiVFGBR0V0ENdhK_7DIeupuOh"

# Fetch current content
response = requests.get(source_url)
new_content = response.text

# Extract paragraphs starting with "Pursuant"
paragraphs = re.findall(r'Pursuant.*?(?=<)', new_content, re.DOTALL)

# Combine the paragraphs into a single string
new_text_message = '\n'.join(paragraphs)

# Load previous content
try:
    with open("previous_content.txt", "r") as f:
        previous_paragraphs = f.read()
except FileNotFoundError:
    previous_paragraphs = ""

# Find the new content by comparing with previous content
new_paragraphs = new_text_message.strip().replace(previous_paragraphs.strip(), '').strip()
if new_paragraphs:
    # Send message to Discord webhook
    data = {"content": "@everyone\n" + new_paragraphs}
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("New text update sent to Discord.")
    else:
        print("Failed to send new text update to Discord. Status code:", response.status_code)

    # Update the previous_content.txt file with new paragraphs
    with open("previous_content.txt", "w") as f:
        f.write(new_text_message)

    # Save the new content to debug.txt for troubleshooting
    with open("debug.txt", "w", encoding="utf-8") as debug_file:
        debug_file.write(new_paragraphs)
else:
    print("No new text to send.")






