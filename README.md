# XDOJ 在线编程评测系统

[![Python](https://img.shields.io/badge/Python-3.6-fee05c)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.0.6-51be95)](https://www.djangoproject.com/)
[![Lorun](https://img.shields.io/badge/Lorun-1.0.1-075fbb)](https://github.com/aditnryn/lorun)
[![license](https://img.shields.io/badge/license-Apache--2.0-green)](https://github.com/AntXinyuan/XDOJ/blob/master/LICENSE)

XDOJ 是一个基于 Python Django 开发的 Web 网站项目（后端部分），用于编程训练评测（Online Judge），提供了公告通知、常规练习、比赛排名、数据统计等实用功能。

本项目是对 [QDUOJ](https://github.com/QingdaoU/OnlineJudge) 的一个模仿精简，沙箱评测功能基于 [Lorun](https://github.com/aditnryn/lorun) 开发。

<p align="center">
<img src="images\XDOJ系统架构图.png" width="80%">
</p>

## 系统流程

系统的核心功能为评测用户提交的解题代码并将对应状态返回给用户，因此整个流程将围绕这一功能展开。具体地，系统流程分*Web部分*和*评测部分*，前者负责对接用户的各类操作，后者负责安全、高效的评测用户代码，整个流程如图所示。

<p align="center">
<img src="images\XDOJ系统流程图_扁平.png" width="90%">
</p>

## 模块设计

项目包含题目(problem)、提交(submission)、比赛(contest)、账户(account)、公告(announcement)、关于(about) 6个模块，针对管理员与普通用户共涉及 28 项功能操作。模块设计如图所示，操作详情见 [Postman-api 文档](https://documenter.getpostman.com/view/9488578/SzmZc135?version=latest)。

<p align="center">
<img src="images\XDOJ模块设计图.png" width="90%">
</p>

## 安装运行
- 系统所需的各项依赖记录于 requirements.txt，使用者可自行安装。
  ```bash
  pip install -r requirements.txt
  ```

- 为便于使用者安装，我们提供了一键初始化脚本 init.sh。
  ```bash
  ./init.sh
  ```

- 当需要运行服务时，可以使用如下命令：
  ```bash
  python manage.py runserver
  ```


## 引用

如果你觉得这个项目对你的研究有帮助的话，请考虑引用：

```bibtex
@misc{xdoj,
    title={XDOJ在线编程评测系统},
    author={XDOJ Contributors},
    howpublished = {\url{https://github.com/AntXinyuan/XDOJ}},
    year={2020}
}
```