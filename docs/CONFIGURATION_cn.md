# ⚙️ 配置指南

本指南涵盖了 SentientResearchAgent 中的所有配置选项，帮助您根据特定需求调整系统。

## 📋 目录

- [配置概述](#-配置概述)
- [配置文件结构](#-配置文件结构)
- [LLM 配置](#-llm-配置)
- [执行配置](#-执行配置)
- [缓存配置](#-缓存配置)
- [日志配置](#-日志配置)
- [HITL 配置](#-hitl-配置)
- [代理配置文件](#-代理配置文件)
- [环境变量](#-环境变量)
- [高级配置](#-高级配置)
- [配置示例](#-配置示例)

## 🌐 配置概述

SentientResearchAgent 使用分层配置系统：

1. **默认配置** - 内置默认值
2. **YAML 配置** - `sentient.yaml` 文件
3. **环境变量** - 覆盖特定值
4. **运行时配置** - 程序化覆盖

### 配置优先级

```
运行时配置 > 环境变量 > YAML 文件 > 默认值
```

### 主配置文件

主配置文件是项目根目录下的 `sentient.yaml`：

```yaml
# sentient.yaml - 主配置文件
llm:
  provider: "openrouter"
  api_key: "${OPENROUTER_API_KEY}"  # 环境变量引用

execution:
  max_concurrent_nodes: 10
  enable_hitl: true

# ... 更多配置
```

## 📁 配置文件结构

### 完整配置模式

```yaml
# LLM 基础设施
llm:
  provider: string              # LLM 提供者
  api_key: string              # API 密钥（可使用环境变量）
  timeout: float               # 请求超时时间（秒）
  max_retries: integer         # 重试次数
  base_url: string             # 可选的自定义端点

# 缓存系统
cache:
  enabled: boolean             # 启用/禁用缓存
  cache_type: string           # "file" 或 "memory"
  ttl_seconds: integer         # 缓存存活时间
  max_size: integer            # 最大缓存条目数

# 执行框架
execution:
  max_concurrent_nodes: integer # 并行执行限制
  max_parallel_nodes: integer   # 批处理大小
  max_execution_steps: integer  # 最大执行步骤数
  rate_limit_rpm: integer       # 速率限制（请求/分钟）
  enable_hitl: boolean          # 启用人在回路
  # ... 更多执行选项

# 日志记录
logging:
  level: string                # 日志级别
  enable_console: boolean      # 控制台输出
  enable_file: boolean         # 文件日志记录
  console_style: string        # 输出样式

# 实验配置
experiment:
  base_dir: string             # 实验目录
  retention_days: integer      # 数据保留期

# 环境
environment: string            # "development", "production" 等

# 默认代理配置文件
default_profile: string        # 要使用的默认代理配置文件
```

## 🤖 LLM 配置

### 基本 LLM 设置

```yaml
llm:
  provider: "openrouter"       # 选项：openrouter, openai, anthropic, google
  api_key: "${OPENROUTER_API_KEY}"  # 使用环境变量
  timeout: 300.0               # 5 分钟超时
  max_retries: 3               # 重试失败请求
```

### 特定提供商配置

#### OpenRouter
```yaml
llm:
  provider: "openrouter"
  api_key: "${OPENROUTER_API_KEY}"
  base_url: "https://openrouter.ai/api/v1"
  default_model: "anthropic/claude-3-opus"
  headers:
    HTTP-Referer: "https://yourapp.com"
    X-Title: "SentientResearchAgent"
```

#### OpenAI
```yaml
llm:
  provider: "openai"
  api_key: "${OPENAI_API_KEY}"
  organization: "${OPENAI_ORG_ID}"  # 可选
  default_model: "gpt-4-turbo-preview"
```

#### Anthropic
```yaml
llm:
  provider: "anthropic"
  api_key: "${ANTHROPIC_API_KEY}"
  default_model: "claude-3-opus-20240229"
  max_tokens: 4096
```

#### Google (Gemini)
```yaml
llm:
  provider: "google"
  api_key: "${GOOGLE_GENAI_API_KEY}"
  default_model: "gemini-pro"
  safety_settings:
    harassment: "BLOCK_NONE"
    hate_speech: "BLOCK_NONE"
```

### 模型选择策略

```yaml
llm:
  model_selection:
    # 针对不同任务使用不同模型
    simple_tasks: "gpt-3.5-turbo"
    complex_tasks: "gpt-4"
    creative_tasks: "claude-3-opus"
    
  # 回退配置
  fallback_models:
    - "gpt-4"
    - "claude-3-sonnet"
    - "gpt-3.5-turbo"
```

## ⚡ 执行配置

### 核心执行设置

```yaml
execution:
  # 并发控制
  max_concurrent_nodes: 10      # 最大并行任务数
  max_parallel_nodes: 8         # 批处理大小
  enable_immediate_slot_fill: true  # 动态任务调度
  
  # 执行限制
  max_execution_steps: 500      # 最大总步骤数
  max_recursion_depth: 5        # 最大任务深度
  node_execution_timeout_seconds: 2400.0  # 40 分钟
  
  # 速率限制
  rate_limit_rpm: 30            # 每分钟请求数
  rate_limit_strategy: "adaptive"  # 或 "fixed"
```

### 超时配置

```yaml
execution:
  timeout_strategy:
    warning_threshold_seconds: 60.0    # 慢任务警告阈值
    soft_timeout_seconds: 180.0        # 尝试优雅停止
    hard_timeout_seconds: 300.0        # 强制终止
    max_recovery_attempts: 3           # 恢复尝试次数
    enable_aggressive_recovery: true   # 激进的死锁恢复
```

### 状态管理

```yaml
execution:
  # 状态更新优化
  state_batch_size: 50          # 批处理状态更新
  state_batch_timeout_ms: 100   # 刷新超时
  enable_state_compression: true # 压缩大状态
  
  # WebSocket 优化
  ws_batch_size: 50             # WebSocket 批处理大小
  ws_batch_timeout_ms: 100      # WebSocket 刷新超时
  enable_ws_compression: true   # 压缩有效负载
  enable_diff_updates: true     # 仅发送更改
```

### 任务处理规则

```yaml
execution:
  # 规划控制
  force_root_node_planning: true  # 根节点始终规划
  skip_atomization: false         # 跳过原子化检查
  atomization_threshold: 0.7      # 复杂性阈值
  
  # 执行策略
  execution_strategy: "balanced"  # 选项：aggressive, balanced, conservative
  optimization_level: "balanced"  # 选项：none, balanced, aggressive
```

## 💾 缓存配置

### 基本缓存设置

```yaml
cache:
  enabled: true
  cache_type: "file"            # 选项：file, memory, redis
  ttl_seconds: 7200             # 2 小时缓存生命周期
  max_size: 500                 # 最大缓存条目数
```

### 高级缓存配置

```yaml
cache:
  # 文件缓存设置
  cache_dir: "runtime/cache/agent"  # 缓存目录
  
  # 缓存策略
  eviction_policy: "lru"        # 选项：lru, lfu, fifo
  
  # 选择性缓存
  cache_filters:
    min_execution_time: 5.0     # 仅缓存慢操作
    min_token_count: 100        # 仅缓存实质性响应
    
  # 缓存预热
  warm_cache_on_startup: true
  cache_warming_profile: "common_queries"
```

### 缓存键配置

```yaml
cache:
  key_generation:
    include_model: true         # 在缓存键中包含模型
    include_temperature: true   # 包含温度
    include_profile: true       # 包含代理配置文件
    normalize_whitespace: true  # 规范化查询空白
```

## 📝 日志配置

### 基本日志记录

```yaml
logging:
  level: "INFO"                 # 选项：DEBUG, INFO, WARNING, ERROR
  enable_console: true
  enable_file: true
  file_rotation: "10 MB"        # 按大小轮换
  file_retention: 3             # 保留 3 个日志文件
```

### 控制台输出样式

```yaml
logging:
  console_style: "clean"        # 选项：clean, timestamp, detailed
  
  # 样式定义：
  # clean: 只有带颜色的消息
  # timestamp: 包含时间戳
  # detailed: 完整详细信息（时间、级别、模块）
```

### 模块特定日志记录

```yaml
logging:
  # 减少特定模块的噪音
  module_levels:
    "sentientresearchagent.server.services.broadcast_service": "WARNING"
    "sentientresearchagent.server.services.project_service": "WARNING"
    "sentientresearchagent.core.project_manager": "WARNING"
    "sentientresearchagent.hierarchical_agent_framework.graph": "INFO"
    "sentientresearchagent.hierarchical_agent_framework.node": "DEBUG"
```

### 结构化日志记录

```yaml
logging:
  # 用于分析的结构化日志记录
  structured:
    enabled: true
    format: "json"              # 选项：json, logfmt
    include_context: true       # 包含执行上下文
    include_metrics: true       # 包含性能指标
```


## 👥 代理配置文件

### 配置文件配置

```yaml
# 默认配置文件选择
default_profile: "general_agent"

# 配置文件特定覆盖
profiles:
  deep_research_agent:
    execution:
      max_concurrent_nodes: 20  # 更多并行度
      max_recursion_depth: 7    # 更深层次的研究
    cache:
      ttl_seconds: 14400        # 更长的缓存（4 小时）
      
  quick_response_agent:
    execution:
      max_concurrent_nodes: 3   # 更少的并行度
      max_execution_steps: 50   # 更少的步骤
    llm:
      timeout: 30.0             # 更快的超时
```

## 🔐 环境变量

### 支持的环境变量

```bash
# API 密钥
OPENROUTER_API_KEY=sk-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GENAI_API_KEY=...
EXA_API_KEY=...

# 配置覆盖
SENTIENT_CONFIG_PATH=/path/to/custom/config.yaml
SENTIENT_PROFILE=deep_research_agent
SENTIENT_LOG_LEVEL=DEBUG
SENTIENT_CACHE_ENABLED=true

# 服务器配置
SENTIENT_HOST=0.0.0.0
SENTIENT_PORT=5000
SENTIENT_DEBUG=false

# 功能标志
SENTIENT_ENABLE_HITL=true
SENTIENT_ENABLE_CACHE=true
SENTIENT_ENABLE_METRICS=true
```

### 在配置中使用环境变量

```yaml
# 引用环境变量
llm:
  api_key: "${OPENROUTER_API_KEY}"
  
# 带默认值
cache:
  enabled: "${SENTIENT_CACHE_ENABLED:true}"  # 默认值为 true
  
# 条件配置
execution:
  enable_hitl: "${SENTIENT_ENABLE_HITL:false}"