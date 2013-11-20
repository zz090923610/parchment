OhMyLifeRecorder
================

怎么说呢。最初写这个软件的动机，是因为自己每天对着电脑的时间很长。一天过后却又记不起当天到底做了什么。
或是随时发现了什么好玩的小东西，有了新灵感，总是会有一些细碎的东西，需要立刻记下来。对于天天对着电脑的人，想让他去坚持
记一本纸质日记是很难的事情，那么为什么我们不能写一些小快灵的代码，去解决个问题呢？我们每天都会在打开的shell里面忙东忙西，
若是随意敲一行命令，就能实现上述功能，岂不是很有趣。


所以我的想法是：写一段极其短小的脚本，能让你在最快的时间内记下你想记的，每天之后还能自动生成一个排版美观良好类似日记的文档，让你对
自己一天的所做所想一目了然。进一步，如果我还能把每天生成的日记让它自动传到SNS上，把每天的喜怒哀乐点点滴滴与朋友分享，那才是最最有趣的。


所以自己花了近一周的业余时间，写出了 `OhMyLifeRecorder` 的原型。到今天，上面说的那一串功能已经很艹很艹的实现了。艹的意思是：
首先在首次使用这段脚本前需要有几个需要手动完成的步骤（当然，这部分将来会改）。其次，在使用的过程中，目前只保证使用本文中指定的命令参数格式会得到正确的结果（所
有未在本文中列出的参数组合的使用后果都是未定义的）。从上可见，目前该脚本仅仅是最初原型，到处都能改进。这也与我一直认为写代码可以分
两步走有关，第一步实现从无到有，第二步实现从有到好。这样的话在每一步里我们可以把精力集中起来分别完成每阶段的任务。


闲话少说，下面是使用方法：


<h3>下载：</h3>
该项目挂载github上，完全开源，地址为 https://github.com/zz090923610/OhMyLifeRecorder

<h3> 首次使用前配置：</h3>
<ul>
<li>由于整体脚本由python3编写，作为原型阶段暂未考虑与python2的兼容，所以需要安装python3环境。</li>

<li>由于整体思路是依托于shell命令行终端设计的，所以理论上在所有Linux包括BSD系列操作系统是可以运行的。对于安装了CygWin的Windows
系统也理论可行。由于未经测试，同时也没做任何跨平台的设计，所以不保证全平台都能运行。</li>

