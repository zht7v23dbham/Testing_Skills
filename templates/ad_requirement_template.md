# 广告需求拆解与测试模板 (Ad-Tech Requirement & Test Template)

## 需求概览 (Requirement Overview)
- **需求名称**: 
- **广告类型**: (e.g., Banner, Video, Native, Interstitial)
- **投放平台**: (e.g., iOS, Android, Web)

## 核心测试点拆解 (Core Test Points)

### 1. 展示与渲染 (Impression & Rendering)
- [ ] **素材加载**: 图片/视频是否正常加载，加载速度是否符合标准。
- [ ] **尺寸适配**: 在不同屏幕尺寸/分辨率下是否正常显示，无遮挡或变形。
- [ ] **关闭/跳过**: 关闭按钮是否可用，跳过倒计时是否准确。

### 2. 交互与跳转 (Interaction & Click)
- [ ] **点击区域**: 点击广告有效区域是否触发跳转。
- [ ] **落地页**: 是否正确跳转到指定的 Landing Page 或 App Store。
- [ ] **Deep Link**: 已安装 App 时是否直接唤起 App。

### 3. 计费与归因 (Billing & Attribution)
- [ ] **曝光上报**: 广告展示成功后，是否发送曝光埋点 (Impression Pixel)。
- [ ] **点击上报**: 广告点击后，是否发送点击埋点 (Click Pixel)。
- [ ] **转化归因**: 下载/安装/注册后，归因系统是否正确记录转化。

### 4. 逻辑与策略 (Logic & Strategy)
- [ ] **定向规则**: 地域、年龄、性别等定向是否生效。
- [ ] **频控 (Frequency Capping)**: 同一用户在规定时间内看到的次数限制。
- [ ] **竞价逻辑**: 出价高者是否优先展示 (Mock 环境验证)。

### 5. 合规与安全 (Compliance & Security)
- [ ] **隐私标签**: 是否显示“广告”字样及隐私政策链接。
- [ ] **内容审核**: 屏蔽违规关键词或素材。
