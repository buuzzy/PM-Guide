---
sidebar_label: '服务器与数据库构建'
title: '第三节' 
---

# 服务器与数据库构建
在前两节，我们完成了前端页面的设计和接口的开发。功能大致能用，但是图片会过期，也不能把图片全都保存在本地加载，这样工作量会巨大。

![01](/img/AI/AI-Wallpaper/part3/01.png)
*如上图，生成的图片一旦过期，会提示“图片加载失败”*

所以第一件事，我们需要把从 OpenAI 生成的图片放到自己的图片服务器（图床）中，第二件事是将数据保存在我们自己的数据库中，比方说储存用户信息、用户写的提示词、生成图片的时间和 url，这涉及到数据的读写。

第三件事是设计一个登录态，用户需要登录之后才能使用我们的网站。不然很多人没有登录就直接使用接口生成图片，这会消耗我们大量的 token，有一定风险。


## 图片储存：AWS
先注册 AWS，国内也可以注册。在过程中如果像我一样遇到网络问题，请直接工单联系客服，反馈速度很快。完成注册登录后，在控制台搜索 “S3”，点击进入存储桶。
![02](/img/AI/AI-Wallpaper/part3/02.png)

点击 “创建存储桶”，填写你的存储桶名称，其他选项默认，点击页面底部创建存储桶按钮即可创建。
![03](/img/AI/AI-Wallpaper/part3/03.png)

完成创建后，回到存储桶列表页，点击刚创建的存储桶，点击权限。在 “屏蔽公共访问权限（存储桶设置）” 一栏中，点击 “编辑”，将权限全部打开。不然网站无法展示服务器上存储的信息。
![04](/img/AI/AI-Wallpaper/part3/04.png)
![05](/img/AI/AI-Wallpaper/part3/05.png)

确认公开访问权限后，在下方的 “存储桶策略” 中点击 “编辑” 按钮，输入策略代码并保存更改。

```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid":"AddPerm",
            "Effect":"Allow",
            "Principal":"*",
            "Action":"s3:GetObject",
            "Resource":"你的储存桶ARM/*"
        }
    ]
}

# 储存桶 ARM 在页面中就有显示，直接复制粘贴进来
```

完成更改后，下拉页面找到 “跨域资源共享”，同样进行编辑并填入代码：

```bash
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "https://localhost:8010/",
            "https://localhost:3000/"
        ]
    }
]

# 在 "AllowedOrigins" 中，如果你已经有现存域名，可以填写你自己的网站。
```

完成配置后，点击页面右上角用户名，点击 “安全凭证”，创建访问密钥。复制你的两个密钥到本地并保存。在项目根目录下创建 .env，我们将两个密钥和存储桶名称放入其中储存。
![06](/img/AI/AI-Wallpaper/part3/06.png)
![07](/img/AI/AI-Wallpaper/part3/07.png)

```javascript
AWS_AK = "你的 Access Key"
AWS_SK = "你的 sercet Key"
AWS_BUCKET_NAME = "你的储存桶名称"
```

为了在项目中使用 AWS 服务，我们需要执行下面的命令，安装 AWS 的 SDK 和 axios 组件：

```bash
# 分别执行下面两个指令
pnpm add @aws-sdk/client-s3 @aws-sdk/lib-storage
pnpm add axios
```

在项目根目录下，我们再去创建 /lib/s3.ts 文件，实现图片上传和文件下载，用来解决 OpenAI 生成壁纸后过期无法永久储存的问题：

```bash
import { S3Client } from "@aws-sdk/client-s3";
import { Upload } from "@aws-sdk/lib-storage";
import { Readable } from "stream";
import axios from "axios";
import fs from "fs";

const client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_AK!,
    secretAccessKey: process.env.AWS_SK!
  }
});

export async function downloadAndUploadImage(
  imageUrl: string,
  bucketName: string,
  s3Key: string
) {
  try {
    const response = await fetch(imageUrl);
    const buffer = await response.arrayBuffer();

    const upload = new Upload({
      client,
      params: {
        Bucket: bucketName,
        Key: s3Key,
        Body: Buffer.from(buffer),
        ContentType: 'image/png'
      }
    });

    return upload.done();
  } catch (e) {
    console.error("upload failed:", e);
    throw e;
  }
}

export async function downloadImage(imageUrl: string, outputPath: string) {
  try {
    const response = await axios({
      method: "GET",
      url: imageUrl,
      responseType: "stream",
    });

    return new Promise((resolve, reject) => {
      const writer = fs.createWriteStream(outputPath);
      response.data.pipe(writer);

      let error: Error | null = null;
      writer.on("error", (err) => {
        error = err;
        writer.close();
        reject(err);
      });

      writer.on("close", () => {
        if (!error) {
          resolve(null);
        }
      });
    });
  } catch (e) {
    console.log("upload failed:", e);
    throw e;
  }
}
```

