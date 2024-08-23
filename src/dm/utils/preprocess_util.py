"""
Preprocess utils
"""
from datetime import datetime
import random
from urllib.parse import urlparse


def get_cst_date(date_string, date_format="%Y%m%d"):
    """
    将给定的日期字符串转换为北京时间的详细日期和时间描述。

    Args:
        date_string (str): 要转换的日期字符串。
        date_format (str): 日期字符串的格式，默认为"%Y%m%d"。

    Returns:
        str: 返回格式为"中国北京时间年-月-日 时:分:秒，星期"的日期时间字符串。

    Raises:
        ValueError: 如果date_string与date_format不匹配, strptime函数会抛出ValueError。
    """
    current_time = datetime.strptime(date_string, date_format)
    weekday_index = current_time.weekday()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]  
    current_time_str = "%d年%02d月%02d日%02d时%02d分%02d秒，%s" % (
        current_time.year, 
        current_time.month, 
        current_time.day, 
        random.randint(7, 23),
        random.randint(1, 60),
        random.randint(1, 60),
        weekdays[weekday_index])
    cst_date = "中国北京时间" + current_time_str + "。"
    return cst_date


def convert_pages_to_knowledge(pages, start=0, end=None):
    """
    将传入的页面列表转换为知识文本

    Args:
        pages (list): 页面列表, 每个页面为一个字典, 包含title, content, publish_time, wangzhan_name, url等字段
        start (int, optional): 开始转换的页面索引, 默认为0
        end (int, optional): 结束转换的页面索引, 默认为None, 表示转换到列表末尾

    Returns:
        str: 转换后的知识文本
    """
    knowledge = ""
    for i, page in enumerate(pages[start:end]):
        if i > 0:
            knowledge += "\n"
        reference = ""
        idx = i + start
        reference += "##参考文章{}\n".format(idx + 1)
        reference += "标题：" + page["title"] + "\n"
        if page.get("publish_time"):
            reference += "文章发布时间：" + page["publish_time"] + "\n"
        reference += "内容：" + page["content"].strip() + "\n"
        if page.get("wangzhan_name"):
            reference += "来源网站名：" + page["wangzhan_name"] + "\n"
        if page.get("url"):
            reference += "来源网站网址：" + urlparse(page["url"]).netloc + "\n"
        knowledge += reference
    return knowledge
