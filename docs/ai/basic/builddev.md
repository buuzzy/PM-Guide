---
sidebar_label: '搭建开发环境'
title: '搭建开发环境' 
---

## 安装软件

### 1. 代码编辑器

代码编辑器通过对应下载地址安装，安装步骤可以按默认选项执行。

| 电脑系统    | 软件名称    | 下载地址                               |
| ------- | ------- | ---------------------------------- |
| Windows | VS Code | https://code.visualstudio.com/     |
| Mac     | X Code  | https://developer.apple.com/xcode/ |

以 VS Code 安装为例：

1. 从官网下载，完成后本地安装；

2. 打开软件，登录 Github 账号（若无则跳过）；

3. 主题配置，建议选择日间版，相较于夜间版更护眼；

4. 勾选启用 Cpoilot，也就是 AI 辅助编程



其他代码编辑器（IDE）还有很多，功能都类似，可以选择你喜欢的工具：

* Trae：https://www.trae.com.cn/

* Cursor：https://www.cursor.com/

* Windsurf：https://codeium.com/windsurf



### 2. 终端工具

终端工具用于跑一些命令，运行和调试项目。

| 电脑系统    | 软件名称             | 下载地址                                                       |
| ------- | ---------------- | ---------------------------------------------------------- |
| Windows | Windows Terminal | https://learn.microsoft.com/zh-cn/windows/terminal/install |
| Mac     | iterm2           | https://iterm2.com/                                        |
|         | WSL2（暂不要求）       | 通过 Linxu 子系统协同开发，可百度了解或 B 站搜教程        |



## 安装插件（VS Code）

### 1. 插件

| 名称          | 功能     | 截图|
| ----------- | ------ | ----|
| Prettier    | 代码格式化  | ![01](/img/AI/basic/builddev/01.png) |
| REST Client | API 调试 | ![02](/img/AI/basic/builddev/02.png) |

### 2. 安装路径

以 VS Code 为例，点击软件左侧 Extensions 搜索对应插件名称，也可以通过快捷键唤起。

![03](/img/AI/basic/builddev/03.png)



## 配置终端

| 软件名称      | 适用系统        | 简介| 命令行 / 下载地址           |
| --------- | ----------- | ---- | -------------------- |
| Homebrew  | Mac         | 一个软件包管理工具，可以帮你下载/更新Mac 终端上的软件  | # 更新homebrew自身 <br/>brew update<br/> # 更新已经安装的软件包<br/>brew upgrade<br/># 安装常用的软件包 <br/>brew install git curl wget unzip<br/>|
| oh-my-zsh | Mac         | 一个终端配置库，可以让你的终端看起来更美观，有一些命令快捷键，让你日常使用起来更方便。不安装对开发项目没影响，安装了可以让开发效率更高。 | https://ohmyz.sh/    |
| git       | Mac/Windows | 帮助你管理代码，可以切换分支，提交修改，回滚恢复修改等。一般终端工具都默认安装了 git，如果没有默认安装，可以自行搜索安装 git。  | https://git-scm.com/ |

## 安装依赖

### 1. fnm

fnm 是一个 nodejs 版本管理工具，可以帮你管理多个 nodejs 版本。你参考官网 github 说明进行安装：https://github.com/Schniz/fnm。Windows 系统可以参照下面的截图进行按照。

**① Mac**

安装 fnm 后，需要把下面的命令配置到 \~/.zshrc，确保 fnm 能正确执行：

````bash
# 使用 nano 编辑器（直接在终端中编辑）
# 打开终端，输入以下命令来编辑文件（以 ~/.zshrc 为例）：
```nano ~/.zshrc ```
````

或者直接用brew安装：brew install fnm

```bash
# 输入which fnm 查看路径（查到路径后可以问gpt对应的配置命令）

# fnm
## mac
export PATH="$HOME/Library/Application Support/fnm:$PATH"
eval "`fnm env`"

## windows
export PATH="$HOME/D/fnm:$PATH"
eval "`fnm env`"
```

**② Windows**

打开 PowerShell，可以通过 Win+R 唤起运行，输入 PowerShell 打开终端。

![04](/img/AI/basic/builddev/04.png)

```powershell
# 设置 PowerShell 执行策略：
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# 当提示是否执行策略时，输入 Y 并回车

# 安装 Scoop：
irm get.scoop.sh | iex

# 等待安装完成，安装 fnm：
scoop install fnm

# fnm 安装完成后，配置 PowerShell：
if(-not(Test-Path $profile)){ New-Iten $profile -Force } notepad $profile

# 在打开的记事本中添加下面这行代码：
fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
# 保存并关闭记事本

# 重启 PowerShell，验证安装：
fnm --version
# 如果显示版本号，说明安装成功
```

### 2. nodejs

nodejs 是一种基础编程语言，跟 go/php/python/java 一样的性质，前端开发领域用的比较多。

安装完 fnm 之后，你可以选择安装一个 nodejs 版本，**推荐安装下面这个版本。**

```powershell
# 安装nodejs
fnm install v19.8.1

# 查看 nodejs 版本
node -v

# 查看 npm 版本
npm -v
```

![05](/img/AI/basic/builddev/05.png)

### 3. pnpm

pnpm 是一个更好的 npm 依赖管理工具。推荐安装。

```powershell
# 安装 pnpm
npm i -g pnpm

# 如果你使用的是 Windows 系统，请参考以下方式安装：
Invoke-WebRequest https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression

## 如果安装失败，参考第二种方法：
npm install -g pnpm

## 如果安装失败，参考第三种方法：
iwr https://get.pnpm.io/install.ps1 -useb | iex

# 查看 pnpm 版本
pnpm -v
``` 