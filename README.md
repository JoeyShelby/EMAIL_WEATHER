基于Python Flask定时通过邮件发送天气预报。天气数据来自高德天气查询API，参考https://lbs.amap.com/api/webservice/guide/api/weatherinfo。
当前通过 Python APScheduler 模块实现 JOB 任务。
每日天气发送
每天通过邮件发送：
今日温度
体感温度
和昨天相比
降雨
需要带伞，穿衣推荐
…..
目前实现：
每天通过邮件发送天气信息，如下所示：
![image](https://github.com/JoeyShelby/EMAIL_WEATHER/assets/57031953/93bdc7ac-7824-4be5-aa79-a808a1ab10e2)

不足：
- 目前只能通过访问/启动任务，停止任务通过重启docker 容器。
- 在前台发送时间不可配置，邮箱地址不可配置，日志不可见
- 邮箱和地区需要手动配置

改进
- [ ] 重新配置下服务器，现在是开发机
- [x] 处理好重复发送问题（用apscheduler做后台任务，好用！）
- [ ] 前台功能：打开，关闭，配置JOB，前台配置邮件地址，查看日志
- [ ] 给一个用户能填邮箱和地址的前台页面

当前工作：
做一个前台页面，让用户维护自己的邮箱和城市。
初步实现：用户查询自己的邮箱，如果存在，显示当前维护的城市。（暂不开放用户直接新建邮箱和城市代码，因为用户可能会乱填。后期实现用户邮箱确认新建）。
- [x] 使用数据库管理receivers表(使用mysql,SQL脚本回头记得传)
- [ ] 前台页面
