import selenium
import time
from tkinter import *
import tkinter.font
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import traceback

def time_trans(sec):
    if sec < 60:
        return f"{sec}s"
    elif sec < 3600:
        return f"{int(sec // 60)}m {round(sec % 60, 2)}s"
    else:
        h = int(sec // 3600)
        m = int((sec - 3600 * h) // 60)
        s = round(sec % 60, 2)
        return f"{h}h {m}m {s}s"
    
name_list = []
total_data_list = []
p_total_data_list = []
url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkdK&pkid=808&qvt=0&query=%EC%95%BC%EA%B5%AC%EC%84%A0%EC%88%98"
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
btn = driver.find_element(By.XPATH,'//*[@id="main_pack"]/section[1]/div[2]/div/div/div[3]/div/a[2]')

for i in range(100):

    start = time.time()
    driver.implicitly_wait(1)
    for j in range(15):
        if i == 0:
            path = f'//*[@id="main_pack"]/section[1]/div[2]/div/div/div[2]/div[{i+1}]/div/ul/li[{j+1}]/div/div/strong/a'
        else:
            path = f'//*[@id="main_pack"]/section[1]/div[2]/div/div/div[2]/div[{i+1}]/ul/li[{j+1}]/div/div/strong/a'
        name = driver.find_element(By.XPATH, path)
        name_list.append(name.text)

    if i == 99:
        print("선수이름 학습완료! 100%")
        break

    btn.click()
    if i == 0:
        end = time.time()
        total = (end - start) * 100
        print(f"예상 소요시간: {time_trans(round(total,2))}")
    print(f"선수이름 학습중... {i+1}%")
    
print(name_list)


for i in range(len(name_list)):
    try:
        start = time.time()
        data_list = []
        p_data_list = []
        info_url = f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query={name_list[i]}'
        driver.get(info_url)
        driver.implicitly_wait(2)
        pos_info = driver.find_element(By.XPATH,'//*[@id="main_pack"]/section[1]/div[1]/div[1]/div[2]/span[3]').text
        if "투수" in pos_info:
            
            num_info = driver.find_element(By.XPATH,'//*[@id="main_pack"]/section[1]/div[2]/div[1]/div/div[2]/dl/div[2]/dd').text.replace("kg","").replace("cm","").split(", ")
            age = 2024 - int(driver.find_element(By.XPATH,'//*[@id="main_pack"]/section[1]/div[2]/div[1]/div/div[2]/dl/div[1]/dd').text.split(".")[0])
            num = str(driver.page_source).split("playerId=")[1].split("&")[0]
            url = f"https://m.sports.naver.com/player/index?from=nx&playerId={num}&category=kbo&tab=record"
            driver.get(url)

            driver.implicitly_wait(2)

            avg = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[1]/li[1]/span').text #방어율
            whip = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[2]/li[4]/span').text #WHIP
            bb = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[2]/li[3]/span').text #볼넷
            wl = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[1]/li[2]/span').text.split("-")
            w = wl[0]
            l = wl[1]
            inn = driver.find_element(By.XPATH, '//*[@id="_basic_record"]/ul[1]/li[3]/span').text #이닝
            k = driver.find_element(By.XPATH, '//*[@id="_basic_record"]/ul[1]/li[4]/span').text #삼진
            p_hit = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[2]/li[1]/span').text #피안타
            p_hr = driver.find_element(By.XPATH, '//*[@id="_basic_record"]/ul[2]/li[2]/span').text #피홈런
            b_speed = driver.find_element(By.XPATH,'//*[@id="record_04"]/div/div/table/tbody/tr[1]').text.replace(" ","").split("km/h")
            b_speed.pop()
            for j in range(len(b_speed)):
                b_speed[j] = float(b_speed[j])
            b_speed = max(b_speed)
            p_data_list.append(float(num_info[0])) #cm
            p_data_list.append(float(num_info[1]))#kg
            p_data_list.append(float(avg))
            p_data_list.append(float(whip))
            p_data_list.append(float(w))
            p_data_list.append(float(l))
            p_data_list.append(inn)
            p_data_list.append(float(k))
            p_data_list.append(float(bb))
            p_data_list.append(float(p_hit))
            p_data_list.append(float(p_hr))
            p_data_list.append(float(age))
            p_data_list.append(b_speed)
            p_total_data_list.append(p_data_list)
        else:
            num_info = driver.find_element(By.XPATH,'//*[@id="main_pack"]/section[1]/div[2]/div[1]/div/div[2]/dl/div[2]/dd').text.replace("kg","").replace("cm","").split(", ")
            age = 2024 - int(driver.find_element(By.XPATH,'//*[@id="main_pack"]/section[1]/div[2]/div[1]/div/div[2]/dl/div[1]/dd').text.split(".")[0])
            num = str(driver.page_source).split("playerId=")[1].split("&")[0]
            url = f"https://m.sports.naver.com/player/index?from=nx&playerId={num}&category=kbo&tab=record"
            driver.get(url)

            driver.implicitly_wait(2)
    
            avg = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[1]/li[1]/span').text
            ops = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[2]/li[4]/span').text
            safe = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[2]/li[3]/span').text #출루율
            hr = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[1]/li[2]/span').text
            hit = driver.find_element(By.XPATH, '//*[@id="_basic_record"]/ul[1]/li[3]/span').text
            rbi = driver.find_element(By.XPATH, '//*[@id="_basic_record"]/ul[1]/li[4]/span').text #타점
            run = driver.find_element(By.XPATH,'//*[@id="_basic_record"]/ul[2]/li[1]/span').text #득점
            sb = driver.find_element(By.XPATH, '//*[@id="_basic_record"]/ul[2]/li[2]/span').text #도루
            data_list.append(float(num_info[0])) #cm
            data_list.append(float(num_info[1])) #kg
            data_list.append(float(avg))
            data_list.append(float(ops))
            data_list.append(float(safe))
            data_list.append(float(hr))
            data_list.append(float(hit))
            data_list.append(float(rbi))
            data_list.append(float(run))
            data_list.append(float(sb))
            data_list.append(float(age))
            total_data_list.append(data_list)
        print(f"데이터 수집중... {round(((i+1)/len(name_list)) * 100, 2)}% ({i+1}/{len(name_list)})")
    except Exception as ex:
        #err_msg = traceback.format_exc()
        #print(err_msg)
        continue
    if i == 0:
            end = time.time()
            total = (end - start) * len(name_list)
            print(f"예상 소요시간: {time_trans(round(total,2))}")
    
print(total_data_list)
print(p_total_data_list)
