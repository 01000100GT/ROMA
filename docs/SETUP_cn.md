# SentientResearchAgent 设置指南

本指南提供了使用 Docker 或原生安装（推荐用于开发）设置 ROMA 的详细说明。

## 先决条件

### Docker 设置
- 已安装 Docker 和 Docker Compose
- Git

### 原生设置（Ubuntu/Debian）
- Ubuntu 20.04+ 或 Debian 11+
- sudo 权限
- Git

## 快速入门

```bash
# 克隆仓库
git clone https://github.com/yourusername/SentientResearchAgent.git
cd SentientResearchAgent

# 运行设置脚本
./setup.sh
```

设置脚本将提示您选择：
1. **Docker 设置** - 容器化环境，最适合生产环境
2. **原生设置** - 直接安装，最适合开发

## Docker 设置

### 快速设置
```bash
./setup.sh --docker
# 或
make setup-docker
```

### 功能
1. 检查 Docker 和 Docker Compose 安装
2. 从模板创建 `.env` 文件
3. 使用 UV 构建优化后的 Docker 镜像以实现快速依赖安装
4. 启动所有服务（后端和前端）
5. 验证服务健康状况

### Docker 命令
```bash
# 查看日志
cd docker && docker compose logs -f

# 停止服务
cd docker && docker compose down

# 重启服务
cd docker && docker compose restart

# 查看状态
cd docker && docker compose ps

# 更改后重建
cd docker && docker compose build
```

### Docker 架构
- **后端**：Python 3.12 与 UV 包管理器
- **前端**：Node.js 23.11.0 与 npm 10.9.2
- **卷**：挂载用于实时开发
- **端口**：后端 (5000)，前端 (5173)

## 原生设置（Ubuntu/Debian）

### 快速设置
```bash
./setup.sh --native
# 或
make setup-native
```

### 功能
1. 从 deadsnakes PPA 安装 Python 3.12
2. 安装 PDM 和 UV 包管理器
3. 安装 NVM、Node.js 23.11.0 和 npm 10.9.2
4. 初始化 PDM 项目，使用 UV 后端
5. 创建虚拟环境并安装依赖
6. 安装前端依赖
7. 创建必要的目录

### 手动步骤

#### 1. 安装 Python 3.12
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### 2. 安装 PDM 和 UV
```bash
# 安装 PDM
curl -sSL https://pdm-project.org/install-pdm.py | python3 -

# 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 添加到 PATH（添加到 ~/.bashrc）
export PATH="$HOME/.local/bin:$PATH"
source "$HOME/.cargo/env"
```

#### 3. 安装 Node.js
```bash
# 安装 NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# 安装 Node.js 和 npm
nvm install 23.11.0
nvm use 23.11.0
npm install -g npm@10.9.2
```

#### 4. 项目设置
```bash
# 初始化 PDM
pdm init --non-interactive --python 3.12 --dist
pdm config use_uv true

# 安装依赖
eval "$(pdm venv activate)"
pdm install

# 安装前端
cd frontend && npm install
```

### 配置
1. 将 `.env.example` 复制到 `.env`
2. 添加您的 LLM API 密钥
3. **可选**：配置全面的 S3 挂载：
   ```bash
   # ===== S3 挂载配置 =====
   # 启用 S3 挂载（接受：true/yes/1/on/enabled）
   S3_MOUNT_ENABLED=true
   
   # 通用挂载目录（所有平台相同）
   S3_MOUNT_DIR=/opt/sentient
   
   # AWS S3 配置
   S3_BUCKET_NAME=您的-s3-存储桶
   AWS_ACCESS_KEY_ID=您的_aws_密钥
   AWS_SECRET_ACCESS_KEY=您的_aws_秘密
   AWS_REGION=us-east-1
   
   # ===== E2B 集成（可选）=====
   E2B_API_KEY=您的_e2b_api_密钥_在这里
   ```
4. 根据需要自定义 `sentient.yaml`

**🔒 配置中的安全功能：**
- **路径验证**：挂载目录经过验证，防止注入攻击
- **AWS 验证**：在尝试挂载之前测试凭据
- **FUSE 检查**：自动验证系统依赖
- **挂载验证**：在继续之前进行全面的功能测试
- **灵活的布尔值**：`S3_MOUNT_ENABLED` 接受多种 true/false 格式

### 💾 S3 数据持久性

SentientResearchAgent 包含一个全面的 S3 挂载解决方案，可在所有环境中实现无缝数据持久性：

```bash
# 设置期间，系统会询问您：
# “设置 S3 挂载以实现数据持久性吗？(y/n)”

# 通用挂载目录：/opt/sentient（所有平台相同）
```

**🔒 企业级安全功能：**
- 🛡️ **路径注入保护** - 经过验证的挂载目录可防止安全漏洞
- 🔐 **AWS 凭证验证** - 挂载前的预检可确保 S3 存储桶访问
- 📁 **安全环境解析** - 安全处理配置文件和环境变量
- 🔍 **挂载验证** - 在继续之前对挂载功能进行全面测试
- ⚡ **FUSE 依赖检查** - 自动验证 macFUSE/FUSE 要求

**🚀 高级挂载功能：**
- 🔄 **精确路径匹配** - 本地、Docker 和 E2B 环境中相同的挂载路径
- ⚡ **零同步延迟** - 通过高性能 goofys 挂载实现实时文件系统访问
- 📁 **动态项目隔离** - 运行时基于项目的文件夹，具有可配置的结构
- 🛠 **跨平台支持** - 在 macOS 和 Linux 上无缝运行，并自动安装
- 🔐 **持久服务** - 通过 systemd/launchd 自动挂载启动，并进行适当配置
- 🔧 **灵活配置** - 布尔值接受多种格式（true/yes/1/on/enabled）

