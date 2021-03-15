import jieba
import numpy as np
import pandas as pd
import re
import time
import os
import tqdm

#获取词典
def get_dict():
    Neg_words = pd.read_csv('MC词典.csv',encoding='utf-8')['Neg'].values.tolist()
    Pos_words = pd.read_csv('MC词典.csv',encoding='utf-8')['Pos'].values.tolist()
    Foudingci = pd.read_csv('MC词典.csv',encoding='utf-8')['Foudingci'].values.tolist()
    return Neg_words,Pos_words,Foudingci
#创建停用词词典
def stopwordslist():
    Stop_words = [line.strip() for line in open('stopwordslist.txt',encoding="utf-8").readlines()]
    return Stop_words
#分词和去除停用词
def seg_depart(text):
    global Stop_words
    text_depart = jieba.cut(text)
    
    outstr = []
    for word in text_depart:
        if word not in Stop_words:#过滤停用词
            if re.findall(r'(\d+)(.*)(\d*)(.*)',word)==[]:#去除数字
                outstr.append(word)

    # with open("words.txt","w") as f:
    #     for i in outstr:
    #         f.write(i+" ")
    return outstr

def sentiment(df):
    start = time.perf_counter()
    global Neg_words,Pos_words,Foudingci
    global Neg_list,Pos_list
    # Neg_wordslist = []
    # Pos_wordslist = []
    tone1 = 0
    tone2 = 0
    comment = list(df['comment'])

    for k in range(len(comment)):
        outstr = seg_depart(comment[k])
        Neg = 0#计数
        Pos = 0
        for i in range(len(outstr)):
            if (outstr[i] in Neg_words):
                Neg_list.append(outstr[i])
                if i>=3:
                    if (outstr[i-1] in Foudingci) or (outstr[i-2] in Foudingci) or (outstr[i-3] in Foudingci):
                        Pos += 1
                        # Pos_wordslist.append(outstr[i-3]+outstr[i-2]+outstr[i-1]+outstr[i])
                    else:
                        Neg += 1
                        # Neg_wordslist.append(outstr[i])
                else:                    
                    Neg += 1
                    # Neg_wordslist.append(outstr[i])

            if outstr[i] in Pos_words:
                Pos_list.append(outstr[i])
                if i>=3:
                    if (outstr[i-1] in Foudingci) or (outstr[i-2] in Foudingci) or (outstr[i-3] in Foudingci):
                        Neg += 1
                        # Neg_wordslist.append(outstr[i-3]+outstr[i-2]+outstr[i-1]+outstr[i])
                    else:
                        Pos += 1
                        # Pos_wordslist.append(outstr[i])
                else:
                    Pos += 1
                    # Pos_wordslist.append(outstr[i])
        if not((Pos == 0) and (Neg == 0)):
            tone1 += (Pos-Neg)/(len(outstr))
            tone2 += (Pos-Neg)/(Neg+Pos)
        # print("Negative words num:",Neg)
        # print("Positive words num:",Pos)
        # print("Total words num:",len(outstr))
        # print(outstr)
        # print(Neg_wordslist)
        # print(Pos_wordslist)
        # print(tone1,tone2)
    tone1 = tone1/len(df)
    tone2 = tone2/len(df)
    result = pd.DataFrame({'date':list(df['date'])[0],'tone1':tone1,'tone2':tone2},pd.Index(range(1)))
    end = time.perf_counter()

    text = list(df['date'])[0]+','+str(tone1)+','+str(tone2)
    # with open('result.txt',"a") as file:
    #     file.write(text+'\n')

    print(list(df['date'])[0],'运行时间：',end-start,'s')
    return result

def f(df):
    print(df)
    print(list(df['date'])[0])

def main():
    global Neg_words,Pos_words,Stop_words,Foudingci
    global Neg_list,Pos_list
    Neg_words,Pos_words,Foudingci = get_dict()
    Stop_words = stopwordslist()
    Neg_list = []
    Pos_list = []
    comment = pd.read_csv('RandomRemark.csv', encoding='utf-8')

    result = comment.groupby('date').apply(sentiment)
    result.to_csv('result.csv')
    # sentiment(list(result)[69][1])
    count = pd.DataFrame({'统计消极词':Neg_list})
    count['统计消极词'].value_counts().to_csv('统计消极词.csv',encoding = 'utf-8-sig')
    count = pd.DataFrame({'统计积极词':Pos_list})
    count['统计积极词'].value_counts().to_csv('统计积极词.csv',encoding = 'utf-8-sig')
    
main()