#!/bin/bash

# 创建数据文件夹
mkdir data
mkdir data/judge
mkdir data/media
mkdir data/temp
mkdir data/test_case

# 创建虚拟环境
python -m venv venv

# 安装项目依赖
cd ./judger/lorun
../../venv/bin/python ./setup.py install
cd ../..
venv/bin/pip install -r requirements.txt

# 迁移数据库
venv/bin/python manage.py makemigrations
venv/bin/python manage.py migrate
