#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Author:shichao
# File: .py

import wmi
import socket, json
from datetime import datetime, date, timedelta

try:
    from urllib import request
except:
    import urllib2 as request

w = wmi.WMI()


class WinTest():
    def __init__(self):
        self.result = {}

    # import osimport socketw = wmi.WMI()

    def os_version(self):
        # 获取操作系统信息for OS in w.Win32_OperatingSystem():
        for OS in w.Win32_OperatingSystem():
            # return OS)
            os = OS.Caption
        return os

    def cpu_num(self):
        # 获取电脑CPU信息for processor in w.Win32_Processor():
        for processor in w.Win32_Processor():
            # return processor)
            cpunucleus = ("%s核" %processor.NumberOfCores)
        return cpunucleus

    def cpu_model(self):
        # 获取电脑CPU信息for processor in w.Win32_Processor():
        for processor in w.Win32_Processor():
            # return processor)
            cpu = processor.Name.strip()
        return cpu

    def memory(self):
        # 获取内存信息for memModule in w.Win32_PhysicalMemory():
        for memModule in w.Win32_PhysicalMemory():
            totalMemSize = int(memModule.Capacity)
            mem = "%dGB" % (totalMemSize / 1024 ** 3)
        return mem

    def disk(self):
        disk_list = []
        # 获取磁盘信息for disk in w.Win32_DiskDrive():
        for physical_disk in w.Win32_DiskDrive():
            for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    diskname = logical_disk.Caption[:1],
                    disksize = ("%dGB" %(int(logical_disk.Size) / (1024 **3)))
                    disk_list.append({'device': diskname[0], 'size': disksize, 'type': 'None'})

        return disk_list

    def hostname(self):
        # 获取计算机名称和IP hostname = socket.gethostname()ip = socket.gethostbyname(hostname)return "计算机名称: %s" %hostname)
        hostname = socket.gethostname()
        return hostname

    def private_ip(self):
        ip_list = []
        for interface in w.Win32_NetworkAdapterConfiguration(IPEnabled='TRUE'):
            ip_list.append(interface.IPAddress[0])
        return ip_list

    def public_ip(self):
        private_ip = self.private_ip()
        ip_api_url = ['http://ip.renfei.net', 'http://ifconfig.me/ip']
        ip_list = []
        try:
            req = request.Request(url=ip_api_url[0])
            res = request.urlopen(req)
            ip = json.loads(res.read().decode())['clientIP']
        except:
            req = request.Request(url=ip_api_url[1])
            res = request.urlopen(req)
            ip = res.read().decode()
        if ip in private_ip:
            ip.append(ip)
            return ip_list
        else:
            ip_list.append('%s' %ip)
            return ip_list
    def network_out(self):
        # 获取最大带宽
        for interface in w.Win32_NetworkAdapterConfiguration():
            index = int(interface.InterfaceIndex)
            for i in w.Win32_NetworkAdapter(Index=index):
                if (i.Speed):
                    network= ("%dM" % (int(i.Speed) / (1000 * 100)))
                    return network


    def get_all(self):
        """
        这里字段必须与API对应
        """
        self.result = {
            "hostname": self.hostname(),
            "os_version": self.os_version(),
            "public_ip": self.public_ip(),
            "private_ip": self.private_ip(),
            "cpu_num": self.cpu_num(),
            "cpu_model": self.cpu_model(),
            "memory": self.memory(),
            "network": self.network_out(),
            "disk": self.disk(),
        }
        json_data = json.dumps(self.result)
        return json_data


if __name__ == "__main__":
    data = WinTest()
    try:
        print(data.get_all())
    except Exception as e:
        result = {'code': 500, 'msg': '采集脚本执行失败！错误：%s' % e}
        print(json.dumps(result))