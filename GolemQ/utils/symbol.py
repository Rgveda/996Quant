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
try:
    import QUANTAXIS as QA
except:
    print('PLEASE run "pip install QUANTAXIS" before call GolemQ.GQUtil.symbol modules')
    pass

from QUANTAXIS.QAUtil.QACode import (QA_util_code_tostr)
from GolemQ.utils.const import _const
    
class EXCHANGE(_const):
    XSHG = 'XSHG'
    SSE = 'XSHG'

def is_stock_cn(code):
    """
    1- sh
    0 -sz
    """
    code = str(code)
    if code[0] in ['5', '6', '9'] or \
        code[:3] in ["009", "126", "110", "201", "202", "203", "204"] or \
        (code.startswith('XSHG')) or \
        (code.endswith('XSHG')):
        if (code.startswith('XSHG')) or \
             (code.endswith('XSHG')):
            if (len(code.split('.')) > 1):
                try_split_codelist = code.split('.')
                if (try_split_codelist[0] == 'XSHG') and (len(try_split_codelist[1]) == 6):
                    code = try_split_codelist[1]
                elif (try_split_codelist[1] == 'XSHG') and (len(try_split_codelist[0]) == 6):
                    code = try_split_codelist[0]
                if (code[:5] in ["00000"]):
                    return True, QA.MARKET_TYPE.INDEX_CN, 'SH', '上交所指数'
        if code.startswith('60') == True:
            return True, QA.MARKET_TYPE.STOCK_CN, 'SH', '上交所A股'
        elif code.startswith('900') == True:
            return True, QA.MARKET_TYPE.STOCK_CN, 'SH', '上交所B股'
        elif code.startswith('50') == True:
            return True, QA.MARKET_TYPE.FUND_CN, 'SH', '上交所传统封闭式基金'
        elif code.startswith('51') == True:
            return True, QA.MARKET_TYPE.FUND_CN, 'SH', '上交所ETF基金'
        else:
            return True, None, 'SH', '上交所未知代码'
    elif code[0] in ['0', '2', '3'] or \
        code[:3] in ['000', '001', '002', '200', '300', '159'] or \
        (code.startswith('XSHE')) or \
        (code.endswith('XSHE')):
        if (code.startswith('000') == True) or \
            (code.startswith('001') == True):
            if (code in ['000003', '000112', '000300', '000132', '000133']):
                return True, QA.MARKET_TYPE.INDEX_CN, 'SH', '中证指数'
            else:
                return True, QA.MARKET_TYPE.STOCK_CN, 'SZ', '深交所主板'
        if code.startswith('002') == True:
            return True, QA.MARKET_TYPE.STOCK_CN, 'SZ', '深交所中小板'
        elif code.startswith('159') == True:
            return True, QA.MARKET_TYPE.FUND_CN, 'SZ', '深交所ETF基金'
        elif code.startswith('200') == True:
            return True, QA.MARKET_TYPE.STOCK_CN, 'SZ', '深交所B股'
        elif code.startswith('399') == True:
            return True, QA.MARKET_TYPE.INDEX_CN, 'SZ', '中证指数'
        elif code.startswith('300') == True:
            return True, QA.MARKET_TYPE.STOCK_CN, 'SZ', '深交所创业板'
        elif (code.startswith('XSHE')) or \
            (code.endswith('XSHE')):
             pass
        else:
            return True, None, 'SZ', '深交所未知代码'
    else:
        return False, None, None, None

def is_furture_cn(code):
    if code[:2] in ['IH', 'IF', 'IC', 'TF', 'JM', 'PP', 'EG', 'CS',
         'AU', 'AG', 'SC', 'CU', 'AL', 'ZN', 'PB', 'SN', 'NI',
         'RU', 'RB', 'HC', 'BU', 'FU', 'SP',
         'SR', 'CF', 'RM', 'MA', 'TA', 'ZC', 'FG', 'IO', 'CY']:
         return True, QA.MARKET_TYPE.FUTURE_CN, 'NA', '中国期货'
    elif code[:1] in ['A', 'B', 'Y', 'M', 'J', 'P', 'I',
                    'L', 'V', 'C', 'T']:
        return True, QA.MARKET_TYPE.FUTURE_CN, 'NA', '中国期货'
    else:
        return False, None, None, None


