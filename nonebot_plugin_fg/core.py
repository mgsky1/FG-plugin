# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

'''
@Desc: 热词生成核心
@Author: huangzhiyuan
@Time: 2022/1/29 上午10:26
@Modify Notes:
'''
import re
import nonebot
import time
from nonebot import logger
from .base import get_config_list, get_scheduler, get_sys_config
from .TextRank4Keyword import TextRank4Keyword

config_list = get_config_list()
sys_config = get_sys_config()
scheduler = get_scheduler()

class DailyConclusion:

    def __init__(self, group_id: str):
        self.__group_id: str = group_id
        self.__begin_time = None
        self.__end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    def __pre_process(self) -> str:
        chat_log = ''
        try:
            with open(sys_config.fg_chatlog_dir_prefix + '/' + self.__group_id, 'r', encoding='utf-8') as f:
                is_first = True
                for eachLine in f:
                    # 获取聊天记录开始时间
                    if is_first:
                        res = re.search('^\d{4}-\d{2}-\d{1,2} \d{1,2}:\d{2}:\d{2}', eachLine)
                        pos = res.span()
                        self.__begin_time = eachLine[pos[0]:pos[1]]
                        is_first = False
                    else:
                        if re.search('^\d{4}-\d{2}-\d{1,2} \d{1,2}:\d{2}:\d{2} \d{5,11}', eachLine) is None:
                            if eachLine.find('<?xml') != -1:
                                continue
                            # 正则非贪婪模式 过滤CQ码
                            eachLine = re.sub('\[CQ:\w+,.+?\]', '', eachLine)
                            # 过滤URL
                            eachLine = re.sub('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',
                                              '', eachLine)
                            # 特殊情况过滤
                            eachLine = eachLine.replace('此处消息的转义尚未被插件支持', '')
                            if eachLine == '\n':
                                continue
                            chat_log += eachLine
        except Exception as error:
            logger.error("发生错误:{0}", error)
        finally:
            logger.info("群{0}的聊天记录处理完毕!", self.__group_id)
            logger.debug("群{0}的聊天记录处理完毕!内容为:{1}", self.__group_id, chat_log)
            return chat_log

    def gen_report(self) -> str:
        content = ''
        template_list = []
        word_num = 0
        word_len = 0
        for config in config_list:
            if config.group_id == self.__group_id:
                template_list.append(config.template_ok)
                template_list.append(config.template_failed)
                word_num = config.word_num
                word_len = config.word_len
                logger.info("群{0}热词生成进程【开始】！", self.__group_id)
                break
        logger.info("群{0}配置：期望显示热词数--{1}, 期望的最小热词长度--{2}", self.__group_id, word_num, word_len)
        chat_log = self.__pre_process()
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=chat_log, lower=True, window=5)
        word_dict = dict()
        for item in tr4w.get_keywords(word_num, word_min_len=word_len):
            word_dict[item.word] = item.weight
        if len(word_dict) >= word_num:
            logger.info("群{0}：热词数量--{1} >= {2}满足展示要求",self.__group_id, len(word_dict), word_num)
            content = template_list[0]
            word_list = list(word_dict.keys())
            for i in range(word_num):
                if content.find("${word}") != -1:
                    content = content.replace("${word}", word_list[i], 1)
        else:
            logger.info("群{0}：热词数量--{1} < {2}不满足展示要求", self.__group_id, len(word_dict), word_num)
            content = template_list[1]
        content = content.replace("${begin_time}", self.__begin_time)
        content = content.replace("${end_time}",self.__end_time)
        for config in config_list:
            if config.group_id == self.__group_id:
                logger.info("群{0}热词生成进程【结束】！", self.__group_id)
                # 清除文件内容
                with open(sys_config.fg_chatlog_dir_prefix + '/' + self.__group_id, 'a', encoding='utf-8') as f:
                    # 定位文件第一个字符
                    f.seek(0)
                    # 清空
                    f.truncate()
                    logger.info("群{0}的聊天记录已清空", self.__group_id)
                break
        logger.debug("群{0}的热词生成进程【结束】!生成的内容为：{1}", self.__group_id, content)
        return content


async def process(group_id: str):
    dy = DailyConclusion(group_id)
    content = dy.gen_report()
    bot = nonebot.get_bot()
    await bot.call_api("send_group_msg", group_id=int(group_id), message=content)
    logger.info("群{0}消息已发送",group_id)


# 配置定时器
for config in config_list:
    scheduler.add_job(process,
                      "cron",
                      hour=config.trigger_hour, minute=config.trigger_min, id="FG-"+config.group_id,
                      args=[config.group_id])
    logger.info("群{0}的定时器添加完毕！配置信息如下:{1}", config.group_id, config)

