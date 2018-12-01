#coding:utf-8

import json
import requests
from bs4 import BeautifulSoup


class Tencent(object):
    def __init__(self):
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.base_url = "https://hr.tencent.com/position.php?&start="
        self.page = 0
        self.item_list = []

    def send_request(self, url):
        """
            发送请求，返回响应
        """
        html = requests.get(url, headers = self.headers).content
        return html

    def parse_page(self, html):
        """
            解析每个职位列表页，获取10条职位信息并保存在item中
            最后存储在列表中
        """
        soup = BeautifulSoup(html, "lxml")
        node_list = soup.select(".even, .odd")

        # 每次迭代表示一条职位信息，同时构建一个item字典存储职位信息
        for node in node_list:
            item = {}
            # 职位名称
            item["position_name"] = node.select("td")[0].a.get_text()
            # 职位链接
            item["position_link"] = u"https://hr.tencent.com/" + node.select("td")[0].a.get("href")

            item["position_type"] = node.select("td")[1].get_text()

            # 招聘人数
            item["people_number"] = node.select("td")[2].get_text()
            # 工作地点
            item["work_location"] = node.select("td")[3].get_text()
            #  发布时间
            item["publish_times"] = node.select("td")[4].get_text()

            self.save_item(item)


    def save_item(self, item):

        json.dump(item, open("tencent.json", "a"))

    def main(self):
        while self.page <= 20:
            full_url = self.base_url + str(self.page)
            html = self.send_request(full_url)
            self.parse_page(html)
            self.page += 10

if __name__ == "__main__":
    spider = Tencent()
    spider.main()
