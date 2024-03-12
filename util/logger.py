import logging
from logging import handlers
import datetime
import pytz


class Logger(object):
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }  # 日志级别关系映射

    def beijing(sec, what):
        beijing_time = datetime.datetime.now(tz=pytz.timezone("PRC"))
        return beijing_time.timetuple()

    def __init__(
        self,
        base_path,
        filename,
        level="info",
        when="MIDNIGHT",
        interval=1,
        backCount=30,
        fmt="[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]:%(message)s",
        sfmt="[%(asctime)s][%(module)s:%(lineno)d][%(levelname)s]:%(message)s"
        
    ):
        self.logger = logging.getLogger(filename)
        self.logger.handlers = []
        format_str = logging.Formatter(fmt)  # 设置日志格式
        # 设置时间格式
        logging.Formatter.converter = self.beijing
        self.logger.setLevel(self.level_relations[level])  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        single_format_str = logging.Formatter(sfmt, '%Y%m%d-%H:%M:%S')
        sh.setFormatter(single_format_str)  # 设置屏幕上显示的格式
        fh = handlers.TimedRotatingFileHandler(
            filename=filename, when=when, interval=interval, backupCount=backCount, encoding="utf-8"
        )
        # fh_all = handlers.TimedRotatingFileHandler(filename=base_path + "/log/all.log", when="D", interval=30, backupCount=backCount, encoding="utf-8")
        fh.setFormatter(format_str)  # 设置文件里写入的格式
        # fh_all.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(fh)
        # self.logger.addHandler(fh_all)
