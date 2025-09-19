# 🤖 代理全面指南

本指南涵盖了 SentientResearchAgent 中关于代理的所有内容——从使用现有代理到创建自定义代理。

## 📋 目录

- [什么是代理？](#-什么是代理)
- [代理类型](#-代理类型)
- [可用代理](#-可用代理)
- [代理配置文件](#-代理配置文件)
- [使用代理](#-使用代理)
- [创建自定义代理](#-创建自定义代理)
- [代理配置](#-代理配置)
- [提示工程](#-提示工程)
- [最佳实践](#-最佳实践)
- [高级主题](#-高级主题)

## 🎯 什么是代理？

代理是 SentientResearchAgent 中的智能工作者。每个代理：
- **专注于**特定类型的任务
- **封装**提示、模型、工具和逻辑
- **处理**任务节点以生成结果
- **集成**各种 LLM 提供商

将代理视为您人工智能公司中的专业员工，每个人都精通自己的特定工作。

## 🏷️ 代理类型

### 1. 🔍 原子化代理

**目的**：确定任务是否需要分解

```yaml
- name: "SmartAtomizer"
  type: "atomizer"
  description: "智能地确定任务复杂度"
```

**输入/输出**：
```python
Input: 带有目标的 TaskNode
Output: {
  "is_atomic": bool,
  "reasoning": "任务需要多个研究步骤",
  "refined_goal": "原始目标的增强版本"
}
```

### 2. 📋 规划代理

**目的**：将复杂任务分解为子任务

```yaml
- name: "DeepResearchPlanner"
  type: "planner"
  description: "创建全面的研究计划"
```

**输入/输出**：
```python
Input: 目标 + 上下文
Output: {
  "subtasks": [
    {"goal": "研究主题 A", "type": "SEARCH"},
    {"goal": "分析发现", "type": "THINK"},
    {"goal": "撰写摘要", "type": "WRITE"}
  ],
  "reasoning": "彻底研究的结构化方法"
}
```

### 3. ⚡ 执行代理

**目的**：执行实际工作

```yaml
- name: "WebSearcher"
  type: "executor"
  task_type: "SEARCH"
  description: "在网络上搜索信息"
```

**类别**：
- **搜索执行器**：信息检索
- **写入执行器**：内容生成
- **思考执行器**：分析和推理

### 4. 🔄 聚合代理

**目的**：合并子任务的结果

```yaml
- name: "ResearchAggregator"
  type: "aggregator"
  description: "综合研究发现"
```

**输入/输出**：
```python
Input: 子结果数组
Output: {
  "synthesis": "综合发现显示...",
  "key_points": ["要点 1", "要点 2"],
  "conclusion": "总体结论"
}
```

### 5. 🔧 计划修改代理

**目的**：根据 HITL 反馈调整计划

```yaml
- name: "PlanModifier"
  type: "plan_modifier"
  description: "将人工反馈整合到计划中"
```

## 📚 可用代理

### 核心代理

#### 研究与搜索代理

| 代理名称 | 类型 | 目的 | 最适合 |
|------------|------|---------|----------|
| `OpenAICustomSearcher` | 执行器 | 使用 OpenAI 进行网络搜索 | 一般研究 |
| `ExaSearcher` | 执行器 | 学术/技术搜索 | 科学论文 |
| `EnhancedSearchPlanner` | 规划器 | 搜索任务分解 | 复杂研究 |

#### 写作代理

| 代理名称 | 类型 | 目的 | 最适合 |
|------------|------|---------|----------|
| `BasicReportWriter` | 执行器 | 一般写作 | 报告、文章 |
| `CreativeWriter` | 执行器 | 创意内容 | 故事、剧本 |
| `TechnicalWriter` | 执行器 | 技术文档 | 文档 |

#### 分析代理

| 代理名称 | 类型 | 目的 | 最适合 |
|------------|------|---------|----------|
| `BasicReasoningExecutor` | 执行器 | 逻辑与分析 | 问题解决 |
| `DataAnalyzer` | 执行器 | 数据解释 | 统计、趋势 |
| `StrategyPlanner` | 执行器 | 战略思维 | 规划、决策 |

### 专业规划器

```yaml
# 深度研究规划器 - 全面研究
DeepResearchPlanner:
  - 多阶段研究方法
  - 引用追踪
  - 事实核查

# 增强搜索规划器 - 优化搜索
EnhancedSearchPlanner:
  - 日期感知搜索
  - 并行搜索策略
  - 来源多样性

# 创意项目规划器 - 创意工作流程
CreativeProjectPlanner:
  - 构思阶段
  - 迭代细化
  - 多模态输出
```

## 🎨 代理配置文件

代理配置文件是针对特定用例优化的预配置代理集合。

### 可用配置文件

#### 1. 🔬 深度研究代理

```yaml
profile: deep_research_agent
purpose: "带引用的全面研究"
agents:
  root_planner: "DeepResearchPlanner"
  search_executor: "OpenAICustomSearcher"
  aggregator: "ResearchAggregator"
```

**最适合**：
- 学术研究
- 市场分析
- 事实核查
- 文献综述

#### 2. 🌐 通用代理

```yaml
profile: general_agent
purpose: "均衡的通用任务"
agents:
  planner: "CoreResearchPlanner"
  executor: "BasicReasoningExecutor"
  aggregator: "GeneralAggregator"
```

**最适合**：
- 混合任务
- 快速查询
- 一般问答
- 探索性工作

#### 3. 💰 加密货币分析代理

```yaml
profile: crypto_analytics_agent
purpose: "加密货币分析"
agents:
  planner: "CryptoAnalysisPlanner"
  data_fetcher: "CryptoDataSearcher"
  analyzer: "TechnicalAnalyzer"
```

**最适合**：
- 市场分析
- 代币研究
- DeFi 协议
- 交易策略

### 使用配置文件

```python
# Python API
from sentientresearchagent import ProfiledSentientAgent

agent = ProfiledSentientAgent.create_with_profile("deep_research_agent")
result = await agent.run("研究量子计算应用")
```

```bash
# CLI
python -m sentientresearchagent --profile deep_research_agent
```

## 🔨 使用代理

### 直接使用代理

```python
# 获取特定代理
from sentientresearchagent.agents import AgentRegistry

registry = AgentRegistry()
search_agent = registry.get_agent(
    action_verb="execute",
    task_type="SEARCH"
)

# 使用代理
result = await search_agent.process(task_node)
```

### 代理选择策略

框架根据以下因素自动选择代理：

1. **任务类型** (SEARCH, WRITE, THINK)
2. **动作动词** (plan, execute, aggregate)
3. **配置文件配置**
4. **节点上下文**

### 上下文传递

代理自动接收上下文：

```python
{
  "task": task_node,
  "relevant_results": [...],  # 来自同级/父级
  "overall_objective": "...",  # 根目标
  "constraints": [...],        # 任何限制
  "user_preferences": {...}    # 样式、长度等
}
```

## 🛠️ 创建自定义代理

### 方法 1：YAML 配置

在 `agents.yaml` 中创建一个新代理：

```yaml
agents:
  - name: "MyCustomSearcher"
    type: "executor"
    adapter_class: "ExecutorAdapter"
    description: "针对我的领域的专业搜索"
    model:
      provider: "litellm"
      model_id: "gpt-4"
      temperature: 0.3
    prompt_source: "prompts.executor_prompts.MY_CUSTOM_PROMPT"
    registration:
      action_keys:
        - action_verb: "execute"
          task_type: "SEARCH"
      named_keys: ["MyCustomSearcher", "custom_search"]
    tools:  # 可选工具配置
      - name: "web_search"
        config:
          api_key: "${EXA_API_KEY}"
    enabled: true
```

### 方法 2：Python 代码

创建自定义代理类：

```python
from sentientresearchagent.agents import BaseAgent
from typing import Dict, Any

class MyCustomAgent(BaseAgent):
    """用于专业任务的自定义代理"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "MyCustomAgent"
        self.description = "处理我的特定用例"
        
    async def process(self, task_node: TaskNode, context: Dict) -> Any:
        """处理任务节点"""
        # 您的自定义逻辑在这里
        prompt = self._build_prompt(task_node, context)
        
        # 调用 LLM
        response = await self.llm.generate(
            prompt=prompt,
            temperature=0.5
        )
        
        # 处理并返回结果
        return self._parse_response(response)
    
    def _build_prompt(self, task_node: TaskNode, context: Dict) -> str:
        """构建自定义提示"""
        return f"""
        任务: {task_node.goal}
        上下文: {context.get('relevant_results', [])}
        
        请仔细完成此任务。
        """
```

### 方法 3：扩展现有代理

```python
from sentientresearchagent.agents import WebSearcher

class EnhancedWebSearcher(WebSearcher):
    """具有附加功能的增强版本"""
    
    async def process(self, task_node: TaskNode, context: Dict) -> Any:
        # 添加预处理
        enhanced_query = self._enhance_query(task_node.goal)
        
        # 使用父级功能
        results = await super().process(task_node, context)
        
        # 添加后处理
        return self._filter_and_rank(results)
```

## ⚙️ 代理配置

### 模型配置

```yaml
model:
  provider: "litellm"        # 或 "openai", "anthropic" 等。
  model_id: "gpt-4"          # 特定模型
  temperature: 0.7           # 创意水平
  max_tokens: 2000           # 响应长度
  top_p: 0.9                 # 核采样
  frequency_penalty: 0.1     # 减少重复
```

### 工具配置

```yaml
tools:
  - name: "web_search"
    type: "exa"
    config:
      num_results: 10
      search_type: "neural"
      
  - name: "calculator"
    type: "python"
    config:
      timeout: 30
```

### 响应模型

使用 Pydantic 定义结构化输出：

```python
from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    confidence: float
    sources: List[str]

# 在代理配置中
response_model: "SearchResult"
```

## 📝 提示工程

### 系统提示

定义代理行为和专业知识：

```python
EXPERT_RESEARCHER_PROMPT = """
您是一位在多个领域拥有深厚知识的专家研究分析师。
您的优势包括：
- 寻找权威来源
- 综合复杂信息
- 识别关键见解
- 事实核查和验证

始终引用您的来源并注明置信水平。
"""
```

### 任务提示

结构化任务执行：

```python
SEARCH_TASK_PROMPT = """
目标: {goal}
上下文: {context}
约束: {constraints}

请搜索解决此目标的信息。
重点关注：
1. 最新、权威的来源
2. 多个视角
3. 事实准确性

请以以下格式回复：
- 主要发现: ...
- 来源: ...
- 置信度: ...
"""
```

### 动态提示

根据上下文调整：

```python
def build_prompt(task_node: TaskNode, context: Dict) -> str:
    base_prompt = SEARCH_TASK_PROMPT
    
    # 添加日期感知
    if "current" in task_node.goal or "latest" in task_node.goal:
        base_prompt += "\n优先获取 2024 年的信息。"
    
    # 添加领域专业知识
    if "medical" in task_node.goal:
        base_prompt += "\n使用医学和科学来源。"
    
    return base_prompt.format(
        goal=task_node.goal,
        context=context
    )
```

## 💡 最佳实践

### 1. 代理设计

**应该**：
- 让代理专注于一项功能
- 使用描述性名称
- 记录预期输入/输出
- 优雅地处理错误

**不应该**：
- 创建过于复杂的代理
- 硬编码特定值
- 忽略上下文
- 跳过验证

### 2. 提示工程

**应该**：
- 具体清晰
- 在有用时提供示例
- 设置清晰的输出格式
- 包含置信度指标

**不应该**：
- 使用模糊语言
- 创建过长的提示
- 重复指令
- 假设上下文