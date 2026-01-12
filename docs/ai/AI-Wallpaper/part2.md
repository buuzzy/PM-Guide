---
sidebar_label: '接口构建与页面设计'
title: '第二节' 
---

# 接口构建与页面设计
:::tip
开篇明义，对内容有任何不理解的请直接问 AI
:::

在上一节，我们大体过了一遍如何创建项目，写一个简单的接口以及优化页面、组件的简单思路。对于 AI 壁纸网站而言，最重要的一点在于如何生成好看的壁纸，这涉及到你调用的图像生成接口。

目前市面上有许多大模型厂商都有图像生成的接口能力，我们将会以 OpenAI 的 Dall-e-3 模型为例进行说明，涉及如何转接接口。同时也会举一个国内厂商的例子。

## 壁纸生成接口
### 请求逻辑
由于 OpenAI 的限制，我们无法在国内充值 API 余额，使用 OpenAI 的 Dall-e 模型。Claude 等其他国外大模型也存在这个问题。

解决方式也很多，我们可以找某宝代充，但通常价格很贵，其次几美元的额度在几次调试过后很快就用完了，成本较高。另一种方式是通过中转接口去实现，价格相对便宜，也能调用 OpenAI 的图像模型。唯一的风险在于合法合规性，通常这些商家的 API 额度来路不明...

购买了中转接口后，商家一般会给你一个 APIKey 和中转地址，这样就可以使用了。如何调用接口，方式则可以参考 OpenAI 的接口文档，让我们一步步来。首先在 /app/api 路径下创建 /gen-wallpaper 文件夹，并在文件夹中新建 `route.ts` 文件，写入如下代码：

```bash
export function POST(req:Request){
    return Response.json({
        code:0,
        message:"ok",
        data:{
            img_url:"https://xxxx.com/xx.png",
        },
    });
}
```

回到 /debug/apitest.http 文件下，写入如下代码：

```bash
### generate wallpaper
POST {{baseUri}}/gen-wallpaper
Content-Type:application/json

{
    "description":"happy new year 2024"
}
```

点击 Send Request 后，会弹出如下请求：

```bash
HTTP/1.1 200 OK
vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch
content-type: application/json
Date: Thu, 13 Mar 2025 08:32:24 GMT
Connection: close
Transfer-Encoding: chunked

{
  "code": 0,
  "message": "ok",
  "data": {
    "img_url": "https://xxxx.com/xx.png"
  }
}
```

这代表着我们向 /gen-wallpaper 发起了一个请求，这个文件进行处理并返回了 json 格式的内容。我们向 OpenAI 或者其他的厂商发送请求也是类似的，我们发起符合对方格式要求的请求，对方返回给生成图片。现在我们要做的仅是完善逻辑。

### 编程方式

在有 API KEY 后，写接口会简单许多。以 OpenAI 为例，我们可以根据他们的官方文档一步步进行操作，或者直接复制所有关联的文档页面给 AI，让它根据官方文档自己写代码。

**在这个过程中需要注意，大部分 AI 并不能识别出网页中的代码块。** 如果你发现 AI 写了一个接口，但是不能用，你可以尝试将整个页面复制给 AI，这样它就能写对了。
![01](/img/AI/AI-Wallpaper/part2/01.png)
*比方说上图中的代码块，AI 仅凭网页链接可能无法读取到。*
<br/>

OpenAI 有一个 node 的 SDK 库，我们安装之后就可以直接发起请求，不用写接口代码了（后面我还会举一个用 AI 写接口的例子）。

```bash
pnpm add openai

# 了解更多用法：github.com/openai/openai-node
```

安装完成后，我们在根目录创建一个 /service 文件夹，并创建 `openai.ts` 文件，输入如下代码：

```bash
import OpenAI from "openai";

export function getOpenAIClient(): OpenAI {
    return new OpenAI({
        apiKey: "your api Key",
        baseURL: "中转接口地址"
    });
}

# 如果你使用的是 OpenAI 的 Api Key，直接填写就可以，删掉 baseURL 这一行。并且通过环境配置完成 Api Key 的配置。
# 如果你使用的是网上购买的中转接口，则 baseURL 这一行填写商家提供给你的地址。 
```

回到 /gen-wallpaper 路径下的 `route.ts` 文件，我们在第一行插入代码：

```bash
import { getOpenAIClient } from "@/service/openai";

# 这代表着我们引用了 /service/openai 的客户端，实现了模块分离。
```

