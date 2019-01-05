from selenium import webdriver
from time import sleep
import json
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')
qq = conf.get('qq','qq')
pwd = conf.get('qq','pwd')
#如未设置环境变量，那么需要去掉下列注释，更改路径
#chromedriver = 'C:/Users/13180/AppData/Local/Google/Chrome/Application/chromedriver.exe'
#driver = webdriver.Chrome(chromedriver)
driver = webdriver.Chrome()
driver.get('https://user.qzone.qq.com/'+qq+'/main')
driver.switch_to.frame('login_frame')
#找到账号密码登陆的地方
driver.find_element_by_id('switcher_plogin').click()
driver.find_element_by_id('u').send_keys(qq)
driver.find_element_by_id('p').send_keys(pwd)
driver.find_element_by_id('login_button').click()
#保存本地的cookie
sleep(5)
cookies = driver.get_cookies()
cookie_dic = {}
for cookie in cookies:
    if 'name' in cookie and 'value' in cookie:
        cookie_dic[cookie['name']] = cookie['value']
    with open('cookie_dic.txt', 'w') as f:
        json.dump(cookie_dic, f)