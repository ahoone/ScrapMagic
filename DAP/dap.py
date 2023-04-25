# import undetected_chromedriver as uc 
# import time 

# text_file = open("output.txt", "w")

# options = uc.ChromeOptions() 
# options.headless = True 
# driver = uc.Chrome(use_subprocess=True, options=options) 
# page = driver.get("https://www.cardmarket.com/en/Magic/Products/Singles/March-of-the-Machine/Ozolith-the-Shattered-Spire") 
# driver.maximize_window() 
# time.sleep(10)
# print(type(page))
# driver.save_screenshot("datacamp.png") 
# driver.close()

# text_file.close()

import undetected_chromedriver as uc 
import time 

text_file = open("output.txt", "w")

options = uc.ChromeOptions() 
options.add_argument('--headless')
driver = uc.Chrome(use_subprocess=True, options=options) 
page = driver.get("https://www.cardmarket.com/en/Magic/Products/Singles/March-of-the-Machine/Ozolith-the-Shattered-Spire") 
driver.maximize_window() 
time.sleep(6)
html_code = driver.page_source  # get the HTML code of the page
text_file.write(html_code)  # write the HTML code to the text file
driver.save_screenshot("datacamp.png") 
driver.close()

text_file.close()


# Cette version est plus simple mais ne fonctionne pas LOL

# from selenium import webdriver 
# from webdriver_manager.chrome import ChromeDriverManager 
# from selenium.webdriver.chrome.service import Service as ChromeService 
# from selenium.webdriver.chrome.options import Options 
# import time 
 
# options = Options() 
# options.headless = True 
 
# driver = webdriver.Chrome(options=options, service=ChromeService( 
# 	ChromeDriverManager().install())) 
# driver.get("https://www.cardmarket.com/en/Magic") 
 
# time.sleep(20) 
 
# driver.save_screenshot("datacamp.png") 
 
# driver.close()