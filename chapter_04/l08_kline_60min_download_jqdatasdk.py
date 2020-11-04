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
聚宽分钟线数据下载
"""

import os
import datetime
import pandas as pd
import numpy as np
from jqdatasdk import (
    auth,
    is_auth,
    get_query_count,
    api as jqapi,
)
from GolemQ.utils.path import (
    mkdirs,
    export_metadata_to_pickle,
    export_metadata_from_pickle,
)
from GolemQ.utils.settings import (
    load_settings,
    save_settings,
)
try:
    import QUANTAXIS as QA
except:
    print('PLEASE run "pip install QUANTAXIS" to call these modules')
    pass

if __name__ == '__main__':
    #password = pd.DataFrame({'host':['jqdatasdk'],
    #    'username':['13981813381'],
    #    'password':['813381']}, columns=['host',
    #                                   'username', 
    #                                   'password'])
    # 用上面的代码保存密码到用户配置 .GolemQ 目录下面
    password = load_settings('password.hdf5')
    auth(password.username[0], password.password[0]) #ID是申请时所填写的手机号；Password为聚宽官网登录密码，新申请用户默认为手机号后6位
    asset = u'000001.XSHE'
    is_auth = is_auth()

    # 查询当日剩余可调用条数
    print(get_query_count())
    print(is_auth)
    codelist = ['000876']
    code = codelist[0]

    # 创建数据下载目录
    index_path = mkdirs(os.path.join(mkdirs('datastore'), 'kline', 'index'))
    print(index_path)

    for year in range(2005, 2017):
        start_date = '{}-01-01'
        end_date = '{}-01-02'
        for asset in indexlist:
            print(asset)
        #his = jqapi.get_price(asset, start_date, end_date, frequency='60m')
        data_day = QA.QA_fetch_stock_min_adv(codelist,
            start='2019-01-01',
            end='2020-08-28',
            frequence='60min')
        his = data_day.data
        export_metadata_to_pickle(index_path, u'{}_{}'.format(asset, year), metadata=his)
        print()


    for year in range(2005, 2017):
        his = export_metadata_from_pickle(index_path, u'{}_{}'.format(asset, year))
        print(his.head(10))