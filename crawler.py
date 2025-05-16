import requests
from bs4 import BeautifulSoup as bs
import time
import openpyxl
import re
import os
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

"""資料儲存"""
def init_excel(filename):
    # 如果檔案已存在，就開啟它；否則就建立新的
    if os.path.exists(filename):
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        # 只在檔案新建時寫入標題列
        ws.append(["公司名稱", "職缺名稱", "職缺連結", "地址", "縣市", "鄉鎮市區", "薪資", "給薪方式",
               "最低薪資", "最高薪資", "平均薪資", "工作經歷", "學歷",
               "科系", "語言能力", "擅長工具", "技能", "其他條件", "頁碼"])
    return wb, ws


"""城市與鄉鎮解析 """
def parse_address(address):
    """解析地址，回傳縣市與鄉鎮市區"""
    if address:
        match = re.search(r'(\S+[縣市])(\S+[鄉鎮市區])', address)
        if match:
            city = match.group(1)
            township = match.group(2)
            return city, township
    return None, None

"""薪資處理函式""" #解析薪資資訊，回傳給薪方式、下限、上限與平均
def parse_salary(salary):
    salary_identifity = re.search(r"([時日月年]薪|待遇面議)", salary)
    pattern = re.search(r"(\d{1,3}(?:,\d{3})*|\d+)(?:~(\d{1,3}(?:,\d{3})*|\d+)|元|元以上)", salary)

    if not salary_identifity:
        return None, None, None, None

    kind = salary_identifity.group(0)
    match kind:
        case "待遇面議":
            return "待遇面議", 40000, 40000, 40000
        case "年薪":
            if pattern:
                low = int(pattern.group(1).replace(",", "")) / 12
                high = int(pattern.group(2).replace(",", "")) / 12 if pattern.group(2) else low
                return "年薪", low, high, (low + high) / 2
        case "月薪":
            if pattern:
                low = int(pattern.group(1).replace(",", ""))
                high = int(pattern.group(2).replace(",", "")) if pattern.group(2) else low
                return "月薪", low, high, (low + high) / 2
        case "日薪":
            if pattern:
                low = int(pattern.group(1).replace(",", "")) * 21
                high = int(pattern.group(2).replace(",", "")) * 21 if pattern.group(2) else low
                return "日薪", low, high, (low + high) / 2
        case "時薪":
            if pattern:
                low = int(pattern.group(1).replace(",", "")) * 8 * 21
                high = int(pattern.group(2).replace(",", "")) * 8 * 21 if pattern.group(2) else low
                return "時薪", low, high, (low + high) / 2

    return None, None, None, None
    

"""詳細工作資訊""" #負責解析並提取工作要求的各個部分（工作經歷、學歷要求、科系要求等）
def extract_job_requirements(work):
    # 初始化變數為 None，避免找不到時未定義
    experience = None
    educational_qualifications = None
    department = None
    language_ability = None
    tools = None
    skill = None
    
    target_labels = ["工作經歷", "學歷要求", "科系要求", "語文條件", "擅長工具", "工作技能", "其他條件"]
    
    for i in work:
        try:
            label = i.find("h3").get_text(strip=True)
        except AttributeError:
            continue  # 如果沒有 h3 就跳過這個 i
        
        if label in target_labels:          
            work_div = i.find("div", class_="t3 mb-0")
            work_content = work_div.get_text(strip=True) if work_div else None
            match label:
                case "工作經歷":
                    experience = work_content
                case "學歷要求":
                    educational_qualifications = work_content
                case "科系要求":
                    department = work_content   
                case "語文條件":
                    language_ability = work_content
                case "擅長工具":
                    tools = work_content
                case "工作技能":
                    skill = work_content     
    return experience, educational_qualifications, department, language_ability, tools, skill


"""爬取單一工作資料"""  #處理網頁的請求、解析，以及組合工作內容、工作要求與其他條件等資料
def single_job_information(job_href):
    url = job_href
    try:
        res = requests.get(url, timeout=10)  # 可以加上 timeout 防止卡死
        res.encoding = 'utf-8'
        if res.status_code == 200:
            print("請求成功！")
        else:
            print("請求失敗，狀態碼：", res.status_code)
            return  # 提前結束
    except requests.exceptions.RequestException as e:
        print("請求失敗，錯誤訊息：", e)
        return  # 提前結束
    
    soup = bs(res.text, "html.parser")

    # 爬取工作內容
    content = soup.find("p", class_="mb-5 r3 job-description__content text-break").text.replace("工作內容:", "")
    
    # 爬取工作要求
    work = soup.find("div", class_="job-requirement-table row")
    work = work.find_all("div", class_="list-row row mb-2")
    
    # 提取各項工作要求
    experience, educational_qualifications, department, language_ability, tools, skill = extract_job_requirements(work)
    
    # 爬取其他條件
    other_conditions = "無資料"  # 預設值
    try:
        other = soup.find("div", class_="job-requirement col opened")
        if other:
            data = other.find("div", class_="col p-0 list-row__data")
            if data:
                p = data.find("p")
                if p:
                    other_conditions = p.get_text(strip=True)
                else:
                    other_conditions = data.get_text(strip=True)
    except AttributeError:
        pass  # 有問題就維持 default 的 "無資料"
    
    return experience, educational_qualifications, department, language_ability, tools, skill, other_conditions

