##  3D 粒子交互系统

芙芙可爱喵~

[立即体验](https://titroupast.github.io/threejs-particles/)

[博客链接](https://titroupast.github.io/fufu_Blog/2025/12/06/3D%E7%B2%92%E5%AD%90%E4%BA%A4%E4%BA%92%E7%B3%BB%E7%BB%9F/)

[GitHub链接](https://github.com/Titroupast/threejs-particles)

![8843670064bd7936ac2278c51ebe422e](https://gastigado.cnies.org/d/public/8843670064bd7936ac2278c51ebe422e.jpg)

### 🎀 项目简介 (Project Overview)

本项目诞生于对最近很火的**3D 粒子交互**。

最近，Web 开发界兴起了利用像 **Gemini** 这样的大型语言模型来生成复杂的 **3D 粒子交互代码** 的热潮。这个项目正是受此启发，进一步思考：既然 AI 可以生成**代码逻辑**，我们是否能将**素材的生成流程**也变得同样自动化和简便呢？

核心灵感在于：**将二维的图片素材** 转换成 **三维的粒子模型数据**，从而将任何一张富有创意的图像，融入到 Three.js 的粒子世界中。

这个工具旨在为 **Three.js/MediaPipe** 驱动的粒子交互应用，提供一个完整的 **模型数据生成、注入和管理** 解决方案，让用户能够轻松地将个性化的图片（如角色、Logo 或图标）变成可以被手势操控的 3D 粒子效果。

整个项目分为两个主要部分：

1.  **💻 Python/CustomTkinter GUI 工具 (`particle_manager.py`)**:
    * **核心功能**: 将用户选择的 PNG/JPG 图片转换为 **Float32Array** 格式的粒子位置和颜色数据。
    * **模型注入**: 自动将生成的 JS 文件保存到项目的 `models` 文件夹，并更新 `index.html` 的 `<head>` 区域以引用该文件。
    * **模型管理**: 扫描并列出 HTML 中引用的模型文件，允许用户一键从项目和 HTML 中彻底删除。
2.  **🌐 Web 交互前端 (`index.html` + JS)**:
    * 基于 **Three.js** 渲染粒子效果。
    * 使用 **MediaPipe Hands** 实现手势交互 ，控制粒子的缩放和爆炸效果。
    * 能够动态加载并切换内置形状（如爱心、土星）和自定义图片模型。

---



### 📋 依赖需求 (Requirements)

为了让这个美丽的工具和应用能够正常运行，您需要准备以下环境和依赖：



#### ⚙️ Python 后端 (项目管理器)

| **依赖名称**      | **用途**                                     | **安装命令**                |
| ----------------- | -------------------------------------------- | --------------------------- |
| **Python 3.x**    | 运行管理器的主程序。                         | (无)                        |
| **CustomTkinter** | 用于创建现代化、美观的桌面 GUI 界面。        | `pip install customtkinter` |
| **Pillow (PIL)**  | 用于加载、处理和分析源图片（提取像素数据）。 | `pip install Pillow`        |

> 💖 **注意**: `particle_manager.py` 文件依赖于 Python 的 **`tkinter`** 库（通常随标准 Python 安装），以及上述额外的 `customtkinter` 和 `Pillow` 库。

---



#### 💻 Web 前端 (3D 粒子应用)

Web 应用主要通过 **CDN** 引入外部库，无需本地安装：

| **库/框架**             | **用途**                      | **CDN 链接 (已在 HTML 中引用)**                           |
| ----------------------- | ----------------------------- | --------------------------------------------------------- |
| **Three.js**            | 核心 3D 渲染引擎。            | `https://unpkg.com/three@0.132.2/build/three.min.js`      |
| **MediaPipe Hands**     | 用于手势识别和追踪。          | `https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js`  |
| **MediaPipe Utilities** | 配合 MediaPipe 使用的工具库。 | `camera_utils.js`, `control_utils.js`, `drawing_utils.js` |

> 🌐 **运行环境**: 任何现代浏览器 (如 Chrome, Edge) 均可，但必须支持 **WebGL** 和 **摄像头权限** 才能启用手势交互功能。

---



### 🚀 运行指南 (Getting Started)

#### 1. 启动管理器

Bash

```bash
python particle_manager.py
```



#### 2. 使用步骤 (新增模型)

1. **选择项目根目录**: 点击 **[选择文件夹]**，选择包含 `index.html` 的目录。管理器会自动创建 `models` 文件夹。
2. **选择源图片**: 点击**[选择图片]**，选择一张您想要转换的 **PNG (推荐透明背景)** 或 JPG 图片。
3. **填写信息**: 输入 **名称 (中文)** 和 **ID (英文)**，ID 将用于生成文件名和 JS 键名。
4. **调整粒子数**: 使用滑块调整生成粒子的数量。
5. **生成并注入**: 点击 **[⚡ 生成并注入到 models 文件夹 ⚡]**，工具将生成 `[ID]_data.js` 文件，并自动修改 `index.html`。



#### 3. 使用步骤 (删除模型)

1. **刷新列表**: 在 **[🗑️ 删除管理]** 标签页，点击 **[🔄 刷新列表]**，加载 `index.html` 中引用的模型文件。
2. **选择文件**: 从下拉菜单中选择要删除的模型文件。
3. **彻底删除**: 点击 **[🗑️ 彻底删除选中模型]**，管理器将删除物理 JS 文件并清除 `index.html` 中对应的 `<script>` 标签。



可视化交互界面如下：

![image-20251206215911435](https://gastigado.cnies.org/d/public/image-20251206215911435.png)