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
@Desc:
@Author: huangzhiyuan
@Time: 2022/1/29 下午18:33
@Modify Notes:
'''
import setuptools

with open('./README.md', 'r', encoding="utf8") as f:
    long_desc = f.read()

setuptools.setup(
    name="nonebot-plugin-fg",
    version="2.0.2",
    author="mgsky1",
    author_email="hzy@acmsmu.cn",
    description="一个基于Nonebot2的QQ群每日总结生成插件，可以根据每日的聊天信息生成每日热词",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/mgsky1/FG-plugin",
    packages=setuptools.find_packages(),
    install_requires=[
        "networkx==2.6.3",
        "numpy==1.22.1",
        "scipy==1.7.3",
        "jieba==0.42.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    package_data={'':['*.txt']}
)

