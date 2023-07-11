import time
import datetime

CertEndTime = 1714838399000

# 转换成localtime
time_local = time.localtime(CertEndTime / 1000)
# 转换成新的时间格式(精确到秒)
dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
print(dt)  # 2024-05-04 23:59:59




d = datetime.datetime.fromtimestamp(CertEndTime / 1000)
# 精确到毫秒
str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
print(str1)  # 2024-05-04 23:59:59.000000