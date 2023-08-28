import requests
from bs4 import BeautifulSoup

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1144028487036981310/JCEHbKYUXLKXqg1Rh6ookQ6YG3iXpFaecc3TZJn_jgB1kRNaBvGhFFqkXfahQXD8Ccdm"

# URL of the webpage you want to monitor
url = "https://lifewatermedia.com/disclaimer/"

try:
    # Fetch current content
    response = requests.get(url)
    current_content = response.text

    # Create BeautifulSoup object
    soup = BeautifulSoup(current_content, "html.parser")

    # Find all elements containing text on the page
    all_text_elements = soup.find_all(string=True)

    # Extract new text elements
    new_text_elements = []
    # ... Your code to extract new text elements ...

    # Check if there are new text elements to send
    if new_text_elements:
        # Construct message
        new_text_message = "\n".join(new_text_elements)

        # Send message to Discord webhook
        data = {"content": new_text_message}
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("New text update sent to Discord.")
        else:
            print("Failed to send new text update to Discord. Status code:", response.status_code)
    else:
        print("No new text to send.")

except Exception as e:
    print("An error occurred:", e)