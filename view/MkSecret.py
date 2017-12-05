#!/usr/bin/env python
#coding:utf-8

import hashlib
def mkaesecret(data):
    examp = hashlib.md5()
    examp.update(data)
    result = examp.hexdigest()
    return  result