#!/usr/local/bin/python3
# coding=utf-8

##http://www.nmc.cn/f/rest/real/58367

import time, json
import urllib.request
import requests
import sched
import datetime
from io import BytesIO
import gzip
import re

cityList = [
    {'code': "58367", 'name': "上海", 'citykey': "101020100"},
    {'code': "58354", 'name': "无锡", 'citykey': "101190201"},
    {'code': "58249", 'name': "泰兴", 'citykey': "101191203"}
]

###添加头部，伪装浏览器
##headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
###Request类的实例，构造时需要传入Url,Data，headers等等的内容
##resquest = urllib.request.Request(url=url, headers=headers)
##response = urllib.request.urlopen(resquest).read()

# 模拟成浏览器
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gbk,utf-8,gb2312",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "User-Agent": "Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Connection": "keep-alive"}
opener = urllib.request.build_opener()
headall = []
for key, value in headers.items():
    item = (key, value)
    headall.append(item)
opener.addheaders = headall

# 将opener安装为全局
urllib.request.install_opener(opener)


# 返回dict类型: twitter = {'image': imgPath, 'message': content}
def getCityWeather_RealTime(cityID):
    url = "http://www.nmc.cn/f/rest/real/" + str(cityID)
    try:
        stdout = urllib.request.urlopen(url)
        weatherInfomation = stdout.read().decode('utf-8')
        jsonDatas = json.loads(weatherInfomation)

        city = jsonDatas["station"]["city"]
        tq = jsonDatas["weather"]["info"]
        temp = jsonDatas["weather"]["temperature"]
        fx = jsonDatas["wind"]["direct"]  # 风向
        fl = jsonDatas["wind"]["speed"]  # 风力
        sd = jsonDatas["weather"]["humidity"]  # 相对湿度
        tm = jsonDatas["publish_time"]

        content = city + ":" + str(tq) + ",当前温度:" + str(temp) + "℃," + str(fx) + ",风速:" + str(fl) + "m/s,相对湿度:" + str(
            sd) + "%." + "发布时间:" + str(tm)
        twitter = {'image': "", 'message': content}

    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None


# 返回dict类型: twitter = {'image': imgPath, 'message': content}
def getCityWeather_AllDay(cityID):
    url = "http://wthrcdn.etouch.cn/weather_mini?citykey=" + str(cityID)
    try:
        stdout = urllib.request.urlopen(url)
        buff = BytesIO(stdout.read())  # 把bytes content转为文件对象
        weatherInfomation = gzip.GzipFile(fileobj=buff).read().decode('utf-8')
        jsonDatas = json.loads(weatherInfomation)

        city = jsonDatas["data"]["city"]
        jsonForecastDatas = jsonDatas["data"]["forecast"]
        ganmao = jsonDatas["data"]["ganmao"]

        content = city + "\n"
        for tqData in jsonForecastDatas:
            fcDate = tqData["date"]
            temp1 = tqData["high"]
            temp2 = tqData["low"]
            fengli = tqData["fengli"]
            fengxiang = tqData["fengxiang"]
            tqType = tqData["type"]

            fl = fengli[9: fengli.index(']')].strip()
            temp1 = temp1[3:].strip()
            temp2 = temp2[3:].strip()
            tqType = tqType.ljust(2)

            content = content + fcDate + "," + tqType + "," + fengxiang + fl + ",温度:" + temp2 + "~" + temp1 + "\n"

        content = content + ganmao + "\n"
        twitter = {'image': "", 'message': content}

    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except (Exception) as e:
        print(">>>>>> OtherError: " + e.args)
    else:
        return twitter
    finally:
        None


def GetWeather1():
    messageStr = "\n"
    for city in cityList:
        title_small = "【实时】"
        twitter = getCityWeather_RealTime(city['code'])
        messageStr = messageStr + title_small + twitter['message'] + '\n'
        messageStr = messageStr + '\n'
        # print(messageStr)

    return messageStr


def GetWeather2():
    messageStr = "\n"
    for city in cityList:
        title_small = "【预测】"
        twitter = getCityWeather_AllDay(city['citykey'])
        messageStr = messageStr + title_small + twitter['message'] + '\n'
        messageStr = messageStr + '\n'
        # print(messageStr)

    return messageStr


def timerFun(sched_Timer):
    while True:
        now = datetime.datetime.now()
        if now.minute == sched_Timer.tm_min:
            SendMessageToWechat(GetWeather1())
            time.sleep(70)

        if now.hour == 7 and now.minute == 5:
            SendMessageToWechat(GetWeather2())
            time.sleep(70)


def SendMessageToWechat(weatherInfo):
    title = "Lawrence 提示您: 注意天气变化保持健康心情\n"
    result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + weatherInfo
    content = 'text=' + title + '&' + 'desp=' + result
    url = "https://sc.ftqq.com/SCU19549Taf958199d61671fe598d76a4199cdb8d5a4ee749585cf.send?%s" % content
    r = requests.get(url)
    r.close()
    print(content)
    print(">>>>>> Send Over!")
    print(datetime.datetime.now())


if __name__ == '__main__':
    sched_Timer = time.strptime("2018-1-10 7:30:00", "%Y-%m-%d %H:%M:%S")
    mes = "Start collecting weather information at:" + time.strftime("%Y-%m-%d %H:%M:%S", sched_Timer)
    print(mes)
    timerFun(sched_Timer)
##    SendMessageToWechat()
