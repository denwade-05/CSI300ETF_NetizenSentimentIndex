import  requests
import  time
import  fake_useragent
from fake_useragent import UserAgent
import json
import re
import pandas as pd

ua = UserAgent()
headers = {'user-agent':ua.random}
data_list=[]

file = pd.read_excel("./沪深300成分股.xlsx")


#def get_symbol():


def get_comment(data):
    #data = json.load()
    pinglun_len = len(data["list"])
    i = 0
    print(pinglun_len)
    #data_list.clear()

    while i < pinglun_len:
        temp_data = data["list"][i]
        # url = base_url+temp_data["target"]
        pre = re.compile('>(.*?)<')
        text = ''.join(pre.findall(temp_data['text']))
        # text = temp_data['text']
        timeBefore = temp_data['timeBefore']
        data_list.append([text, timeBefore])
        #print(text , timeBefore)
        i += 1



# headers = {
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
# }

'''
https://xueqiu.com/query/v1/symbol/search/status?
u=271614261599941
&uuid=1364939774078627840
&count=10&comment=0
&symbol=SH601398
&hl=0
&source=all
&sort=time
&page=200
&q=
&type=11
&session_token=null
&access_token=62effc1d6e7ddef281d52c4ea32f6800ce2c7473
'''

url='https://xueqiu.com/query/v1/symbol/search/status'
for gupiao_index in range(0,300):
    print(format(file["股票代码"][gupiao_index],"06"),"START")
    data_list.clear()
    for i in range(1,101):
        params={
        "u": 271614261599941,
        "uuid": 1364939774078627840,
        "count": 20,
        "comment": 0,
        #"symbol": "SH601607",
        "symbol": "SH"+format(file["股票代码"][gupiao_index],"06"),
        "hl": 0,
        "source": "all",
        "sort": "time",
        "page": i,
        "q":"" ,
        "type": 11,
        "session_token":"null",
        "access_token": "62effc1d6e7ddef281d52c4ea32f6800ce2c7473"
        }
        # params = {
        #     "u": 331610870198814,
        #     "uuid": 1351437266307919872,
        #     "count": 100,
        #     "comment": 0,
        #     "symbol": "SH510300",
        #     "hl": 0,
        #     "source": "user",
        #     "sort": "time",
        #     "page": i,
        #     "q": "",
        #     "type": 13,
        #     "session_token": "null",
        #     "access_token": "176b14b3953a7c8a2ae4e4fae4c848decc03a883"
        # }

        #是否正常得到数据
        flag = 0
        #访问的次数
        times = 0
        while flag == 0:
            response = requests.get(url, params,headers=headers)
            temp = response.json()
            if 'code'  in temp:
                time.sleep(0.5)
            else:
                flag = 1
            times += 1
            #print(times)
        get_comment(temp)
        print("Page {} OK!".format(i))

    data_csv = pd.DataFrame(data_list)
    data_csv.to_csv("./data_沪深300/{}_data_{}.csv".format(gupiao_index,params["symbol"]),encoding="utf_8_sig",index=False)
    print(format(file["股票代码"][gupiao_index], "06"), "END")
    # 保存
    #data = [1, 2, 3]
    # with open('./data_json_gongshang/data{}.json'.format(i), 'w+') as pf:
    #     json.dump(temp, pf)
    # print("json {} OK!".format(i))

    # # 读取
    # with open('data.json', 'r') as sf:
    #     data = json.load(sf)

    # print(temp)
    # print(times)
