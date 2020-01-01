# coding:utf8
import logging


"""
    
用来格式化打印日志到文件和控制台
"""
path = '.'
logger = None
# create logger
# 这里可以修改开源模块的日志等级
#设置日志打印格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#设置变量 ，用来保存日志文件， mode = 'a',a代表append
c = logging.FileHandler(path + "/lib/logs/all.log", mode='a', encoding='utf8')
#日志名字
logger = logging.getLogger('frame log')
#打印日志的等级
logger.setLevel(logging.DEBUG)
c.setFormatter(formatter)
#输出到日志文件
logger.addHandler(c)

# create console handler and set level to debug
ch = logging.StreamHandler()
#打印日志等级到控制台，没生效
ch.setLevel(logging.DEBUG)
# # add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# 打印debug级别日志
def debug(ss):
    global logger
    try:
        logger.debug(ss)
    except:
        return

# 打印info级别日志
def info(str):
    global logger
    try:
        logger.info(str)
    except:
        return

# 打印debug级别日志
def warn(ss):
    global logger
    try:
        logger.warning(ss)
    except:
        return

# 打印error级别日志
def error(ss):
    global logger
    try:
        logger.error(ss)
    except:
        return

# 打印异常日志
def exception(e):
    global logger
    try:
        logger.exception(e)
    except:
        return


# 调试
if __name__ == '__main__':
    debug('test')

