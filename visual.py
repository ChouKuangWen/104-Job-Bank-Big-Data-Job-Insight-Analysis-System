import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# 設定字型，這裡使用 'SimHei'（黑體字型），如果沒有安裝可以換成其他支援中文的字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 這是設定中文顯示字型
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

"""各縣市職缺製圖函式"""
def city_vacancies(city_job_counts):
    # 生成不同顏色
    colors =  [
        '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
        '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC', '#86BCB6'
    ]

    # 畫圖
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(city_job_counts['縣市'], city_job_counts['工作機會數'], color=colors, width=0.9)

    # x 軸設定
    ax.set_xticklabels(city_job_counts['縣市'], rotation=0, ha='center',fontsize=12)
    ax.set_xticks(np.arange(len(city_job_counts)))

    # y 軸標籤改成直式（你可以選一種）
    # 方法一：換行方式
    ax.set_ylabel('工\n作\n機\n會\n數', rotation=0, labelpad=20, fontsize=14)
    ax.yaxis.label.set_position((-0.2, 0.4))  # 這裡把 Y 標籤往下移

    # **加這一行：總工作數量**
    total_jobs = city_job_counts['工作機會數'].sum()

    # 每個 bar 上方加 數量 + 百分比
    for bar in bars:
        height = bar.get_height()
        percent = height / total_jobs * 100
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                f'{int(height)} ({percent:.1f}%)', ha='center', va='bottom', fontsize=10)

    # 標題與排版
    ax.set_xlabel('縣市',fontsize=14)
    ax.set_title('各縣市工作機會數',fontsize=24)
    # 加上 y 軸網底（水平線）
    ax.grid(axis='both', linestyle='--', linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.show()


"""台北、新北之鄉鎮區市職缺分布製圖函式"""
def township_vacancies(township_job_counts):
    """
    畫出台北市與新北市各鄉鎮市區的工作機會數長條圖。

    參數：
    - job_counts: pandas DataFrame，包含「縣市」、「鄉鎮市區」、「職缺數量」三欄。
    """
    # 合併縣市與鄉鎮市區欄位為標籤
    township_job_counts = township_job_counts.copy()
    township_job_counts["區域"] = township_job_counts["縣市"] + " " + township_job_counts["鄉鎮市區"]

    # 排序（依照職缺數量由大到小）
    township_job_counts = township_job_counts.sort_values("職缺數量", ascending=False)

    # 顏色列表（可自行擴充）
    colors = [
        '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
        '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC',
        '#86BCB6', '#A4CEE3', '#8FBC94', '#C94C4C', '#FFB347'
    ] * ((len(township_job_counts) // 15) + 1)  # 若資料比色多，重複色系

    # 畫圖
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(township_job_counts["區域"], township_job_counts["職缺數量"], color=colors[:len(township_job_counts)], width=0.8)

    # X 軸設定
    ax.set_xticks(np.arange(len(township_job_counts)))
    ax.set_xticklabels(township_job_counts["區域"], rotation=45, ha='right', fontsize=10)

    # Y 軸設定
    ax.set_ylabel('工\n作\n機\n會\n數', rotation=0, labelpad=25, fontsize=14)
    ax.yaxis.label.set_position((-0.06, 0.4))

    # 加上 bar 數值標籤與百分比
    total = township_job_counts["職缺數量"].sum()
    for bar in bars:
        height = bar.get_height()
        percent = height / total * 100
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                f'{int(height)} ({percent:.1f}%)', ha='center', va='bottom', fontsize=9)

    # 標題與美化
    ax.set_title("台北市與新北市各鄉鎮市區職缺分布", fontsize=20)
    ax.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.show()


#長條圖：縣市平均薪資比較
def city_salary_barchart(salary_stats):
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=salary_stats, x="縣市", y="平均薪資", palette="pastel")
    plt.xticks(rotation=45)
    plt.title("各縣市平均月薪資（長條圖）", fontsize=16)
    plt.ylabel("平\n均\n薪\n資", rotation=0, fontsize=14, labelpad=20)
    plt.xlabel("縣市", fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    for bar in ax.patches:
        height = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2  # 長條中心位置
        ax.text(x, height + 500, f"{height:,.0f}", ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


#縣市平均薪資小提琴圖
def city_salary_violinplot(df):
    plt.figure(figsize=(14, 6))
    sns.violinplot(data=df, x="縣市", y="平均薪資", palette="Pastel1", inner="quartile", cut=0)
    plt.xticks(rotation=45)
    plt.title("各縣市月薪資分布（小提琴圖）", fontsize=16)
    plt.ylabel("平\n均\n薪\n資", rotation=0, fontsize=14, labelpad=20)
    plt.xlabel("縣市", fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



#雙北鄉鎮區平均薪資條狀圖（Bar Chart）
def township_salary_barchart(df):
    df = df[df["縣市"].isin(["台北市", "新北市"])]
    df = df.dropna(subset=["平均薪資"])

    # 計算平均薪資
    salary_by_township = df.groupby("鄉鎮市區")["平均薪資"].mean().sort_values(ascending=False).reset_index()

    # 畫圖
    plt.figure(figsize=(14, 6))
    ax = sns.barplot(data=salary_by_township, x="鄉鎮市區", y="平均薪資", palette="pastel")
    plt.xticks(rotation=45)
    plt.title("台北市與新北市各行政區平均月薪資（長條圖）", fontsize=16)
    plt.ylabel("平\n均\n薪\n資", rotation=0, fontsize=14, labelpad=20)
    plt.xlabel("行政區", fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    for bar in ax.patches:
        height = bar.get_height()
        x = bar.get_x() + bar.get_width() / 2  # 長條中心位置
        ax.text(x, height + 500, f"{height:,.0f}", ha='center', va='bottom')
    plt.tight_layout()
    plt.show()



#雙北鄉鎮區平均薪資小提琴圖（Violin Plot）
def township_salary_violinplot(df):
    df = df[df["縣市"].isin(["台北市", "新北市"])]
    df = df.dropna(subset=["平均薪資"])

    plt.figure(figsize=(14, 6))
    sns.violinplot(data=df, x="鄉鎮市區", y="平均薪資", palette="Pastel1", inner="quartile", cut=0)
    plt.xticks(rotation=45)
    plt.title("台北市與新北市各行政區月薪資分布（小提琴圖）", fontsize=16)
    plt.ylabel("平\n均\n薪\n資", rotation=0, fontsize=14, labelpad=20)
    plt.xlabel("行政區", fontsize=14)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


"""繪製技能統計的長條圖"""
def top_skills_bar(top_skills):
    skills, counts = zip(*top_skills)
    plt.figure(figsize=(12, 6))
    plt.bar(skills, counts, color='skyblue')
    plt.xticks(rotation=45)
    plt.title("Top 20 熱門技能")
    plt.ylabel("出現次數")
    plt.tight_layout()
    plt.show()
    
"""繪製技能共現熱力圖"""   
def plot_skill_heatmap(matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix.astype(int), cmap="YlGnBu", annot=True, fmt="d")
    plt.title("技能共現熱力圖")
    plt.tight_layout()
    plt.show()