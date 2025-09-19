# 🔧 SentientResearchAgent 入门

欢迎！本指南将帮助您在几分钟内启动并运行 SentientResearchAgent。让我们构建您的第一个智能代理系统！🚀

## 📋 目录

- [先决条件](#-先决条件)
- [安装](#-安装)
- [快速入门](#-快速入门)
- [您的第一个任务](#-您的第一个任务)
- [使用 Web 界面](#-使用-web-界面)
- [基本 API 使用](#-基本-api-使用)
- [理解输出](#-理解输出)
- [后续步骤](#-后续步骤)
- [故障排除](#-故障排除)

## 📦 先决条件

在开始之前，请确保您拥有：

- **操作系统**：Linux、macOS 或 Windows（带 WSL）
- **Python**：3.12 或更高版本
- **Node.js**：23.11.0 或更高版本（用于前端）
- **Git**：用于克隆仓库

## 🚀 安装

### 选项 1：自动化设置（推荐）

最简单的入门方法：

```bash
# 克隆仓库
git clone https://github.com/yourusername/SentientResearchAgent.git
cd SentientResearchAgent

# 运行设置脚本
./setup.sh
```

选择：
- **Docker 设置** - 隔离环境，非常适合试用
- **原生设置** - 直接安装用于开发

### 选项 2：手动安装

#### 步骤 1：后端设置

```bash
# 安装 PDM (Python 依赖管理器)
pip install pdm

# 初始化项目
pdm init --non-interactive --python 3.12 --dist
pdm config use_uv true

# 安装依赖项
pdm install

# 激活虚拟环境
eval "$(pdm venv activate)"
```

#### 步骤 2：前端设置

```bash
# 导航到前端目录
cd frontend

# 安装依赖项
npm install

# 返回项目根目录
cd ..
```

#### 步骤 3：配置

```bash
# 复制示例环境文件
cp .env.example .env

# 使用您的 API 密钥编辑 .env
# 所需密钥：
# - OPENROUTER_API_KEY（或其他 LLM 提供商）
# - 可选：EXA_API_KEY（用于网络搜索）
```

## 🎯 快速入门

### 1. 启动服务器

```bash
# 简单启动
python -m sentientresearchagent

# 使用自定义配置
python -m sentientresearchagent --config sentient.yaml
```

您应该会看到：
```
🚀 正在 0.0.0.0:5000 启动 Sentient Research Agent 服务器
📡 WebSocket: http://localhost:5000
🌐 前端: http://localhost:3000
📊 系统信息: http://localhost:5000/api/system-info
```

### 2. 打开 Web 界面

在浏览器中导航到 `http://localhost:3000`。您将看到任务执行界面。

### 3. 尝试一个简单任务

在 Web 界面中：
1. 单击“新建任务”
2. 输入目标：`“太阳能有什么好处？”`
3. 单击“执行”
4. 观看系统分解并执行您的任务！

## 🔍 您的第一个任务

让我们了解一下提交任务时会发生什么：

### 示例：研究任务

```python
# 使用 Python API
from sentientresearchagent import SentientAgent

async def main():
    # 创建一个代理
    agent = SentientAgent.create()
    
    # 执行研究任务
    result = await agent.run(
        "比较电动汽车和氢燃料汽车对环境的影响"
    )
    
    print(result)

# 运行示例
import asyncio
asyncio.run(main())
```

### 幕后发生的事情

1. **任务分析** 🔍
   - 系统分析您的目标
   - 确定是否需要分解

2. **规划** 📋
   - 创建包含子任务的计划：
     - 研究电动汽车影响
     - 研究氢燃料汽车影响
     - 比较和综合发现

3. **执行** ⚡
   - 子任务在可能的情况下并行运行
   - 每个任务都使用专业代理

4. **聚合** 📊
   - 结果智能地组合
   - 生成最终报告

## 🖥️ 使用 Web 界面

### 主要功能

#### 1. 任务提交
![任务输入](images/task-input.png)
- 用自然语言输入您的目标
- 选择代理配置文件（可选）
- 配置执行设置

#### 2. 实时可视化
![任务图](images/task-graph.png)
- 实时查看任务分解
- 跟踪执行进度
- 查看任务依赖关系

#### 3. 结果查看
![结果](images/results.png)
- 结构化输出显示
- 下载结果
- 查看执行跟踪

### 界面组件

- **任务树**：所有任务的可视化层次结构
- **状态指示器**：
  - 🔵 PENDING - 等待开始
  - 🟡 RUNNING - 正在执行
  - 🟢 DONE - 成功完成
  - 🔴 FAILED - 遇到错误
- **详细信息面板**：单击任何任务以查看详细信息

## 🔌 基本 API 使用

### REST API

#### 执行任务

```bash
curl -X POST http://localhost:5000/api/simple/execute \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "撰写一篇关于量子计算的博客文章",
    "profile": "general_agent"
  }'
```

#### 快速研究

```bash
curl -X POST http://localhost:5000/api/simple/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "可再生能源的最新发展"
  }'
```

### WebSocket API (实时)

```javascript
// 连接到 WebSocket
const socket = io('http://localhost:5000');

// 监听更新
socket.on('task_update', (data) => {
  console.log('任务更新:', data);
});

// 流式执行
socket.emit('simple_execute_stream', {
  goal: '分析加密货币市场趋势',
  stream: true
});
```

### Python SDK

```python
from sentientresearchagent import ProfiledSentientAgent

# 使用特定配置文件
agent = ProfiledSentientAgent.create_with_profile("deep_research_agent")

# 执行配置
result = await agent.run(
    goal="研究人工智能的历史",
    config={
        "max_depth": 3,
        "enable_caching": True,
        "timeout": 300
    }
)
```

## 📊 理解输出

### 任务结果结构

```json
{
  "task_id": "root",
  "goal": "您的原始目标",
  "status": "DONE",
  "result": {
    "content": "最终合成结果...",
    "metadata": {
      "sources": ["源 1", "源 2"],
      "confidence": 0.95,
      "execution_time": 45.2
    }
  },
  "subtasks": [
    {
      "task_id": "root.1",
      "goal": "子任务 1",
      "result": "..."
    }
  ]
}
```

### 执行跟踪

每次执行都会在 `runtime/projects/traces/` 中创建一个详细的跟踪：
- 任务分解决策
- 代理调用
- 任务之间传递的上下文
- 时间信息

## 🎓 常见用例

### 1. 研究任务

```python
result = await agent.run(
    "研究 2023-2024 年癌症治疗的最新突破"
)
```

### 2. 内容创作

```python
result = await agent.run(
    "创建一份关于可持续生活实践的综合指南"
)
```

### 3. 分析任务

```python
result = await agent.run(
    "分析远程工作对软件开发人员的优缺点"
)
```

### 4. 复杂查询

```python
result = await agent.run(
    "设计一款用于心理健康跟踪的移动应用程序，包括功能、"
    "用户界面模型和实施计划"
)
```

## ⚙️ 配置技巧

### 基本配置

编辑 `sentient.yaml`：

```yaml
# 使用更快的执行速度进行测试
execution:
  max_concurrent_nodes: 5  # 并行运行更多任务
  enable_hitl: false       # 禁用自动化的人工审查

# 选择您的 LLM 提供商
llm:
  provider: "openrouter"
  model_id: "anthropic/claude-3-opus"  # 或任何支持的模型
```

### 代理配置文件

选择预配置的配置文件：
- `general_agent` - 适用于大多数任务的平衡配置
- `deep_research_agent` - 带有引用的彻底研究
- `creative_agent` - 用于创意写作和构思

## 🚨 故障排除

### 常见问题

#### 1. “连接被拒绝”错误

```bash
# 确保服务器正在运行
python -m sentientresearchagent

# 检查端口 5000 是否可用
lsof -i :5000
```

#### 2. “API 密钥无效”错误

```bash
# 验证您的 .env 文件
cat .env | grep API_KEY

# 确保密钥设置正确
export OPENROUTER_API_KEY="您的密钥在这里"
```

#### 3. 前端无法加载

```bash
# 重建前端
cd frontend
npm run build
cd ..

# 重启服务器
python -m sentientresearchagent
```

### 调试模式

使用详细日志运行：

```bash
python -m sentientresearchagent --debug
```

检查 `runtime/logs/sentient.log` 中的日志

## 🎯 后续步骤

现在您已启动并运行：

1. **[核心概念](CORE_CONCEPTS.md)** - 了解系统如何工作
2. **[代理指南](AGENTS_GUIDE.md)** - 创建自定义代理
3. **[示例](examples/)** - 查看高级实现
4. **[API 参考](API_REFERENCE.md)** - 完整的 API 文档

## 💡 专业提示

1. **从简单开始**：从简单的任务开始，然后再进行复杂的任务
2. **使用配置文件**：利用预配置的配置文件以获得更好的结果
3. **监控进度**：观察任务图以了解执行情况
4. **检查跟踪**：执行跟踪有助于调试和优化
5. **缓存结果**：启用缓存以加快重复查询

## 🤝 获取帮助

- **文档**：查看 `/docs` 中的其他指南
- **示例**：浏览 `/notebooks` 中的 Jupyter 示例
- **问题**：在 GitHub 上报告错误
- **社区**：在 GitHub Discussions 中加入讨论

---

准备好构建一些惊人的东西了吗？开始尝试不同的任务，看看 SentientResearchAgent 能做什么！🚀