from botcity.web.browsers.chrome import default_options
from botcity.web import WebBot, Browser
from bot_compare_price_and_shipping.amazon import InitDataAndBrowser
import pandas as pd
import requests

class BotBestBuy(InitDataAndBrowser):

    def generate_link_bestbuy(self):        # Genertaes link with search data
        self.base_url_bestbuy = 'https://www.bestbuy.com/'

        self.url_bestbuy = ("https://www.bestbuy.com/site/searchpage.jsp?st=cell+phone+" + self.product_search.replace(
            " ",
            "+") + "&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true"
                   "&iht=y&usc=All+Categories&ks=960&keys=keys")

        return self.open_brws(self.url_bestbuy)


    def input_zip_code_bestbuy(self):
        # change USA Bestbuy page
        if not self.find_text("usa", threshold=230, waiting_time=10000):
            self.not_found("usa")

        self.click()
        self.click()
        self.key_esc()
        self.scroll_down(1)

        # input zip code collect ship
        if not self.find_text("zip_code", threshold=230, waiting_time=10000):
            self.not_found("zip_code")
        self.click()

    def collect_infos_bestbuy(self):
        self.enter()
        self.wait(2000)
        self.paste(self.zip_code)
        self.enter()
        self.wait(2000)
        self.page_source()

        self.soup_bestbuy = self.page_source()
        self.product_link = []

        # find for product boxes
        self.product_list_bestbuy = self.soup_bestbuy.find_all('li', attrs={'class': 'sku-item'})

        self.product_link = []

        # for each product box found, collect link and after concatenate with base link
        for item in self.product_list_bestbuy[0:2]:
            for link in item.find_all('a', attrs={'class': 'image-link'}):
                self.product_link.append(self.base_url_bestbuy + link['href'])

        self.list_bestbuy = []

        # open link concatenate, extract this information and append in list
        for link in self.product_link:
            self.browse(link)
            self.page_source()
            self.soup_search = self.page_source()


            self.product_name = self.soup_search.find('h1', attrs={'class': 'heading-5 v-fw-regular'}).text.strip()
            self.list_bestbuy.append(self.product_name)
            self.product_price = self.soup_search.find('div', attrs={
                'class': 'priceView-hero-price priceView-customer-price'}).text.strip()
            self.list_bestbuy.append(f"$ {self.product_price[1:7]}")

            self.control_a()
            self.wait(1000)
            self.control_c()
            search_ship_bestbuy = self.get_clipboard()

            self.list_bestbuy.append(search_ship_bestbuy[search_ship_bestbuy.find("FREE"):
                                                         search_ship_bestbuy.find("FREE") + 13])

        print(f'Second site - Data Collected!')
        self.stop_browser()

        # Turns list of data in small lists with 3 data
        def list_short(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
            # print(lst)

        self.list_two = list(list_short(self.list_bestbuy, 3))

        return self.list_two

    def data_frame_bestbuy(self):
        self.df_bestbuy = pd.DataFrame([self.list_two[0], self.list_two[1]],
                                       columns=["Product", "Price", "shipping"], index=['bestbuy.com', 'bestbuy.com'])

        return self.df_bestbuy

    def not_found(self, label):
        print(f"Element not found{label}")

    def load_mages_amazon(self):
        self.add_image("usa", self.get_resource_abspath("usa.png"))
        self.add_image("zip_code", self.get_resource_abspath("zip_code.png"))
