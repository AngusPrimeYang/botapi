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

    # 從 daily_english.py 模組引入 format_for_line 函式
    # from daily_english import get_interview_sentence, format_for_line
    # content = get_interview_sentence()
    # message = format_for_line(content)

    from daily_english import load_state, check_yesterday_answer, get_new_lesson
    # 1. 載入舊狀態並回饋
    old_state = load_state()
    yesterday_feedback = check_yesterday_answer(old_state)
    # 2. 生成新內容
    new_content, correct_option = get_new_lesson()
    # 2. 生成訊息
    message = '\n'.join(yesterday_feedback, "--- 📖 今天的學習內容 ---", new_content, "👉 請寫下你的答案 (A/B/C/D)，明天我會為你對獎！")

    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message # 'Daily motion from GitHub Actions！'
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