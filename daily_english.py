import datetime
import os
import json
import re

from prompt_client import generate
from word_bank import DailyTarget, pick_daily_target

STATE_FILE = "learning_state.json"
USER_ANSWER_FILE = "my_answer.txt" # 使用者在此檔案輸入 A, B, C 或 D


def _contains_target_words(text: str, target: DailyTarget) -> bool:
    lowered = text.lower()
    for pick in target.picks:
        word_hit = re.search(rf"\b{re.escape(pick.word.lower())}\b", lowered)
        collo_hit = pick.collocation.lower() in lowered
        if not (word_hit or collo_hit):
            return False
    return True


def _generate_for_target(prompt: str, target: DailyTarget) -> str:
    result = generate(prompt)
    if _contains_target_words(result, target):
        return result
    return generate(prompt)


def get_interview_sentence():
    target = pick_daily_target()
    prompt = f"""
    請為我生成一條適合「外商公司軟體工程師/架構師面試」使用的英文句子。
    {target.prompt_block()}
    輸出格式要求：
    1. 【每日金句】：英文句子 (含中文翻譯)
    2. 【關鍵單字】：上述指定單字，含音標、詞性、指定搭配的解釋與例句。
    3. 【面試情境】：對應今天指定的面試階段，說明為何這樣說比較專業。
    4. 請使用繁體中文說明。
    """
    return _generate_for_target(prompt, target)

def get_new_lesson():
    target = pick_daily_target()
    prompt = f"""
    請生成一則外商面試英文教學。
    {target.prompt_block()}
    包含：
    1. 【每日金句】與翻譯。
    2. 【關鍵單字】：上述指定單字與指定搭配的解釋。
    3. 【選擇練習題】：針對該金句或指定搭配設計一個英文問答情境選擇題（A, B, C, D）。
    4. 【系統標記】：請在最後一行輸出 'ANSWER: [正確選項字母]'（例如 ANSWER: A）。
    請用繁體中文。
    """
    result = _generate_for_target(prompt, target)
    
    # 解析答案
    lines = result.strip().split('\n')
    correct_option = "A" # 預設
    for line in lines:
        if "ANSWER:" in line:
            correct_option = line.split(":")[-1].strip()
            result = result.replace(line, "") # 隱藏答案不顯示在今天的輸出中
    
    save_state(correct_option)
    return result, correct_option

def save_state(correct_option):
    new_state = {
        "date": str(datetime.date.today()),
        "correct_option": correct_option
    }
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_state, f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def check_yesterday_answer(state):
    if not state:
        return "👋 歡迎開始第一天的練習！"
    
    yesterday_date = state.get("date")
    correct_answer = state.get("correct_option")
    
    # 檢查使用者是否有作答
    user_ans = ""
    if os.path.exists(USER_ANSWER_FILE):
        with open(USER_ANSWER_FILE, 'r') as f:
            user_ans = f.read().strip().upper()
    
    feedback = f"\n--- 📅 昨天的回顧 ({yesterday_date}) ---\n"
    if not user_ans:
        feedback += f"昨天你沒有作答喔。正確答案是：【{correct_answer}】\n"
    elif user_ans == correct_answer:
        feedback += f"🎉 太棒了！你的答案 [{user_ans}] 是正確的！\n"
    else:
        feedback += f"❌ 可惜了，你選了 [{user_ans}]，但正確答案應該是 【{correct_answer}】。\n"
    
    # 清空答案檔供今天使用
    with open(USER_ANSWER_FILE, 'w') as f: f.write("")
    return feedback

def format_for_line(content):
    lines = content.strip().split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            line = line.replace('#', '').strip()
            line = f"✦ {line} ✦"
        if line.startswith('**') and line.endswith('**'):
            line = line.strip('*').strip()
            line = f"▸ {line}"
        formatted_lines.append(line)
    today = datetime.date.today().strftime("%Y-%m-%d")
    header = f"📘 外商面試每日一句 - {today}\n{'━' * 20}\n"
    message = header + '\n'.join(formatted_lines)
    return message

if __name__ == "__main__":
    content = get_interview_sentence()
    message = format_for_line(content)
    print(message)
