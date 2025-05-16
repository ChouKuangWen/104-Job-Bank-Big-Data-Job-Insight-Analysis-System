import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import visual
from collections import Counter
from itertools import combinations
from collections import defaultdict
import LLM
# 讀取 Excel 檔案
df = pd.read_excel('104大數據職缺資料.xlsx')

# 顯示資料前幾列確認欄位
print(df.head())
print(df.describe())


"""職缺縣市分佈"""
# 用縣市欄位分組並計算數量
city_job_counts = df["縣市"].value_counts().reset_index()
city_job_counts.columns = ["縣市", "工作機會數"]
# 顯示結果
print(city_job_counts)
visual.city_vacancies(city_job_counts)  #製作縣市職缺圖


"""台北、新北之鄉鎮區市職缺分布"""
# 篩選出台北市和新北市的職缺
df_filtered = df[df["縣市"].isin(["台北市", "新北市"])]
# 根據縣市與鄉鎮市區進行統計
township_job_counts = df_filtered.groupby(["縣市", "鄉鎮市區"]).size().reset_index(name="職缺數量")
# 顯示結果
print(township_job_counts)
visual.township_vacancies(township_job_counts)


"""縣市平均薪資"""
# 統計各縣市平均薪資與標準差
salary_stats = df.groupby("縣市")["平均薪資"].agg(["mean", "std"]).reset_index()
# 改欄位名稱
salary_stats.columns = ["縣市", "平均薪資", "薪資標準差"]
# 依平均薪資排序（由高到低）
salary_stats = salary_stats.sort_values(by="平均薪資", ascending=False)
# 顯示結果
print(salary_stats)
#visual.city_salary_barchart(salary_stats)
#visual.city_salary_violinplot(df)


"""台北及新北各區平均薪資"""
# 只抓台北市與新北市
filtered_df = df[df["縣市"].isin(["台北市", "新北市"])]
# 統計各鄉鎮市區的平均薪資與標準差
township_salary_stats = filtered_df.groupby("鄉鎮市區")["平均薪資"].agg(["mean", "std"]).reset_index()
# 改欄位名稱
township_salary_stats.columns = ["鄉鎮市區", "平均薪資", "薪資標準差"]
# 依平均薪資排序（由高到低）
township_salary_stats = township_salary_stats.sort_values(by="平均薪資", ascending=False)
# 顯示結果
print(township_salary_stats)
visual.township_salary_barchart(df)
visual.township_salary_violinplot(df)

"""經歷要求"""
experience_levels = ["不拘", "1年以上", "2年以上", "3年以上",
                     "4年以上", "5年以上", "6年以上", "8年以上", "10年以上"]
experience = df["工作經歷"].value_counts().reindex(experience_levels, fill_value=0).reset_index()
experience.columns = ["工作經歷", "count"]
print(experience)

"""學歷要求(展開)"""
education = df["學歷"]
# 定義學歷層級與「以上」的展開對應
education_levels = ["不拘", "高中", "專科", "大學", "碩士", "博士"]
expand_mapping = {
    "高中以上": ["高中", "專科", "大學", "碩士", "博士"],
    "專科以上": ["專科", "大學", "碩士", "博士"],
    "大學以上": ["大學", "碩士", "博士"],
    "碩士以上": ["碩士", "博士"]
}

# 展開所有條件
expanded = []

for entry in education:
    if pd.isna(entry):
        continue
    if entry.strip() == "不拘":
        expanded.append("不拘")
    else:
        parts = entry.split("、")
        for p in parts:
            p = p.strip()
            if p in expand_mapping:
                expanded.extend(expand_mapping[p])
            else:
                expanded.append(p)

# 統計每個學歷出現次數
all_educations = pd.Series(expanded)
education_counts = (
    all_educations.value_counts()
    .reindex(education_levels, fill_value=0)
    .reset_index()
)
education_counts.columns = ["學歷", "count"]

# 顯示結果
print(education_counts)



"""學歷要求(不展開)"""
education_levels = ["不拘",
    "高中以上",
    "專科以上",
    "大學以上",
    "碩士以上",
    "高中、專科、大學",
    "專科、大學",
    "專科、大學、碩士",
    "大學、碩士",
    "高中",
    "專科",
    "大學",
    "碩士",
    "博士",
    ]

education = df["學歷"].value_counts().reindex(education_levels, fill_value=0).reset_index()
print(education)

"""技能及擅長工具"""


# 分割技能（根據常見分隔符）
def split_skills(text):
    for sep in [',', '/', '、', ';', '，', '|']:
        text = text.replace(sep, ',')
    return [skill.strip().lower() for skill in text.split(',') if skill.strip()]


# 合併兩欄位，去除缺失值
tool_series = df['擅長工具'].dropna().astype(str)
skill_series = df['技能'].dropna().astype(str)
combined_series = pd.concat([tool_series, skill_series], ignore_index=True)

# 對每列做拆分
all_skills = combined_series.apply(split_skills)


# 展平成一個列表
flat_skills = []
for sublist in all_skills:
    for skill in sublist:
        flat_skills.append(skill)



# 過濾掉無意義的技能詞

exclude_keywords = {"不拘", "無資料", "未填寫", "無", "皆可", "n/a", "none", "nan"}
filtered_skills = []

for s in flat_skills:
    if s not in exclude_keywords:
        filtered_skills.append(s)

# 統計技能出現次數
skill_counts = Counter(filtered_skills)
top_skills = skill_counts.most_common(20)
print(top_skills)
#顯示技能統計長條圖
visual.top_skills_bar(top_skills)
#LLM處理
#print(LLM.generate_skill_summary_with_llm(top_skills))


#技能關聯分析 (熱力圖)
co_occurrence = defaultdict(lambda: defaultdict(int))

for skills in all_skills:
    for skill1, skill2 in combinations(set(skills), 2):
        co_occurrence[skill1][skill2] += 1
        co_occurrence[skill2][skill1] += 1

# 建立共現矩陣，將集合轉換為列表
top_skill_set = list(set([s for s, _ in top_skills]))
matrix = pd.DataFrame(index=top_skill_set, columns=top_skill_set).fillna(0)

for s1 in top_skill_set:
    for s2 in top_skill_set:
        if s2 in co_occurrence[s1]:
            matrix.loc[s1, s2] = co_occurrence[s1][s2]

#繪製技能共現熱力圖
visual.plot_skill_heatmap(matrix)









