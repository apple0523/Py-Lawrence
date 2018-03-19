import re
import time
import random
import urllib.request
import urllib.error


# 爬取单个网页,默认不使用代理服务器
def use_proxy(url, timeout, proxy_addr=False):
    try:
        if proxy_addr == False:
            data = urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8')
        else:
            proxy = urllib.request.ProxyHandler({"http": proxy_addr})
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
            data = urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8')
        return data
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code())
        if hasattr(e, 'reason'):
            print(e.reason())
        time.sleep(10)
    except Exception as e:
        print('except:' + str(e))
        time.sleep(1)

    # 获取所有文章的链接,若使用代理则需要proxy参数


def get_link_list(key, pagestart, pageend, proxy=False):
    headers = ("User-Agent", "XXXXX")  # 可以使用F12,刷新网页后查看Network-->Headers,找到User-Agent替换XXXXX
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    # 设为全局opener
    urllib.request.install_opener(opener)
    link_lists = []
    try:
        keycode = urllib.request.quote(key)
        # 开始爬取关键词对应的页面文章链接
        for i in range(pagestart, pageend + 1):
            html = "http://weixin.sogou.com/weixin?type=2&query=" + keycode + '&page=' + str(i)
            timeout = random.choice(range(80, 180))
            data1 = use_proxy(html, timeout, proxy)
            pattern = '<div class="txt-box">.*?(http://.*?)"'
            linklist = re.findall(pattern, data1, re.S)
            for j in range(len(linklist)):
                list_dict = {}
                tmp = linklist[j].replace('amp;', '')
                list_dict['page'] = i
                list_dict['link'] = tmp
                link_lists.append(list_dict)
                print("收到第 %d 页, 第 %d 条文章链接" % (i, j))
        return link_lists
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code())
        if hasattr(e, 'reason'):
            print(e.reason())
        time.sleep(10)
    except Exception as e:
        print('except:' + str(e))
        time.sleep(2)

    # 将对应的微信链接中的所有文章取出来，写成html形式,写入filepath下


def get_content(listurl, filepath, proxy=False):
    try:
        # 设置本地文件的起始html
        html1 = '''''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
    <html xmlns="http://www.w3.org/1999/xhtml"> 
    <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
    <title>微信文章页面</title> 
    </head> 
    <body> 
    '''
        # 设置本地文件的结束html
        html2 = '''''</body> 
    </html> 
    '''
        timeout = random.choice(range(80, 180))
        for i in range(len(listurl)):
            tmp_url = link_list[1]['link']
            data1 = use_proxy(tmp_url, timeout, proxy)
            # 获取文章标题
            title_pat = "<title>(.*?)</title>"
            title = re.findall(title_pat, data1)[0]
            # 获取文章内容
            content_pat = 'id="js_content">(.*?)id="js_sg_bar">'
            content = re.findall(content_pat, data1, re.S)[0]
            # 设置文章初始内容
            thistitle = '此次没有找到标题'
            thiscontent = '此次没有找到内容'
            if (title != ''):
                thistitle = title
            if (content != ''):
                thiscontent = content
            article_name = filepath + '/' + str(i) + '.html'
            # 写入起始内容
            fh = open(article_name, 'wb')
            fh.write(html1.encode('utf-8'))
            fh.close()
            data_all = "<p>标题为：" + thistitle + "</p><p>内容为：" + thiscontent + "</p><br>"
            # 写入文章内容
            fh = open(article_name, 'ab')
            fh.write(data_all.encode('utf-8'))
            fh.close()
            # 写入结束
            fh = open(article_name, 'ab')
            fh.write(html2.encode('utf-8'))
            fh.close()
            print("第 %d 篇文章收下..." % i)
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code())
        if hasattr(e, 'reason'):
            print(e.reason())
        time.sleep(10)
    except Exception as e:
        print('except:' + str(e))
        time.sleep(2)

    # %%测试代码


key = '乌镇饭局'
link_list = get_link_list(key, 0, 3)
get_content(link_list, 'weixin_articles')

# %%
''''' 
使用方法： 
1.设置要搜索的关键词 key 
2.使用函数get_link_list()获取相应的链接，设置好pagestart,pageend 
3.使用get_content()获取相应的文章并保存到本地 
'''
# %%
''''' 
函数use_proxy():爬取单个网页,默认不使用代理服务器 
参数说明: 
proxy_addr : 传入的代理服务器地址 
url : 爬取的网页 
timeout : 网络最长允许延时时间 

函数get_link_list():获取页面中所有文章的链接 
参数说明: 
key : 关键词,输入字符串，中/英文 
pagestart : 爬取的文章开始页 
pageend : 爬取的文章结束页 
proxy : 代理IP，默认不使用代理服务器 

函数get_content():将对应的微信链接中的所有文章取出来，写成html形式,写入filepath下 
参数说明: 
listurl : 是由get_link_list()函数得到的链接列表 
filepath : 是写成html后存入的目录 
proxy : 代理IP，默认不使用代理 
'''
# %% 微信文章抓取
# 为了应对URL异常，需要增加sleep,可以使用代理服务器