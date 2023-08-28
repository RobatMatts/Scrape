import requests
import re
import os

# URLs
source_url = "https://biotechresearchreport.com/disclaimer/"
webhook_url = "https://discord.com/api/webhooks/1144028487036981310/JCEHbKYUXLKXqg1Rh6ookQ6YG3iXpFaecc3TZJn_jgB1kRNaBvGhFFqkXfahQXD8Ccdm"

# Fetch current content
response = requests.get(source_url)
new_content = response.text

# Extract paragraphs starting with "Pursuant"
paragraphs = re.findall(r'Pursuant.*?(?=<)', new_content, re.DOTALL)

# Combine the paragraphs into a single string
new_text_message = '\n'.join(paragraphs)

# Load previous content
previous_paragraphs = ""
if os.path.exists("previous_content.txt"):
    with open("previous_content.txt", "r") as f:
        previous_paragraphs = f.read()

# Find the new content by comparing with previous content
new_paragraphs = new_text_message.strip().replace(previous_paragraphs.strip(), '').strip()
if new_paragraphs:
    # Send message to Discord webhook
    data = {"content": "@everyone\n" + new_paragraphs}
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("New text update sent to Discord.")
    else:
        error_message = "@everyone new promo but I am broken beep boop please check manually"
        print("Failed to send new text update to Discord. Status code:", response.status_code)
        data = {"content": error_message}
        requests.post(webhook_url, json=data)  # Send the error message to Discord

    # Update the previous_content.txt file with new paragraphs
    with open("previous_content.txt", "w") as f:
        f.write(new_text_message)

    # Save the new content to debug.txt for troubleshooting
    with open("debug.txt", "w", encoding="utf-8") as debug_file:
        debug_file.write(new_paragraphs)

    # Commit and push changes to the repository
    os.system("git config --global user.name 'GitHub Actions'")
    os.system("git config --global user.email 'actions@github.com'")
    os.system("git add previous_content.txt debug.txt")
    os.system("git commit -m 'Update previous_content.txt and debug.txt'")
    os.system("git push")
else:
    print("No new text to send.")
