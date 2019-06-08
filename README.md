# README

这是数字图像处理的第三次作业，做的是图像边缘检测，稍微整理了一下，没怎么封装。

## Catalog

1. Filters
2. Noise
3. Dark light
4. HedHED(Holistically-Nested Edge Detection ( 整体嵌套
   边缘检测 ))
5. ~~Corrosion & Expansion(腐蚀膨胀)~~

## Filters

### prewitt:

![](https://github.com/butub1/Edge-detection/blob/master/Submission/images/image3.png)

可以看出x, y 分别提取x方向和y方向的边缘

使用绝对值(l1范数)和使用l2范数效果上看是差不多的，所以很多时候大家直接使用绝对值来加速计算。

