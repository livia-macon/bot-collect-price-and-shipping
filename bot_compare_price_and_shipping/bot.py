from botcity.web import WebBot, Browser
from bot_compare_price_and_shipping.amazon import BotAmazon
from bot_compare_price_and_shipping.bestbuy import BotBestBuy
from bot_compare_price_and_shipping.ebay import BotEbay
from bot_compare_price_and_shipping.amazon import InitDataAndBrowser
import pandas as pd


class Bot(WebBot):
    def action(self, execution=None):

        # Go Amazon.com
        self.search_amazon = BotAmazon('Samsung galaxy z fold 3', 'Fold 3', '32789')
        self.search_amazon.generate_link()
        self.search_amazon.input_zip_code()
        list_one = self.search_amazon.collect_infos_amazon()
        df_amazon = self.search_amazon.data_frame_amazon()
        # print(df_amazon)

        # Go BestBuy.com
        self.search_bestbuy = BotBestBuy("Samsung galaxy z fold 3 unlocked", "none",  "32789")
        self.search_bestbuy.generate_link_bestbuy()
        self.search_bestbuy.input_zip_code_bestbuy()
        list_two = self.search_bestbuy.collect_infos_bestbuy()
        df_bestbuy= self.search_bestbuy.data_frame_bestbuy()
        # print(df_bestbuy)

        # Go Ebay.com
        self.search_ebay = BotEbay("Samsung galaxy z fold 3", "none", "32789")
        self.search_ebay.generate_link_ebay()
        self.search_ebay.input_zip_code_ebay()
        list_three = self.search_ebay.collect_infos_ebay()
        df_ebay = self.search_ebay.data_frame_ebay()
        # print(df_ebay)

        self.df_all_info = pd.concat([df_amazon, df_bestbuy, df_ebay])
        print(self.df_all_info)

        self.df_all_info.to_excel("data_collect.xlsx", index=True)



if __name__ == '__main__':
    Bot.main()