<li>下载后请将压缩包解压，之后可以把得到的文件夹放在任意你想放的位置(当然，`/var/tmp`除外)。</li>
<li>之后运行: `python3 /path/to/OhMyLifeRecorder.py -i`， 进行初始化，这个操作会在你的`Home`目录下建立两个文件夹用于存放数据。</li>
<li>之后在根据你用的系统和shell的不同，找到相应的配置文件。（例如在Mac OS X 下的`bash`配置文件为`~/.bash_profile`，在Ubuntu下`bash`的配置文件为`~/.bashrc`之类），找到后在其中末尾添加一行 `source ~/OhMyLifeRecorderUserData/alias`</li>
<li>最后，强烈建议添加两个alias到bash配置文件， 
<ul>
<li>一个是 `alias recorder='python3 /path/to/OhMyLifeRecorder.py'`, 之前在这里发现了个移植性bug，本来打算这个alias是可以大家自己改的，但是现在还是先一定用`recorder`吧。等接下来功能写全了后我再统一解决移植性问题和个性化问题～</li>
<li>另外一个是`alias refresh_aliases='source /path/to/bash_configure_file'`，用途将后续说明。`/path/to/bash_configure_file`为刚刚说过的被我们修改过的shell配置文件的路径。</li>
</ul>
</li>
<li>在此之后你需要为python3安装2个第三方库，分别是 [markdown](http://pypi.python.org/packages/source/M/Markdown/Markdown-2.3.1.tar.gz) 和 [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/bs4/download/4.3/beautifulsoup4-4.3.2.tar.gz) 。
安装方法是下载后将其解压，命令行`cd`到解压得到的文件夹，先运行`python3 setup.py build`，无错误之后再运行`sudo python3 setup.py install`。按以上方法将两个库安装后，所有准备工作就完成了,重启shell生效。
</li>
</ul>

<h3>使用： </h3>

<li>首先我们在此定义一个名叫`job`的概念，1，可以理解它为工作，任务，事项等我们能做的所有事情的一个抽象，2，也可以用作心情日记，生活日记，私人日记，工作日志等等的分类。
所以在记录我们的生活之前我们要创建一个或若干个`job`。对于前者，`job`可以标定事件的起止时间和完成状态，从而记录自己的时间分配。对于前者和后者，我们都可以给它们添加
评论用于记录我们想记录的与之相关的东西。</li>
<li>其次我们定义一个名叫`comment`的概念。顾名思义，意思是评论。根据分析，我们需要记录的琐碎事项有很大概率与我们正在做的事情
相关。所以`comment`被设计为依赖`job`。这样可以实现一个琐碎语句与进行中事项的高度结合。当然对于与所做事情无关的`comment`，我们完全可以把他们关联到前述2中的分类。</li>

<li>创建`job` : `recorder -c"WorkName"`推荐使用大驼峰命名方式，因为之后会直接用这个名字创建文件，所以推荐使用字母数字下划线，最好不要留空格。</li>
<li>刷新shell配置。如果最初你添加了`alias refresh_aliases='source /path/to/bash_configure_file'`到shell配置文件中，你只需输入`refresh_aliases`即可实现刷新。 这步的原因是创建工作后为了实现极简化操作Recorder会创建一个以jobWorkName为名字的alias。根据Unix系统机制和shell程序机制，我们需要手动刷新一下shell配置来使新添加的alias生效，或是重启shell使之生效。[为什么不能自动生效？](http://stackoverflow.com/questions/19946321/create-unix-alias-using-a-python3-script)</li>
<li>更改`job`的状态:

`job`状态一共分为4类。created, proceeding, suspended, finished。我们需要根据实际情况在不同时间切换某一`job`的状态，以实现记录我们`job`状况，掌握时间开销。


切换`job`状态的方法为:


`jobWorkName -g` 切换`job`状态到proceeding。

`jobWorkName -p` 切换`job`状态到suspended。

`jobWorkName -f` 切换`job`状态到finished。
</li>
<li>

对`job`发表评论：

你可以在任意时间对任何已创建的`job`发表评论。目前评论仅限于文字内容。方法为:

`jobWorkName -m "This is your comment. You can write maybe in 中文."`

</li>

<li>
此外，你或许会想看看一个`job`的整个完成进度和所有评论。你只需：

`jobWorkName -o`

</li>
<li>

当然，你会想把一整个`job`的完成进度和所有评论导出为MarkDown格式，你只需：

`jobWorkName -d`

这样你就可以在`~/OhMyLifeRecorderDigest`目录下找到对应工作的.md文件，你可以直接上传至博客，或是生成个pdf应付老板。

</li>
<li>

很自然的，当一天结束时候我们会希望对一天的所有做一个总结，可以使用【导出每日摘要】功能，它可以自动生成一个MarkDown格式的文档，把一天的事情写的清清楚楚。

使用方法：

`recorder -d`之后在`~/OhMyLifeRecorderDigest`下可找到自动生成当天的`DailyDigestYYYY-MM-DD.md`摘要文件（如何生成指定日期的摘要？如何生成一段时间（1周）内的摘要？这个只是个传参数的问题，留待之后再写）。

</li>
<li>

除此之外，你可能只是想在shell中查看今天都做了些什么，这时你可以使用【显示每日摘要】功能

使用方法：

`recorder -o`即可。

</li>
<li>

最后，你可能想把自己这一天的摘要，日记上传至SNS与朋友分享，我目前已实现了自动生成人人网日志的功能：

使用方法

`recorder -r`之后输入你的人人网帐号密码，一篇自动排版的日志就会自动上传。
</li>
</p>

<h3>其他问题</h3>
<ul>
<li><h6>为什么用python？<h6>总的说做这种小快灵的东西，或是实现一个想法，python这类脚本语言实现起来总是很快的。特别是在实验某些原型的功能时。</li>
<li><h6>为什么还没做windows版？没做跨平台测试？</h6>时间太紧。日后都会有的。</li>
<li><h6>为什么一定要使用shell？没有GUI版？</h6>首先这个想法形成时针对的用户群还是*nix程序员。对于他们shell是最快最好的一个选择。至于GUI版，之后会有的。</li>
<li><h6>为何源码看起来十分粗糙？</h6>在这一阶段主要关心功能的实现，下一阶段将会对代码的简洁性，完整性，和整体效率做优化和考量。</li>
</ul>

<h6>最后，感谢大家，若是您也对ohMyLifeRecorder感兴趣，请在github上[fork](https://github.com/zz090923610/OhMyLifeRecorder)之～</h6>


