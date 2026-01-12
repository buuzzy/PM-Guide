---
sidebar_position: 2
sidebar_label: 如何做清单调研
---

# 如何做清单调研

如果只是对某个新功能做比对分析，可以简化到只做概要设计的拆解，在上一篇文章中我们提到的加粗的模块设计和功能清单必不可少，尤其是功能清单。



功能清单的逆向设计在于对于竞品影响用户体验效率的功能进行分模块对比，讲求关键。但在电商、金融、企业服务、在线教育等成熟行业，产品大多都仰赖服务商提供的解决方案，产品经理更多要去做精细化的功能清单，告诉乙方具体的操作。相较于第一种方式会更加繁琐。

## 关键功能清单

我们先来聊第一种方式，针对竞品的**关键功能**进行分模块对比。以券商产品举例：

|          | **我们的产品** | **竞品 A** | **竞品 B** | **竞品 C** | **竞品 D** |
| -------- | --------- | -------- | -------- | -------- | -------- |
| **导购模块** |           |          |          |          |          |
| 社区内容     | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |          |
| 直播       |           | <div class="text-center">✅</div>        |          |          | <div class="text-center">✅</div>        |
| 搜索       | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          |
| 榜单       |           |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| 首页推荐     | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| **行情模块** |           |          |          |          |          |
| 指标工具     | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| 基本面      |           | <div class="text-center">✅</div>        |          |          | <div class="text-center">✅</div>        |
| 技术面      | <div class="text-center">✅</div>         |          | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |
| **售卖产品** |           |          |          |          |          |
| 投顾       | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |          |
| 付费指标     | <div class="text-center">✅</div>         |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| VIP 会员   | <div class="text-center">✅</div>         |          | <div class="text-center">✅</div>        |          |          |
| **交易模块** |           |          |          |          |          |
| 直接支付     | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| 分期付款     | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |
| 白条付款     | <div class="text-center">✅</div>         | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          |          |
| ...      |           |          |          |          |          |

看起来比较简单，但似乎内容有些单薄，用互联网黑话来说是颗粒度太粗。不同的支持程度没有被表达出来，我们还可以进行进一步的细化，举个例子：

|      | **我们的产品** | **竞品 A**        | **竞品 B** | **竞品 C**        | **竞品 D**             |
| :---- | :--------- | :--------------- | :-------- | :--------------- | :-------------------- |
| 社区内容 | <div class="text-center">✅</div>         | ✅，但是没有运营，只有关键词屏蔽功能 |     <div class="text-center">❌</div>   | ✅，且围绕股票做了很多社区相关功能 | ✅，且社区精细化运营做的很好，甚至有积分体系 |

通过第一层的功能清单逆向分析后，我们往往可以找到一些重要的功能机会，这时候可以更微观的针对性逆向拆解，呼应我们自己的详细设计。 例如当我们想研究值不值得做社区的功能、怎么做的时候。 我们可以只围绕着该功能的细节对比，例如：

|          | **竞品 A**                 | **竞品 C**                          | **竞品 D**                                        |
| :-------- | :------------------------ | :--------------------------------- | :----------------------------------------------- |
| 社区入口     |    · 一级菜单             |      · 一级菜单<br/> · 首页瀑布流 <br/> · 行情详情页              |             · 一级菜单 <br/> · 首页瀑布流 <br/> · 行情详情页 <br/> · 搜索结果页 <br/> · 消息推送                                    |
| 社区话题     | ×                        | 周更                                | 日更，甚至小时更                                        |
| 社区活动     | 几乎没有                     | 跟随热点事件不定期举办                       | 定期举行社区活动                                        |
| 社区成长体系   | ×                        | ×                                 | 基于用户活跃的成长体系                                     |
| 社区频道     | ×                        | ×                                 | ✅                                               |
| ...      |                          |                                   |                                                 |
| **主观体会** |                          |                                   |                                                 |
| 体感       | A 虽然有基础的社区功能，但长期处于不维护的状态 | C 比较佛系，对社区还是基于热点新闻去运营。虽然活动很少，但有新意 | D 的社区运营结合了新闻、行情进行话题运营和推送。成长体系和话题高度榜单，有形成雪球社区的雏形 |
| 思考       | 1. 结合新闻事件进行话题运营|2. 尝试构建社区生态，建立一套用户成长体系|3. 需要为社区提供更多入口，以刺激用户留存活跃|

根据产品的种类不同，分析的角度还会有很多种情况。例如有些产品特别注重对用户交互体验的分析，有些产品特别注重操作效率的分析，这里就不展开了。



总之，当你做足了功课之后，产出的竞品分析文档对团队会有不错的参考价值，对你自己更是有极其强烈的思考推动价值。优秀的产品经理常常可以非常快的想起某个竞品、功能的做法。

## 精细化功能清单

精细化功能清单可以理解为是对某一关键功能进行更深入的拆解，过程大致和关键功能清单类似，过程会更加细致。举个例子，下面是我做 ETF 专区改版时做的功能清单：

