---
sidebar_label: '如何上线一个网站？'
title: '如何上线一个网站？' 
---

# 如何上线一个网站？
## 购买域名
后续会推出许多项目，这些项目都需要通过 Web 端，也即网站的形式呈现。因此在这个过程中会涉及到如何购买域名，如何配置域名，通过 vercel 等其他工具部署以实现上线。

于是干脆写一个通用教程，后续涉及到网站配置和部署上线看这一篇就足够了。

需要注意的是，这篇文章仅针对域名在海外的配置，与阿里云或腾讯云的配置逻辑不相同。如果你需要在国内部署上线，可以查找其他相关文章。

市面上有许多域名商，比方说腾讯云、阿里云。他们都提供了域名购买和配置的能力，但通过这些渠道购买往往存在溢价。我这里推荐的域名商是 [Namesilo](https://www.namesilo.com/)，价格相对低廉。

首先让我们打开 [Namesilo](https://www.namesilo.com/)，在搜索框中搜索你想要的域名名称。
![01](/img/AI/basic/buildwebsite/01.png)

比方说我搜索的域名名称是 buuzzy，对应的搜索结果就会展示相关联的域名和价格。一般来说 .com 的网站最贵，其次是一些不常见的域名，比方说你正在浏览的网站：www.buuzzy.top
![02](/img/AI/basic/buildwebsite/02.png)

加入购物车之后，点击 checkout。
![03](/img/AI/basic/buildwebsite/03.png)

因为此时我们还未登录，我们先完成注册登录流程。
![04](/img/AI/basic/buildwebsite/04.png)

完成注册登录之后，进入结账页面。
![05](/img/AI/basic/buildwebsite/05.png)

点击左侧 Add New Payment Method，选择支付方式。这里我选用的是支付宝进行支付，如果有海外银行卡也可以使用。
![06](/img/AI/basic/buildwebsite/06.png)

点击 PAY，扫码完成支付。
![07](/img/AI/basic/buildwebsite/07.png)

完成支付后，会跳转至仪表盘，至此我们完成第一部分操作。接下来我会演示如何使用 Cloudflare 进行 DNS 解析。
![08](/img/AI/basic/buildwebsite/08.png)

## DNS解析
点击 [Cloudflare](https://www.cloudflare-cn.com/)，完成注册登录。
![09](/img/AI/basic/buildwebsite/09.png)

我们默认进入账户主页，点击“添加域”。
![10](/img/AI/basic/buildwebsite/10.png)

输入你刚才在 Namesilo 购买的域名，选择“快速扫描 DNS 记录”，点击继续。
![11](/img/AI/basic/buildwebsite/11.png)

这里会出现许多方案，我们不选择付费方案。下拉选择免费方案，点击继续。
![12](/img/AI/basic/buildwebsite/12.png)

Cloudflare 会给我们下图中的一些 DNS 配置地址，先不管，点击继续前往激活。
![13](/img/AI/basic/buildwebsite/13.png)

复制下方两个名称服务器地址，暂时不管下方的提示。
![14](/img/AI/basic/buildwebsite/14.png)

回到 NameSilo，在 Domain Manager 中点击 Quick settings，粘贴两个名称服务器地址。第三个可以删掉或不管。
![15](/img/AI/basic/buildwebsite/15.png)

等待几秒，可以在 DNS 中看到配置的地址，已经和 Cloudflare 一致了。
![16](/img/AI/basic/buildwebsite/16.png)

回到 Cloudflare，点击左侧 SSL/TLS，点击概述，加密模式选择 “完全”。
![17](/img/AI/basic/buildwebsite/17.png)

## 域名部署
进入 [vercel](https://vercel.com/) 或者其他你选择部署的工具，这里以 vercel 进行演示，先进入你的项目，点击 Settings，点击左侧导航栏中的 domains。
![18](/img/AI/basic/buildwebsite/18.png)

点击 Add。
![19](/img/AI/basic/buildwebsite/19.png)

在 Domain 输入我们的域名，其他项默认。
![20](/img/AI/basic/buildwebsite/20.png)

Vercel 会尝试与 Cloudflare 进行连接，授权 DNS 记录后就能完成操作，以前只能手动连接。
![21](/img/AI/basic/buildwebsite/21.png)

完成授权后，Vercel 会给一个 CNAME，我们需要回到 Cloudflare 添加。
![22](/img/AI/basic/buildwebsite/22.png)

回到 Cloudflare 的 DNS - 记录，首先删除三个类型为 NS 的记录。同时删除类型为 A，名称为 www 的记录。
![23](/img/AI/basic/buildwebsite/23.png)

添加一条记录，将 Vercel 中的类型、名字、价值（Vaule）填入其中。
![24](/img/AI/basic/buildwebsite/24.png)

保存之后，回到 Vercel，我们就可以看到 加载成功了。
![25](/img/AI/basic/buildwebsite/25.png)

稍等一会儿，我们就可以看到域名成功配置了项目。
![26](/img/AI/basic/buildwebsite/26.png)