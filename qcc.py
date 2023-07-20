import pymssql
import pandas as pd
import importlib #提供import语句
import sys
import time #提供延时功能
from selenium.webdriver.common.by import By    #用于获取网页中的相关元素、标签
from selenium import webdriver
importlib.reload(sys)    #避免utf-8等编码问题的出现

class aqc():
    def __init__(self):
        pass

    # 数据库获取公司名称
    def company(self):
        conn = pymssql.connect(host="10.2.0.45:1433", user="sa", password="Frbi2020", database="CyBi", charset="utf8")
        df = pd.read_sql("select * from dbo.View_Frbi_gsxx order by 数量 desc",con=conn)
        conn.close()
        return df['客户']
    
    # 模拟打开浏览器并完成登录
    def browser_login(self):
        #伪装成浏览器，防止被识破
        option = webdriver.ChromeOptions()
        option.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"')    #请求头
        driver = webdriver.Chrome(options=option)    #打开chrome浏览器
        #打开爱企查登录页面
        driver.get('https://aiqicha.baidu.com/')
        time.sleep(30) #等待20s以用于完成手动登录操作
        return driver
    
    # 初次搜索目标
    def search_first(self, driver, txt):
        # 主页面搜索
        driver.find_element(By.ID,'aqc-search-input').send_keys(txt)
        srh_btn = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[1]/div[2]/button')
        srh_btn.click()
        time.sleep(3)
        # 列表窗口点击进入详情窗口
        srh_a = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[1]/div[4]/div[2]/div/div[1]/div[2]/div/h3/a')
        srh_a.click()
        time.sleep(3)
        # 关闭列表窗口并切换至详情窗口
        driver.close()
        ws=driver.window_handles[0]
        driver.switch_to.window(ws)
    
    # 持续搜索目标
    def search(self, driver, txt):
        # 清楚搜索框数据，并搜索新内容
        driver.find_element(By.ID,'aqc-header-search-input').clear()
        driver.find_element(By.ID,'aqc-header-search-input').send_keys(txt)
        srh_btn = driver.find_element(By.XPATH,'/html/body/div/div[1]/header/div/div[2]/button')
        srh_btn.click()
        time.sleep(3)
        # 列表窗口点击进入详情窗口
        srh_a = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[1]/div[4]/div[2]/div/div[1]/div[2]/div/h3/a')
        srh_a.click()
        time.sleep(3)
        # 关闭列表窗口并切换至详情窗口
        driver.close()
        ws=driver.window_handles[0]
        driver.switch_to.window(ws)

    # 获取公司信息
    def get_res(self, driver, txt):
        # 通用链接
        universal_link = '/html/body/div[1]/div[2]/div/div[6]/div[1]/div[3]/table/tbody'
        try:
            # 名称
            name = driver.find_element(By.XPATH, universal_link + '/tr[1]/td[2]/span').text
        except:
            name = ''
        try:
            # 电话
            phone = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]/div/span[2]/span/span').text
        except:
            phone = ''
        try:
            # 邮箱
            email = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div[2]/div/a').text
        except:
            email = ''
        try:
            # 统一社会信用代码
            code = driver.find_element(By.XPATH, universal_link + '/tr[1]/td[4]/span').text
        except:
            code = ''
        try:
            # 法定代表人
            representative = driver.find_element(By.XPATH, universal_link + '/tr[2]/td[2]/div[2]/a').text
        except:
            representative = ''
        try:
            # 经营状态
            status = driver.find_element(By.XPATH, universal_link + '/tr[2]/td[4]').text
        except:
            status = ''
        try:
            # 成立日期
            establish = driver.find_element(By.XPATH, universal_link + '/tr[3]/td[2]').text
        except:
            establish = ''
        try:
            # 行政区划
            district = driver.find_element(By.XPATH, universal_link + '/tr[3]/td[4]').text
        except:
            district = ''
        try:
            # 注册资本
            capital = driver.find_element(By.XPATH, universal_link + '/tr[4]/td[2]').text
        except:
            capital = ''
        try:
            # 企业类型
            type = driver.find_element(By.XPATH, universal_link + '/tr[5]/td[2]').text
        except:
            type = ''
        try:
            # 所属行业
            industry = driver.find_element(By.XPATH, universal_link + '/tr[5]/td[4]').text
        except:
            industry = ''
        try:
            # 营业期限
            term = driver.find_element(By.XPATH, universal_link + '/tr[8]/td[2]').text
            term_start = term[:10]
            term_end = term[-10:]
        except:
            term_start = ''
            term_end = ''
        try:
            # 参保人数
            insured_persons = driver.find_element(By.XPATH, universal_link + '/tr[9]/td[4]').text
        except:
            insured_persons = ''
        try:
            # 曾用名
            former = driver.find_element(By.XPATH, universal_link + '/tr[10]/td[2]/p/span').text
        except:
            former = ''
        try:
            # 注册地址
            address = driver.find_element(By.XPATH, universal_link + '/tr[11]/td[2]/span').text
        except:
            address = ''
        try:
            # 经营范围
            scope = driver.find_element(By.XPATH, universal_link + '/tr[12]/td[2]/div').text.replace('\n... 展开','')
        except:
            scope = ''

        res = [txt, name, phone, email, code, representative, status, establish, district, capital, type, industry, term_start, term_end, insured_persons, former, address, scope]
        for j in range(len(res)):
            res[j] = str(res[j])
        return res

aq = aqc()
driver = aq.browser_login()
company = ['爱奇艺', '百度', '腾讯', '华为']
resd = []
for i in range(len(company)):
    txt = company[i]
    if i == 0:
        aq.search_first(driver, txt)
    else:
        aq.search(driver, txt)
    res = aq.get_res(driver, txt)
    resd.append(res)
resd = pd.DataFrame(resd)
resd.columns = ['txt', 'name', 'phone', 'email', 'code', 'representative', 'status', 'establish', 'dsitrict', 'capital', 'type', 'industry', 'term_start', 'term-end', 'insured_persons', 'former', 'address', 'scope']
print(resd)
resd.to_csv("gsxx.csv",mode='a',index=False,header=True)