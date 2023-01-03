#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
# 地区
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
# 可用区
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
# 实例
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
# 硬盘请求
from aliyunsdkecs.request.v20140526.DescribeDisksRequest import DescribeDisksRequest

# 导入json
import json


# 封装类方法
class AliCloud():
    # 获取id和key
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    # 地区
    def region_list(self):
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeRegionsRequest()
        try:
            res = client.do_action_with_exception(req)
            data = json.loads(res.decode())
            return {'code': 200, 'data': data}
        except Exception as e:
            return {'code': 500, 'msg': e.get_error_msg()}

    # 可用区
    def zone_list(self, region_id):
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeZonesRequest()
        req.add_query_param('RegionId', region_id)
        try:

            res = client.do_action_with_exception(req)
            data = json.loads(res.decode())
            return {'code': 200, 'data': data}
        except Exception as e:
            return {'code': 500, 'msg': e.get_error_msg()}

    # 实例
    def instance_list(self, region_id):
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeInstancesRequest()
        req.add_query_param('RegionId', region_id)
        try:
            res = client.do_action_with_exception(req)
            data = json.loads(res.decode())
            return {'code': 200, 'data': data}
        except Exception as e:
            return {'code': 500, 'msg': e.get_error_msg()}

    # 实例关联的硬盘
    def instance_disk(self,instance_id):
        client = AcsClient(self.secret_id, self.secret_key)
        req = DescribeDisksRequest()
        req.add_query_param('InstanceId',instance_id)
        try:
            res = client.do_action_with_exception(req)
            data = json.loads(res.decode())
            return {'code': 200, 'data': data}
        except Exception as e:
            return {'code': 500, 'msg': e.get_error_msg()}


if __name__ == '__main__':
    cloud = AliCloud('xxxxx', 'xxxxx')
    result = cloud.region_list()
    result = cloud.zone_list('cn-chengdu')
    result = cloud.instance_list('cn-chengdu')
    result = cloud.instance_disk('i-2vca412cljeu1qux48a2')

    print(result)