---
layout: post
title: "'Rate Your Face Photo' a ML&Wechaty practice"
date: 2017-09-17 21:00 +0800
author: huyingxi
---

> Author: [@huyingxi](https://github.com/huyingxi/wechaty_selfie) enjoying ML&Wechaty at BUPT

Recently I found a fun and easy to use middleware for WeChat, called [Wechaty](https://github.com/Chatie/wechaty).
Wechaty can help developers quickly build applications based on Wechat, and it was born with a huge number of Potential users. 

So I build a fun application based on Wechaty - [wechaty_selfie](https://github.com/huyingxi/wechaty_selfie)!
This is a ChatBot that can score the self-portrait.

------
Which one is more beautiful?
Say goodbye to your choice of difficulty!
------

<div align=center>
<img src=https://github.com/huyingxi/wechaty_selfie/blob/master/li.jpg width='700px' />
</div>


<!--more-->

## Screenshot of the application
<div align=center>
<img src=https://github.com/huyingxi/wechaty_selfie/blob/master/result.jpg width="400px" />
</div>

## Our development steps
Once you have a little nodejs knowledge, and a little deep learning basis, you can build it.

* Build the deep learning model
The most important of this course is the data. We crawled data(eg. picture URL, release time, the number of praise, the number of comments)  with 'selfie' label from instagram. 
* Filter data
In order to make the training data more convincing, we will release a long time to retain the dynamic information, because we default release time is greater than the threshold of the dynamic access to the number of comments, the number of comments is stable, and the release time is lower than The dynamics of this threshold may not have been sufficient to get enough exposure, here because we crawled the data is not good enough, the time threshold is set to 2000 seconds.
* Scoring strategy selection
According to the screening after the dynamic information (self-timer picture URL, the number of praise, the number of comments) and other mapping analysis, view the distribution of the number of praise, we found that most of the points like 0-10, so we are simple and rude Will point praise as a score, and here you can try several variants of the number of features, such as the number of praise + comments and other prescriptions.
* Download  pictures
According to the filter after the self-timer picture URL to download pictures, and download the image down reshape, into 224 * 224 dimensions
* Build DL model
To build the neural network, in order to quickly build, we use the image processing network VGG16 feature extraction, and in the top layer to add five full connection layer, and finally a 10 classification of softMax output, and training models to store down, In order to call in the webselfie project
* Build project
Build wechaty project, including wechaty module and depth learning picture grading model.
* debugging, success



## Appendix, packages we used

* pylab: used for drawing
* matplotlib: used for drawing
* requests: used to handle http requests
* numpy: used for matrix operations
* h5py: used for formatting data sets
* keras: for deep learning
* Wechaty: wechat middleware
* Fs: used to transfer pictures


## Some optimization recommendations
If you are interested, would like to take this one application for their own and friends around the self-portrait photo recommendations. Then you can consider how many points:
* (1) If you want to use insta's selfie picture when training data, it must crawl for a long time, the score is stable.
* (2) can try several different scoring strategies, I think this is the most fun.
* (3) can build a more complex depth of learning model. There should be a model that is more applicable to the scene.



## Finally
I strongly recommend that you now click on the link below, there are surprises waiting for you！

[Wechaty](https://github.com/Chatie/wechaty)
