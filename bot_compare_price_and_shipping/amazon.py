from botcity.web import WebBot, Browser
import pandas as pd
import requests
import re


class InitDataAndBrowser(WebBot):

    def __init__(self, product_search, par_filter, *args):  # Data fecth
        super().__init__(self)
        self._driver_path = "./chromedriver.exe"
        self._headless = False
        self.product_search = product_search
        self.par_filter = par_filter
        self.zip_code = args

    def open_brws(self, url):
        self.wait(2000)
        self.url = url
        res = requests.get(self.url)
        print(res)
        try:
            if res.status_code == 200 or 503:
                print("The server is available, let's the browse.")
                self.browse(self.url)
                self.maximize_window()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

class BotAmazon(InitDataAndBrowser):

    def generate_link(self):   # Genertaes link with search data
        self.base_url = 'https://www.amazon.com/'

        self.url_amazon = ("https://www.amazon.com/s?k=cell+phone+" + self.product_search.replace(" ", "+")
                           + "&rh=n%3A7072561011&dc&qid=1637622313&refresh=1&rnid=2941120011&ref=sr_nr_n_1")

        return self.open_brws(self.url_amazon)

    def input_zip_code(self):
        self.find("click_zip_code")
        self.click_relative(156, 5, clicks=1)
        self.wait(2000)
        self.tab()
        self.tab()

        self.paste(self.zip_code)
        self.tab()
        self.enter()
        self.wait(1000)
        self.enter()
        self.wait(2000)

    def collect_infos_amazon(self):
        self.page_source()
        self.soup = self.page_source()

        # find for product boxes
        self.product_list_amazon = self.soup.find_all('div', attrs={
            'class': 'a-section a-spacing-medium'})

        self.list_amazon = []
        self.product_link_amazon = []

        # for each product box found, collect link and after concatenate with base link
        for item in self.product_list_amazon[1:2]:
            for link in item.find_all('a', attrs={'class': 'a-link-normal s-no-outline'}):
                self.product_link_amazon.append(self.base_url + link['href'])

        # open link concatenate, extract this information and append in list
        for links in self.product_link_amazon[0:2]:
            self.browse(links)
            self.page_source()
            self.soup_search = self.page_source()

            self.product_name = self.soup_search.find('h1', attrs={'class': 'a-size-large a-spacing-none'}).text.strip()

            if self.par_filter in self.product_name:

                product_name = self.soup_search.find('h1', attrs={'class': 'a-size-large a-spacing-none'}).text.strip()
                self.list_amazon.append(product_name)

                product_price = self.soup_search.find('span',
                                                      attrs={'class': 'a-offscreen'}).text.strip()

                self.list_amazon.append(product_price)

                self.search_ship = self.soup_search.find("p")

                self.control_a()
                self.wait(1000)
                self.control_c()
                search_ship_amazon = self.get_clipboard()

                self.list_amazon.append(search_ship_amazon[search_ship_amazon.find("FREE d"):
                                                           search_ship_amazon.find("FREE d") + 13])

            else:
                continue

        # Turns list of data in small lists with 3 data
        def list_short(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        self.list_one = list(list_short(self.list_amazon, 3))

        print(f'First site - Data Collected!')
        self.stop_browser()

        return self.list_one

    def data_frame_amazon(self):
        self.df_amazon = pd.DataFrame([self.list_one[0], self.list_one[1]],
                                      columns=["Product", "Price", "shipping"], index=['Amazon.com', 'Amazon.com'])

        return self.df_amazon

    def not_found(self, label):
        print(f"Element not found{label}")

    def load_images_amazon(self):
        self.add_image("click_zip_code", self.get_resource_abspath("click_zip_code.png"))