**🏗️ 架构优势：**
1. **统一数据层**：所有环境都访问完全相同的 S3 挂载目录
2. **无路径转换**：通过所有系统中的一致 `${S3_MOUNT_DIR}` 消除复杂性
3. **即时可用性**：数据工具包写入的文件立即出现在 E2B 沙盒中
4. **安全 Docker 集成**：动态 compose 文件选择，具有经过验证的挂载路径
5. **生产就绪**：具有全面错误处理的企业安全验证

**工作原理：**
```bash
# 本地系统：数据工具包保存到
${S3_MOUNT_DIR}/project_123/binance/price_data_1642567890.parquet

# Docker 容器：完全相同的路径
${S3_MOUNT_DIR}/project_123/binance/price_data_1642567890.parquet  

# E2B 沙盒：相同的路径结构
${S3_MOUNT_DIR}/project_123/binance/price_data_1642567890.parquet
```

确保 S3_MOUNT_DIR 在所有平台中都是通用的绝对路径，以便文件路径保持一致。

**完美的数据一致性，零配置开销！**

### 🐳 使用 goofys 的 Docker S3 挂载（setup.sh 管道）

当您运行 `./setup.sh` 并选择 Docker 时，脚本会：

1. 验证 `.env` 中的 `S3_MOUNT_ENABLED` 和 `S3_MOUNT_DIR`。
2. 如果启用且有效，则使用 `docker/docker-compose.yml` 和 S3 覆盖 `docker/docker-compose.s3.yml` 启动 Compose。
3. 覆盖权限，授予容器内部 `goofys` 所需的 FUSE 权限（`/dev/fuse`、`SYS_ADMIN`、apparmor unconfined）。
4. 后端容器入口点运行 `/usr/local/bin/startup.sh`，它在启动应用程序之前使用 `goofys` 挂载 S3。

macOS 注意（Docker 模式）：Docker Desktop 不支持容器内的 FUSE 挂载。我们的设置在主机上以通用路径（`/opt/sentient`）挂载 S3，并将其绑定挂载到容器中。容器启动时会检测现有挂载并验证其是否映射到预期存储桶，从而跳过容器内的 goofys。在 Linux Docker 引擎上，容器可以直接挂载。

通过 `.env` 中的环境变量 `GOOFYS_EXTRA_ARGS` 传递额外的 `goofys` 标志：

```bash
# .env
S3_MOUNT_ENABLED=true
S3_MOUNT_DIR=/opt/sentient
S3_BUCKET_NAME=您的-s3-存储桶
AWS_ACCESS_KEY_ID=您的_密钥
AWS_SECRET_ACCESS_KEY=您的_秘密
AWS_REGION=us-east-1

# 可选：额外的 goofys 标志
GOOFYS_EXTRA_ARGS="--allow-other --stat-cache-ttl=10s --type-cache-ttl=10s"
```

注意：
- `.env` 中的所有变量都由 Compose 注入到后端容器中，并由 `startup.sh` 读取。
- 镜像中指定的命令 (`uv run python -m sentientresearchagent`) 由 `startup.sh` 通过 `exec "$@"` 原样转发。

### 运行应用程序

#### 使用 Screen（推荐）
```bash
# 启动后端
screen -S backend_server
eval "$(pdm venv activate)"
python -m sentientresearchagent
# 按 Ctrl+A，然后按 D 键分离

# 启动前端
screen -S frontend_server
cd frontend && npm run dev
# 按 Ctrl+A，然后按 D 键分离

# 查看屏幕
screen -ls

# 重新连接到屏幕
screen -r backend_server
```

#### 直接运行
```bash
# 终端 1 - 后端
eval "$(pdm venv activate)"
python -m sentientresearchagent

# 终端 2 - 前端
cd frontend && npm run dev
```

## 环境配置

### API 密钥
两种设置方法都需要 `.env` 文件中的 API 密钥：

```bash
# OpenRouter API 密钥（必需）
OPENROUTER_API_KEY=您的_openrouter_api_密钥_在这里

# 可选 API 密钥
EXA_API_KEY=您的_exa_api_密钥_在这里
GOOGLE_GENAI_API_KEY=您的_google_genai_api_密钥_在这里
```

### 配置文件
- **主配置文件**：`sentient.yaml`
- **环境**：`.env`（从 `.env.example` 创建）
- **代理配置文件**：`src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles/`

## 故障排除

### 常见问题

#### Docker 问题
- **端口冲突**：确保端口 5000 和 5173 空闲
- **权限被拒绝**：使用 sudo 运行 Docker 命令或将用户添加到 docker 组
- **构建失败**：使用 `docker system prune` 清除 Docker 缓存

#### 原生设置问题
- **Python 版本**：确保 Python 3.12 处于活动状态
- **找不到 PDM**：将 `~/.local/bin` 添加到 PATH
- **找不到 UV**：Source `~/.cargo/env`
- **Node 版本**：使用 `nvm use 23.11.0` 切换版本

### 健康检查
```bash
# 检查后端
curl http://localhost:5000/api/health

# 检查前端
curl http://localhost:3000
```

### 日志
- **Docker 日志**：`cd docker && docker compose logs -f`
- **原生日志**：检查项目根目录中的 `logs/` 目录

## 开发工作流

### 进行更改
1. **后端**：`src/` 中的更改会自动重新加载
2. **前端**：Vite HMR 提供即时更新
3. **配置**：更改 `sentient.yaml` 后重启服务

### 使用不同的代理配置文件
```bash
# 使用特定配置
python -m sentientresearchagent --config sentient.yaml

# 使用不同的配置文件
python -m sentientresearchagent --profile deep_research_agent