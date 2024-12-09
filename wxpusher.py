#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WxPusher Python SDK.

File: wxpusher.py
Author: huxuan
Email: i(at)huxuan.org
"""
import requests
import os
import json

import exceptions

BASEURL = 'http://wxpusher.zjiecode.com/api'


class WxPusher():
    """WxPusher Python SDK."""

    default_token = None
    default_topic_ids = None

    @classmethod
    def send_message(cls, content, **kwargs):
        """Send Message."""
        payload = {
            'appToken': kwargs.get('token',cls.default_token),
            'content': content,
            'summary': kwargs.get('summary'),
            'contentType': kwargs.get('content_type', 1),
            'topicIds': kwargs.get('topic_ids', cls.default_topic_ids),
            'uids': kwargs.get('uids', []),
            'verifyPay': kwargs.get('verify'),
            'url': kwargs.get('url'),
        }
        print(payload)
        url = f'{BASEURL}/send/message'
        return requests.post(url, json=payload).json()

    @classmethod
    def query_message(cls, message_id):
        """Query message status."""
        url = f'{BASEURL}/send/query/{message_id}'
        return requests.get(url).json()

    @classmethod
    def create_qrcode(cls, extra, valid_time=1800, token=None):
        if not token:
            return
        """Create qrcode with extra callback information."""
        payload = {
            'appToken': cls._get_token(token),
            'extra': extra,
            'validTime': valid_time,
        }
        url = f'{BASEURL}/fun/create/qrcode'
        return requests.post(url, json=payload).json()

    @classmethod
    def query_user(cls, page, page_size, token=None):
        if not token:
            return
        """Query users."""
        payload = {
            'appToken': cls._get_token(token),
            'page': page,
            'pageSize': page_size,
        }
        url = f'{BASEURL}/fun/wxuser'
        return requests.get(url, params=payload).json()

    @classmethod
    def _get_token(cls, token=None):
        """Get token with validation."""
        token = token or cls.default_token
        if not token:
            raise exceptions.WxPusherNoneTokenException()
        return token

# 读取API配置
if not os.path.exists("api.conf"):
    raise FileNotFoundError("未找到`./api.conf`文件，请遵循README提示操作")
with open("api.conf", encoding="utf-8") as f:
    api_conf = json.load(f)
    WxPusher.default_token = api_conf['wxpush_token']
    WxPusher.default_topic_ids = api_conf['wxpush_topic_ids']

if __name__ == "__main__":
   res = WxPusher.send_message(
                "testgd"
            )
   print(res)