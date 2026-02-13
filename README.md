# 测试专家技能工程 (Testing Expert Skills Project)

这是一个专业的测试技能工程，旨在为 TRAE IDE 提供强大的测试辅助能力。本项目包含多个核心 Skill 和一系列标准化的测试模板，完全支持中文环境，并提供多种测试用例格式的生成能力。

## 目录结构

- `.trae/skills/`:
    - **testing-expert**: 通用测试专家技能，适用于各类项目的需求拆解与用例生成。
    - **tencent-ads-tester**: **(New)** 腾讯广告 Marketing API 专属测试专家，针对广告投放、报表、鉴权等场景进行深度定制。
    - **kuaishou-ads-tester**: **(New)** 快手磁力引擎 API 专属测试专家，覆盖 Unit 层级、魔力建站及 DMP 测试。
    - **ocean-engine-tester**: **(New)** 巨量引擎（Ocean Engine）Marketing API 专属测试专家，覆盖 Project/Promotion 新版架构及巨量千川。
    - **security-tester**: **(New)** 安全测试专家技能，覆盖 OWASP Top 10 及 API 安全扫描。
- `templates/`: 标准化测试文档模板。
  - `security_test_checklist.md`: **(New)** 安全测试通用检查单。
  - `security_scan_example.py`: **(New)** Python 安全基线扫描脚本模板。
  - `ui_test_playwright_guide.md`: Playwright CLI 交互式调试指南与最佳实践。
  - `ui_test_playwright_pytest.py`: Playwright + Pytest UI 自动化测试脚本模板。
  - `api_test_pytest.py`: 通用 Python Pytest 接口自动化测试模板。
  - `tencent_ads_pytest.py`: 腾讯广告 API 专用 Pytest 模板。
  - `kuaishou_ads_pytest.py`: 快手磁力引擎 API 专用 Pytest 模板。
  - `ocean_engine_pytest.py`: 巨量引擎 API 专用 Pytest 模板。
  - `test_case_template.md`: 通用功能测试用例模板 (Markdown)。
  - `functional_test.csv`: 功能测试用例模板 (CSV/Excel)。
  - `api_test_checklist.md`: 接口测试九大维度检查单。
  - `api_test_postman_apifox.json`: 接口测试集合模板 (Postman/Apifox)。
  - `ad_requirement_template.md`: 广告类需求拆解模板。
- `examples/`: 使用示例，展示了如何将测试需求转化为不同格式的产物。
  - `example_ad_campaign_test.md`: 需求拆解与 Markdown 用例。
  - `example_ad_campaign_pytest.py`: 对应的自动化测试脚本。
  - `example_ad_campaign_postman.json`: 对应的 Postman 接口集合。
  - `example_ad_campaign.csv`: 对应的 Excel/CSV 功能用例。

## 技能介绍 (Skills Overview)

### 1. 通用测试专家 (Testing Expert)
适用于绝大多数测试场景。
- **能力**: 需求拆解、多格式用例生成 (Markdown/CSV/JSON)、九大接口测试维度覆盖。
- **调用示例**: "帮我生成一个登录功能的测试用例，输出为 CSV 格式。"

### 2. 腾讯广告测试专家 (Tencent Ads Tester)
专为腾讯广告 Marketing API 开发者设计。
- **能力**: 
    - **OAuth 2.0 鉴权**: 自动处理 Token 获取与刷新。
    - **广告全流程**: 覆盖推广计划、广告组、创意创建与状态流转。
    - **沙箱支持**: 默认生成针对 `sandbox-api.e.qq.com` 的测试脚本。
- **调用示例**: "写一个创建广告组的接口自动化脚本，使用 Pytest，要在沙箱环境运行。"

### 3. 快手磁力引擎测试专家 (Kuaishou Ads Tester)
专为快手磁力引擎开发者设计。
- **能力**:
    - **特有结构**: 适配 `Campaign -> Unit -> Creative` 层级结构。
    - **鉴权适配**: 支持 `Access-Token` Header 鉴权方式。
    - **业务特性**: 覆盖魔力建站、磁力金牛、OCPM 双出价等特有业务场景。
