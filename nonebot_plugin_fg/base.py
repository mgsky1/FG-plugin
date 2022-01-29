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
@Desc: 全局基类
@Author: huangzhiyuan
@Time: 2022/1/29 下午23:00
@Modify Notes:
'''

from nonebot import get_driver
from nonebot import logger
from nonebot.config import Config
from .config import parse_json_conf
import nonebot_plugin_apscheduler

scheduler = nonebot_plugin_apscheduler.scheduler
logger.info("FG--apscheduler定时插件已载入")
sys_config = get_driver().config
# 解析配置文件
config_list = parse_json_conf(sys_config.fg_config_location)
logger.info("FG--配置文件已载入")

def get_scheduler() -> nonebot_plugin_apscheduler.scheduler:
    return scheduler

def get_sys_config() -> Config:
    return sys_config

def get_config_list() -> list:
    return config_list
