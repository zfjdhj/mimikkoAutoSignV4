import logging
from logging import handlers
import datetime
import pytz
import os


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
        sfmt="[%(asctime)s][%(module)s:%(lineno)d][%(levelname)s]:%(message)s",
        screen=True
    ):
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            print(f'创建日志目录：{dir}')
            os.makedirs(dir)
            os.system(f"chmod 777 {dir}")
        self.logger = logging.getLogger(filename)

        # 关闭并移除旧的 handler，避免未关闭文件句柄
        for h in list(self.logger.handlers):
            try:
                h.flush()
            except Exception:
                pass
            try:
                h.close()
            except Exception:
                pass
            self.logger.removeHandler(h)
        self.logger.propagate = False

        # 设置时间格式
        logging.Formatter.converter = self.beijing
        self.logger.setLevel(self.level_relations[level])  # 设置日志级别
        # screen
        if screen:
            sh = logging.StreamHandler()  # 往屏幕上输出
            single_format_str = logging.Formatter(sfmt, '%Y%m%d-%H:%M:%S')
            sh.setFormatter(single_format_str)  # 设置屏幕上显示的格式
            self.logger.addHandler(sh)
        # file
        format_str = logging.Formatter(fmt, '%Y%m%d-%H:%M:%S')  # 设置日志格式
        if when:
            fh = handlers.TimedRotatingFileHandler(
                filename=filename, when=when, interval=interval, backupCount=backCount, encoding="utf-8"
            )
        else:
            fh = logging.FileHandler(filename=filename, encoding="utf-8")
        fh.setFormatter(format_str)
        self.logger.addHandler(fh)
