from fpdf import FPDF, HTMLMixin
import markdown
import os

class PDF(FPDF, HTMLMixin):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

        # 設定所有樣式的字型
        self.add_font('msjh', '', r'C:\Windows\Fonts\msjh.ttc', uni=True)   # Regular
        self.add_font('msjh', 'B', r'C:\Windows\Fonts\msjh.ttc', uni=True)  # Bold
        self.add_font('msjh', 'I', r'C:\Windows\Fonts\msjh.ttc', uni=True)  # Italic
        self.add_font('msjh', 'BI', r'C:\Windows\Fonts\msjh.ttc', uni=True) # Bold Italic
        self.set_font('msjh', '', 12)

    def chapter_title(self, title):
        self.set_font('msjh', '', 14)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)

    def chapter_body(self, markdown_text):
        self.set_font('msjh', '', 12)
        html = markdown.markdown(markdown_text)  # Markdown 轉 HTML
        self.write_html(html)  # 支援 HTML 的文字排版
        self.ln()

    def insert_image(self, image_path, w=180):
        if os.path.exists(image_path):
            self.image(image_path, w=w)
            self.ln()

def report(report_overview, city_job, township_job, city_salary, township_salary,
           experience_data, education_data, skill_data, summary, conclusion):
    
    pdf = PDF()
    pdf.add_page()

    # 各章節：文字可為 Markdown 格式
    pdf.chapter_title("報表總覽說明")
    pdf.chapter_body(report_overview)

    pdf.chapter_title("一、縣市職缺分布")
    pdf.insert_image("output/city_vacancies.png")
    pdf.chapter_body(city_job)

    pdf.chapter_title("二、台北與新北職缺分布")
    pdf.insert_image("output/township_vacancies.png")
    pdf.chapter_body(township_job)

    pdf.chapter_title("三、縣市平均薪資")
    pdf.insert_image("output/city_salary_barchart.png")
    pdf.insert_image("output/city_salary_violinplot.png")
    pdf.chapter_body(city_salary)

    pdf.chapter_title("四、台北與新北區域平均薪資")
    pdf.insert_image("output/township_salary_barchart.png")
    pdf.insert_image("output/township_salary_violinplot.png")
    pdf.chapter_body(township_salary)

    pdf.chapter_title("五、工作經歷分析")
    pdf.chapter_body(experience_data)

    pdf.chapter_title("六、學歷要求分析")
    pdf.chapter_body(education_data)

    pdf.chapter_title("七、技能與工具統計")
    pdf.insert_image("output/top_skills_bar.png")
    pdf.chapter_body(skill_data)

    pdf.chapter_title("八、技能關聯分析（共現熱力圖）")
    pdf.insert_image("output/skill_heatmap.png")
    pdf.chapter_body(summary)

    pdf.chapter_title("九、結論")
    pdf.chapter_body(conclusion)

    # 儲存報表
    pdf.output("大數據職缺分析報告.pdf", 'F')