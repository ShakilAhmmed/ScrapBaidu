import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator
import time
import csv

class ScrapApplication:
    def __init__(self):
        # self.translator = Translator(to_lang="en")
        print("Scarapping Baidu")

    def sent_request(self):
        browser = webdriver.Chrome("/opt/lampp/htdocs/Django/BaiduScrap/chromedriver")
        browser.get("https://qianxi.baidu.com/")
        source = browser.page_source
        time.sleep(10)
        browser.close()
        return source
        # response = requests.get("https://qianxi.baidu.com/")
        # time.sleep(10)
        # return response.content if response.status_code == 200 else 'Unreachable'

    def soup_data(self):
        translator = Translator()
        try:
            soup = BeautifulSoup(self.sent_request(), 'lxml')
            find_main_div = soup.find("div", {"class": "mgs-list-box"})
            find_data_div = find_main_div.find("table")
            all_city_names = find_data_div.find_all("span", {"class": "mgs-date-city"})
            all_city_province = find_main_div.find_all("span", {"class": "mgs-date-province"})

            all_tr_get =find_data_div.find_all("tr",{"class":"undefined"})
            proportion = [proportion.text for tr in all_tr_get for index, proportion in  enumerate(tr.find_all("td"))  if index == 2 ]

            data_set = list(zip(all_city_names, all_city_province,proportion))
            translated_data_organize = []
            i = 1;
            for data in data_set:

                translated_data_organize.append([
                    i,
                    translator.translate(data[0].text, dest='en').text,
                    translator.translate(data[1].text, dest='en').text,
                    data[2]
                ])
                i +=1 
                # get_data = {
                #     'city_name': translator.translate(data[0].text, dest='en').text,
                #     'province': translator.translate(data[1].text, dest='en').text,
                #     'proportion': data[2],
                # }
                # translated_data_organize.append(get_data)
            with open("baidu_file.csv",'w',newline='') as csvfile:
                fieldnames=['SlNo','CityName','Province','Proportion']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
                writer.writerows(translated_data_organize)
            print("Successfully Scrapped")
        except:
            print("Please Try Again Later or Check Your Internet Connection")
    # def store_to_csv(self):
    #     with open("baidu_file.csv",'w',newline='') as csvfile:
    #         fieldnames=['SlNo','CityName','Province','Proportion']
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
    #         get_data_set = self.soup_data()
    #         writer.writerows(get_data_set)
        # print(translator.translate(city_name.text, dest='en').text)


if __name__ == "__main__":
    scrap_app = ScrapApplication()
    scrap_app.soup_data()
