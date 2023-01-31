from queue import Empty
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json

brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path
#options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = ["https://aibe.lt/akcijos/","https://barbora.lt/akcijos"]
dict = {}

for link in url:
    driver.get(link)
    if link == "https://aibe.lt/akcijos/":
        pard = "Aibe"
        prekes = driver.find_elements(By.CLASS_NAME,'bestOffers-block-discountProduct-name')
        e = driver.find_elements(By.CLASS_NAME,'discount-price-now-euro')
        c = driver.find_elements(By.CLASS_NAME,'discount-price-now-cent')
        #sena_kaina = driver.find_elements(By.CLASS_NAME, 'discount-without-card-price')
        data = driver.find_element(By.CLASS_NAME, 'top-block-date').text
        for pav, kaina_eur, kaina_centai in zip(prekes, e, c):
            kaina_centai.text.replace("\n", "")
            kaina = str(kaina_eur.text + "," + kaina_centai.text)
            if len(dict)==0:
                new = {pard:[{"name": pav.text.replace("\n", ""),  "price":kaina.replace("\n", ""), "date":data}]}
                dict.update(new)
            else:
                dict[pard].append({"name": pav.text.replace("\n", ""),  "price":kaina.replace("\n", ""), "date":data})

    if link == "https://barbora.lt/akcijos":
        pard="Barbora"
        data_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.maximize_window()
        dict.update({pard:[]})
        for i in range(1,2):
            driver.find_element(By.LINK_TEXT, "{0}".format(i)).click()
            prekes = driver.find_elements(By.XPATH, "//*[@class='b-page-specific-content']//span[@itemprop='name']" )
            kaina = driver.find_elements(By.CLASS_NAME, "b-product-price-current-number" )
            #sena_kaina = driver.find_elements(By.CLASS_NAME, "b-product-crossed-out-price" )
            linkas = driver.find_elements(By.XPATH, "//a[@class='b-product-title b-product-title--desktop b-link--product-info']")
            sar = []
            for i in linkas:
                sar.append(i.get_attribute('href'))

            for pav, kaina_db, link in zip(prekes, kaina, sar):
                data_driver.get(str(link))
                data = data_driver.find_element(By.CLASS_NAME,'b-product-info--offer-valid-to').text
                dict[pard].append({"name": pav.text, "price":kaina_db.text, "link":link, "date":data})

with open("sample.json", "w", encoding='utf-8') as outfile:
    outfile.write(json.dumps(dict, ensure_ascii=False, indent=4))