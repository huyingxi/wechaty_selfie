# wechaty_selfie
一个给图片评分的wechaty项目

* Chatie Blog: [Score Your Face Photo: a ML & Wechaty practice](https://blog.chatie.io/2017/09/18/wechaty-selfie-bot.html)

# 效果演示
<img src = https://github.com/huyingxi/wechaty_selfie/blob/master/hello.gif height="550"/>

## 所需包：
* pylab：用于绘图
* matplotlib:用于绘图
* requests：用于处理http请求
* numpy：用于矩阵运算
* h5py：用于数据集的格式处理
* keras：用于深度学习

## 建模步骤：
* Step 1 : 首先针对获取到的数据进行第一步筛选：时间筛选，筛选出存在时间大于2000秒的数据.因为Instagram只能爬取到最近发布的动态，所以我们尽可能的筛选出发布时间最久的动态；
* Step 2 : 对上一步筛选的数据进行分析，获取点赞数和粉丝数并绘图；
* Step 3 : 首先将点赞数和该点赞数的个数进行绘制，查看点赞数的分布情况:可见大多分布在0-10（甚至0-8）之间 因此直接将用户点赞数当作评分，构造一个0-9的10分类问题；
* Step 4 : 然后查看上一步筛选出来的数据，将重要数据：点赞数、粉丝数进行统计。根据之前统计的经验，我们决定直接将点赞数作为评分，并将该数据写入data_new_grade_direct；
* Step 5 : 下载图片，访问刚才筛选出来的图片URL，data_new_grade_direct.txt,将下载好的图片reshape成224，224大小；
* Step 6 : 将下载好的图片和评分一起存储为h5格式；
* Step 7 : 搭建神经网络，采用图像处理先进网络VGG16进行特征提取，并在顶层添加了5个全连接层，最后是一个10分类的softMax输出，并将训练好的模型存储下来，以便在webselfie工程中调用。

## 使用指南：
* 用户发送'selfie', 回复"请发一张你的头像"。
   * 若用户回复消息为图片格式,则获取评分。
   * 否则,回复"发送的不是图片格式,请重新发送selfie"

## 补充：
* 因为我们下载的数据集：Instgram上面爬取的带SELFIE标签的动态，都是最新发布的，所以得到的点赞数非常少。大多为0赞，其余多分布在0-10之间。
对于这样的数据集，我们尝试了多种评分规则，都没有规律可循，必须诚实的说，最终我们的模型也没有被训练起来，模型能给出评分，但是这样的评分不具备现实意义。
* 模型采用的是VGG16+五个全连接层。
