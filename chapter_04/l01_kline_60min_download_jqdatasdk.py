# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2018-2020 azai/Rgveda/GolemQuant
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
聚宽小时线(60分钟线)数据下载，范围精选白马蓝筹股，下载到当前目录 \datastore\kline\stock\ 下
需开通聚宽本地数据接口，文档：https://www.joinquant.com/help/api/help?name=JQData
申请地址: https://www.joinquant.com/default/index/sdk#jq-sdk-apply
"""

import os
import datetime
import pandas as pd
import numpy as np
import time

from jqdatasdk import (
    auth,
    is_auth,
    get_query_count,
    api as jqapi,
)
from GolemQ.utils.path import (
    mkdirs,
    export_metadata_to_pickle,
    import_metadata_from_pickle,
)
from GolemQ.utils.settings import (
    exists_settings,
    input_settings,
    load_settings,
    save_settings,
)
try:
    import QUANTAXIS as QA
except:
    print('PLEASE run "pip install QUANTAXIS" to call these modules')
    pass

if __name__ == '__main__':
    # 定义保存云端量化数据源用户名密码的的 pd.DataFrame 结构
    password = pd.DataFrame({'host':['jqdatasdk'],
                             'username':[None],
                             'password':[None]}, 
                            columns=['host',
                                     'username',
                                     'password'])

    # 将用户密码token等信息保存到系统的当前用户目录 %userprofile%/.GolemQ 目录下面
    pwd_save_file = 'jqdatasdk_pwd.pickle'
    if (exists_settings(pwd_save_file)):
        password = load_settings(pwd_save_file)
    else:
        password = input_settings(pattern=password,
                                  filename=pwd_save_file,)   
        save_settings(pwd_save_file, password)

    #ID是申请时所填写的手机号；Password为聚宽官网登录密码，新申请用户默认为手机号后6位
    auth(password.username[0], 
         password.password[0])
    is_auth = is_auth()

    # 查询当日剩余可调用条数
    print(get_query_count())
    print(is_auth)

    indexlist = [ '000001.XSHG', '000002.XSHG', '000003.XSHG', '000004.XSHG',  
                  '000005.XSHG', '000006.XSHG', '000007.XSHG', '000009.XSHG',
                  '000009.XSHG', '000010.XSHG', '000015.XSHG', '000016.XSHG',  
                  '000036.XSHG', '000037.XSHG', '000038.XSHG', '000039.XSHG',  
                  '000040.XSHG', '000300.XSHG', '000112.XSHG', '000133.XSHG', 
                  '000903.XSHG', '000905.XSHG', '000906.XSHG', '000993.XSHG',
                  '000989.XSHG', '000990.XSHG', '000991.XSHG', '000992.XSHG', 
                  '399001', '399006', 
                  '513030', '399684', '159934', '512000', 
                  '159987', '399616', '510050', '513100', 
                  '510850', '518880', '510180', '159916', 
                  '512980', '512090', '515000', 
                  '510900', '512910', '513050', '510300', 
                  '399384', '510810', '399987', '159905', 
                  '399396', '399997', '159919', 
                  '159941', '159920', ]
    indexlist = jqapi.normalize_code(indexlist)
    code = indexlist[0]

    # 创建数据下载目录
    frequence = '60min'
    index_path = mkdirs(os.path.join(mkdirs('datastore'), 
                                     'kline', 'index', frequence))
    print(index_path)

    for year in range(2017, 2005, -1):
        start_date = '{}-01-01'.format(year)
        end_date = '{}-01-02'.format(year + 1)
        for asset in indexlist:
            print(asset, start_date, end_date,)
            indexfile = os.path.join(index_path, u'{}_{}_{}.pickle'.format(asset, 
                                                                           year, 
                                                                           frequence))
            if os.path.isfile(indexfile ):
                print('文件已经存在，跳过 ', indexfile)
                continue
            try:
                print(indexfile )
                his = jqapi.get_price(asset, start_date, end_date, frequency='60m')
                export_metadata_to_pickle(index_path, u'{}_{}'.format(asset, year), 
                                          metadata=his)
                #data_day = QA.QA_fetch_stock_min_adv(codelist,
                #    start='2019-01-01',
                #    end='2020-08-28',
                #    frequence='60min')
                #his = data_day.data
            except Exception as e:
                print(asset, e)
            time.sleep(1)


    for year in range(2017, 2005, -1):
        start_date = '{}-01-01'.format(year)
        end_date = '{}-01-02'.format(year + 1)
        for asset in indexlist:
            print(asset, start_date, end_date,)
            indexfile = os.path.join(index_path, u'{}_{}_{}.pickle'.format(asset, year, frequence))
            his = import_metadata_from_pickle(index_path, u'{}_{}'.format(asset, year))
            print(his.head(10))


    # 创建数据下载目录
    frequence = '60min'
    stock_path = mkdirs(os.path.join(mkdirs('datastore'), 'kline', 'stock', frequence))
    print(stock_path)

    stocklist = ['002230', '600900', '300560', '300146', 
                '002271', '603129', '002557', '002603', 
                '600161', '600477', '000661', '600519', 
                '603520', '002503', '000157', '002179', 
                '600585', '600298', '600104', '002594', 
                '603288', '300760', '300715', '002007', 
                '002258', '300433', '300059', '600612', 
                '603515', '603486', '002352', '300314', 
                '600332', '601138', '600522', '600031', 
                '600436', '603444', '601933', '601611', 
                '000876', '002714', '002415', '601558', 
                '603517', '000895', '603259', '002831', 
                '000333', '300498', '601100', '600030', 
                '600188', '600352', '600009', '002382', 
                '600887', '601888', '600309', '000858', 
                '002475', '603713', '300750', '002050', 
                '600547', '600660', '600570', '603899', 
                '002705', '300015', '601877', '000568', 
                '600486', '300144', '600276', '000651', 
                '601318', '600563', '600066', '300122', 
                '300263', '601857', '600600', '000538', 
                '300325', '000671', '600036']
    #stocklist = []
    stocklist = jqapi.normalize_code(stocklist)

    for year in range(2017, 2005, -1):
        start_date = '{}-01-01'.format(year)
        end_date = '{}-01-02'.format(year + 1)
        for asset in stocklist:
            print(asset, start_date, end_date,)
            stockfile = os.path.join(stock_path, u'{}_{}_{}.pickle'.format(asset, year, frequence))
            if os.path.isfile(stockfile ):
                print('文件已经存在，跳过 ', stockfile)
                continue
            try:
                print(stockfile )
                his = jqapi.get_price(asset, start_date, end_date, frequency='60m')
                export_metadata_to_pickle(stock_path, u'{}_{}'.format(asset, year), metadata=his)
                #data_day = QA.QA_fetch_stock_min_adv(codelist,
                #    start='2019-01-01',
                #    end='2020-08-28',
                #    frequence='60min')
                #his = data_day.data
            except Exception as e:
                print(asset, e)
            time.sleep(1)


    for year in range(2017, 2005, -1):
        start_date = '{}-01-01'.format(year)
        end_date = '{}-01-02'.format(year + 1)
        for asset in stocklist:
            print(asset, start_date, end_date,)
            stockfile = os.path.join(stock_path, u'{}_{}_{}.pickle'.format(asset, year, frequence))
            his = import_metadata_from_pickle(stock_path, u'{}_{}'.format(asset, year))
            print(his.head(10))