# Playwright 网页自动化测试指南 (CLI & Pytest)

本指南包含两部分：
1.  **Playwright CLI 交互式调试指南**: 用于快速探索、生成选择器和调试 UI 流程。
2.  **Pytest UI 自动化测试最佳实践**: 用于编写稳定、可维护的自动化测试脚本。

---

## 第一部分：Playwright CLI 交互式调试 (CLI-First Automation)

Playwright CLI 是一个强大的工具，允许你直接从终端驱动真实的浏览器。它非常适合调试、生成选择器以及验证 UI 交互逻辑。

### 1. 环境准备 (Prerequisite)

在使用 CLI 之前，请确保已安装 Node.js 和 npm（因为 CLI 依赖于 `npx`）。

```bash
# 验证 Node/npm 是否安装
node --version
npm --version

# 如果未安装，请先安装 Node.js。
# 推荐全局安装 playwright-cli 以便随时调用：
npm install -g @playwright/cli@latest
playwright-cli --help
```

### 2. 快速开始 (Quick Start)

使用 `playwright-cli` (或 `npx playwright`) 启动浏览器并执行操作：

```bash
# 打开网页 (带头模式，方便观察)
npx playwright open "https://playwright.dev" --headed

# 常用操作指令
# 1. 获取当前页面快照 (Snapshot) - 获取元素 ID (如 e1, e2)
npx playwright snapshot

# 2. 点击元素 (使用快照中的 ID)
npx playwright click e15

# 3. 输入文本
npx playwright type "Playwright"

# 4. 按键
npx playwright press Enter

# 5. 截图
npx playwright screenshot
```

### 3. 核心工作流 (Core Workflow)

高效使用 CLI 的标准循环：

1.  **打开页面 (`open`)**: 启动浏览器访问目标 URL。
2.  **生成快照 (`snapshot`)**: 获取当前 DOM 的稳定元素引用 (Refs)。
3.  **交互 (`interact`)**: 使用快照中的 Ref (如 `e3`) 进行点击、输入等操作。
4.  **重新快照**: 发生页面跳转、弹窗、Tab 切换或 DOM 发生重大变化后，必须重新生成快照。
5.  **捕获产物**: 必要时截图或保存 PDF。

**最小闭环示例**:

```bash
npx playwright open "https://example.com"
npx playwright snapshot
npx playwright click e3  # 点击链接跳转
npx playwright snapshot  # 页面变化后重新快照
```

### 4. 推荐模式 (Recommended Patterns)

#### 表单填写 (Form Fill)
```bash
npx playwright open "https://example.com/form"
npx playwright snapshot
npx playwright fill e1 "user@example.com"  # 填写用户名
npx playwright fill e2 "password123"       # 填写密码
npx playwright click e3                    # 点击提交
npx playwright snapshot                    # 检查结果
```

#### 调试与追踪 (Debugging with Traces)
```bash
npx playwright open "https://example.com" --headed
npx playwright tracing-start
# ... 执行一系列交互 ...
npx playwright tracing-stop --path trace.zip
# 使用 Trace Viewer 查看: npx playwright show-trace trace.zip
```

#### 多标签页操作 (Multi-tab)
```bash
npx playwright tab-new "https://example.com"
npx playwright tab-list
npx playwright tab-select 0
npx playwright snapshot
```

### 5. 防错指南 (Guardrails)

*   **引用失效**: 任何时候操作失败提示 "element not found"，请立即执行 `snapshot` 刷新引用。
*   **显式命令**: 尽量使用明确的 `click`, `fill` 命令，避免滥用 `eval`。
*   **可视化**: 调试时始终加上 `--headed` 参数。

---

## 第二部分：Pytest UI 自动化测试模板 (Automation Script)

作为测试专家，我们推荐使用 **Python + Pytest + Playwright** 编写可维护的自动化测试脚本。

### 1. 核心优势
*   **自动等待 (Auto-wait)**: 消除 `sleep`，减少 Flaky Tests。
*   **浏览器上下文 (Context)**: 每个测试用例独立上下文，互不干扰，且启动极快。
*   **代码生成 (Codegen)**: 使用 `playwright codegen` 快速录制脚本。

### 2. 目录结构建议
```
tests/
  ├── ui/
  │   ├── conftest.py       # 共享 Fixture (登录状态、浏览器配置)
  │   ├── pages/            # Page Object 模型
  │   │   ├── login_page.py
  │   │   └── home_page.py
  │   └── test_login.py     # 测试用例
```

### 3. 示例代码
请参考同目录下的 `ui_test_playwright_pytest.py` 模板文件。
