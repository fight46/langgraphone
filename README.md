# LangGraph One

一个用于学习 **LangGraph** 的轻量级 Python 示例项目。基于 LangGraph 构建最简单的对话工作流，通过 LangChain 的 `ChatOpenAI` 接口调用 **DeepSeek Chat**，支持在终端进行多轮对话。

> 当前是入门示例：只有一个大模型节点，不包含工具调用、RAG、持久化记忆或多 Agent 协作。

## 功能

- 使用 `StateGraph` 定义、编译并运行对话工作流。
- 通过 `messages` 状态维护**当前进程内**的多轮对话上下文。
- 调用 DeepSeek 官方 OpenAI 兼容接口（`deepseek-chat`）。
- 终端交互，支持 `exit`、`quit`、`q` 退出。

## 工作流程

```text
用户输入
   ↓
START
   ↓
llm_node（读取历史消息，调用 DeepSeek）
   ↓
END
   ↓
输出回答，并更新本地消息列表
   ↓
等待下一轮输入
```

每次调用 `graph.invoke({"messages": messages})` 时，程序会将此前保存的消息列表传入图中。这里的“记忆”仅存在于运行期间，退出后不会自动保存。

## 项目结构

```text
langgraphone/
├── main.py           # LangGraph 工作流与命令行对话入口
├── requirements.txt  # Python 依赖
├── .gitignore        # 忽略密钥、虚拟环境和缓存
└── .env              # 本地 API Key（自行创建，不提交到 Git）
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/fight46/langgraphone.git
cd langgraphone
```

### 2. 创建 Python 虚拟环境

建议使用 Python 3.10 或更新版本。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

其中，`venv` 用于创建隔离的 Python 环境，`source` 用于在 macOS/Linux 终端激活该环境。

### 3. 安装依赖

```bash
python -m pip install -r requirements.txt
```

项目使用 `langgraph`、`langchain-openai`；源码还使用 `python-dotenv` 的 `load_dotenv`。若环境中尚未安装 `python-dotenv`，执行：

```bash
python -m pip install python-dotenv
```

### 4. 配置 DeepSeek API Key

在项目根目录新建 `.env` 文件：

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key
```

请将 `your_deepseek_api_key` 替换为自己的密钥。**不要把真实密钥上传至 GitHub。** 项目的 `.gitignore` 已包含 `.env`。

### 5. 运行

```bash
python main.py
```

示例（回复内容仅供演示）：

```text
你：你好
AI：你好！有什么可以帮你？

你：刚才我说了什么？
AI：你刚才说了“你好”。

你：exit
对话结束。
```

## 关键代码与原理

| 组件 | 作用 |
| --- | --- |
| `State` | 用 `TypedDict` 定义图共享的消息状态 |
| `add_messages` | 合并节点返回的新消息与已有消息 |
| `call_llm` | 调用大模型生成回复的节点函数 |
| `StateGraph` | 组织节点与边，描述执行流程 |
| `START → llm_node → END` | 当前项目的单节点执行路径 |
| `graph.compile()` | 将工作流编译为可执行图 |
| `graph.invoke(...)` | 执行一轮图调用 |

## 后续学习方向

可以在此基础上逐步增加工具调用（Tool Calling）、条件分支、检查点持久化（Checkpointer）、RAG 检索，以及更复杂的多节点 Agent 工作流。

## License

当前仓库尚未添加开源许可证。代码公开可见不等于已授予他人自由使用或再分发的许可。
