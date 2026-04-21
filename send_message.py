import requests
import os
import sys

def send_message():
    # 從系統環境變數讀取 Token 與 ID
    token = os.getenv('LINE_ACCESS_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    if not token or not user_id:
        print("錯誤：找不到環境變數 LINE_ACCESS_TOKEN 或 LINE_USER_ID")
        sys.exit(1)

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': 'Daily motion from GitHub Actions！'
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("訊息發送成功！")
    else:
        print(f"發送失敗，錯誤碼：{response.status_code}")
        print(response.text)

if __name__ == "__main__":
    send_message()