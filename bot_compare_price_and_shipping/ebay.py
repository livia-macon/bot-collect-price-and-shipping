from botcity.web.browsers.chrome import default_options
from bot_compare_price_and_shipping.amazon import InitDataAndBrowser
from selenium import webdriver
from botcity.web import WebBot, Browser
import pandas as pd
import openpyxl
import requests

class BotEbay(InitDataAndBrowser):

    def generate_link_ebay(self):
        self.base_url_ebay = 'https://www.ebay.com/'

        self.url_ebay = ("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="
                         + self.product_search.replace(" ", "+") + "&_sacat=0&LH_TitleDesc=0&_odkw="
                                                                   "samsung+galaxy+z+fold+3&_osacat=0")
        # return self.open_brws_ebay(self.url_ebay)
        return self.open_brws(self.url_ebay)

    def input_zip_code_ebay(self):
        if not self.find( "frete_para", matching=0.97, waiting_time=10000):
            self.not_found("frete_para")
        self.click_relative(76, 6)

        self.tab()
        self.wait(2000)
        self.type_keys('E')
        self.type_keys('S')
        self.type_down()
        self.type_down()
        self.type_down()
        self.tab()
        self.paste(self.zip_code)
        self.enter()

    def collect_infos_ebay(self):
        self.page_source()
        self.soup_ebay = self.page_source()
        self.list_ebay = []

        self.product_list_ebay = self.soup_ebay.find_all('div', attrs={'class': 's-item__image'})

        self.product_link_ebay = []
        # for each product box found, collect link and after concatenate with base link
        for item in self.product_list_ebay[4:6]:
            for link in item.find_all('a'):
                self.product_link_ebay.append(link['href'])

        self.par_filter_amazon = 'Fold 3'

        # open link concatenate, extract this information and append in list
        for links in self.product_link_ebay:
            self.browse(links)
            self.wait(4000)
            self.page_source()
            self.soup_search_ebay = self.page_source()


            self.product_name = self.soup_search_ebay.find('h1', attrs={'class': 'it-ttl'}).text.strip()
            self.list_ebay.append(self.product_name[13:].replace("\xa0", "").replace("\n", "")
                                  .replace("\t", "").replace("e", "").strip())

            self.product_price = self.soup_search_ebay.find('span', attrs={'class': 'notranslate'}).text.strip()
            self.list_ebay.append(self.product_price.replace("\xa0", "").replace("\n", "").replace("US ", ""))

            self.product_ship_free = self.soup_search_ebay.find('table', attrs={'class': 'sh-tbl'})
            self.product_ship_free_ = self.product_ship_free.find('td').text.strip()
            self.list_ebay.append(self.product_ship_free_)

        # Turns list of data in small lists with 3 data


        def list_short(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        self.list_three = list(list_short(self.list_ebay, 3))
        print(f'Third site - Data Collected!')

        return self.list_three

    def data_frame_ebay(self):
        self.df_ebay = pd.DataFrame([self.list_three[0], self.list_three[1]],
                                    columns=["Product", "Price", "shipping"], index=['ebay.com', 'ebay.com'])

        return self.df_ebay

    def load_mages_amazon(self):
        self.add_image("frete_para", self.get_resource_abspath("frete_para.png"))

    def not_found(self, label):
        print(f"Element not found{label}")