def is_cryptocurrency(code):
    code = str(code)
    if (code.startswith('HUOBI') == True) or code.startswith('huobi') == True or \
        code.endswith('husd') == True or code.endswith('HUSD') == True:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'huobi.pro', '数字货币'
    elif code.endswith('bnb') == True or code.endswith('BNB') == True or \
        code.startswith('BINANCE') == True or code.startswith('binance') == True:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'Binance', '数字货币'
    elif code.startswith('BITMEX') == True or code.startswith('bitmex') == True:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'Bitmex', '数字货币'
    elif code.startswith('OKEX') == True or code.startswith('OKEx') == True or \
        code.startswith('okex') == True or code.startswith('OKCoin') == True or \
        code.startswith('okcoin') == True or code.startswith('OKCOIN') == True:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'OKEx', '数字货币'
    elif code.startswith('BITFINEX') == True or code.startswith('bitfinex') == True or \
        code.startswith('Bitfinex') == True:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'Bitfinex', '数字货币'
    elif (code[:-7] in ['adausdt', 'bchusdt', 'bsvusdt', 'btcusdt', 'btchusd', 
                     'eoshusd', 'eosusdt', 'etcusdt', 'etchusd', 'ethhusd', 
                     'ethusdt', 'ltcusdt', 'trxusdt', 'xmrusdt', 'xrpusdt', 
                     'zecusdt']) or \
        (code[:-8] in ['atomusdt', 'algousdt', 'dashusdt', 'dashhusd', 'hb10usdt']) or \
        (code[:-6] in ['hthusd', 'htusdt']):
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'huobi.pro', '数字货币'
    elif code.endswith('usd') == True or code.endswith('USD'):
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'NA', '数字货币'
    elif code.endswith('usdt') == True or code.endswith('USDT') == True:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'NA', '数字货币'
    elif code[:3] in ['BTC', 'btc', 'ETH', 'eth',
                      'EOS', 'eos', 'ADA','ada',
                      'BSV', 'bsv', 'BCH', 'bch', 
                      'xmr', 'XMR', 'LTC', 'ltc',
                      'xrp', 'XRP', 'ZEC', 'zec',
                      'trx', 'TRX', 'ZEC', 'zec']:
        return True, QA.MARKET_TYPE.CRYPTOCURRENCY, 'NA', '数字货币'
    else:
        return False, None, None, None
    

