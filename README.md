基于Python Flask定时通过邮件发送天气预报。天气数据来自高德天气查询API，参考https://lbs.amap.com/api/webservice/guide/api/weatherinfo。
当前通过 Python schedule 模块实现 JOB 任务。但缺点非常明显：
1. 通过启动和关闭Flask应用控制