接下来，你可以告诉 AI，在 /gen-wallpaper 文件下，我想要在生成图片后调用 /s3.ts 中的方法，将图片上传 AWS 的图床并拿到新的图床地址，并把新的地址返回。修改 /gen-wallpaper/route.ts 文件，代码如下：

```bash
import { getOpenAIClient } from "@/service/openai";
import { downloadAndUploadImage } from "@/lib/s3";

export async function POST(req: Request) {
    try {
        const { description } = await req.json();
        
        if (!description) {
            return Response.json({ 
                code: 400, 
                message: "Description is required" 
            }, { status: 400 });
        }

        const client = getOpenAIClient();
        
        // 生成图片
        const response = await client.images.generate({
            prompt: description,
            model: "dall-e-3",
            n: 1,
            size: "1792x1024",
            quality: "standard",
            style: "natural"
        });

        if (!response?.data?.[0]?.url) {
            throw new Error("Invalid response from image generation API");
        }

        // 上传到S3
        const s3Result = await downloadAndUploadImage(
            response.data[0].url,
            process.env.AWS_BUCKET_NAME!, // 确保在.env中设置了这个值
            `wallpapers/${Date.now()}-${Math.random().toString(36).slice(2)}.png`
        );

        return Response.json({
            code: 0,
            message: "success",
            data: {
                img_description: description,
                img_url: s3Result.Location, // 使用S3返回的永久链接
                created_at: new Date().toISOString(),
                img_size: "1792x1024"
            }
        });
    } catch (error: any) {
        console.error("Generate wallpaper error:", error);
        return Response.json({
            code: 500,
            message: error.message || "生成图片失败"
        }, { status: 500 });
    }
}
```

回到网页，我们输入提示词，点击生成按钮。此时我们会发现流程上发生了变化。在命令行工具中，我们看到：

```bash
# API 请求成功
POST /api/gen-wallpaper 200 in 49547ms

# AWS SDK 工作政策
(node:36692) NOTE: The AWS SDK for JavaScript (v2) is in maintenance mode.
```

在 AWS 的储存桶中，我们也看到我们的图片也被储存了。这意味着从生成图片到永久存储再到前端展示的完整链路都正常工作。
![08](/img/AI/AI-Wallpaper/part3/08.png)

但目前我们图片储存还是通过 `localStorage` 储存在本地，接下来要做是将本地存储为云存储。因为如果你要上线网站，肯定会有许多人使用你的网站，这涉及不同用户的大量数据，用户也需要看到自己生成的壁纸，而非下次进来看不见了，又得重新生成。


## 云存储：superbase
关于云存储，国内的可以用阿里云或者腾讯云的服务，出海的选用 AWS 或者 superbase，superbase 适合跑一些简单的项目 demo，想法验证成功后就可以用 AWS。下面我们用 superbase 举例，同样还是先完成注册登录环节，来到 Dashboard。

*Tips：可以问下 AI 为什么要使用 AWS + superbase 结合的形式。*
![09](/img/AI/AI-Wallpaper/part3/09.png)

点击 All project - create a new project，填写项目名称和数据库密码，创建新项目。
![10](/img/AI/AI-Wallpaper/part3/10.png)

点击 “connent”，复制你直连的 postgresql。
![11](/img/AI/AI-Wallpaper/part3/11.png)
![12](/img/AI/AI-Wallpaper/part3/12.png)

如果你忘记了你的密码，可以在 “Project Settings” 点击 Database 进行 Reset，复制新密码。
![13](/img/AI/AI-Wallpaper/part3/13.png)

回到项目，在 /.env.local 文件下输入你的链接：

```bash
# postgres db
POSTGRES_URL = "postgresql://postgres:[YOUR-PASSWORD]..."

## YOUR-PASSWORD 填写你创建项目时使用的密码

```

根据官方文档，通过命令行工具安装数据库。

```bash
# 安装数据库必备文件
pnpm add pg

# 安装依赖
pnpm add -D @types/pg
```

