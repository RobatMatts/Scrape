import requests
import re
import os

# URLs
source_url = "https://biotechresearchreport.com/disclaimer/"
webhook_url = "https://discord.com/api/webhooks/1144028487036981310/JCEHbKYUXLKXqg1Rh6ookQ6YG3iXpFaecc3TZJn_jgB1kRNaBvGhFFqkXfahQXD8Ccdm"

# Extract paragraphs starting with "Pursuant"
paragraphs = re.findall(r'Pursuant.*?(?=<)', new_content, re.DOTALL)

# Load existing tickers from ticker.txt
try:
    with open("ticker.txt", "r") as f:
        existing_tickers = set(line.strip() for line in f.readlines())
except FileNotFoundError:
    existing_tickers = set()

# Initialize a flag to track if any new tickers were found
new_ticker_found = False

# Check each paragraph for tickers
for paragraph in paragraphs:
    match = re.search(r'\b[A-Z]{4,5}\b', paragraph)
    if match:
        ticker = match.group()
        if ticker not in existing_tickers:
            new_ticker_found = True
            data = {"content": "@everyone\nNew ticker: {}\n{}".format(ticker, paragraph)}
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print("New text update sent to Discord for ticker:", ticker)
            else:
                print("Failed to send new text update to Discord for ticker:", ticker)
            existing_tickers.add(ticker)

            # Update ticker.txt with new tickers
            with open("ticker.txt", "a") as f:
                f.write(ticker + "\n")

# Commit and push changes to the repository
os.system("git config --global user.name 'GitHub Actions'")
os.system("git config --global user.email 'actions@github.com'")
os.system("git add ticker.txt")
os.system("git commit -m 'Update ticker.txt'")
os.system("git push")

# Print status message
if new_ticker_found:
    print("New ticker(s) detected and sent to Discord.")
else:
    print("No new tickers to send.")