- **调用示例**: "帮我写一个快手 OCPM 广告组创建的测试脚本，包含深度转化出价。"

### 4. 巨量引擎测试专家 (Ocean Engine Tester)
专为巨量引擎及巨量千川开发者设计。
- **能力**:
    - **新版架构**: 优先使用 v3.0 `Project -> Promotion` 结构。
    - **巨量千川**: 支持直播带货、短视频带货的计划创建与报表查询。
    - **鉴权适配**: 支持 Header `Access-Token` 鉴权方式。
- **调用示例**: "写一个巨量千川直播带货计划的创建脚本，使用 Pytest。"

### 5. 安全测试专家 (Security Tester)
专注于应用安全与合规性。
- **能力**:
    - **OWASP Top 10**: 覆盖注入、XSS、身份认证失效等常见漏洞。
    - **API 安全**: 检测速率限制、IDOR、敏感信息泄露。
    - **自动化扫描**: 生成 Python 脚本进行安全基线检查（Headers, Cookies, 敏感文件）。
- **调用示例**: "帮我写一个 Python 脚本，扫描网站的敏感文件泄露和安全响应头。"

## 核心功能 (Core Capabilities)

1.  **自动化测试 (Python Pytest)**:
    *   **接口测试**: 自动生成标准的 Python `pytest` + `requests` 测试脚本。
    *   **UI 测试**: 基于 **Playwright** + **Pytest**，支持 Page Object 模式和自动等待。
    *   **安全扫描**: 生成 `requests` 脚本进行轻量级安全巡检。
2.  **多格式支持**:
    *   **接口测试**: 支持生成 **JSON** (Postman Collection v2.1, Apifox 兼容) 格式。
    *   **功能测试**: 支持生成 **CSV** (可直接用 Excel 打开) 和 **Markdown** 表格。
    *   **安全检查单**: 提供 Markdown 格式的 OWASP 检查清单。
3.  **需求拆解**: 将复杂的业务需求转化为可测试的场景。
4.  **广告业务专项**: 针对广告投放（展示、点击、归因、计费）的深度测试策略。

## 如何使用 (How to Use)

### 1. 安装到 TRAE
本工程已经符合 TRAE 的 Skill 结构规范。
- 确保 `.trae/skills` 目录下包含对应的技能文件夹。
- 在 TRAE 对话中，AI 会根据你的问题自动选择合适的 Skill。

### 2. 调用示例

*   **通用场景**:
    > "帮我写一个订单创建接口的自动化测试用例，使用 Python Pytest，覆盖库存不足的场景。"
*   **UI 自动化**:
    > "帮我写一个 Playwright 脚本，测试用户登录流程，要使用 Page Object 模式。"
*   **安全测试 (New)**:
    > "帮我生成一个 API 安全测试检查单，重点关注越权和数据泄露。"
*   **广告平台场景**:
    > "我是腾讯广告开发者..." / "写一个快手广告组创建..." / "测试巨量广告 v3.0..."
*   **生成 Excel/CSV 用例**:
    > "帮我生成一个购物车功能的测试用例，输出为 CSV 格式，方便我导入 Excel。"

## 优化建议 (Optimization Suggestions)

当前工程已具备全面的功能、接口及广告业务测试能力，以下是进一步的优化方向：

1.  **性能测试集成 (Performance)**:
    *   目前缺乏性能测试模板。建议增加 **JMeter (.jmx)** 或 **k6 (JavaScript)** 的脚本生成能力，以覆盖高并发场景。
2.  **CI/CD 流水线 (Pipeline)**:
    *   建议添加 **GitHub Actions** 或 **GitLab CI** 的配置文件模板，实现测试脚本的自动触发与运行。
3.  **Mock 服务 (Mock Server)**:
    *   对于广告 API 测试，建议增加一个简单的 **Mock Server** (基于 Flask/FastAPI) 模板，用于模拟广告平台的异步回调（如归因回传），方便本地调试。
