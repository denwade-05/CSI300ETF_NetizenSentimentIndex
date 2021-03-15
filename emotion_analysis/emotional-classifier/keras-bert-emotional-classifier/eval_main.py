# -*- coding: utf-8 -*-

from dataset import tokenizer
from models import model
import settings
import codecs
import xlrd
import xlwt
import pandas as pd
import numpy as np
from datetime import datetime
from xlrd import xldate_as_tuple
from dateutil.parser import parse



# 加载训练好的参数
model.load_weights(settings.BEST_WEIGHTS_PATH)

#输出单个结果
def judgeEmotion(comment):
    sentence = comment
    token_ids, segment_ids = tokenizer.encode(sentence)
    output = model.predict([[token_ids, ], [segment_ids, ]])[0][0]
    if output > 0.5:
        ret = 1
    else:
        ret = -1
    return ret

#读取文件、输出所有结果
def count_emotion():
    #读取
    worksheet = xlrd.open_workbook(r'E:\neuralnetwork\NLP\keras-bert-emotional-classifier\RandomRemark.xlsx')
    sheet_names = worksheet.sheet_names()
    for sheet_name in sheet_names:
        sheet = worksheet.sheet_by_name(sheet_name)
        rows = sheet.nrows  # 获取行数
    #新建表格
    new_workbook = xlwt.Workbook(encoding= 'etf-8')
    new_worksheet = new_workbook.add_sheet('sheet1')
    new_worksheet.write(0,0, 'date')
    new_worksheet.write(0,1, 'positive')
    new_worksheet.write(0,2, 'negative')
    positive = 0
    negative = 0
    j = 1
    indx = 0
    for i in range(j,rows):
        indx = indx + 1
        comment = (sheet.cell(i, 0).value)
        comment = str(comment)
        if len(comment)>=100:
            indx = indx - 1
            continue
        score = judgeEmotion(comment)
        #读取date
        cell_value = sheet.cell(i, 1).value
        date = datetime(*xldate_as_tuple(cell_value, 0))
        cell_value = date.strftime('%Y/%m/%d %H:%M:%S')
        #写入
        new_worksheet.write(indx,0,cell_value)
        if score > 0:
            positive = positive + 1
            new_worksheet.write(indx, 1, 1)
            new_worksheet.write(indx, 2, 0)
        elif score < 0:
            negative = negative + 1
            new_worksheet.write(indx, 1, 0)
            new_worksheet.write(indx, 2, 1)
        print('positive:', positive)
        print('negative:', negative)
        print('total:', indx)
        new_workbook.save(r'E:\keras-bert-emotional-classifier\result.xls')
if __name__ == '__main__':
    count_emotion()


