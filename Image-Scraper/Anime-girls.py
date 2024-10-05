from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import base64
import time
import requests


user_input = input("What kind of images would you like: ")
user_number = int(input("How many images would you like (The max is around 600): "))
chrome = r"C:\Users\emreb\Downloads\chromedriver-win64\chromedriver.exe"
url = "https://www.google.com/search?client=chrome&hs=rW6&sca_esv=f39be0dcf9683254&sca_upv=1&q=" + user_input + "&udm=2&fbs=AEQNm0CgMcZ11KbHg1uunEmuo39LYaLxf_n_v5Qu9vkTINnKPNxSSRV--bGiJa6CXOAP_uho18w_8TFWAZHfYwF06xuG_Ptl2Mt4OfgI78AO22t4xQSvFNCtCIocfDggG0toe9ysROhxwufVs0P9m6xSI2nzQp-0il7-wIewHirNx4vLX0y--OG-BxVv2lphcbOm-VNtAVtkwSGUW8-tEKCHqzJiv-npDzvG0CozvVY3T_iaZYJ2cG0&sa=X&ved=2ahUKEwiV-fD6tYOIAxUzhv0HHZlDL0oQtKgLegQIFhAB"


service = Service(chrome)

driver = webdriver.Chrome(service=service)

driver.get(url)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

image_element = soup.findAll("img")

a = 0
index = 0
for i in image_element:
    if a < 8:
        a += 1
        continue
    if i["src"] == "https://fonts.gstatic.com/s/i/productlogos/googleg/v6/24px.svg":
        continue
    if int(i["height"]) == 12 or int(i["height"]) == 16:
        continue
    try:
        image_srcc = i["src"]
        if ',' in image_srcc:
            header, encoded = image_srcc.split(',', 1)
            image_data = base64.b64decode(encoded)

            format_type = header.split('/')[1].split(';')[0]

            filename = f'image_{index}.{format_type}'
            if format_type == "gif":
                continue
            with open(filename, 'wb') as file:
                file.write(image_data)

            index += 1
        else:
            filename = f'image_{index}.jpeg'
            link_img = requests.get(image_srcc)
            with open(filename, "wb") as file:
                file.write(link_img.content)
            index += 1
            if index == user_number:
                break
    except:
        continue
driver.quit()
