# -*-coding:utf-8 -*-
import urllib2
import re


class Neihanspider:
    """
    用于爬取内涵段子的
    """
    def __init__(self):
        """
        构造函数，用于初始化数据
        """
        # 爬取的页面的页数
        self.page = 1

        # 用于控制是否爬取的
        self.work = True

        # 写入文件的记录数
        self.count = 0

    def loadpage(self, page):
        """
        爬取网页信息
        :param page:
        :return: item_list:爬取的页面
        """
        print("-" * 10 + "正在爬取第%d页" % self.page + "-" * 10)
        # 构造要爬取的页面的url
        url = "http://www.neihanpa.com/article/list_5_"+str(self.page)+".html"

        # 构造User_agent伪装成浏览器
        ua_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)  Chrome/49.0.2623.221"}

        # url ua_headers作为Request()方法的参数，构造并返回一个Request对象
        request = urllib2.Request(url, headers=ua_headers)

        # 添加额外的headers
        request.add_header("Connection", "keep-alive")

        # Request对象作为urlopen()方法的参数，发送给服务器并接收响应
        response = urllib2.urlopen(request)

        # 获取服务器返回的页面内容
        gbk_html = response.read().decode("gbk").encode("utf-8")
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        item_list = pattern.findall(gbk_html)
        return item_list

    def dealpage(self, item_list):
        """
        去除页面无用信息
        调用写入函数
        """
        print("-" * 10 + "正在写入第%d页" % self.page + "-" * 10)
        for item in item_list:
            cont = item.replace("<br />", "").replace("<br>", "").replace("&ldquo;", "\"").replace("&rdquo;", "\"")
            cont = cont.replace("&hellip;", " ").replace("&nbsp;", "").replace("&rsquo;", "").replace("&lsquo;", "")
            cont = cont.replace("mdash;", "")
            cont = cont.replace("<p>", "").replace("</p>", "").replace("\t", "").replace("  ", "").replace("&quot;", "")

            self.count += 1
            self.writeout(cont, self.count)
        print("-" * 10 + "第%d页写入完成" % self.page + "-" * 10)

    def writeout(self, cont, count):
        """
        :param cont: 写入内容
        :param count: 写入的记录条数
        """
        with open("./内涵段子.txt".decode("utf-8"), "a+") as f:
            f.write(cont)
            print("-" * 10 + "正在写入第%d条" % count)

    def start(self):
        while True:
            try:
                itme_list = self.loadpage(self.page)
            except urllib2.URLError, e:
                print e.reason
                continue
            self.dealpage(itme_list)

            if self.work:
                self.page += 1
            # 默认爬取前20页
            if self.page >20:
                print "按回车继续..."
                print "输入 quit 退出"
                command = raw_input()
                if command == "quit" :
                    self.work = False
                    break


if __name__ == "__main__":
    spid = Neihanspider()
    spid.start()

