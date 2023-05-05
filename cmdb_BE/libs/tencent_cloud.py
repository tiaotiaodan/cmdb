from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models

# 获取域名列表
from tencentcloud.domain.v20180808 import domain_client, models

import json

class TCloud():
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.cred = credential.Credential(self.secret_id, self.secret_key)

    # 获取地区
    def region_list(self):
        client = cvm_client.CvmClient(self.cred, None)
        req = models.DescribeRegionsRequest()  # 获取地区
        try:
            resp = client.DescribeRegions(req)  # resp=[{"Region": "ap-guangzhou", "RegionName": "华南地区(广州)", "RegionState": "AVAILABLE"}, ]
            resp.code = 200
            return resp
        except TencentCloudSDKException as e:
            return {'code': '500', 'msg': e.message}
    # 可用区
    def zone_list(self, region_id):
        client = cvm_client.CvmClient(self.cred, region_id)
        req = models.DescribeZonesRequest()
        try:
            resp = client.DescribeZones(req)
            resp.code = 200
            return resp
        except TencentCloudSDKException as e:
            return {'code': '500', 'msg': e.message}
    # 实例信息数据查询
    def instance_list(self, region_id):
        client = cvm_client.CvmClient(self.cred, region_id)  # 获取上海区域
        req = models.DescribeInstancesRequest()
        # req.InstanceIds = "ins-1511w4tn" #根据实例id获取
        try:
            resp = client.DescribeInstances(req)
            resp.code = 200
            return resp
        except TencentCloudSDKException as e:
            return {'code': '500', 'msg': e.message}

    # 获取账号下所有域名
    def domain_list(self, Offset, Limit ):
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = domain_client.DomainClient(self.cred, "")
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeDomainNameListRequest()
        try:
            params = {
                "Offset": Offset,
                "Limit": Limit
            }
            req.from_json_string(json.dumps(params))
            # 返回的resp是一个DescribeDomainBaseInfoResponse的实例，与请求对象对应
            resp = client.DescribeDomainNameList(req)
            resp.code = 200
            return resp
        except TencentCloudSDKException as e:
            return {'code': '500', 'msg': e.message}


if __name__ == '__main__':
    cloud = TCloud("ID", "KEY")
    # result = cloud.region_list()
    # result = cloud.zone_list("ap-shanghai")
    # result = cloud.instance_list("ap-shanghai")
    result = cloud.domain_list(0, 100)
    print(result)

    print(result.DomainSet)
    print(result.DomainSet[0].IsPremium)

    print(result.DomainSet[0].DomainName)

    code = result.code
    print(code)