这意味着我们能够请求 OpenAI 的接口了，接下来需要明确如何请求，需要哪些具体参数。我们可以在 OpenAI 的[官方文档](https://platform.openai.com/docs/guides/image-generation#language-specific-tips)中找到请求示例。根据示例内容，我们插入代码：

```bash
import { getOpenAIClient } from "@/service/openai";

export async function POST(req: Request) {
    const { description } = await req.json();
    const client = getOpenAIClient();

    const result = await client.images.generate({
        prompt:`generate a desktop wallpaper about:${description}`,
        model: "dall-e-3",
        n: 1,
        size: "1792x1024",
        quality: "standard",
        style: "natural"
    });

console.log("generate wallpaper result:",  result);
```

其中的 model 选用了 dall-e-3 模型，n 代表数量，限制为 1，size 就是图片尺寸，以此类推。**再次强调，如果对代码中的哪些内容不理解，请直接向 AI 提问！！**



回到 /apitest 文件，发送请求，你会在终端底部发现请求正在加载中。等到加载完毕，页面右侧会显示加载信息。按 ctrl+J 唤起命令行，你也可以看到加载的图片地址和成功提示。

![02](/img/AI/AI-Wallpaper/part2/02.png)

返回的信息如下：

```bash
{
  "code": 0,
  "message": "success",
  "data": {
    "img_description": "happy new year 2024",
    "img_url": "生成的图片壁纸",
    "created_at": "2025-03-13T11:26:18.826Z"
  }
}

# 返回了我们输入的参数，包括：成功提示、图片描述、图片地址、生成时间和地点
```

我们尝试打开生成的图片链接，就能看到 AI 生成的图片了。不过在网站上，我们的设计会更进一步，直接在网站上展示生成的图片。

接下来我们会遇到一个问题，OpenAI 生成的图片会临时保存在他们的服务器中，照片会过期。如下图所示，当我的图片没有保存时，前端无法读取到图片地址，就会发生报错。

![03](/img/AI/AI-Wallpaper/part2/03.png)

那么我们后续需要展示这些图片，就要思考如何把照片下载下来，然后保存在云服务器中。比方说保存到亚马逊的服务器（AWS）。

:::tip
接下来，我们会涉及一个概念，关于前后端分离，可以通过 AI 搜索了解相关内容：
1. 什么叫做前后端分离？
2. 服务端渲染加载数据的好处和坏处？
3. 前后端分离请求数据的好处和坏处？
4. 设计一个网站时，应该采用哪种形式？（*我们会使用前后端分离的方式，你懂的*）
:::

## AI 前端设计
完成壁纸生成接口设计之后，整个网站的基本逻辑已经完成。接下来需要对页面进行美化。有几种方式：

1. **使用组件**

第一种是通过前端 UI 组件复制代码，你可以在 [基础知识 ](/docs/ai/basic/basicknowledge.md)中的众多网站中找到你喜欢的风格。复制代码到 VS code 后，如果发生报错，你可以告诉 AI 将代码调整为合适的格式。
![04](/img/AI/AI-Wallpaper/part2/04.png)
![05](/img/AI/AI-Wallpaper/part2/05.png)

2. **AI 生成**

第二种方式相对简单，直接让 AI 参考某个漂亮的网站或者直接参考某家大厂的风格，为你美化组件：

```bash
# 方式一：给一个参考网站
https://xxx.com/
请你参考这个网站的样式，帮我修改 components 目录里面的组件以及其他文件，使得变得更美观。仅作美化，不涉及其他代码

# 方式二：给风格提示词
请你参考苹果、谷歌等公司的网站风格，帮我设计网站 UI，修改 components 目录里面的组件以及其他文件
```

提示词仅作示意，你可以根据实际需求进行探索。或者现在网上有许多 1：1 复制网站 UI 的产品，你也可以通过这些工具直接获得代码，复制到你当前位于 /components 下的组件文件中。复制代码后，刷新页面，你就能看到很漂亮的网站主页了。

### 多轮调试
AI 并不能一次性帮你解决问题，实际上对于页面设计你需要经历多轮调试才能够完成。比方说对图标样式不满意、出现一些不必要的组件，想要删除等等，这些属于细节上的美化，你可以通过 AI 实现。

另一类发生较多的问题是代码错误。前期大部分问题可能集中在语法错误，把 `"use client"` 写成了 `"user client"`。无论什么问题，丢给 AI 让它给出代码。

需要注意的是，AI 可能会钻牛角尖，这个时候通常无法解决你的问题，所以最好百度解决。你还需要在过程中学习，多问为什么写这行代码，这段代码这是什么意思，它实现了什么能力...

### 生成壁纸

在前期，我们先让生成按钮能够调用图像生成的接口。也就是当我点击“生成” 按钮时，前端会发送一个请求，并将生成的图片传送回来。同时还需要注意几个要点：
1. 用户未输入文字时，按钮不支持点击（如果不输入内容，AI 不知道你想要什么）
2. 用户点击按钮后，AI 正在生成图片时，按钮不支持点击（如果遇到反复请求的情况，可能会造成崩溃）
...

因为我们已经写好了请求的接口代码并已经调试成功了，我们可以将相关文档发给 AI，让它帮我处理。点击 “生成” 按钮生成壁纸的逻辑也能够很快搞定。如下图所示，我们在输入框输入内容，/gen-wallpaper 就会发起接口请求生成壁纸（左图）。命令行也会返回输入和输出的内容（右图）。
![06](/img/AI/AI-Wallpaper/part2/06.png)
![07](/img/AI/AI-Wallpaper/part2/07.png)
在下一节，我们会讲用户数据、壁纸数据如何储存在云服务器和数据库。完成之后，用户就能够在网页上生成壁纸，并在下方的壁纸列表中实现。