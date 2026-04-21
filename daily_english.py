import google.generativeai as genai
import datetime
import os

# 設定你的 API KEY
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_interview_sentence():
    prompt = """
    請為我生成一條適合「外商公司軟體工程師/架構師面試」使用的英文句子。
    輸出格式要求：
    1. 【每日金句】：英文句子 (含中文翻譯)
    2. 【關鍵單字】：2-3 個核心單字，含音標、詞性、解釋與例句。
    3. 【面試情境】：說明這句話適合在面試的什麼階段（如：專案介紹、處理衝突、談薪資）以及為何這樣說比較專業。
    4. 請使用繁體中文說明。
    """
    
    response = model.generate_content(prompt)
    return response.text

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
