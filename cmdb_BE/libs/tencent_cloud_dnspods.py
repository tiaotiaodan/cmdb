from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

# dnspods域名解析
from tencentcloud.dnspod.v20210323 import dnspod_client, models

import json

class TCloud_Dnspod():
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.cred = credential.Credential(self.secret_id, self.secret_key)


    # 获取域名解析
    def domain_dnspods_list(self, domain_name):
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(self.cred, "")
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeRecordListRequest()
        try:
            params = {
                "Domain": domain_name
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个DescribeRecordListResponse的实例，与请求对象对应
            resp = client.DescribeRecordList(req)
            return resp
        except TencentCloudSDKException as e:
            return {'code': '500', 'msg': e.message}


if __name__ == '__main__':
    cloud = TCloud_Dnspod("ID", "key")
    # result = cloud.region_list()
    # result = cloud.zone_list("ap-shanghai")
    # result = cloud.instance_list("ap-shanghai")
    result = cloud.domain_dnspods_list("fwqaq.cn")
    print(result)