*这有点像在你的车后面挂一个小的置物箱，你也可以这么理解，你的项目就是一辆车，数据库就是你车辆后面挂载的用来装货的小仓库。*

在根目录下创建 /models 文件夹，在 /model 下创建 `db.ts` 文件，输入以下代码：

```bash
import { Pool } from "pg";

let globalPool: Pool;

export function getDb() {
  if (!globalPool) {
    const connectionString = process.env.POSTGRES_URL;
    console.log("connectionString", connectionString);

    globalPool = new Pool({
      connectionString,
    });
  }

  return globalPool;
}
```

有了连接池之后，我们去写相关的数据连接。在 /models 下创建 `wallpaper.ts`文件，在这个文件我们要实现壁纸的读写：先获取壁纸，再插入壁纸。

```bash
import { QueryResult, QueryResultRow } from "pg";

import { Wallpaper } from "@/types/wallpaper";
import { getDb } from "./db";

export async function insertWallpaper(wallpaper: Wallpaper) {
  const db = getDb();
  const res = await db.query(
    `INSERT INTO wallpapers 
        (user_email, img_description, img_size, img_url, llm_name, llm_params, created_at) 
        VALUES 
        ($1, $2, $3, $4, $5, $6, $7)
    `,
    [
      wallpaper.user_email,
      wallpaper.img_description,
      wallpaper.img_size,
      wallpaper.img_url,
      wallpaper.llm_name,
      wallpaper.llm_params,
      wallpaper.created_at,
    ]
  );

  return res;
}

export async function getWallpapersCount(): Promise<number> {
  const db = getDb();
  const res = await db.query(`SELECT count(1) as count FROM wallpapers`);
  if (res.rowCount === 0) {
    return 0;
  }

  const { rows } = res;
  const row = rows[0];

  return row.count;
}

export async function getUserWallpapersCount(
  user_email: string
): Promise<number> {
  const db = getDb();
  const res = await db.query(
    `SELECT count(1) as count FROM wallpapers WHERE user_email = $1`,
    [user_email]
  );
  if (res.rowCount === 0) {
    return 0;
  }

  const { rows } = res;
  const row = rows[0];

  return row.count;
}

export async function getWallpapers(
  page: number,
  limit: number
): Promise<Wallpaper[] | undefined> {
  if (page < 1) {
    page = 1;
  }
  if (limit <= 0) {
    limit = 50;
  }
  const offset = (page - 1) * limit;

  const db = getDb();
  const res = await db.query(
    `select w.*, u.email as user_email, u.nickname as user_name, u.avatar_url as user_avatar from wallpapers as w left join users as u on w.user_email = u.email order by w.created_at desc limit $1 offset $2`,
    [limit, offset]
  );
  if (res.rowCount === 0) {
    return undefined;
  }

  const wallpapers = getWallpapersFromSqlResult(res);

  return wallpapers;
}

export function getWallpapersFromSqlResult(
  res: QueryResult<QueryResultRow>
): Wallpaper[] {
  if (!res.rowCount || res.rowCount === 0) {
    return [];
  }

  const wallpapers: Wallpaper[] = [];
  const { rows } = res;
  rows.forEach((row) => {
    const wallpaper = formatWallpaper(row);
    if (wallpaper) {
      wallpapers.push(wallpaper);
    }
  });

  return wallpapers;
}

export function formatWallpaper(row: QueryResultRow): Wallpaper | undefined {
  let wallpaper: Wallpaper = {
    id: row.id,
    user_email: row.user_email,
    img_description: row.img_description,
    img_size: row.img_size,
    img_url: row.img_url,
    llm_name: row.llm_name,
    llm_params: row.llm_params,
    created_at: row.created_at,
  };

  if (row.user_name || row.user_avatar) {
    wallpaper.created_user = {
      email: row.user_email,
      nickname: row.user_name,
      avatar_url: row.user_avatar,
    };
  }

  try {
    wallpaper.llm_params = JSON.parse(JSON.stringify(wallpaper.llm_params));
  } catch (e) {
    console.log("parse wallpaper llm_params failed: ", e);
  }

  return wallpaper;
}
```

在根目录下创建 /types 文件夹，在 /types 下创建 wallpaper.d.ts 文件用来储存字段类型：

