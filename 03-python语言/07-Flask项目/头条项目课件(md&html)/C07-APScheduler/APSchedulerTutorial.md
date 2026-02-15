# APScheduler使用

> - APScheduler （advanceded python scheduler）是一款Python开发的定时任务工具。
>
> - 文档地址 <https://apscheduler.readthedocs.io/en/latest/userguide.html#starting-the-scheduler>
> - 参考文档<https://www.jianshu.com/p/4f5305e220f0>

[TOC]

<!-- toc -->

## 1. APScheduler特点

> - 特点：
>   - 不依赖于Linux系统的crontab系统定时，独立运行
>   - 可以动态添加新的定时任务
>     - 如:下单后30分钟内必须支付，否则取消订单，就可以借助此工具（每下一单就要添加此订单的定时任务）
>   - 对添加的定时任务可以做持久保存
> - APScheduler由四大组件构成：
>   - 执行器 `executors`： 用于执行任务，可以设定执行模式为单线程或线程池
>   - 触发器 `triggers` ：用于设定触发任务的条件
>   - 任务储存器 `job stores`：用于存放任务，把任务存放在内存或数据库中，可以持久化存储
>   - 调度器 `schedulers`： 把上方三个组件作为参数，通过创建调度器实例来运行



## 2. 安装和使用方式

### 2.1 安装

```shell
pip install apscheduler
```

### 2.2 使用方式

> - 定义执行器字典
> - 实例化调度器
> - 添加任务
> - 开启定时任务
>
> ```python
> from datetime import datetime
> 
> from apscheduler.schedulers.background import BackgroundScheduler # 非阻塞调度器 可以在其他程序中使用，比如在flask中使用
> from apscheduler.schedulers.blocking import BlockingScheduler # 阻塞调度器 独立进程时使用
> 
> from apscheduler.executors.pool import ProcessPoolExecutor # 进程执行器
> from apscheduler.executors.pool import ThreadPoolExecutor # 线程执行器
> 
> # 1. 定义执行器字典
> executors = {
> 'default': ThreadPoolExecutor(max_workers=5), # 执行任务的最大线程数为5
> # 'default': ProcessPoolExecutor(max_workers=5), # 执行任务的最大进程数为5
> }
> 
> # 2. 实例化调度器
> # scheduler = BlockingScheduler(executors=executors) # 阻塞调度器
> scheduler = BackgroundScheduler(executors=executors) # 非阻塞调度器，异步执行
> 
> # 定义要定时执行的任务
> def func(name, age):
>     print('{}此时此刻{}岁了！过生日了！'.format(name, age))
> 
> # 3. 添加任务
> # 3.1 date触发器，只执行一次（当前一次和下一次，最多可以执行2次）
> # scheduler.add_job(func, 'date', run_date=datetime(2019, 7, 14, 23, 31, 50), args=['狗丫', 18])
> scheduler.add_job(func, 'date', run_date=datetime.now()+timedelta(seconds=10), args=['狗丫', 18])
> # datetime.datetime() 返回的是UTC时间，所以使用datetime.now()+timedelta(seconds=10)更方便计算
> 
> # 3.2 interval触发器，周期执行，参数为时间间隔
> # scheduler.add_job(func, 'interval', seconds=2, args=['狗丫', 18])
> 
> # 3.3 cron触发器，周期执行，参数为（x年）x月x日星期x，x点x分x秒执行
> scheduler.add_job(func, 'cron', year=2019, month=9, day=2,
>                   hour=3, minute=39, second=1, args=['狗丫', 18])
> 
> # 4. 定时任务开启
> scheduler.start()
> 
> while 1:
>     print(datetime.now())
>     sleep(10)
> ```

## 3. 使用方式解读

### 3.1 任务储存器job stores

> > **默认情况下，任务存放在内存中**。也可以配置存放在不同类型的数据库中。如果任务存放在数据库中，那么任务的存取有一个序列化和反序列化的过程，同时修改和搜索任务的功能也是由任务储存器实现。
>
> - toutiao项目中将定时任务放到了内存中，如果你想了解数据库中用法，请参考文档或博客
>   - 文档地址 <https://apscheduler.readthedocs.io/en/latest/userguide.html#starting-the-scheduler>
>   - 参考文档<https://www.jianshu.com/p/4f5305e220f0>

### 3.2 调度器scheduler 

> > 负责管理定时任务
>
> - `BlockingScheduler`:  作为独立进程时使用
>
>   ```python
>   from apscheduler.schedulers.blocking import BlockingScheduler
>   
>   scheduler = BlockingScheduler()
>   scheduler.start()  # 此处程序会发生阻塞
>   ```
>
> - `BackgroundScheduler`:  在框架程序（如Django、Flask）中使用
>
>   ```python
>   from apscheduler.schedulers.background import BackgroundScheduler
>   
>   scheduler = BackgroundScheduler()
>   scheduler.start()  # 此处程序不会发生阻塞 
>   ```

### 3.3 执行器executors

