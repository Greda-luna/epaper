import random
from lxml import etree
import time
import csv
import requests
base_url = 'http://szb.fxrbs.cn:81/fxrb/html/2018-'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'Cookie':'_d_id=4cbb1c6968b3aed3da6b1065782e42; __51cke__=; __tins__123=%7B%22sid%22%3A%201711935228766%2C%20%22vd%22%3A%2034%2C%20%22expires%22%3A%201711937793642%7D; __51laig__=34'
}
file_name = '辽宁_阜新_日报_2018-01-01_2018-12-31.csv'
file_head = ['id','标题','成文日期','来源','url源地址','内容']

for month in range(8,9):
    month = "{:02d}".format(month)
    for day in range(7,32):
        day = "{:02d}".format(day)
        for node in range(1,9):
            url = base_url+month+'/'+day+'/'+'node_'+str(node)+'.htm'
            time.sleep(2)
            response = requests.get(url,headers=headers)
            if response.status_code==404:
                break
            else:
                tree = etree.HTML(response.text)
                content_link = tree.xpath('//ul[@class="ul02_l"]//a/@href')
                for i in range(len(content_link)):
                    content_url = base_url+month+'/'+day+'/' + content_link[i]
                    time.sleep(1)
                    response = requests.get(content_url, headers=headers)
                    response.encoding = response.apparent_encoding
                    tree = etree.HTML(response.text)
                    title = "".join(tree.xpath('//td[@class="font01"]/text()'))
                    content_detail = "".join(tree.xpath('//div[@id="ozoom"]//text()')).replace('\xa0', '').replace('\r',
                                                                                                                   '').replace(
                        '\n', '')
                    id = str(154)
                    time_end = str(2018)+'/'+month+'/'+day
                    source = '阜新日报'
                    current_url = content_url
                    content_list = []
                    # extend函数将多个字符串放入一个列表中
                    content_list.extend([id, title, time_end, source, current_url, content_detail])
                    # 保存数据
                    with open(file_name, 'a', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(content_list)
                    print('保存了一个数据')
            print('保存了' + month +'/'+day + '/' + str(node) + '的数据')