```bash
import { User } from "./user";

export interface Wallpaper {
  id?: number;
  user_email: string;
  img_description: string;
  img_size: string;
  img_url: string;
  llm_name: string;
  llm_params?: any;
  created_at: string;
  created_user?: User;
}

# 如果你使用 AI 创建了壁纸列表，有可能 AI 会自定义一些字段，以便在壁纸列表中展示用户昵称、壁纸尺寸等要素。你可以按照我的代码来，并让 AI 全局修改关联的字段即可。
```

在根目录下创建 /data 文件夹，在 /data 下创建 `install.sql` 文件，用来定义了 `wallpapers` 表的结构，用于在 Supabase 中存储壁纸的元数据信息：

```sql
CREATE TABLE wallpapers (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    img_description TEXT,
    img_size VARCHAR(255),
    img_url TEXT,
    llm_name VARCHAR(100),
    llm_params JSON,
    created_at timestamptz
);
```

回到 superbase，点击 SQL Editor，复制上面这段代码，点击 “run” 运行，Results 会提示成功。
![14](/img/AI/AI-Wallpaper/part3/14.png)

点击 Table Editor，你会看见你已经创建了一个新表了，这个表就是你上面代码中填写的字段。
![15](/img/AI/AI-Wallpaper/part3/15.png)

回到 /api/gen-wallpaper/route.ts 文件，复制以下代码进行优化。综上，代码实现了用户点击生成按钮后：
1. 请求图像生成接口，拿到图片地址；
2. 把生成的图片地址上传到 AWS，拿到 AWS 图床地址；
3. 把生成的参数和返回的图片地址保存到数据库中

```bash
import { getOpenAIClient } from "@/service/openai";
import { downloadAndUploadImage } from "@/lib/s3";
import { Wallpaper } from "@/types/wallpaper";
import { ImageGenerateParams } from "openai/resources/images.mjs";
import { insertWallpaper } from "@/models/walpaper";

// 响应类型定义
type GenerateResponse = {
    code: number;
    message: string;
    data?: {
        img_description: string;
        img_url: string;
        created_at: string;
        img_size: string;
    }
};

export async function POST(req: Request) {
    try {
        // 验证环境变量
        if (!process.env.AWS_BUCKET_NAME) {
            throw new Error("AWS_BUCKET_NAME is required");
        }

        // 解析并验证请求参数
        const { description } = await req.json();
        if (!description || description.length > 1000) {
            return Response.json({ 
                code: 400, 
                message: "Description is invalid or too long" 
            }, { status: 400 });
        }

        // 初始化 OpenAI 客户端
        const client = getOpenAIClient();
        
        // 配置生成参数
        const img_size = "1792x1024";
        const llm_name = "dall-e-3";
        const llm_params: ImageGenerateParams = {
            prompt: description,
            model: llm_name,
            n: 1,
            size: img_size,
            quality: "standard",
            style: "natural"
        };

        // 调用 OpenAI 生成图片
        const response = await client.images.generate(llm_params);
        if (!response?.data?.[0]?.url) {
            throw new Error("Invalid response from image generation API");
        }

        // 上传图片到 AWS S3
        const s3Result = await downloadAndUploadImage(
            response.data[0].url,
            process.env.AWS_BUCKET_NAME,
            `wallpapers/${Date.now()}-${Math.random().toString(36).slice(2)}.png`
        );

        if (!s3Result?.Location) {
            throw new Error("Failed to get S3 upload URL");
        }

        // 准备数据库记录
        const now = new Date().toISOString();
        const wallpaper: Wallpaper = {
            user_email: "buuzzy@163.com", // TODO: 从认证系统获取用户邮箱
            img_description: description,
            img_size,
            img_url: s3Result.Location,
            llm_name,
            llm_params: JSON.stringify(llm_params),
            created_at: now
        };

        // 保存到数据库
        await insertWallpaper(wallpaper);

        // 返回成功响应
        return Response.json({
            code: 0,
            message: "success",
            data: {
                img_description: description,
                img_url: s3Result.Location,
                created_at: now,
                img_size
            }
        } as GenerateResponse);

    } catch (error: any) {
        // 错误日志和响应
        console.error("Generate wallpaper error:", error);
        return Response.json({
            code: 500,
            message: error.message || "生成图片失败"
        } as GenerateResponse, { status: 500 });
    }
}
```

回到网页，输入提示词并点击生成按钮，就可以看到在 AWS S3 图床和 Superbase 数据库各生成了一则数据。这代表着我们跑通了流程。

