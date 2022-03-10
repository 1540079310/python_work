
import os
import re
from fake_useragent import UserAgent
import requests


#===============删除path路径下空文件夹====================
def deldir(path):
    # path = r"E:\兴趣\05-其他\05-其他\Picture\Still\柠檬"
    try:
        files = os.listdir(path)
        for file in files:
            if os.path.isdir(os.fspath(path + "/" + file)):
                if not os.listdir(os.fspath(os.fspath(path + "/" + file))):
                    os.rmdir(os.fspath(path + "/" + file))
                else:
                    deldir(os.fspath(path + "/" + file))
                    if not os.listdir(os.fspath(path + "/" + file)):
                        os.rmdir(os.fspath(path + "/" + file))
            elif os.path.isfile(os.fspath(path + "/" + file)) == 0:
                os.remeve(os.fspath(path + "/" + file))
        return
    except FileNotFoundError:
        print("文件夹路径错误")



#===============连接网站====================
def link(url):
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)
    return response.text


# ===============保存一页图片====================
def imgdown(path, urls_, dir_names):
    headers = {'User-Agent': UserAgent().random}
    for url_, dir_name in zip(urls_, dir_names):
        if not os.path.exists(path + './' + dir_name):
            os.mkdir(path + './' + dir_name)
            response = requests.get(url=url_, headers=headers)
            html = response.text
            # print(html)
            urls = re.findall('<img .*? src="(.*?).jpg" .*?>', html)
            print(urls)
            for url in urls:
                url = url + ".jpg"
                file_name = url.split('/')[-1]
                response = requests.get(url=url, headers=headers)
                with open(path + './' + dir_name + './' + file_name, mode='wb') as f:
                    f.write(response.content)
                    print('正在保存', file_name)
        else:
            print("{}已存在".format(dir_name))
    print("下载完成")
    deldir(path)


# ===============自动翻页保存图片====================
def imgsdown(homelink, path):
    if homelink:
        mainhtml = link(homelink)
        # print(mainhtml)
        urls_ = re.findall('<a href="(.*?)" rel=".*?">.*?</a>', mainhtml)
        dir_names = re.findall('<a href=".*?" rel="bookmark">(.*?)</a>', mainhtml)
        try:
            imgdown(path, urls_, dir_names)
            pagelink = re.findall('<a class="next page-numbers" href="(.*?)">', mainhtml)[-1]
            # print(pagelink)
            imgsdown(pagelink, path)
        except:
            print("全部下载完成")
    else:
        print("全部下载完成")


# ===============m3u8地址下载====================

# path = r"E:\兴趣\05-其他\05-其他\Movie\2022"
# url = re.findall('iframe src=".*?=(.*?)" ', html)[-1] #含m3u8的地址
# title = '视频名称'
def m3u8down(path, title, url):
    if not os.path.exists(path + './{}.mp4'.format(title)):
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url=url, headers=headers)
        html = response.text
        urllast = html.split('\n')[-1]
        url = url.rstrip('index.m3u8') + urllast
        # print(url)
        response = requests.get(url=url, headers=headers)
        content = response.text
        # print(content)
        tslists = re.findall('EXTINF:.*?,\n(.*?)\n#', content)
        for tslist in tslists:
            url = url.rstrip('index.m3u8') + tslist
            # print(url)
            response = requests.get(url=url, headers=headers)
            video = response.content
            url = url.rstrip(tslist) + 'index.m3u8'
            with open(path + './{}.mp4'.format(title), 'ab+') as f:
                f.write(video)
                print('{}下载完成....'.format(title))
    else:
        print('{}已存在....'.format(title))



def headerimport():
    pass


if __name__ == '__main__':
    path = input("请输入路径")
    deldir(path)