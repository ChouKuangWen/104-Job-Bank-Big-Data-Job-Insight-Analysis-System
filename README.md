# 104人力銀行-大數據職缺洞察分析系統
---
## 簡介
104人力銀行大數據職缺相關分
本專案為針對 104 人力銀行「大數據」相關職缺的爬蟲與分析，透過自動化爬蟲技術蒐集職缺資訊，並以視覺化方式呈現熱門技能、需求趨勢與地區分佈等洞察，協助求職者或人資了解市場趨勢。
---

## 專案特色

- 自動化爬取 104 職缺資料（包含職務名稱、公司、工作內容、技能需求、地區等）
- 關鍵字比對篩選出與「大數據」相關職缺，關鍵字包含:
    數據、data、Data Analyst、資料分析師、Data Scientist、資料科學家、Data Engineer、
    資料工程師、Machine Learning Engineer、機器學習工程師、AI Engineer、人工智慧工程師、
    Big Data Engineer、大數據工程師、Intelligence、分析師、資料架構師

- 各縣市及雙北鄉鎮區市職缺及其平均薪資數據統計與視覺化
- 經歷、學歷、具備技能要求數據統計與視覺化
- 技能關聯性熱力圖
- 串接 Google Gemini API（gemini-2.0-flash 模型）以生成自然語言分析結果
- 整合所有分析數據產生PDF檔

---
## 安裝與使用方式

1. 環境安裝
git clone https://github.com/ChouKuangWen/104-Job-Bank-Big-Data-Job-Insight-Analysis-System/tree/main
cd 104-Job-Bank-Big-Data-Job-Insight-Analysis-System
pip install -r requirements.txt

2. 執行爬蟲
python crawler.py

3. 啟動資料分析
python main.py

---
## .env 設定
請在專案根目錄建立 `.env` 檔案，內容如下：
```bash
GEMINI_API_KEY=你的 Google Gemini API 金鑰


---
## 目錄結構

104-Job-Bank-Big-Data-Job-Insight-Analysis-System/
├── crawler.py             # 爬取 104 職缺資料
├── visual.py              # 資料視覺化
├── main.py                # 主程式
├── LLM.py                 # 以生成自然語言分析結果
├── report.py              # 將所有分析結果產生PDF檔
├── 104大數據職缺資料.xlsx  # 儲存爬下來的資料
├── output/                # 儲存視覺化後的資料圖片
├── 大數據職缺分析報告.pdf  # 輸出之分析結果
└── README.md

---
## 資料處理流程

資料清理與轉換包含：
- **年薪轉月薪**：年薪除以 12
- **日薪轉月薪**：日薪乘以 21
- **時薪轉月薪**：時薪乘以 8再乘以21

---
## 成果示範
以下是自動生成的 PDF 分析報告示例：
- [大數據職缺分析報告.pdf](./大數據職缺分析報告.pdf)
