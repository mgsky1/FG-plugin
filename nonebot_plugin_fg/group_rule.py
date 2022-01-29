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
@Desc: 自定义规则：只处理群消息
@Author: huangzhiyuan
@Time: 2022/1/27 下午8:14
@Modify Notes:
'''
import nonebot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.event import GroupMessageEvent


class GroupRule:
    async def __call__(
            self,
            event_type: Event,
    ) -> bool:
        nonebot.logger.debug("消息类型：{0}", type(event_type))
        if isinstance(event_type, GroupMessageEvent):
            return True
        else:
            return False