"""# ========== 主程式主迴圈 """
def main():
    filename = "104 Python職缺資料.xlsx"
    wb, ws = init_excel(filename)
    page = 1
    url = f"https://www.104.com.tw/jobs/search/?jobsource=joblist_search&keyword=pytho%E5%A4%A7%E6%95%B8%E6%93%9A&mode=s&page=114&order={page}"
    count = 0
    
    while True:
    #while page<= 10:
        res = requests.get(url)
        #print(res.text)
        res.encoding='utf-8'
        if res.status_code == 200:
            print(res)
        else:
            print("請求失敗")
            page += 1
            continue
        soup = bs(res.text, "html.parser")
        #print(soup.prettify())
        print("------------------------")
        datas = soup.find_all("div", class_="info-container")
        #dates = soup.find_all("div", class_="job-mobile__date mt-1 t4")
        #print(dates.text.strip())
        if not datas:
            print("沒有更多資料了，結束爬蟲。")
            break
        for data in datas:
            count+=1
            
            # 工作名稱
            try:
                job_name = data.find("a").text
            except AttributeError:
                job_name = None
            
            #判斷工作名稱是否含有數據相關的關鍵字
            keywords = ["數據", "data", "Data Analyst", "資料分析師", "Data Scientist",
            "資料科學家", "Data Engineer", "資料工程師", "Machine Learning Engineer",
            "機器學習工程師", "AI Engineer", "人工智慧工程師", "Big Data Engineer",
            "大數據工程師", "Intelligence", "分析師", "資料架構師"]
            
            # 判斷 job_name 是否存在，且包含任一關鍵字
            if job_name and any(keyword.lower() in job_name.lower() for keyword in keywords):
    
                # 公司名稱
                try:
                    company = data.select("a")[1].text
                except (IndexError, AttributeError):
                    company = None

                # 工作連結
                try:
                    job_href = data.find("a").get("href")
                except AttributeError:
                    job_href = None
                if not job_href:
                    continue
                # 公司資訊字串
                try:
                    company_data = data.select("a")[1].get("title")
                except (IndexError, AttributeError):
                    company_data = None

                # 地址
                if company_data and "公司住址：" in company_data:
                    try:
                        address = company_data.split("公司住址：")[1]
                    except IndexError:
                        address = None
                else:
                    address = None

                # 薪資
                try:
                    salary = data.select("a")[6].text
                except (IndexError, AttributeError):
                    salary = None

                city, township = parse_address(address)
                salary_way, salary_low, salary_high, salary_avg = parse_salary(salary)
            
                job_info = single_job_information(job_href)
                if not job_info or any(i is None for i in job_info):
                    print("該職缺資料不完整，跳過")
                    continue
            
                experience, educational_qualifications, department, language_ability, tools, skill, other_conditions = job_info
            
                time.sleep(1)           
                #address = data.
                #print(f"第{count}篇")
                #print(company)
                #print(f"職缺名稱:{job_name}") 
                #print(f"連結:{job_href}")
                #print(f"地址:{address}")
                #print(f"縣市:{city}")
                #print(f"鄉鎮市區:{township}")     
                #print(f"薪資:{salary}")
                #print(f"給薪方式:{salary_way}")
                #print(f"薪資下限:{salary_low}")
                #print(f"薪資上限:{salary_high}")
                #print(f"平均薪資:{salary_avg}")
                #print(f"工作經歷:{experience}")
                #print(f"學歷:{educational_qualifications}")
                #print(f"科系:{department}")
                #print(f"語言能力:{language_ability}")
                #print(f"擅長工具:{tools}")
                #print(f"技能:{skill}")
                #print(f"其他條件:\n{other_conditions}")
                #print(f"工作內容:{content}")
                #print("-------------------------------------------------")
                # 寫入 excel
                row = [company, job_name, job_href, address, city, township, salary, salary_way, 
                   salary_low, salary_high, salary_avg, experience, educational_qualifications, 
                   department, language_ability,tools, other_conditions, page]

                # 清洗非法字元
                cleaned_row = [ILLEGAL_CHARACTERS_RE.sub("", str(cell)) if cell else "" for cell in row]

                # 寫入工作表
                ws.append(cleaned_row)    
                wb.save("104 Python職缺資料.xlsx")
        page += 1
        url = f"https://www.104.com.tw/jobs/search/?jobsource=joblist_search&keyword=pytho%E5%A4%A7%E6%95%B8%E6%93%9A&mode=s&page=114&order={page}"
        time.sleep(1)  # 避免被鎖 IP
        print(f"總共擷取到 {count} 筆資料，{page-1} 頁。")
    
if __name__ == "__main__":
    main()