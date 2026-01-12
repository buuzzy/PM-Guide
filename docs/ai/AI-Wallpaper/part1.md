---
sidebar_label: '环境配置'
title: '第一节' 
---

# 环境配置

:::tip
对操作中有任何不理解的地方，都可以询问 AI。

比方说：

1. 命令行是什么，什么叫做命令行工具，cd 命令是什么？
2. 接口是什么，接口中的 GET 和 POST 请求是什么意思？
:::

## 前言
第一次课程，我们将复刻做一个 AI 壁纸网站。此类网站的一般逻辑是用户输入提示词，由图像大模型根据提示词生成图片。网站还会以列表形式展示用户生成的图片，以及支持用户注册登录。

我们以一个 AI 壁纸网站作为示例，大部分 AI 壁纸网站都会包括如下核心要素：
1. 图像生成：支持用户输入提示词，并通过特定大模型生成图像；
2. 壁纸列表：展示用户生成的壁纸；
3. 个人中心：支持用户注册、登录，查看自己的壁纸

![01](/img/AI/AI-Wallpaper/part1/01.png)

根据示例网站，我们需要做的内容包括但不限于：
1. 如何去实现图像生成？即用户点击 “生成” 按钮背后的逻辑；
2. 如何以列表形式展示用户生成的图像？最好还要显示图像描述以及作者；
3. 个人中心的逻辑如何实现？如何让用户完成注册、登录？
...

而这些内容，我们可以通过编程和接入第三方服务来实现。大家不要对 Coding 有天然的恐惧，Coding 看起来难，但说到底还是工具，总会有 “不会用 >> 用得惯 >> 用的好” 的过程。在 AI 的帮助下，编程的难度已经下降了非常多，最终限制你的还是想象力、执行力和用户洞察。

## 创建项目

开始项目之前，打开 Powershell，检查 nodejs 和 pnpm 有没有进行安装，正常显示版本名后进入下一步骤。如果还未安装，你可以查看 [搭建开发环境](/docs/ai/basic/builddev.md) 进行安装。

```bash
# 检查 node 版本
node -v

# 检查 pnpm 版本
pnpm --version
```

通过 `cd` 命令，定位到你想要创建项目的文件夹，通过 `npx` 命令创建初始项目文档。完成创建后，通过 `code .` 命令打开编译器。

```bash
# cd 命令：返回当前目录上一级
cd ..

# cd 命令：进入当前目录下一级
cd 目录名称

# 定位到你想要创建项目的文件夹后，执行下述命令，创建初始项目文档
npx create-next-app@latest

## 第一项需要输入你的项目名称，你可以填：aiwallpaper
## 其他选项按照默认选项选择就可以，你可以一直按回车键
## 成功创建后，Powershell 会提示 ‘Success’

# 打开编译器
code .

# 如果你有多个编译器，你可以在系统变量调整 IDE 排序优先级，这样系统会优先排序靠前的编译器。
```

以我为例，我定位到了桌面（Desktop）目录，并且通过命令行（code .）打开了编译器。

![02](/img/AI/AI-Wallpaper/part1/02.png)

输入 `pnpm.dev` 命令进行本地调试，按住 ctrl 点击 http://localhost:3000/ 就可以看到一个初始页面，这就是我们创建的项目页面，只不过此时它没有内容，我们要做的就是让它变成我们最开始展示的 AI 壁纸网站。

![03](/img/AI/AI-Wallpaper/part1/03.png)

## 组织页面结构

打开编译器，在 /app 目录下有一个文件叫做 page.tsx，这就是创建的项目初始页面。打开 page.tsx，删掉 `return` 括号里面的所有内容，输入 hello world 并快捷键 ctrl + s 保存。

```bash
import Image from "next/image";

export default function Home() {
  return (
    <div>hello world</div>
  );
}
```

回到页面，我们就可以看到我们输入的内容。在页面左上角有一段英文，hello world。你可以在 `<div>` 中插入任何你想输入的内容，相应会在页面上展示。写代码并不难，你已经做到了。

接下来需要创建页面结构，不同目录下有不同的页面，就像淘宝一样，你点开 App，默认是主页，点开个人中心，又是另一个页面，页面间都有层级关系。比方说电脑桌面的目录就是： C:\Users\用户名\desktop

在 /app 目录下创建文件夹 /blog，在文件夹下新建文件，文件名为：`page.tsx`，在文件中输入代码：

```bash
export default function(){
    return <div>你好</div>;
}
```

这个操作的意思就是在网页的 /app 目录下，页面会显示 “你好” 文字。
![04](/img/AI/AI-Wallpaper/part1/04.png)

同样地，你还可以继续在 /app 目录下创建更多文件夹和页面，或者在 /blog 目录下创建文件夹和页面。比方说：
1. 在 /app 目录下创建 /website，那么访问路径就是：localhost:3000/website
2. 在 /blog 目录下创建 /detail，那么访问路径就是：localhost:3000/blog/detail

所以你不用担心如何通过代码去实现页面之间的层级关系，也不用去思考路由的问题。仅需通过新建文件夹和 `page.tsx` 页面，就可以实现网站间的层级结构。

## 构建API接口
除了组织页面结构，另一个重要的点是 API。也就是需要通过接口去处理各种后端逻辑。我们还是回到上面示例的 AI 壁纸网站。当我们在输入框中输入提示词，点击 “生成” 按钮时，此时前端会发起一个接口请求到后台。

