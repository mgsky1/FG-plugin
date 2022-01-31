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
@Desc: 热词配置相关类
@Author: huangzhiyuan
@Time: 2022/1/27 下午2:57
@Modify Notes:
'''
from pydantic import BaseModel, validator
import json


class GroupModel(BaseModel):

    group_id: str
    trigger_hour: int = 0
    trigger_min: int = 0
    word_num: int
    word_len: int
    template_ok: str
    template_failed: str

    @validator("trigger_hour")
    def hour_checker(cls, hour: int):
        def is_validate(hour: int) -> bool:
            if (hour >= 24) and (hour < 0):
                return False
            else:
                return True
        if not is_validate(hour):
            raise ValueError("小时数要介于0-23之间")
        else:
            return hour

    @validator("trigger_min")
    def min_checker(cls, min: int):
        def is_validate(min: int) -> bool:
            if (min >= 60) and (min < 0):
                return False
            else:
                return True
        if not is_validate(min):
            raise ValueError("分钟数要介于0-59之间")
        else:
            return min

def parse_json_conf(json_conf_path):
    group_config_list = []
    with open(json_conf_path, 'r', encoding='utf8') as json_conf_file:
        configs = json.load(json_conf_file)
        for config in configs:
            group_config_list.append(GroupModel(**config))
    return group_config_list