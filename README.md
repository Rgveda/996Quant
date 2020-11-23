# GolemQ

A PowerToys based QUANTAXIS

这是一个基于 QUANTAXIS 二次开发的量化系统子项目

发起这个子项目的原因是我人称BugKing，也没有精力去仔细测试，有些随手PR的代码可能会干扰QUANTAXIS主版本稳定性（是的，1.9.30版本无法获取A股财报的Bug是我PR上去的\>\_<）；某些开发了代码功能存在跟天神原始设计不相同的；或者规划路线图跟天神设计理念不同的；或者依赖或者模仿第三方量化平台接口的(我担心有法律之类的风险，所以也不适合PR到QUANTAXIS)。有的功能和代码因为我不是金融科班出身，也不知道现在的前沿趋势，贸然PR到QUANTAXIS，然后又自己发觉功能不妥或者不实用，然后又匆忙在QUANTAXIS中移除。再比如一部分功能代码我设计为cli命令行格式运行，而QA主要设计为Docker发布运行。

这导致了一部分代码因为现实需求被我写出来，正在使用，但是跟QA风格并不匹配，而没有办法在Docker的HTML前端中顺利使用，暂时我也没相处好办法和QUANTAXIS 进行 PR 合并。

但是又有很多朋友问这些常用的功能使用情况，为了发布我不得不打包代码，索性发布自己的第一个Git项目吧，也算是人生头一回原创 Git仓库了。

## 安装：

在 QUANTAXIS Docker 中打开 Dashboard

选择 qacommunity，打开 cli 控制台，输入 bash

输入 git clone https://github.com/Rgveda/GolemQ.git

cd GolemQ

python setup.py install

## 使用：

### 功能包括：

来源新浪财经的A股实盘行情 l1快照数据

在 repo 根目录下面，输入：

python -m GolemQ.cli --sub sina_l1

只保存部分股票数据，输入：

python -m GolemQ.cli --sub sina_l1 --codelist "600783、601069、002152、000582、002013、000960、000881
、000698、600742、600203、601186、601007、600328、600879"

### 读取实盘l1数据

这里完成的动作包括，读取l1数据，重采样为1min数据，重采样为日线/小时线数据，具体方法为打开 Jupyter，输入

*from GolemQ.fetch.kline import \(*
    *get_kline_price,*
    *get_kline_price_min,*
*\)*

*data_day, codename = get_kline_price\("600519", verbose=True\)*

为避免出现很多打印信息，可以设置参数 *verbose=False*

*data_day, codename = get_kline_price_min\("6003444", verbose=False\)*

### 已知Bug：

上证指数 000001 实盘走势和平安银行混淆。 目前已经修正 ——2020.11.22

成交量：Volumne和Amount 计算方式不对。

未能正确处理 *000001.XSHG 600519.SH* 这类格式的代码，能返回K线数据，但是不含今日实盘数据

### 常见问题

无法运行命令

*PS C:\Users\azai\source\repos\GolemQ> python -m GolemQ.cli --sub sina_l1*

提示

*C:\Users\azai\AppData\Local\Programs\Python\Python37\python.exe: Error 
while finding module specification for 'GolemQ.cli' 
(ModuleNotFoundError: No module named 'GolemQ')*

解决方法输入 cd .. 切换到上一层目录

*PS C:\Users\azai\source\repos\GolemQ> cd ..*

*PS C:\Users\azai\source\repos> python -m GolemQ.cli --sub sina_l1*

Program Last Time 3.762s

Not Trading time 现在是中国A股收盘时间 2020-10-15 16:28:05.310437

Not Trading time 现在是中国A股收盘时间 2020-10-15 16:28:07.314858

Not Trading time 现在是中国A股收盘时间 2020-10-15 16:28:09.323150

Not Trading time 现在是中国A股收盘时间 2020-10-15 16:28:11.334017


## 例子

### 读取实盘行情数据K线

在 repo 根目录下面，输入

*python -m GolemQ.test_cases.fetch_test.realtime*

## 模仿优矿DataAPI数据接口

挖了坑，未完成，待续

## 计划

模仿聚宽API接口——To be continue...

Firstblood!

By 阿财 

2020.10.14