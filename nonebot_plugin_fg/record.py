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
@Desc:记录聊天信息
@Author: huangzhiyuan
@Time: 2022/1/27 下午4:12
@Modify Notes:
'''
import nonebot
import time
from .base import get_config_list, get_sys_config
from pathlib import Path
from nonebot import on_message
from nonebot.rule import Rule
from nonebot.log import logger
from .group_rule import GroupRule
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

group_chat = on_message(rule=Rule(GroupRule()))

config_list = get_config_list()
sys_config = get_sys_config()

@group_chat.handle()
async def record(event : GroupMessageEvent):
    chat_log_path = Path(sys_config.fg_chatlog_dir_prefix)
    chat_log_path.mkdir(parents=True, exist_ok=True)
    # 打印消息
    logger.info("接收到一条群消息:群号:{0}, 发送者:{1}, 内容:{2}",
                        event.group_id, event.user_id, event.raw_message)
    # 遍历配置文件，将消息记录在对应群号的txt文件中
    for config in config_list:
        if str(event.group_id) == config.group_id:
            with open(sys_config.fg_chatlog_dir_prefix + '/' + str(event.group_id), 'a', encoding='utf-8') as f:
                msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + str(event.user_id) + '\n' + \
                      event.raw_message + '\n'
                f.write(msg)
                f.flush()
                nonebot.logger.debug("消息{0}--已写入", msg)
            break