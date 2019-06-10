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

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%873.PNG)

可以看出 x, y 分别提取x方向和y方向的边缘

使用绝对值(l1范数)和使用l2范数效果上看是差不多的，所以很多时候大家直接使用绝对值来加速计算。stardard是skimage的接口.

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%874.PNG)

prewitt两个算子对于横向和纵向的边缘很敏感，检测墙壁边缘的话，非常合适。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%875.PNG)

对于圆形或者说弧形边缘的提取也不错，但实际上laplace算子处理弧形边缘的效果更好。

### laplace

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%876.PNG)

这里laplace的standard做法和我的实现的不同地方在于，卷积之后得到的矩阵，在归一化到[0, 255]时，如果矩阵名为img, 我做的操作是`output = img * 255 / img.max() `, 而standard实现应该是直接截断，也就是`output = np.clip(img, 0, 255)`, 所以图[4]比图[1]要亮很多。图[2]是原图+边缘产生的锐化效果，图[3]则是原图-边缘得到的模糊边缘的效果。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%877.PNG)

这是另外一个laplace filter kernel， 效果上感觉差不多。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%878.PNG)

对于横向和纵向的边缘提取，可想而知，比较无力。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%879.PNG)

但是对于弧形的边缘，就十分敏感，包括小一些的纹理，都能检测出来，比prewitt算子效果好很多。

### sobel

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8710.PNG)

Sobel算子应当是最常用的算子了，用Lenna.jpg来测试，感觉看不出什么。图[3]是x和y方向的边缘的简单绝对值加和，图[3]为x,y边缘均方根， 图[6]diff是计算图[4]和图[5]平均每个pixel的像素值差异，算这个是想评估一下自己的方法和标准做法的区别，不过标准做法应该是用的和图[3]一样的l1范数。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8711.PNG)

显然Sobel算子和Prewitt算子都对水平和竖直的边缘敏感，Sobel对于大的边缘应当更加敏感。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8712.PNG)

对于弧形的边缘就效果比较差了，边缘上有不少断点，这里的标准做法就表现的比较奇怪，看起来像是x和y的简单叠加，但确有明显的十字形。

### scharr

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8713.PNG)

Scharr算子是sobel算子的改进型，效果直观上确实会更好一些，对于大边缘的捕捉更好。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8714.PNG)

对于弧形边缘，断点的问题也比sobel要轻。

### Canny 算法

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8715.PNG)

Canny算法应当是目前被使用最多的边缘检测的传统方法，用的是Sobel算子。算法上会先取一下Gauss Blur（可选参数有sigma,即Gauss kernel的方差，越大越模糊,图上写成了gamma） 然后用Sobel计算梯度，得到每个点的梯度和梯度方向，再然后做所谓的非极大值抑制，其实就是对于单个点来说，在它的梯度方向，如果它是最大的，那么它很可能就是边缘，实际实现上，将所有的点在4个不同的方向上[0-45, 45-90, 90-135, 135-180]寻找符合要求的点，就能得到一个候选的bool值的矩阵，然后在这个基础上卡边缘点的阈值，确认真实边缘和潜在的边缘，最后还有一步抑制孤立点的操作。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8716.PNG)

因为使用的是Sobel算子，所以对于水平、竖直边缘的识别效果不错，当然Gauss blur加得太大是提取不到什么边缘的。



![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8717.PNG)

对于圆形的边缘，在加适当的Gauss blur的时候，能比较好地提取出图片的轮廓，这或许能用在图像分割上。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8731.PNG)

我把skimage的实现代码的中间输出打出来看，其中 local_maxima就是选取过对应局部极大点的图，pts是检测到梯度方向在对应区间的点的图，可以明显看到，就是确实是分成了四个不同的方向区间去进行计算的。这里的阈值统一取[50, 100]

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8732.PNG)细节上就看不出来多东西，这应该是因为图太简单了。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8733.PNG)把Gauss加大, 方向就百年的非常明显。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8734.PNG)再加大一点就.......



## Noise

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8718.PNG)

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8719.PNG)

一开始加在255*255的图中加了一万个点，啥都看不出来，之后就只加1000个点，取看对于单个噪声，不同kernel的表现。

### prewitt

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8720.PNG)

用prewiit的时候，单个噪声点，过一个x方向的filter，就变成了6个点，因为在过filter的时候，会对输出取绝对值，把负梯度转换成正的梯度，所以是6个点没有在错。但这样噪声就被放大了，用Gauss blur，可以一定程度上把噪声的影响弱化。





![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8721.PNG)

这是加了Gauss blur的噪声再过prewitt算子的结果，可以发现噪声变模糊，数值上变小了。

### laplace



![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8722.PNG)

对于laplace也有放大噪声同样的问题。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8723.PNG)

嗯，其实还是蛮有趣的，有点像万花筒。十字万花筒！

### sobel

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8724.PNG)

回字万花筒！注意图[3]这个回字，再后面Canny的情况下，出现了同样的回字，印证了，Canny算法确实使用了Sobel算子，而且用的还是l1范数的实现，相比于l2范数，可以加速运算。这里图5的标准实现就不知道加了什么奇怪的操作了。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8725.PNG)

### scharr

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8726.PNG)

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8727.PNG)

### canny 算法

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8728.PNG)

再没有加Gauss blur前（虽然Canny自己也有Gauss blur），还是能够找到噪声点，呈现回字型。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8729.PNG)

加了Gauss blur就什么都没有了，一定程度上说明，加Gauss blur确实可以抑制噪声（但这里可能是连正常的而边缘都模糊没了）

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8735.PNG)整体上来看，canny算法对于噪声还是非常鲁棒的，即便加了10000个噪声点，也能检测到比较好的边缘。当然需要比较合适的参数。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8736.PNG)

Gauss blur 加大就分不清噪声和边缘了。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8737.PNG)再加大，就变成了**染色体分裂**示意图，染色体分裂，纺锤丝形成，这个高考要考！！

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8738.PNG)

通常情况下是不会有10000那么多噪声的，1000应该够吧。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/more%E5%B9%BB%E7%81%AF%E7%89%8739.PNG)

## Dark light

暗光最常见的场景就是拍摄天体了，这时候边缘很难检测出来，不同的算子的表现能力也不同。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8730.PNG)

### prewiit

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8731.PNG)

检测到了一部分的边缘，但是断断续续，不连贯，效果显然是不好的。这种暗光情况，首先要做的就是做直方图均衡化！



![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8732.PNG)

均衡化之后，能够检测到更多的边缘，但是噪声也因此更多了。

### lalplace

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8733.PNG)

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8734.PNG)

### sobel

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8735.PNG)

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8736.PNG)

### scharr

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8738.PNG)

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8737.PNG)

### canny

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8740.PNG)

canny算法提取道的特征还是相对好的，而且边缘更加连续一点。

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8741.PNG)

均衡化之后什么都没提取到...， 这个bug下次de

## Hed

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8742.PNG)

有数据集就可以搞网络了。HED是15年的文章，是全卷积网络，权值用的Vgg16, 导出中间输出叫做side output, 过1x1卷积还原通道然后反卷积还原尺寸，5张图通过fusion层融合，一起取算loss.

代码参见:<https://github.com/moabitcoin/holy-edge>

paper: <https://arxiv.org/pdf/1504.06375.pdf>

![](http://psu6g0x7b.bkt.clouddn.com/homework/digital_image_processing/pptx/%E5%B9%BB%E7%81%AF%E7%89%8743.PNG)

