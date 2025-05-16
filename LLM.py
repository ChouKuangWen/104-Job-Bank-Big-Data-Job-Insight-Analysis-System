import google.generativeai as genai

# 設定 API 金鑰
genai.configure(api_key="輸入Google Gemini API 金鑰")

# 建立模型
model = genai.GenerativeModel("gemini-2.0-flash")

# 建立對話並生成回答

def generate_skill_summary_with_llm(top_skills):
    skill_list_text = "\n".join([f"{skill}: {count} 次" for skill, count in top_skills])
    prompt = f"""
以下是某段時間內從職缺中統計的技能需求次數，請以專業且可讀性高的方式進行自然語言摘要：
{skill_list_text}

請幫我分析：有哪些技能最受歡迎？是否呈現某些趨勢？這些技能是否與資料分析、資料工程、AI 發展有關？請以專業報告語氣回答。
"""
    response = model.generate_content(prompt)
    return response.text


