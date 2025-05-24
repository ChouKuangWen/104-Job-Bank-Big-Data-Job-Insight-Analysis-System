import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# 設定 API 金鑰
genai.configure(api_key=api_key)

# 建立模型
model = genai.GenerativeModel("gemini-2.0-flash")

#報表總覽說明
def generate_overview_summary(total_jobs):
    prompt = f"""
截至 2025-04-26，共有 {total_jobs} 筆職缺資料。
請用專業口吻進行開場摘要，說明分析目的與背景。
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text

#縣市職缺分佈摘要
def generate_city_distribution_summary_with_llm(city_job_counts):
    city_list_text = "\n".join([f"{city}: {count} 筆職缺" for city, count in city_job_counts.iterrows()])
    prompt = f"""
以下是某段時間內職缺的縣市分佈統計，請進行專業摘要：
{city_list_text}

請說明：哪些縣市職缺數量最多？是否有城鄉差距？對求職者與企業的意義為何？
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text


#鄉鎮職缺分佈摘要
def generate_town_distribution_summary_with_llm(township_job_counts):
    town_list_text = "\n".join([f"{town}: {count} 筆職缺" for town, count in township_job_counts.iterrows()])
    prompt = f"""
以下是各鄉鎮市區的職缺數量統計：
{town_list_text}

請以專業語氣說明：職缺是否集中在特定地區？對地區經濟與勞動市場有何影響？
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text

#縣市平均薪資摘要
def generate_city_salary_summary_with_llm(salary_stats):
    city_salary_text = "\n".join([f"{row['縣市']}: {row['平均薪資']:.0f} 元" for _, row in salary_stats.iterrows() ])
    prompt = f"""
以下是各縣市的平均薪資：
{city_salary_text}

請分析：哪些地區薪資較高？是否與產業聚落或生活成本有關？
"""   
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text


#鄉鎮平均薪資摘要
def generate_town_salary_summary_with_llm(township_salary_stats):
    town_salary_text = "\n".join([f"{row['鄉鎮市區']}: {row['平均薪資']:.0f} 元" for _, row in township_salary_stats.iterrows()])
    prompt = f"""
以下是各鄉鎮的平均薪資：
{town_salary_text}

請指出薪資落差明顯的區域，並討論可能原因與勞動市場影響。
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text



#經歷要求摘要
def generate_experience_summary_with_llm(experience):
    # experience_df 預期有兩欄：工作經歷, count
    experience_list_text = "\n".join([f"{row['工作經歷']}: {row['count']} 筆職缺" for _, row in experience.iterrows()])
    prompt = f"""
以下是某段時間內職缺的工作經歷要求統計，請以專業且可讀性高的方式進行自然語言摘要：
{experience_list_text}

請分析：
1. 不同經歷年限的職缺數量分布如何？
2. 無經驗或新鮮人（不拘、0年經驗）是否有足夠就業機會？
3. 是否有明顯偏好特定經歷年限？
請以專業報告語氣回答。
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text



#學歷要求摘要
def generate_education_summary_with_llm(education):
    # education_df 預期有兩欄：學歷, count
    education_list_text = "\n".join([f"{row['學歷']}: {row['count']} 筆職缺" for _, row in education.iterrows()])
    prompt = f"""
以下是某段時間內職缺的學歷要求統計，請以專業且可讀性高的方式進行自然語言摘要：
{education_list_text}

請分析：
1. 各學歷層級的職缺數量分布。
2. 是否偏好特定科系背景（若資料可得，請說明）。
3. 學歷要求對求職者的影響及就業機會。
請以專業報告語氣回答。
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text


#熱門技能摘要
def generate_skill_summary_with_llm(top_skills):
    skill_list_text = "\n".join([f"{skill}: {count} 次" for skill, count in top_skills])

    prompt = f"""
以下是某段時間內從職缺中統計的技能需求次數：
{skill_list_text}

此外，已產生一張技能熱力圖，圖中以顏色深淺表達技能出現的頻率，顏色越深代表該技能越熱門。

請根據上方的數據與熱力圖資訊進行分析，回答以下問題：
1. 哪些技能最受歡迎？
2. 是否有技能類別集中特別高（如資料分析、工程開發、AI 等）？
3. 技能分佈是否顯示產業趨勢？
4. 這些技能是否與資料分析、資料工程、AI 發展有關？

請以專業報告語氣回答，條理清晰且具可讀性。
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text

#熱力圖
def generate_skillmatrix_summary_with_llm(matrix):
    """
    使用 Gemini LLM 生成技能共現摘要。
    """
    matrix = matrix.astype(float)

    # 共現次數最高
    max_val = matrix.values.max()
    if max_val == 0:
        return "目前技能之間沒有共現資料。"

    # 找出共現次數最高的技能對
    top_pairs = []
    for s1 in matrix.index:
        for s2 in matrix.columns:
            if s1 != s2 and matrix.loc[s1, s2] == max_val:
                top_pairs.append((s1, s2))

    # 前五個總共現次數最多的技能
    skill_scores = matrix.sum(axis=1).sort_values(ascending=False)
    top_skills = skill_scores.head(5).to_dict()

    # 將資料組成 prompt 給 Gemini
    prompt = f"請根據以下技能共現資料，撰寫一段摘要分析：\n\n"
    prompt += f"共現次數最高為 {int(max_val)}，出現於技能組合：\n"
    for s1, s2 in top_pairs:
        prompt += f"- {s1} 與 {s2}\n"

    prompt += "\n最常與其他技能共現的前五大技能為：\n"
    for skill, score in top_skills.items():
        prompt += f"- {skill}（共現總次數：{int(score)}）\n"

    prompt += "\n請說明這些結果代表的意義，以及可能的應用建議。"
    prompt += "\n請用繁體中文撰寫摘要分析。"
    
    # 呼叫 Gemini API
    response = model.generate_content(prompt)

    return response.text



#結論與建議
def generate_conclusion_summary():
    prompt = """
根據職缺數量、分佈、薪資與技能統計，請提供一份綜合性的總結與建議。
需包含：求職者應如何應對？企業在招募策略上可如何調整？
"""
    prompt += "\n請用繁體中文撰寫摘要分析。"
    response = model.generate_content(prompt)
    return response.text

