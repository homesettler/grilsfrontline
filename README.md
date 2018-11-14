# grilsfrontline
少女前线手游 模拟器Python脚本（python3.6 windows）

# 环境配置
环境需求： 

  windows
  
  python3.6
  
  模拟器:网易MuMu模拟器(理论上可更换)
  
  客户端:安卓哔哩哔哩服

python包

  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow
  
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pywin32
  
# 注意事项

1. 屏幕缩放比例需调至100%
2. 因电脑硬件水平和网速水平不一，第一次运行脚本时可以根据需要调整PING参数的值，理论上越卡PING越大，PING的值为操作时等待的秒数，第二次运行时，可将PING修改为0
3. 脚本会在当前目录下创建一个"init"文件夹里面是初始化的截图，具体会在原理中说明
4. 运行脚本时需要游戏处于主界面，运行脚本后，开始的5s内请将当前应用设置为模拟器，中途不可进行操作。

# 原理
通过截取当前屏幕的某一块区域并与init文件夹中的图片比较相似度，判断当前所处的界面来判断操作是否结束。
运用pywin32 模拟鼠标点击，滚轮，键盘输入。

# 脚本运行流程
未完成

# 尚待开发
