import sys
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import http.client
from anticaptchaofficial.recaptchav2proxyon import *
from selenium.webdriver.common.by import By


def get_txt_data():
    try:
        links0 = open('Dolphin_Enty_auth.txt', 'r').read().split('\n')
        auth = []
        links0[0].replace(' ','')
        links0[1].replace(' ','')
        auth.append(links0[0])
        auth.append(links0[1])
    except:
        print('Ошибка обработки файла-Dolphin_Enty_auth.txt')
        return None

    try:
        links=open('твиттеры.txt','r').read().split('\n\n')
        twitter=[]
        for link in links:
            perem=link.split('\n')
            login=perem[0].split(':')
            password=perem[1].split(':')
            mail = perem[2].split(':')
            mailpassword=perem[3].split(':')
            accountdate=perem[4].split(':')
            mass=[]
            mass.append(login[1].replace(' ',''))
            mass.append(password[1].replace(' ', ''))
            mass.append(mail[1].replace(' ', ''))
            mass.append(mailpassword[1].replace(' ', ''))
            mass.append(accountdate[1].replace(' ', ''))
            twitter.append(mass)
    except:
        print('Ошибка обработки файла-твиттеры.txt')
        return None

    try:
        links2=open('дискорды.txt','r').read().split('\n')
        discord=[]
        for link in links2:
            dis=link.split(':')
            discord.append(dis[2])
    except:
        print('Ошибка обработки файла-дискорды.txt')
        return None

    try:
        links3=open('Приват ключи.txt','r').read().split('\n')
        private_key=[]
        for link in links3:
            l=link.replace(' ','')
            if l!='PrivateKey':
                private_key.append(l)
    except:
        print('Ошибка обработки файла-Приват ключи.txt')
        return None

    try:
        links4=open('proxy.txt','r').read().split('\n')
        proxy=[]
        for link in links4:
            mass=link.split(':')
            proxy.append(mass)
    except:
        print('Ошибка обработки файла-proxy.txt')
        return None

    return auth, twitter, discord, private_key, proxy

def get_Dolphin_token(auth):
    url = "https://anty-api.com/auth/login"
    payload={
        'username':f'{str(auth[0])}',
        'password':f'{str(auth[1])}'}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    print('Отправка запроса на anty-api.com/auth/login для получения токена')
    js=response.text
    try:
        js_to = json.loads(js)
        print('Токен удачно получен')
        print(f"token:{js_to['token']}")
    except:
        print('Ошибка обращения к серверу, запуск повторного запроса')
        time.sleep(3)
        get_Dolphin_token()
    return js_to['token']

