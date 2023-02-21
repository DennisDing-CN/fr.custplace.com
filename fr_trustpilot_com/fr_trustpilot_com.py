import random
import re
import threading
import time
import httpx
from parsel import Selector
import execjs


PROXY_LIST = ["http://104.223.212.10:65432", "http://104.223.212.101:65432", "http://104.223.212.104:65432"]


def do_request(url, add_header=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    if add_header:
        headers.update(add_header)
    for i in range(3):
        try:
            res = httpx.get(url, headers=headers, timeout=10, proxies=random.choice(PROXY_LIST), follow_redirects=True)
        except Exception as e:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            error_msg = f"timeout {i+1} times\n"
            log_msg = f"{current_time} [ERROR] Request {url} {error_msg} 错误:{e}"
            print(log_msg, end='', sep='')
            # logging.log(msg=log_msg, level=logging.INFO)
        else:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if res.status_code == 200 or res.status_code == 404:
                log_msg = f"{current_time} {res.request.method} {url} {res.status_code} OK\n"
                print(log_msg, end='', sep='')
                # logging.log(msg=log_msg, level=logging.INFO)
                return res
            else:
                error_msg = f"{res.status_code} fail {i+1} times\n"
                log_msg = f"{current_time} [ERROR] {res.request.method} {url} {error_msg}"
                print(log_msg, end='', sep='')
                # logging.log(msg=log_msg, level=logging.INFO)
    return None


q = ['https://fr.custplace.com/Zoomici','https://fr.custplace.com/Zooplus','https://fr.custplace.com/Zonealarm','https://fr.custplace.com/Zodio','https://fr.custplace.com/zeturf','https://fr.custplace.com/ZENSE','https://fr.custplace.com/Zepass','https://fr.custplace.com/Zattoo','https://fr.custplace.com/Zara']

def main():
    with open('fr_trustpilot_com.js', 'r', encoding='utf-8') as f:
        line = f.read()
        js_ = execjs.compile(line)
    while True:
        if not q:
            break
        url = q.pop()
        res = do_request(url)
        if res:
            html = Selector(res.text)
            introduce_content = re.sub('\n', '', ''.join(html.xpath('//div[@class="bg-white rounded shadow-lt  pt-4 pb-5 px-5 leading-relaxed block"]//text()').getall()))
            telephone = re.sub('\n', '', ''.join(html.xpath("//svg/path[@d='M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z']/../..//text()").getall()))
            email = re.sub('\n', '', ''.join(html.xpath("//svg/path[@d='M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z']/../../@href").getall()))
            if 'email-protection' in email:
                new_email = 'https://fr.custplace.com' + email
                email = str(js_.call('n', new_email, 52))
            else:
                email = ''
            meta = {
                "url": url,
                "email": email,
                "telephone": telephone,
                "introduce_content": introduce_content,
            }
            print(meta)


def run_thead(name, count, *args):
    thread_list = []
    for i in range(count):
        th = threading.Thread(target=name, args=args)
        th.start()
        thread_list.append(th)
    for thread in thread_list:
        thread.join()


run_thead(main, 20)