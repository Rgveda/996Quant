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
绘制最简单的K线图，画K线图是一定要会画的，以后处理CV形态识别K线训练图片都是要自己画图的，这是基本功。
"""

from datetime import datetime as dt
from datetime import timedelta
from datetime import timezone
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mdates

try:
    import QUANTAXIS as QA
except:
    print('PLEASE run "pip install QUANTAXIS" before run this demo')
    pass

from GolemQ.utils.path import (
    load_cache,
    save_cache,
)

try:
    import talib
except:
    print('PLEASE run "pip install talib" before call these methods')
    pass


def ohlc_plot_protype(ohlc_data, code=None, codename=None, title=None):

    # 暗色主题
    plt.style.use('Solarize_Light2')

    # 正常显示中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    # 设定布局
    fig = plt.figure(figsize = (22,9))
    plt.subplots_adjust(left=0.04, right=0.96)
    if (title is None):
        fig.suptitle(u'阿财的 {:s}（{:s}）量化学习笔记绘制K线DEMO'.format(codename, 
                                                            code), fontsize=16)
    else:
        fig.suptitle(title, fontsize=16)
    ax1 = fig.add_subplot(111)
    
    # 绘制K线
    ohlc_data = ohlc_data.reset_index([1], drop=False)
    mc_stock_cn = mpf.make_marketcolors(up='r',down='g')
    s_stock_cn = mpf.make_mpf_style(marketcolors=mc_stock_cn)
    mpf.plot(data=ohlc_data, ax=ax1, type='candle', style=s_stock_cn)

    # 设定最标轴时间
    datetime_index = ohlc_data.index.get_level_values(level=0).to_series()
    DATETIME_LABEL = datetime_index.apply(lambda x: 
                                          x.strftime("%Y-%m-%d %H:%M")[2:16])
    ax1.set_xticks(range(0, len(DATETIME_LABEL), 
                         round(len(DATETIME_LABEL) / 12)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(DATETIME_LABEL) / 12)])
    ax1.grid(True)
    return ax1, DATETIME_LABEL


def ma30_cross_func(data):
    """
    MA均线金叉指标
    """
    MA5 = talib.MA(data.close, 5)
    MA10 = talib.MA(data.close, 10)
    MA30 = talib.MA(data.close, 30)
    MA90 = talib.MA(data.close, 90)
    MA120 = talib.MA(data.close, 120)

    MA30_CROSS = pd.DataFrame(np.c_[MA5,
                                    MA10,
                                    MA30,
                                    MA90,
                                    MA120],
                              columns=['MA5', 
                                       'MA10', 
                                       'MA30', 
                                       'MA90',
                                       'MA120'], 
                              index=data.index)    

    return MA30_CROSS


def ohlc_plot_with_ma(ohlc_data, features, 
                      code=None, codename=None, title=None):
    """
    增加 MA 移动平均线
    """
    ax1, DATETIME_LABEL = ohlc_plot_protype(ohlc_data, 
                                            code='399300', 
                                            codename=u'沪深300')
    ax1.plot(DATETIME_LABEL, features['MA30'], lw=0.75, 
             color='blue', alpha=0.6)
    ax1.plot(DATETIME_LABEL,
             features['MA90'], lw=1, color='crimson',
             alpha=0.5)
    ax1.plot(DATETIME_LABEL, features['MA120'], lw=1,
             color='limegreen', alpha=0.5)
    
    return ax1

if __name__ == '__main__':
    start = dt.now() - timedelta(hours=19200)
    end = dt.now(timezone(timedelta(hours=8))) + timedelta(minutes=1)
    symbol = '399300'
    frequence = '60min'
    try:
        # 尝试用QA接口读取K线数据
        data_min = QA.QA_fetch_index_min_adv('399300',
            start='{}'.format(start),
            end='{}'.format(end),
            frequence=frequence)
        if (len(data_min.data) > 100):
            fllename = 'kline_{}_{}.pickle'.format(symbol,
                                   frequence)
            save_cache(fllename, data_min.data)
        features = ma30_cross_func(data_min.data)
        ohlc_data = data_min.data.tail(320)
    except:
        # 没有装QA或者没有数据，尝试读取 pickle 缓存
        fllename = 'kline_{}_{}.pickle'.format(symbol,
                                       frequence)
        ohlc_data = load_cache(fllename)
        features = ma30_cross_func(ohlc_data)
        ohlc_data = ohlc_data.tail(320)

    ohlc_plot_with_ma(ohlc_data, features.tail(320), 
                      code='399300', 
                      codename=u'沪深300')
    plt.show()