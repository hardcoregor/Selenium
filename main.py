import undetected_chromedriver as uc
import os
import time

from termcolor import cprint
from extension import proxies

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def claim_fauect(wallet, proxy):
    options = uc.ChromeOptions()
    script_address = os.getcwd()

    if len(proxy) != 0:
        ip,port,username,password = proxy.split(':')
        proxies(username, password, ip, int(port),script_address+'\\Proxies\\'+ip)
        options.add_argument('--load-extension='+script_address+'\\Proxies\\'+ip)

    options.headless = False
    chrome_driver_path = 'chromedriver.exe'
    driver = uc.Chrome(executable_path=chrome_driver_path, options=options) #IF YOU WANNA MAKE TRHOUT GOOGLE CHROME
    driver.get('https://artio.faucet.berachain.com/')
    driver.maximize_window()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#radix-\\:r0\\:')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#terms'))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#radix-\:r0\: > div.max-h-\[100vh-200px\)\].flex.flex-grow-0.flex-col.gap-4.overflow-y-scroll.sm\:h-full.sm\:max-h-\[600px\] > div.flex.gap-4 > button.inline-flex.h-fit.items-center.justify-center.transition-duration-300.transition.focus-visible\:outline-none.focus-visible\:ring-2.focus-visible\:ring-ring.focus-visible\:ring-offset-2.disabled\:opacity-30.disabled\:pointer-events-none.ring-offset-background.bg-primary.text-primary-foreground.hover\:opacity-90.px-4.py-2.rounded-md.text-lg.font-semibold.leading-7.flex-1'))).click()
        
        input_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(12) > div.relative.flex.min-h-screen.w-full.flex-col.overflow-hidden.bg-background > main > div > div.flex.w-full.flex-col-reverse.items-center.justify-between.py-12.xl\:flex-row > div > div.flex.flex-col.gap-1 > div.relative > div > input'))
        )

        input_element.send_keys(wallet)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(12) > div.relative.flex.min-h-screen.w-full.flex-col.overflow-hidden.bg-background > main > div > div.flex.w-full.flex-col-reverse.items-center.justify-between.py-12.xl\:flex-row > div > button'))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(12) > div.relative.flex.min-h-screen.w-full.flex-col.overflow-hidden.bg-background > main > div > div.flex.w-full.flex-col-reverse.items-center.justify-between.py-12.xl\:flex-row > div > button'))).click()
    except Exception as e:
        print(e, 'Faucet Error!')

    print(wallet, 'done')
    time.sleep(1)
    driver.close()
    time.sleep(1)
    driver.quit() 

def start():
    with open('settings/wallets.txt', 'r', encoding='utf-8') as file:
        wallets = file.read().splitlines()
    with open('settings/proxy.txt', 'r', encoding='utf-8') as file:
        proxies = file.read().splitlines()

    if len(proxies) != len(wallets):

        cprint('Proxies count doesn\'t match wallets count. Add proxies or leave proxies file empty', 'red')
        return
    
    queue = list(zip(wallets, proxies))

    for wallet, proxy in queue:
        try:
            claim_fauect(wallet, proxy)
        except:
            pass

start()