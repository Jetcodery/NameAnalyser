# NameAnalyser

我们家蓁蓁宝宝今年农历三月出生，为了起名方便，在陪产假期间结合部分repo重新实现了本起名脚本，便于快速获得名字的含义、计算笔画数、生辰八字评分、五格评分等等；

## 环境准备：

1、Python3.6及以上

2、因为需要模拟浏览器行为，selenium需要浏览器驱动，仅测试过Chrome浏览器，需注意浏览器版本号，在https://chromedriver.storage.googleapis.com/index.html中查找对应版本号的chromedriver，下载后放置于python解析器的同目录下（使用which python获得路径，如：/path/to/anaconda3/envs/Jet_python3/bin/python, 则应放置于bin目录下）

3、环境安装，依赖版本参考requirements.txt：

`pip install -r requirements.txt`

## 使用方法：



#### 1、编辑config.yaml脚本，输入需要的信息：

```yaml
NameInfo:
  LastName: '李'                               # 姓氏
  FirstName0: ['芃', '蓁']                     # 名字第一个字，输入一些喜欢的字
  FirstName1: ['澄', '泽', '沐', '朔', '浚']    # 名字第二个字，输入一些喜欢的字

BirthInfo:
  DateType: '阳历'                             # 一般不用改
  Year: 2023                                  # 诞生年
  Month: 5                                    # 诞生所在月（阳历）
  Day: 20                                     # 诞生日（阳历）
  Hour: 18                                    # 诞生时（不记得就随便填个吧）
  Minute: 27                                  # 诞生分（不记得就随便填个吧）
  BirthProvince: '上海'                        # 诞生省
  BirthCity: '上海'                            # 诞生市
  Sex: '男'                                    # 性别
  RealSunTime: '否'                            # 是否使用真太阳时（不用管）

Runner:
  SleepTime: 1                                # 请求表单间隔时间
  OutputDir: 'output3'                        # 定义一个输出目录
```



#### 2、执行main.py脚本

`python main.py`



## 注意事项

1、实现过程不太严谨，未对各种边界情况做测试，比如暂时不支持四个字的名字等等，欢迎提issue进行改进；

2、免责声明：脚本使用selenium对"http://life.httpcn.com/xingming.asp"进行模拟浏览访问获取信息，请勿暴力调用或用于商业盈利等；

3、本项目仅供娱乐，产出的内容仅供参考。

4、鸣谢：

```
# https://github.com/pwxcoo/chinese-xinhua
# https://github.com/chinese-poetry
# https://github.com/peiss/chinese-name-score
# https://github.com/CrystalMarch/bazi
```