![16](/img/AI/AI-Wallpaper/part3/16.png)
![17](/img/AI/AI-Wallpaper/part3/17.png)
![18](/img/AI/AI-Wallpaper/part3/18.png)

如果出现了问题，且不好定位。就让 AI 帮你生成调试监听，我们能够更快定位到哪个环节出错了。

此外需要注意，直连模式不支持 IPv4，部分系统只能解析到 Supabase 数据库的 IPv6 地址，但无法通过 IPv6 建立连接，导致 `getaddrinfo ENOTFOUND` 或 `ENETUNREACH` 错误。可以采用 Supabase 的 Session Pooler 连接方式。
![19](/img/AI/AI-Wallpaper/part3/19.png)


## 用户登录：Clerk
首先需要梳理哪些地方需要登录。比方说用户进入页面，他可以进行浏览，无需登录。当他想要查看别人的图片详情页或者生成图片时，需要校验他的登录状态。在用户登录环节，由于这个功能相对成熟，我们可以不用专门写代码，可以使用第三方现成的 SDK 集成到自己的项目即可。

我们以 Clerk 为例，登录进入控制台后，首次登录会让你创建项目，输入项目名称后会来到创建项目页面。复制 API keys 并保存到项目文件 /.env.local 中。
![20](/img/AI/AI-Wallpaper/part3/20.png)

输入安装指令，安装 ckerk 的 SDK：

```bash
pnpm add @clerk/nextjs
```

进入 [clerk](https://clerk.com/docs/quickstarts/nextjs)，你可以根据步骤逐步执行，或者像我一样，复制整个页面的代码让 AI 帮我完成注册和登录组件的设计。
![21](/img/AI/AI-Wallpaper/part3/21.png)

如果有报错信息，同样还是丢给 AI，让它帮你调整。
![22](/img/AI/AI-Wallpaper/part3/22.png)

如果 AI 把前端搞得一塌糊涂，你还可以截一个你喜欢的 AI 壁纸网站的图片让它帮你生成页面或组件。
![23](/img/AI/AI-Wallpaper/part3/23.png)

实际操作中，你可以还需要让 AI 处理首次登录账户的跳转逻辑。
![24](/img/AI/AI-Wallpaper/part3/24.png)

同时，确保新用户登录时，我们会读写新用户的用户名，并保存到 superbase 的数据库中。
![25](/img/AI/AI-Wallpaper/part3/25.png)

最后，我希望在壁纸列表中，显示生成图片的真实用户名，使用 Clerk 的 userId 作为唯一标识符，避免用户名重复问题。确保所有壁纸都有用户名和头像，即使是历史数据。
![26](/img/AI/AI-Wallpaper/part3/26.png)

## 项目发布：Vercel

点击 Add New，选择 Project，如果你没有项目，可以新建一个。
![27](/img/AI/AI-Wallpaper/part3/27.png)
![28](/img/AI/AI-Wallpaper/part3/28.png)

进入部署页面，输入项目名称，调整 Build Command 和 Install Command，并输入你放在项目文档中 /.env.local 的变量和变量名，这里可以直接复制粘贴，不用一个个手动输入。此外，也不要忘记输入你的图像生成接口的名称和地址。点击部署就完成了。
![29](/img/AI/AI-Wallpaper/part3/29.png)

如果你使用的是中转接口，登录您的 Vercel 账户，进入您的项目，点击 "Settings" 选项卡，在左侧菜单中选择 "Environment Variables"，添加以下环境变量：
* OPENAI_API_BASE_URL：您的中转接口 URL
* OPENAI_API_KEY：您的 API 密钥

然后回到项目文档 /.env.local，让其使用环境变量：

```bash
import OpenAI from "openai";

export function getOpenAIClient(): OpenAI {
    return new OpenAI({
        apiKey: process.env.OPENAI_API_KEY || "sk-ZDjyPa3L3I8q39GejNEUVTnWZ3tuSt0iA8TpEEVncvNFReLE",
        baseURL: process.env.OPENAI_API_BASE_URL || "https://xiaoai.plus/v1"
    });
}
```

部署过程可能会报错，没有关系，还是问 AI 解决即可。
![30](/img/AI/AI-Wallpaper/part3/30.png)

最终部署提示 Ready，意味着跑通了。你可以在线上环境访问你设计的网站，并生成壁纸。
![31](/img/AI/AI-Wallpaper/part3/31.png)