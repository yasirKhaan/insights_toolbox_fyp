from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

class Screenshot:

    def screenshot_taken(self):
        options = webdriver.ChromeOptions()
        options.headless = False
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(100)

        driver.get('hhttp://127.0.0.1:8000/dashboard')
        # driver.get('https://www.lipsum.com/')

        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'), S('Height'))
# driver.find_element_by_tag_name('body').screenshot('sample1.png');
        driver.find_element(By.TAG_NAME, 'body').screenshot('sample.png')

ss = Screenshot()
ss.screenshot_taken()



