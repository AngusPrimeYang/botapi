# 📘 外商面試每日英文 LINE Bot

每天自動推送一則外商軟體工程師面試英文教學到你的 LINE，內容包含金句、關鍵單字、面試情境說明與選擇練習題。

## 功能特色

- **每日金句**：生成適合外商面試場景的英文句子與中文翻譯
- **關鍵單字**：核心單字附音標、詞性、解釋與例句
- **面試情境**：說明句子適用的面試階段（專案介紹、處理衝突、談薪資等）
- **選擇練習題**：每日一題英文情境選擇題，附正確答案即時對獎
- **自動排程**：透過 GitHub Actions 每日 UTC 22:22（約台灣時間早上 06:22）自動發送

## 技術架構

| 元件 | 說明 |
|------|------|
| `daily_english.py` | 核心邏輯：組合 prompt、解析 AI 回應、格式化 LINE 訊息 |
| `prompt_client.py` | Gemini API 封裝，使用 `gemini-2.5-flash` 模型，含 503 自動重試 |
| `send_message.py` | LINE Messaging API 推播，串接內容生成與訊息發送 |
| `.github/workflows/main.yml` | GitHub Actions 排程，每日自動觸發 |

## 環境需求

- Python 3.14+
- [Google Gemini API Key](https://aistudio.google.com/apikey)
- [LINE Messaging API](https://developers.line.biz/console/) Channel Access Token 與 User ID

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export LINE_ACCESS_TOKEN="your-line-channel-access-token"
export LINE_USER_ID="your-line-user-id"
```

### 3. 本地執行

單純預覽生成內容（不發送 LINE）：

```bash
python daily_english.py
```

生成內容並發送到 LINE：

```bash
python send_message.py
```

## GitHub Actions 自動排程

專案已設定 GitHub Actions workflow，每日 UTC 22:22 自動執行。

### 設定 Repository Secrets

在 GitHub repo 的 **Settings → Secrets and variables → Actions** 中新增：

| Secret 名稱 | 說明 |
|-------------|------|
| `GEMINI_API_KEY` | Google Gemini API 金鑰 |
| `LINE_ACCESS_TOKEN` | LINE Channel Access Token |
| `LINE_USER_ID` | 接收訊息的 LINE User ID |

也可透過 **Actions → Line Auto Bot → Run workflow** 手動觸發。

## 專案結構

```
.
├── .github/workflows/main.yml   # GitHub Actions 排程設定
├── daily_english.py             # 每日英文內容生成與格式化
├── prompt_client.py             # Gemini API 客戶端
├── send_message.py              # LINE 訊息推播
├── requirements.txt             # Python 依賴套件
├── pyproject.toml               # 專案設定
```

## License

此專案為個人學習用途。
