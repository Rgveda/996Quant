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
这里定义的是一些本地目录
"""

import os
import datetime
import pandas as pd


"""创建本地文件夹


1. setting_path ==> 用于存放配置文件 setting.cfg
2. cache_path ==> 用于存放临时文件
3. log_path ==> 用于存放储存的log
4. download_path ==> 下载的数据/财务文件
5. strategy_path ==> 存放策略模板
6. bin_path ==> 存放一些交易的sdk/bin文件等
"""

basepath = os.getcwd()
path = os.path.expanduser('~')
user_path = '{}{}{}'.format(path, os.sep, '.GolemQ')


def mkdirs_user(dirname):
    if not (os.path.exists(os.path.join(user_path, dirname)) and \
        os.path.isdir(os.path.join(user_path, dirname))):
        print(u'文件夹',dirname,'不存在，重新建立')
        #os.mkdir(dirname)
        os.makedirs(os.path.join(user_path, dirname))
    return os.path.join(user_path, dirname)


def mkdirs(dirname):
    if not (os.path.exists(os.path.join(basepath, dirname)) and \
        os.path.isdir(os.path.join(basepath, dirname))):
        print(u'文件夹',dirname,'不存在，重新建立')
        #os.mkdir(dirname)
        os.makedirs(os.path.join(basepath, dirname))
    return os.path.join(basepath, dirname)


def export_csv_min(code, market_type):
    """
    训练用隶属数据导出模块
    """
    if (isinstance(code, list)):
        code = code[0]

    frequence = '60min'
    if (market_type == QA.MARKET_TYPE.STOCK_CN):
        market_type_alis = 'A股'
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        market_type_alis = '指数'
    elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
        market_type_alis = '数字货币'


    #print(u'{} 开始读取{}历史数据'.format(QA_util_timestamp_to_str()[2:16],
    #                                    market_type_alis),
    #        code)
    if (market_type == QA.MARKET_TYPE.STOCK_CN):
        data_day = QA.QA_fetch_stock_min_adv(code,
                                            '1991-01-01',
                                            '{}'.format(datetime.date.today(),
                                            frequency=frequence))
 
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        #data_day = QA.QA_fetch_index_day_adv(code,
        #                                    '1991-01-01',
        #                                    '{}'.format(datetime.date.today(),))
        data_day = QA.QA_fetch_index_min_adv(code,
                                            '1991-01-01',
                                            '{}'.format(datetime.date.today(),
                                            frequency=frequence))
 
    elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
        frequence = '60min'
        data_hour = data_day = QA.QA_fetch_cryptocurrency_min_adv(code=code,
                start='2009-01-01',
                end=QA_util_timestamp_to_str(),
                frequence=frequence)

    if (data_day is None):
        #print('{}没有数据'.format(code))
        pass
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        mkdirs(os.path.join(export_path, 'index'))
        data_day.data.to_csv(os.path.join(export_path, 'index', '{}_{}_kline.csv'.format(code, frequence)))
    elif (market_type == QA.MARKET_TYPE.STOCK_CN):
        mkdirs(os.path.join(export_path, 'stock'))
        data_day.data.to_csv(os.path.join(export_path, 'stock', '{}_{}_kline.csv'.format(code, frequence)))
        
    return data_day.data


def export_hdf_metadata(export_path, code, frequence='60min', metadata=None):
    """
    训练用隶属特征数据导出模块
    """
    if (isinstance(code, list)):
        code = code[0]

    if (metadata is None):
        #print('{}没有数据'.format(code))
        pass
    else:
        print(os.path.join(export_path, '{}_{}.hdf5'.format(code, frequence)),
              metadata.tail(10))
        #metadata.to_hdf(os.path.join(export_path, '{}_{}.hdf5'.format(code, frequence)), key='df', mode='w')
        metadata.to_pickle(os.path.join(export_path, '{}_{}.hdf5'.format(code, frequence)))
    return metadata


def export_metadata_to_pickle(export_path, code, frequence='60min', metadata=None):
    """
    训练用隶属特征数据导出模块
    """
    if (isinstance(code, list)):
        code = code[0]

    if (metadata is None):
        #print('{}没有数据'.format(code))
        pass
    else:
        print(os.path.join(export_path, '{}_{}.pickle'.format(code, frequence)),
              metadata.tail(3))
        #metadata.to_hdf(os.path.join(export_path, '{}_{}.hdf5'.format(code, frequence)), key='df', mode='w')
        metadata.to_pickle(os.path.join(export_path, '{}_{}.pickle'.format(code, frequence)))
    return metadata


def import_metadata_from_pickle(export_path, code, frequence='60min'):
    if (isinstance(code, list)):
        code = code[0]

    print(os.path.join(export_path, '{}_{}.pickle'.format(code, frequence)))
    metadata = pd.read_pickle(os.path.join(export_path, '{}_{}.pickle'.format(code, frequence)))
    return metadata


def save_hdf_min(code, market_type, export_path='export', features=None):
    """
    训练用隶属特征数据导出模块
    """
    if (isinstance(code, list)):
        code = code[0]

    frequence = '60min'
    if (features is None):
        #print('{}没有数据'.format(code))
        pass
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        mkdirs(os.path.join(export_path, 'index'))
        features.to_hdf(os.path.join(export_path, 'index', '{}_{}_features.hdf'.format(code, frequence)), key='df', mode='w')
    elif (market_type == QA.MARKET_TYPE.STOCK_CN):
        mkdirs(os.path.join(export_path, 'stock'))
        features.to_hdf(os.path.join(export_path, 'stock', '{}_{}_features.hdf'.format(code, frequence)), key='df', mode='w')

    return features


def export_hdf_min(code, market_type, export_path='export', features=None):
    """
    训练用隶属数据导出模块
    """
    if (isinstance(code, list)):
        code = code[0]

    frequence = '60min'
    if (market_type == QA.MARKET_TYPE.STOCK_CN):
        market_type_alis = 'A股'
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        market_type_alis = '指数'
    elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
        market_type_alis = '数字货币'


    #print(u'{} 开始读取{}历史数据'.format(QA_util_timestamp_to_str()[2:16],
    #                                    market_type_alis),
    #        code)
    if (market_type == QA.MARKET_TYPE.STOCK_CN):
        data_day = QA.QA_fetch_stock_min_adv(code,
                                            '1991-01-01',
                                            '{}'.format(datetime.date.today()),
                                            frequence=frequence)
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        #data_day = QA.QA_fetch_index_day_adv(code,
        #                                    '1991-01-01',
        #                                    '{}'.format(datetime.date.today(),))
        data_day = QA.QA_fetch_index_min_adv(code,
                                            '1991-01-01',
                                            '{}'.format(datetime.date.today()),
                                            frequence=frequence)
    elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
        frequence = '60min'
        data_hour = data_day = QA.QA_fetch_cryptocurrency_min_adv(code=code,
                                                                start='2009-01-01',
                                                                end='{}'.format(datetime.date.today()),
                                                                frequence=frequence)

    if (data_day is None):
        #print('{}没有数据'.format(code))
        pass
    elif (market_type == QA.MARKET_TYPE.INDEX_CN):
        mkdirs(os.path.join(export_path, 'index'))
        data_day.data.to_hdf(os.path.join(export_path, 'index', '{}_{}_kline.hdf'.format(code, frequence)), key='df', mode='w')
    elif (market_type == QA.MARKET_TYPE.STOCK_CN):
        mkdirs(os.path.join(export_path, 'stock'))
        data_day.data.to_hdf(os.path.join(export_path, 'stock', '{}_{}_kline.hdf'.format(code, frequence)), key='df', mode='w')

    return data_day.data
