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
聚宽小时线(60分钟线)数据下载，范围 沪深300，下载到当前目录 \datastore\kline\stock\ 下
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
    asset = u'000001.XSHE'
    is_auth = is_auth()

    # 查询当日剩余可调用条数
    print(get_query_count())
    print(is_auth)

    # 创建数据下载目录
    frequence = '60min'
    stock_path = mkdirs(os.path.join(mkdirs('datastore'), 'kline', 
                                     'stock', frequence))
    print(stock_path)

    for year in range(2017, 2005, -1):
        last_query_count = get_query_count()
        print(u'剩余可查询条数', last_query_count)
        stocklists = []
        for month in range(1, 12):
            index_date = '{}-{}-01'.format(year, month)
            # 获取特定日期截面的所有沪深300的股票成分
            stocklist = jqapi.get_index_stocks('000300.XSHG', 
                                               date=index_date)
            time.sleep(0.2)
            stocklists = stocklists + stocklist
            
        # 去除重复代码
        stocklists = list(set(stocklists))
        print(u'{}年 沪深300指数 一共有成分个股:{}个'.format(year, 
                                                len(stocklists)), 
              stocklists)
        stocklists = jqapi.normalize_code(stocklists)        

        start_date = '{}-01-01'.format(year)
        end_date = '{}-01-02'.format(year + 1)
        for asset in stocklists:
            if (last_query_count['spare'] < 1280):
                print(u'剩余查询条数已经不足，退出行情查询抓取...')
                break

            print(asset, start_date, end_date,)
            stockfile = os.path.join(stock_path, 
                                     u'{}_{}_{}.pickle'.format(asset,    
                                                               year, 
                                                               frequence))
            if os.path.isfile(stockfile):
                print('文件已经存在，跳过 ', stockfile)
                continue
            try:
                print(stockfile)
                his = jqapi.get_price(asset, 
                                      start_date, 
                                      end_date, 
                                      frequency='60m')
                export_metadata_to_pickle(stock_path, 
                                          u'{}_{}'.format(asset,
                                                          year), 
                                          metadata=his)
            except Exception as e:
                last_query_count = get_query_count()
                print(asset, last_query_count, e)
            time.sleep(1)


    for year in range(2017, 2005, -1):
        stocklists = []
        for month in range(1, 12):
            index_date = '{}-{}-01'.format(year, month)
            # 获取特定日期截面的所有沪深300的股票成分
            stocklist = jqapi.get_index_stocks('000300.XSHG', 
                                               date=index_date)
            time.sleep(0.2)
            stocklists = stocklists + stocklist
            
        # 去除重复代码
        stocklists = list(set(stocklists))
        print(u'查验数据 {}年 沪深300指数 一共有成分个股:{}个'.format(year, 
                                                len(stocklists)), 
              stocklists)
        stocklists = jqapi.normalize_code(stocklists)        

        start_date = '{}-01-01'.format(year)
        end_date = '{}-01-02'.format(year + 1)
        for asset in stocklists:
            print(asset, start_date, end_date,)
            stockfile = os.path.join(stock_path, 
                                     u'{}_{}_{}.pickle'.format(asset, 
                                                               year, 
                                                               frequence))
            his = import_metadata_from_pickle(stock_path, 
                                              u'{}_{}'.format(asset, 
                                                              year))
            print(his.head(10))