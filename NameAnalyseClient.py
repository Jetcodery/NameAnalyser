import sys
import time
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# encoder = 'utf-8'
encoder = 'GB18030'
# encoder = 'gb2312'

def get_name_score(rawname, postconfig):
    url = "http://life.httpcn.com/xingming.asp"
    pprint(postconfig)
    # name = input("请输入姓氏：")
    # name1 = input("请输入名字：")
    # sex = input("请输入性别：")
    # dateType = input("请输入日期类型（公历/阴历）：")
    # year = input("请输入出生年份：")
    # month = input("请输入出生月份：")
    # day = input("请输入出生当天号数：")
    # hour = input("请输入出生时辰：")
    # minute = input("请输入出生时分钟数：")
    # province = input("请输入出生的省份：")
    # city = input("请输入出生的城市：")
    # whether = 0
    # flag = input("是否考虑真太阳时（是/否）：")
    # if flag == '是':
    #     whether = 1
    # else:
    #     whether = 0
    # value = 1
    # if sex == '男':
    #     value = 1
    # else:
    #     value = 0

    lastname = rawname[0]
    firstname = rawname[1:]

    sex_value = 1 if postconfig.get('Sex', '男') == '男' else 0
    dateType = '公历' if postconfig.get('DateType', '公历') in ['公历', '阳历'] else '阴历'
    year = str(postconfig.get('Year', '2023'))
    month = str(postconfig.get('Month', '4'))
    day = str(postconfig.get('Day', '21'))
    hour = str(postconfig.get('Hour', '18'))
    minute = str(postconfig.get('Minute', '27'))
    province = postconfig.get('BirthProvince', '上海')
    city = postconfig.get('BirthCity', '上海')
    UseRealSuntime = 1 if postconfig.get('RealSunTime', '是') == '是' else 0

    option = webdriver.ChromeOptions()
    option.headless = True
    driver = webdriver.Chrome(options=option)
    # driver = webdriver.Chrome()

    driver.get(url)
    driver.find_element(By.XPATH,'//*[@id="cbz2"]').click()
    driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div[1]/form/input[3]').send_keys(lastname)
    driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div[1]/form/input[4]').send_keys(firstname)
    element = driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div[1]/form/select')
    Select(element).select_by_value(str(sex_value))


    if dateType == '公历':
        driver.find_element(By.XPATH,'//*[@id="gongli"]').click()
    elif dateType == '阴历':
        driver.find_element(By.XPATH,'//*[@id="nongli"]').click()
    else:
        print("输入有误，请重试。")
        sys.exit(1)

    element1 = driver.find_element(By.XPATH,'//*[@id="year"]')
    Select(element1).select_by_value(year)
    element2 = driver.find_element(By.XPATH,'//*[@id="month"]')
    Select(element2).select_by_value(month)
    element3 = driver.find_element(By.XPATH,'//*[@id="day"]')
    Select(element3).select_by_value(day)
    element4 = driver.find_element(By.XPATH,'//*[@id="hour"]')
    Select(element4).select_by_value(hour)
    element5 = driver.find_element(By.XPATH,'//*[@id="minute"]')
    Select(element5).select_by_value(minute)


    element6 = driver.find_element(By.XPATH,'//*[@id="pid"]')
    Select(element6).select_by_value(province)

    time.sleep(3)

    element7 = driver.find_element(By.XPATH,'//*[@id="cid"]')
    Select(element7).select_by_value(city)


    if UseRealSuntime:
        driver.find_element(By.XPATH,'//*[@id="ztytime"]').click()

    driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div[3]/div[1]/div[2]/div[1]/form/input[5]').click()


    r = driver.page_source
    soup = BeautifulSoup(r, "html.parser")
    shengxiao_tag = soup.find('img', {'src': '/images/icon_xx_sx.gif'})
    shengxiao = shengxiao_tag.find_next('a').text
    suxing_tag = soup.find('img', {'src': '/images/icon_xx_mg.gif'})
    suxing = suxing_tag.next_sibling.strip()
    pusa = soup.find('img', {'src': '/images/icon_xx_bmf.gif'}).find_next('a').text

    print(f'命卦分析: {suxing}')
    print(f'生肖: {shengxiao}')
    print(f'本命佛: {pusa}')

    table = soup.find('table', class_='tablecolor')
    # 天格、人格、地格、外格、总格的信息在<td>标签的align属性为"left"的<td>标签内
    td_lefts = table.find_all('td', align='left')
    five_elements = []
    for td_left in td_lefts:
        five_elements.append(td_left.get_text().strip())

    wuge_score = 'None'
    bazi_score = 'None'
    for node in soup.find_all("div", class_="chaxun_b"):
        if "姓名五格评分" not in node.get_text():
            continue
        score_fonts = node.find_all("font")
        wuge_score = score_fonts[0].get_text()
        bazi_score = score_fonts[1].get_text()
        wuge_score = wuge_score.replace("分", "").strip()
        bazi_score = bazi_score.replace("分", "").strip()

    return {
        '生肖': shengxiao,
        '命卦分析': suxing,
        '本命佛': pusa,
        '五格': [i.strip() for i in five_elements[0].split('\n\n')],
        '五格评分': wuge_score,
        '八字评分': bazi_score
    }



if __name__ == '__main__':
    get_name_score()