def get_codelist(codepool):
    """
    将各种‘随意’写法的A股股票代码列表，转换为6位数字list标准规格，
    可以是“,”斜杠，“，”，可以是“、”，或者其他类似全角或者半角符号分隔。
    """
    if (isinstance(codepool, str)):
        codelist = [code.strip() for code in codepool.splitlines()]
    elif (isinstance(codepool, list)):
        codelist = codepool
    else:
        print(u'Unsolved stock_cn code/symbol string:{}'.format(codepool))

    ret_codelist = []
    for code in codelist:
        if (len(code) > 6):
            try_split_codelist = code.split('/')
            if (len(try_split_codelist) > 1):
                ret_codelist.extend(try_split_codelist)
            elif (len(code.split(' ')) > 1):
                try_split_codelist = code.split(' ')
                ret_codelist.extend(try_split_codelist)
            elif (len(code.split('、')) > 1):
                try_split_codelist = code.split('、')
                ret_codelist.extend(try_split_codelist)
            elif (len(code.split('，')) > 1):
                try_split_codelist = code.split('，')
                ret_codelist.extend(try_split_codelist)
            elif (len(code.split(',')) > 1):
                try_split_codelist = code.split(',')
                ret_codelist.extend(try_split_codelist)
            elif (code.startswith('XSHE')) or \
                (code.endswith('XSHE')):
                ret_codelist.append('{}.XSHE'.format(QA_util_code_tostr(code)))
                pass
            elif (code.startswith('XSHG')) or \
                (code.endswith('XSHG')):
                #Ztry_split_codelist = code.split('.')
                ret_codelist.append('{}.XSHG'.format(QA_util_code_tostr(code)))
            else:
                if (QA_util_code_tostr(code)):
                    pass
                print(u'Unsolved stock_cn code/symbol string:{}'.format(code))
        else:
            ret_codelist.append(code)

    # 去除空字符串
    ret_codelist = list(filter(None, ret_codelist))
    #print(ret_codelist)

    # 清除尾巴
    ret_codelist = [code.strip(',') for code in ret_codelist]
    ret_codelist = [code.strip('\'') for code in ret_codelist]

    # 去除重复代码
    ret_codelist = list(set(ret_codelist))

    return ret_codelist


def get_block_symbols(blockname, stock_cn_block=None):
    """
    自定义结构板块，用于分析板块轮动，结构化行情和国家队护盘行情
    例如证券软件的“军工”板块股票超过200支过于庞大，在这里进行精选和过滤
    """
    if (stock_cn_block is None):
        stock_cn_block = QA.QA_fetch_stock_block_adv() 
    blockset = {'军工': ['150182', '512660', '512560', '512710'],
                '银行': ['512800', '515020', '159933', '512730', '515820', '515280'],
                '医疗': ['512170',],
                '医药': ['512170',],
                '黄金概念': ['518880', '159934'],
                '黄金': ['518880', '159934'],
                '证券': ['512000', '512880'],
                '酒': ['512690'],
                '白酒': ['512690'],
                '文化传媒': ['512980', '159805'],
                '传媒': ['512980', '159805'],
                }
    blockset['银行'].extend(stock_cn_block.get_block(['银行', '中小银行']).code)
    blockset['证券'].extend(stock_cn_block.get_block(['证券']).code)

    blockset['酒'].extend(stock_cn_block.get_block(['白酒', '啤酒']).code)
    blockset['白酒'] = blockset['酒']

    blockset['机场航运'] = stock_cn_block.get_block(['机场航运', '航运']).code
    blockset['航运'] = stock_cn_block.get_block(['机场航运', '航运']).code

    lockheed = list(set(stock_cn_block.get_block(['军工']).code).intersection(stock_cn_block.get_block(['国防军工']).code))
    blockset['军工'].extend(list(set(lockheed).intersection(stock_cn_block.get_block(['行业龙头', '证金持股']).code)))

    # 这个问题是“生物疫苗”，和"医疗器械"是否算医疗类
    medic = stock_cn_block.get_block(['生物医药', '医疗器械', '医疗改革', '医药商业']).code
    blockset['医疗'].extend(list(set(medic).intersection(stock_cn_block.get_block(['行业龙头', '证金持股']).code)))
    blockset['医药'] = blockset['医疗']

    culture = stock_cn_block.get_block(['文化传媒', '传媒', '传播与文化产业',]).code
    blockset['文化传媒'].extend(list(set(culture).intersection(stock_cn_block.get_block(['行业龙头', '证金持股']).code)))
    blockset['传媒'] = blockset['文化传媒']

    gold = stock_cn_block.get_block(['黄金概念', '黄金']).code
    blockset['黄金'].extend(list(set(gold).intersection(stock_cn_block.get_block(['行业龙头', '证金持股']).code)))
    blockset['黄金概念'] = blockset['黄金']

    if (blockname in blockset.keys()):
        return blockset[blockname]
    else:
        return stock_cn_block.get_block(blockname).code