|            | **竞品 A** | **竞品 B** | **竞品 C** | **竞品 D** | **竞品 E** | **竞品 D** |
| :---------- | :-------- | :-------- | :-------- | :-------- | :-------- | :-------- |
| **功能入口**   |          |          |          |          |          |          |
| 首页九宫格      | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          |
| 行情(市场)     | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          |          |          |
| 理财         | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | ✅        |
| 搜索         |          |          | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        | ✅        |
| **页面布局**   |          |          |          |          |          |          |
| BANNER     |          |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          |
| 功能宫格       |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| **ETF 筛选** |          |          |          |          |          |          |
| 按行业/板块     | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |
| 按规模（宽基）    | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |
| 按概念/题材     |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |          |          |
| 按数据        | <div class="text-center">✅</div>        |          |          |          |          | <div class="text-center">✅</div>        |
| 按指数估值/资金   | <div class="text-center">✅</div>        |          |          | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        | <div class="text-center">✅</div>        |
| 按市场热点      |          |          | <div class="text-center">✅</div>        |          |          | <div class="text-center">✅</div>        |
| 按国际市场      |          |          | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |          |
| 按营销推荐      |          |          | <div class="text-center">✅</div>        |          |          | <div class="text-center">✅</div>        |
| 按应用内关注     | <div class="text-center">✅</div>        |          | <div class="text-center">✅</div>        |          |          | <div class="text-center">✅</div>        |
| ...        |          |          |          |          |          |          |

此外，还需要写清楚说明，标记出数量和占比，为项目经理和乙方提供一个直观参考（该不该做）：

|            | **数量** | **占比** | **说明**                             |
| ---------- | ------ | ------ | :---------------------------------- |
| **功能入口**   |        |        |                                    |
| 首页九宫格      | <div class="text-center">10</div>     | <div class="text-center">91%</div>    | 可通过首页九宫格进入 ETF 专区功能页               |
| 行情(市场)     | <div class="text-center">5</div>      | <div class="text-center">45%</div>    | 可通过行情（市场）导航栏进入 ETF 专区功能页           |
| 理财         | <div class="text-center">9</div>      | <div class="text-center">82%</div>    | 可通过理财导航栏进入 ETF 专区功能页               |
| 搜索         | <div class="text-center">6</div>      | <div class="text-center">55%</div>    | 可通过应用内搜索功能查找并跳转到 ETF 专区功能页         |
| **页面布局**   |        |        |                                    |
| BANNER     | <div class="text-center">5</div>      | <div class="text-center">45%</div>    | 展示和 ETF 相关的推荐、营销信息，通常以 BANNER 形式展示 |
| 功能宫格       | <div class="text-center">10</div>     | <div class="text-center">91%</div>    | 以宫格视图展示更多和 ETF 相关的功能               |
| **ETF 筛选** |        |        |                                    |
| 按行业/板块     | <div class="text-center">10</div>     | <div class="text-center">91%</div>    | 以行业对 ETF 进行筛选划分，再以涨跌幅进行倒序排序        |
| 按规模（宽基）    | <div class="text-center">8</div>      | <div class="text-center">73%</div>    | 以规模对 ETF 进行筛选划分，通常展示为宽基指数          |
| 按概念/题材     | <div class="text-center">7</div>      | <div class="text-center">64%</div>    | 以概念对 ETF 进行筛选划分，再以涨跌幅进行倒序排序        |
| 按数据        | <div class="text-center">2</div>      | <div class="text-center">18%</div>    | 按影响 ETF 价格变动的数据进行筛选划分，或仅展示特定 ETF   |
| 按指数估值/资金   | <div class="text-center">9</div>      | <div class="text-center">82%</div>    | 按估值对指数进行排序，并推荐与该指数相关联的 ETF         |
| 按市场热点      | <div class="text-center">4</div>      | <div class="text-center">36%</div>    | 按市场关注度较高(异动)对 ETF 进行排序展示           |
| 按国际市场      | <div class="text-center">3</div>      | <div class="text-center">27%</div>    | 按国际投资标的收益对 ETF 进行排序展示              |
| 按营销推荐      | <div class="text-center">2</div>      | <div class="text-center">18%</div>    | 按运营编辑对 ETF 进行排序展示                  |
| 按应用内关注     | <div class="text-center">4</div>      | <div class="text-center">36%</div>    | 按搜索、点击等形式对 ETF 进行排序展示              |

<br/>

当然，这只是冰山一角。因为 ETF 专区的页面和栏目不止有一个，所以调研的功能清单数量直线上升。要增加的表字段也会更多，比方说：

| **调研问题**             | **调研方式**         |
| :-------------------- | :---------------- |
| **细节**               |                  |
| 竞品是否有这个功能？           | 通过 “有” 或 “无” 表述  |
| 竞品的功能包括了哪些栏目和子功能？    | 罗列栏目和子功能，横向对比竞品  |
| 描述竞品的功能定义，最好展示图片     | 解释竞品功能，附上对应图片    |
| 竞品的功能深度分别是几级？        | 通过 1、2、3... 进行表述 |
| 竞品的功能展示了哪些字段，展示的方式是？ | 通过罗列字段，附图进行说明    |
| **结论**               |                  |
| 这些功能在竞品中所占的比重分别是？    | 通过数量和占比进行展示      |
| 这些功能在竞品中的主线是？        | 说明功能主线及功能逻辑      |
| 大致分析竞品功能的创新点或意图      | 竞品功能分析           |

<br/>

整体上说，精细化功能清单并没有难点，但是烦人之处在于其对产品功能细节的精确捕捉，需要耗费一定的时间去做大量重复性调研，所以知道为什么大厂乐意招那么多实习生和产品助理岗了吧，因为总有人得去做这些工作。😢


<br/>

Ref：
* 如果你想大致了解一个金融产品功能的功能清单长什么样子，请浏览：[ETF专区竞品调研](https://docs.qq.com/sheet/DYklGcW92am9VSmpY?tab=BB08J2)