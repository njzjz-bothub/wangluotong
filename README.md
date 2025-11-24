# WangLuoTong

`wangluotong` is a command-line tool to log in to USTC WLT.

## Installation

In a server at USTC, assume you have a Python environment, and then run

```bash
pip install wangluotong -i https://mirrors.ustc.edu.cn/pypi/simple
```

## Usage

```bash
wangluotong --username <username> --password <password>
```

You can also set environment variables:
```bash
export WANGLUOTONG_USERNAME=<username>
export WANGLUOTONG_PASSWORD=<password>
wangluotong
```
