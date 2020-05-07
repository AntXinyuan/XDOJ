#!/bin/bash

# 创建数据文件夹
mkdir data
mkdir data/judge
mkdir data/media
mkdir data/temp
mkdir data/test_case
# 安装项目依赖
pip install -r requirements.txt
# 迁移数据库
python manage.py makemigrations
python manage.py migrate