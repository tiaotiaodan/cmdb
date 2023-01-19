#!/usr/bin/python3
# coding:utf-8

"""
获取所有的vcenter相关信息
包括exsi的硬件资源信息和vmware客户端的硬件分配信息
"""
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
import atexit
import argparse
import json


# 面向对象操作
class EsxiApi():
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password


        Esxi_Connect = SmartConnectNoSSL(host=self.ip, port=self.port, user=self.username, pwd=self.password)
        atexit.register(Disconnect, Esxi_Connect)
        content = Esxi_Connect.RetrieveContent()
        esxi_content = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        esxi_obj = [view for view in esxi_content.view]
        self.esxi_obj = esxi_obj

    def hostname(self):
        for esxi in self.esxi_obj:
            hostname = esxi.summary.config.name
        return hostname

    def os_version(self):
        for esxi in self.esxi_obj:
            os_version = "%s" % esxi.summary.config.product.fullName

        return os_version

    def public_ip(self):
        ip_list= []
        public_ip = "%s" % self.ip
        ip_list.append(public_ip)
        return ip_list

    def private_ip(self):
        ip_list = []
        private_ip = "%s" % self.ip
        ip_list.append(private_ip)
        return ip_list

    def cpu_num(self):
        for esxi in self.esxi_obj:
            cpu_num = "%s核" % (int(esxi.summary.hardware.numCpuCores) * int(esxi.summary.hardware.numCpuPkgs))
        return cpu_num

    def cpu_model(self):
        for esxi in self.esxi_obj:
            cpu_model = "%s" % esxi.summary.hardware.cpuModel
        return cpu_model

    def memory(self):
        for esxi in self.esxi_obj:
            memory = "%.2fG" % (esxi.summary.hardware.memorySize / 1024 / 1024 / 1024)
        return memory

    def disk(self):
        disk = []
        for esxi in self.esxi_obj:
            for ds in esxi.datastore:
                device = ds.name
                size = "%dGB" % (int(ds.summary.capacity) / 1024 / 1024 / 1024)
                type = "%s" % ds.summary.type
                disk.append({'device': device, 'size': size, 'type': type})
        return disk

    def network(self):
        for esxi in self.esxi_obj:
            for nt in esxi.network:
                print(nt)

        return nt

    def get_all(self):
        """
        这里字段必须与API对应
        """
        self.result = {
            #"hostname": self.hostname(),
            "os_version": self.os_version(),
            "public_ip": self.public_ip(),
            "private_ip": self.private_ip(),
            "cpu_num": self.cpu_num(),
            "cpu_model": self.cpu_model(),
            "memory": self.memory(),
            "disk": self.disk(),
            #"network": self.network(),
            # "put_shelves_date": self.system_up_time(),  # 上架时间默认设置系统启动时间
        }
        try:
            json_data = json.dumps(self.result)
            result = {"code": 200, "msg":"获取数据成功", "data": json_data }
        except Exception as e:
            result = {'code': 500, 'msg': '采集脚本执行失败！错误：%s' % e}
        return result

if __name__ == '__main__':


    esxi = EsxiApi("172.16.128.89", 443, "root", "Sobey@2021")
    result = esxi.get_all()
    print(result)