> 在定时任务该执行时，以进程或线程方式执行任务
>
> - ThreadPoolExecutor
>
>   使用方法
>
>   ```python
>   from apscheduler.executors.pool import ThreadPoolExecutor
>   executors = {
>       'default': ThreadPoolExecutor(20) # 最多20个线程同时执行
>   }
>   scheduler = BackgroundScheduler(executors=executors)
>   ```
>
> - ProcessPoolExecutor
>
>   使用方法
>
>   ```python
>   from apscheduler.executors.pool import ProcessPoolExecutor
>   executors = {
>       'default': ProcessPoolExecutor(max_workers=5) # 最多5个进程同时执行
>   }
>   scheduler = BackgroundScheduler(executors=executors)
>   ```

### 3.4 触发器trigger 

> 指定定时任务执行的时机
>
> - date触发器 在特定的时间日期执行
>
>   > 只执行一次（当前一次和下一次，最多可以执行2次）
>
>   ```python
>   from datetime import date
>   
>   # 在2019年11月6日00:00:00执行
>   sched.add_job(my_job, 'date', run_date=date(2009, 11, 6))
>   
>   # 在2019年11月6日16:30:05
>   sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5))
>   sched.add_job(my_job, 'date', run_date='2009-11-06 16:30:05')
>   
>   # 立即执行
>   sched.add_job(my_job, 'date')  
>   sched.start()
>   ```
>
> - interval触发器 经过指定的时间间隔执行
>
>   > 周期执行，参数为时间间隔
>
>   ```python
>   from datetime import datetime
>   
>   # 每两小时执行一次
>   sched.add_job(job_function, 'interval', hours=2)
>   
>   # 在2010年10月10日09:30:00 到2014年6月15日的时间内，每两小时执行一次
>   sched.add_job(job_function, 'interval', hours=2, start_date='2010-10-10 09:30:00', end_date='2014-06-15 11:00:00')
>   ```
>
>   > - **weeks** (*int*) – number of weeks to wait
>   > - **days** (*int*) – number of days to wait
>   > - **hours** (*int*) – number of hours to wait
>   > - **minutes** (*int*) – number of minutes to wait
>   > - **seconds** (*int*) – number of seconds to wait
>   > - **start_date** (*datetime|str*) – starting point for the interval calculation
>   > - **end_date** (*datetime|str*) – latest possible date/time to trigger on
>   > - **timezone** (*datetime.tzinfo|str*) – time zone to use for the date/time calculations
>
>   ```python
>   
>   ```
>
> - cron触发器 按指定的周期执行
>
>   > 周期执行，参数为（x年）x月x日星期x，x点x分x秒执行
>
>   ```python
>   # 在6、7、8、11、12月的第三个周五的00:00, 01:00, 02:00和03:00 执行
>   sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
>   
>   # 在2014年5月30日前的周一到周五的5:30执行
>   sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')
>   ```
>
>   > - **year** (*int|str*) – 4-digit year
>   > - **month** (*int|str*) – month (1-12)
>   > - **day** (*int|str*) – day of the (1-31)
>   > - **week** (*int|str*) – ISO week (1-53)
>   > - **day_of_week** (*int|str*) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
>   > - **hour** (*int|str*) – hour (0-23)
>   > - **minute** (*int|str*) – minute (0-59)
>   > - **second** (*int|str*) – second (0-59)
>   > - **start_date** (*datetime|str*) – earliest possible date/time to trigger on (inclusive)
>   > - **end_date** (*datetime|str*) – latest possible date/time to trigger on (inclusive)
>   > - **timezone** (*datetime.tzinfo|str*) – time zone to use for the date/time calculations (defaults to scheduler timezone)

### 3.5 添加任务

> - `调度器(executors=执行器字典).add_job(任务函数没有括号, '触发方式', 时间参数, args=[任务函数参数], kwargs={任务函数参数})`，如：
>
> ```python
> scheduler.add_job(func, 'cron', minute=23, args=['狗丫', 18])
> ```

### 3.6 启动

```python
scheduler.start()
```

> - 注意：再提醒一下！
>   - 对于BlockingScheduler ，程序会阻塞在这，防止退出
>     - 独立使用APScheduler时使用
>   - 对于BackgroundScheduler，程序会立即返回，后台运行
>     - 在其他进程中使用APScheduler时使用

## 4. [拓展]任务管理

### 4.1 任务管理的方式

> - 方式1
>
>   ```python
>   job = scheduler.add_job(myfunc, 'interval', minutes=2)  # 添加任务
>   job.remove()  # 删除任务
>   job.pause() # 暂定任务
>   job.resume()  # 恢复任务
>   ```
>
> - 方式2
>
>   ```python
>   scheduler.add_job(myfunc, 'interval', minutes=2, id='my_job_id')  # 添加任务	
>   scheduler.remove_job('my_job_id')  # 删除任务
>   scheduler.pause_job('my_job_id')  # 暂定任务
>   scheduler.resume_job('my_job_id')  # 恢复任务
>   ```

### 4.2 停止APScheduler运行

> ```python
> scheduler.shutdown()
> ```