在下图右侧，控制台 - 网络中，我们可以看到用户在点击 “生成” 按钮后整个 API 请求的链路。不用担心，相对于成熟产品，我们的逻辑并不会太复杂。

![05](/img/AI/AI-Wallpaper/part1/05.png)

和组织页面结构一样，我们也可以通过层级结构对 API 进行区分。

在 /app 路径下，创建 /api 文件夹，并在 /api 路径下创建 /hello-world 和 /test 文件夹。在 /hello-world 文件夹下创建 `route.ts` 文件，这是使用 Next 写接口的格式。

在 /hello-world 路径下的 `route.ts` 文件中输入代码：

```bash
export function GET(req:Request){
    return Response.json(
        {
            code:1,
            message:'ok'
        }
    )
}

# 请注意，确保你已经按照了两个所需插件
# 关于接口请求中 GET 和 POST 的用法，可以询问 AI
```

你可以访问 localhost:3000/api/hello-world 看到返回的内容：
![06](/img/AI/AI-Wallpaper/part1/06.png)

同样，在 /test 路径下也创建一个 `route.ts` 文件，使用如下 POST 请求。

```bash
export function POST(req:Request){
    return Response.json(
        {
            data:["xxx","xxx"],
        }
    )
}
```

但当我们访问 localhost:3000/api/test 时，提示失败。这是 POST 的特性决定的，我们需要去进行请求才能获取接口里面的内容。

在根目录下创建 /debug 文件夹，并在文件夹中创建 /apitest.http 文件，输入如下代码：

```bash
@baseUri=http://localhost:3000/api

### test
POST  {{baseUri}}/test
```

这个能力是一个 VS Code 插件，它能够帮助我们快速对 API 进行调试。点击 “Send Request” 后，在右侧会显示返回内容。这意味着我们的请求成功了。如下图所示。

![07](/img/AI/AI-Wallpaper/part1/07.png)

*关于请求的写法和用法说明，大家可以点击此处 [Nextjs](https://nextjs.org/docs/app/building-your-application/routing/route-handlers) 查看更多。*

简单回顾一下，到这里，我们大概了解了一个页面是怎么写的以及 API 请求的两种形式。跟页面相关的可以放在 /App 路径下，跟调试相关的可以放在 /debug 路径下。

## 创建页面组件

接下来，需要进一步对页面进行完善。通常来说，这类 AI 壁纸网站都有头部、Slogo、输入框和生成按钮、壁纸列表以及底部声明。我们可以把页面拆分为几个组件，然后让页面调用这几个组件，这样就不用在一个页面中写非常多的代码，更加灵活。

我们在根目录下创建 /components 文件夹，并在该目录下分别创建 /footer、/header、/input、/wallpapers，并在这四个目录下各自创建一个 `index.tsx` 文件。然后在各自的 `index.tsx` 文件中写入代码：

```bash
## 在 /header/index.tsx 文件中写入代码：
export default function(){
    return <header>这是头部</header>
}

## 同理，/footer、/input、/wallpapers 分别代表页面的底部、输入框、壁纸列表，各自填入。
```

回到 /app，在 `page.tsx` 文件下写入如下代码：

```bash
import Header from "@/components/header";
import Wallpapers from "@/components/wallpapers";
import Footer from "@/components/footer";
import Input from "@/components/input";
import Image from "next/image";

export default function Home() {
  return (
    <div>
      <Header />
      <Input />
      <Wallpapers />
      <Footer />
    </div>
  );
}
```

这表示我们从 /components 中引用（import）组件，并在主页面进行展示。回到网页，页面展示了我们在组件中写入的内容，你可以理解为这是一种引用，我们不必把所有代码放在 page.tsx 中。其实代码写到这里，基本的雏形已经具备了。剩下要做的就是把不同的组件进行美化，就能够在首页展示了。
![08](/img/AI/AI-Wallpaper/part1/08.png)

## 页面美化

在这个环节，会使用到 tailwindcss 对页面进行美化，提高写代码的效率，你可以在 tailwindcss.com 了解更多。如果你的项目文件下没有 tailwindcss 文件，可以根据如下操作进行，或者查阅操作手册：[Tailwind CSS4 安装(NPM)](https://www.runoob.com/tailwindcss/tailwindcss4-installbynpm.html)

```bash
# TailwindCSS V3
## 卸载当前版本（若已安装其他版本，没有则忽略）
npm uninstall tailwindcss postcss autoprefixer
## V3 版本安装
npm install -D tailwindcss@3.4.1 postcss autoprefixer
## 初始化配置
npx tailwindcss init -p


# TailwindCSS V4
## 版本安装
npm install tailwindcss @tailwindcss/postcss postcss
## 将 Tailwind 添加到 PostCSS 配置中
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  }
}

## 在 CSS 文件中添加 @import 以导入 Tailwind CSS（一般为 global.css 文件)
@import "tailwindcss";
```

页面组件美化，你可以在[基础知识](/docs/ai/basic/basicknowledge.md)中找到许多可用的组件，复制代码到文件中，修改格式后就可以使用。这个环节是可以通过 AI 来实现的，只需要告诉 AI，你想要头部、底部或其他组件长成什么样，它就会生成代码。而你需要做的就是进行微调，直到实现你想要的效果。