def create_profile(token,proxy):
    conn = http.client.HTTPSConnection("anty-api.com")
    payload = json.dumps({
        "common": {
            "platform": "windows",
            "browserType": "anty",
            "useragent": {
                "mode": "manual",
                "value": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
            },
            "webrtc": {
                "mode": "altered",
                "ipAddress": None
            },
            "canvas": {
                "mode": "noise"
            },
            "webgl": {
                "mode": "real"
            },
            "webglInfo": {
                "mode": "random"
            },
            "geolocation": {
                "mode": "real",
                "latitude": None,
                "longitude": None
            },
            "cpu": {
                "mode": "real",
                "value": None
            },
            "memory": {
                "mode": "manual",
                "value": 8
            },
            "timezone": {
                "mode": "auto",
                "value": None
            },
            "locale": {
                "mode": "auto",
                "value": None
            }
        },
        "items": [
            {
                "name": "dolphin",
                "tags": [""],
                "mainWebsite": "",
                "notes": {
                    "content": None,
                    "color": "blue",
                    "style": "text",
                    "icon": None
                },
                #"proxy": #f'{proxy[0]}:{proxy[1]}:{proxy[2]}:{proxy[3]}',#f'http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}',
                "proxy":{
                    "type":"socks5",
                    "host":f"{proxy[0]}",
                    "port":f"{proxy[1]}",
                    "login":f"{proxy[2]}",
                    "password":f"{proxy[3]}"
                },
                "statusId": 0,
                "doNotTrack": False
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    conn.request("POST", "/browser_profiles/mass", payload, headers)
    res = conn.getresponse()
    data = res.read()
    js_to=json.loads(data.decode("utf-8"))
    return js_to['ids'][0]

def delete_profile(token,id):
    print("Удаление профиля")
    conn = http.client.HTTPSConnection("anty-api.com")
    payload = ''
    headers = {'Authorization': f'Bearer {token}'}
    conn.request("DELETE", f"/browser_profiles/{id}", payload, headers)
    res = conn.getresponse()

def run_browser(PROFILE_ID,name):
    print(f"Запуск браузера '{name}'")
    url=f'http://localhost:3001/v1.0/browser_profiles/{PROFILE_ID}/start?automation=1'
    response=requests.request("GET", url)
    js = response.text
    js_to = json.loads(js)
    port=js_to['automation']['port']
    wsEndpoint=js_to['automation']['wsEndpoint']
    return port,wsEndpoint

def stop_browser(PROFILE_ID,name):
    print(f"Остановка браузера '{name}'")
    url = f'http://localhost:3001/v1.0/browser_profiles/{PROFILE_ID}/stop'
    requests.request("GET", url)

def run_selen(port,twitter,discord,private_key,proxy):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
    driver.implicitly_wait(20)
    def Metamask():
        global btn
        nonlocal driver,private_key
        flag = True
        iter_error = 0
        while flag:
            try:
                handles=driver.window_handles
                if len(handles)>1:
                    handle1 = handles[0]
                    handle2 = handles[1]
                    driver.switch_to.window(handle1)
                    driver.close()
                    driver.switch_to.window(handle2)
                    flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 20:
                    flag = False
        time.sleep(3)

        flag=True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                assert btn.text == "Get Started" or btn.text == "Начало работы"
                btn.click()
                flag=False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[1]
                assert btn.text == "Create a Wallet" or btn.text == "Создать кошелек"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                assert btn.text == "I Agree" or btn.text == "Я согласен(-на)"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(1)
        driver.find_element(By.ID,'create-password').send_keys("12345678")
        time.sleep(1)
        driver.find_element(By.ID,'confirm-password').send_keys("12345678")
        time.sleep(1)
        driver.find_elements(By.CLASS_NAME,'first-time-flow__checkbox')[0].click()
        time.sleep(1)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                assert btn.text == "Create" or btn.text == "Создать"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(5)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                assert btn.text == "Next" or btn.text == "Далее"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-secondary')[0]
                assert btn.text == "Remind me later" or btn.text == "Напомните мне позже"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(3)
        driver.get('chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#new-account/import')
        time.sleep(3)

        flag = True
        iter_error = 0
        while flag:
            try:
                inp = driver.find_element(By.TAG_NAME,'input')
                inp.send_keys(private_key)
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                assert btn.text == "Import" or btn.text == "Импорт"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False

    def Twitter():
        global btn
        nonlocal driver,twitter
        driver.get('https://twitter.com/i/flow/login')
        time.sleep(3)

        flag = True
        iter_error = 0
        while flag:
            try:
                inp = driver.find_element(By.TAG_NAME,'input')
                inp.send_keys(twitter[0])
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        inp.send_keys(twitter[0])
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag=True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'r-qvutc0')[14]
                assert btn.text == "Next" or btn.text == "Далее"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                inp = driver.find_elements(By.TAG_NAME,'input')[1]
                inp.send_keys(twitter[1])
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        inp.send_keys(twitter[1])
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'r-qvutc0')[20]
                assert btn.text == "Log in" or btn.text == "Войти"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(3)

        if driver.find_elements(By.CLASS_NAME,'r-qvutc0')[2].text=='Help us keep your account safe.' or driver.find_elements(By.CLASS_NAME,'r-qvutc0')[2].text=='Помогите нам сохранить вашу учетную запись в безопасности':
            flag = True
            iter_error = 0
            while flag:
                try:
                    inp = driver.find_element(By.TAG_NAME,'input')
                    inp.send_keys(twitter[2])
                    flag = False
                except:
                    time.sleep(1)
                    iter_error += 1
                    if iter_error >= 5:
                        try:
                            inp.send_keys(twitter[2])
                        except:
                            pass
                        flag = False
            time.sleep(2)

            flag = True
            iter_error = 0
            while flag:
                try:
                    btn = driver.find_elements(By.CLASS_NAME,'r-qvutc0')[26]
                    assert btn.text == "Next" or btn.text == "Далее"
                    btn.click()
                    flag = False
                except:
                    time.sleep(1)
                    iter_error += 1
                    if iter_error >= 5:
                        try:
                            btn.click()
                        except:
                            pass
                        flag = False
        else:
            try:
                inp = driver.find_element(By.TAG_NAME,'input')
                inp.send_keys(twitter[2])
                btn = driver.find_elements(By.CLASS_NAME,'r-qvutc0')[26]
                btn.click()
            except:
                pass

    def Discord():
        nonlocal driver,discord
        driver.get('https://discord.com/login')
        time.sleep(3)
        script="function login(token){setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `\"${token}\"`}, 50);setTimeout(() => {location.reload();}, 2500);}"
        script=script+f"login('{discord}');"
        driver.execute_script(script)

    def Hanabi():
        global btn
        nonlocal driver
        driver.get('https://www.premint.xyz/8hanabi/')
        time.sleep(3)
        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn')[0]
                assert btn.text == "Connect"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'btn')[0]
                assert btn.text.replace('\n','') == "Connect Wallet"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'web3modal-provider-name')[0]
                assert btn.text == "MetaMask"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 5:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(2)

        global_flag=True
        main_window = driver.current_window_handle
        while global_flag:
            handless=driver.window_handles
            if len(handless)>1:
                for handle in driver.window_handles:
                    if handle != main_window:
                        popup = handle
                        driver.switch_to.window(popup)
                        time.sleep(2)

                        flag = True
                        iter_error = 0
                        while flag:
                            try:
                                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                                assert btn.text == "Next" or btn.text == "Далее"
                                btn.click()
                                flag = False
                            except:
                                time.sleep(1)
                                iter_error += 1
                                if iter_error >= 5:
                                    try:
                                        btn.click()
                                    except:
                                        pass
                                    flag = False
                        time.sleep(3)

                        flag = True
                        iter_error = 0
                        while flag:
                            try:
                                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                                assert btn.text == "Connect" or btn.text == "Подключиться"
                                btn.click()
                                flag = False
                            except:
                                time.sleep(1)
                                iter_error += 1
                                if iter_error >= 5:
                                    try:
                                        btn.click()
                                    except:
                                        pass
                                    flag = False
                        time.sleep(8)

                        flag = True
                        iter_error = 0
                        while flag:
                            try:
                                btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                                assert btn.text == "Sign" or btn.text == "Подписать"
                                btn.click()
                                flag = False
                            except:
                                time.sleep(1)
                                iter_error += 1
                                if iter_error >= 5:
                                    try:
                                        btn.click()
                                    except:
                                        pass
                                    flag = False
                        driver.switch_to.window(main_window)
                        global_flag=False
        time.sleep(8)
        handless = driver.window_handles
        if len(handless) > 1:
            for handle in driver.window_handles:
                if handle != main_window:
                    popup = handle
                    driver.switch_to.window(popup)
                    time.sleep(2)

                    flag = True
                    iter_error = 0
                    while flag:
                        try:
                            btn = driver.find_elements(By.CLASS_NAME,'btn-primary')[0]
                            assert btn.text == "Sign" or btn.text == "Подписать"
                            btn.click()
                            flag = False
                        except:
                            time.sleep(1)
                            iter_error += 1
                            if iter_error >= 5:
                                try:
                                    btn.click()
                                except:
                                    pass
                                flag = False
                    driver.switch_to.window(main_window)
        time.sleep(3)
        flag=True
        iter_error = 0
        while flag:
            if driver.current_url=="https://www.premint.xyz/8hanabi/":
                flag=False
            else:
                time.sleep(1)
                iter_error+=1
                if iter_error >= 20:
                    flag = False
        driver.get('https://www.premint.xyz/accounts/twitter/login/?process=connect&next=%2F8hanabi%2F')
        time.sleep(2)
        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'submit')[0]
                assert btn.get_attribute('value') == "Authorize app" or btn.get_attribute('value') == "Авторизовать приложение"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 2:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(3)
        driver.get('https://www.premint.xyz/accounts/discord/login/?process=connect&next=%2F8hanabi%2F&scope=guilds.members.read')
        time.sleep(2)

        flag = True
        iter_error = 0
        while flag:
            try:
                btn = driver.find_elements(By.CLASS_NAME,'contents-3ca1mk')[1]
                assert btn.text == "Authorize" or btn.text == "Авторизовать"
                btn.click()
                flag = False
            except:
                time.sleep(1)
                iter_error += 1
                if iter_error >= 2:
                    try:
                        btn.click()
                    except:
                        pass
                    flag = False
        time.sleep(3)

        try:
            driver.find_element(By.ID,'id_custom_field').send_keys('12124')
        except:
            pass
        time.sleep(1)


        solver = recaptchaV2Proxyon()
        solver.set_verbose(1)
        solver.set_key("")
        solver.set_website_url("https://www.premint.xyz/8hanabi/")
        solver.set_website_key("")
        solver.set_proxy_type('socks5')
        solver.set_proxy_address(proxy[0])
        solver.set_proxy_port(str(proxy[1]))
        solver.set_proxy_login(proxy[2])
        solver.set_proxy_password(proxy[3])
        solver.set_user_agent("Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
        g_response = solver.solve_and_return_solution()

        if g_response != 0:
            print("g-response: " + g_response)
            try:
                time.sleep(1)
                driver.execute_script("document.getElementsByTagName('textarea')[0].style.display='block'")
                driver.execute_script("document.getElementsByTagName('textarea')[0].style.marginTop='0px'")
                driver.execute_script("document.getElementsByTagName('textarea')[0].style.marginLeft='0px'")
                driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{g_response}";')
                time.sleep(1)
                func = driver.find_element(By.ID,'id_captcha').get_attribute('data-callback')
                driver.execute_script(f"{func}('{g_response}')")
                time.sleep(1)
                try:
                    btns = driver.find_elements(By.TAG_NAME,'button')
                    for b in btns:
                        if b.get_attribute('name') == 'registration-form-submit':
                            b.click()
                except:
                    pass
                with open('output.txt', 'a+') as the_file:
                    the_file.write(f'{twitter[0]}:{discord}:{private_key}\n')
            except:
                pass
            time.sleep(1)
        else:
            print("task finished with error")

    flag_podsub=True
    if flag_podsub:
        try:
            print('Шаг 1-Metamask')
            Metamask()
            time.sleep(5)
        except:
            flag_podsub=False
    if flag_podsub:
        try:
            print('Шаг 2-Twitter')
            Twitter()
            time.sleep(5)
        except:
            flag_podsub=False
    if flag_podsub:
        try:
            print('Шаг 3-Discord')
            Discord()
            time.sleep(8)
        except:
            flag_podsub=False
    if flag_podsub:
        try:
            print('Шаг 4-Hanabi')
            Hanabi()
            time.sleep(5)
        except:
            pass
    driver.quit()

n=input('Введите количество циклов=')
i=0
iter_twitter=0
iter_discord=0
iter_private_key=0
iter_proxy=0

if get_txt_data()==None:
    sys.exit(0)
else:
    auth,twitter,discord,private_key,proxy=get_txt_data()

len_twitter=len(twitter)
len_discord=len(discord)
len_private_key=len(private_key)
len_proxy=len(proxy)

while i<int(n):
    if iter_twitter>=len_twitter:
        iter_twitter=0
    if iter_discord>=len_discord:
        iter_discord=0
    if iter_private_key>=len_private_key:
        iter_private_key=0
    if iter_proxy>=len_proxy:
        iter_proxy=0

    flag_run=True
    if flag_run:
        try:
            token=get_Dolphin_token(auth)
            time.sleep(3)
        except:
            flag_run=False

    if flag_run:
        try:
            id=create_profile(token,proxy[iter_proxy])
            time.sleep(3)
        except:
            flag_run=False

    if flag_run:
        try:
            port,wsEndpoint=run_browser(id,'dolphin')
            time.sleep(3)
        except:
            flag_run = False
            stop_browser(id, 'dolphin')
            delete_profile(token, id)

    if flag_run:
        try:
            run_selen(port,twitter[iter_twitter],discord[iter_discord],private_key[iter_private_key],proxy[iter_proxy])
            time.sleep(3)
        except:
            flag_run = False
            stop_browser(id, 'dolphin')
            delete_profile(token, id)
    try:
        stop_browser(id,'dolphin')
        time.sleep(5)
        delete_profile(token,id)
    except:
        pass

    iter_twitter+=1
    iter_discord+=1
    iter_private_key+=1
    iter_proxy+=1
    i+=1


