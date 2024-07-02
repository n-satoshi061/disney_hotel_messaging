import requests
import os

def send_line_notify(message):
    line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {line_notify_token}"
    }
    data = {
        "message": message
    }
    
    response = requests.post(line_notify_api, headers=headers, data=data)
    print(response.status_code)
    print(response.text)

# Test the function
send_line_notify("これはテストメッセージです。")
