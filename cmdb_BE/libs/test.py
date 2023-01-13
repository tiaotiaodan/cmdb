#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py
import json

def test():
    result = {
        "test": "Uploaded file successfully, executed successfully",
    }
    json_data = json.dumps(result)
    return json_data



if __name__ == "__main__":
    data = test()
    try:
        print(data)
    except Exception as e:
        result = {'code': 500, 'msg': 'Execution failed'}
        print(json.dumps(result))