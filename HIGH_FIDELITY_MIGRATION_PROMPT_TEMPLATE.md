# 高保真迁移 Prompt 模板

> 用途：当你希望我做出接近 `InstinctMJ` 这种效果的迁移，而不是只做一个最小可用 task port 时，直接复制此模板即可。

---

## 1. 你真正想要的迁移类型

如果你希望最终结果接近 `InstinctMJ`，你要明确要求的是：

> **系统级、高保真、兼容 Instinct 生态的迁移**

而不是：

- 只把一个 task 先跑起来
- 只在 mjlab 里做一个简化版 config
- 只做最小可用近似实现

---

## 2. 推荐 Prompt 模板（完整版）

```text
我要你做的是“系统级高保真迁移”，目标效果参考 InstinctMJ，而不是只做一个最小可用 task port。

请按下面要求执行：

【目标】
把 <源项目/源任务族> 从 InstinctLab / IsaacLab 体系迁移到 mjlab 上，并尽量保持原始 Instinct 生态的语义、结构和工作流。

【迁移风格】
优先做“高保真迁移”而不是“mjlab 原生最简重写”：
- 尽量保留原始目录结构、任务分层、命名方式、manager 语义
- 不要为了简洁主动压缩模块数量
- 不要只迁 task config；原任务依赖的关键子系统也要一起迁
- 不要使用 proxy / approximation 替代关键子系统，除非目标框架客观缺失能力
- 如果不得不近似实现，必须在代码和文档中明确标注“临时近似实现”

【仓库边界】
- 源仓库：<路径1>、<路径2>、<路径3>
- 目标目录：<新目录路径>
- 默认只读参考：<哪些目录>
- 默认不要修改：<哪些仓库>
- 如必须改动这些仓库，先停下来汇报

【迁移范围】
除了 task 本身，还要迁移这些依赖能力（如原任务依赖它们）：
- motion_reference
- noisy_camera / grouped ray caster
- volume_points
- terrain importer / virtual obstacle
- reward manager / multi reward
- monitor system
- train / play / export / onnx workflow
- instinct_rl 对接层

【兼容目标】
请尽量保持：
- task id 风格与 Instinct 一致
- train/play CLI 风格与 Instinct 一致
- logs 目录结构与 Instinct 一致
- obs_format / observation pack 与 instinct_rl 兼容
- runner config 使用 instinct_rl 风格，而不是仅用 mjlab 默认 rsl_rl

【执行要求】
1. 先阅读源代码与目标框架代码，给出迁移映射：
   - 源文件 -> 目标文件
   - 哪些是直接迁移
   - 哪些需要重写
   - 哪些是缺失能力，需要补子系统
2. 然后分阶段实施：
   - 第1阶段：搭建项目骨架
   - 第2阶段：迁 task family
   - 第3阶段：迁传感器/terrain/motion/reference 等子系统
   - 第4阶段：迁训练与回放工作流
3. 每阶段结束后都更新一个 markdown 进度文档
4. 文档中必须写清：
   - 已迁移内容
   - 未迁移内容
   - 近似实现内容
   - 与原始版本仍存在的差异
5. 不要静默做简化；任何简化都要显式说明

【当前优先级】
优先迁移：
- <任务族1>
- <任务族2>
- <任务族3>

请先输出：
A. 迁移计划
B. 文件映射表
C. 你判断必须一并迁移的子系统列表

然后再开始改代码。
```

---

## 3. 精简版 Prompt（适合单任务但仍希望高保真）

```text
我要迁移的不只是这个 task config，而是这个 task 在原系统里真正依赖的整套能力。
请不要给我最小可用版本，也不要默认做近似替代。
请按 InstinctMJ 的思路做高保真迁移：
- 保留原 task 结构
- 保留原 motion / sensor / reward / monitor / training workflow
- 优先兼容 instinct_rl
- 如目标框架缺能力，再做临时近似，并明确记录到 md
```

---

## 4. 最关键的补充句子

如果你不想让我偷懒走“相似任务代替”的路线，建议再加一句：

```text
如果你发现可以用 mjlab 现成任务大致替代原任务，请不要直接替代。
优先正式迁移原任务语义与结构，而不是用相似任务顶替。
```

---

## 5. 为什么这个模板有效

如果不明确说清楚，我通常会更偏向：

- 先复用 mjlab 现有能力
- 先让一个 task 最小可用
- 再逐步补齐

这会更接近“实验性工作区迁移”，而不是 `InstinctMJ` 这种：

- 独立包
- 多任务族
- 自定义 env wrapper
- 自定义 motion/sensor/terrain/reward/monitor
- 完整 instinct_rl 对接工作流

所以，如果你想让我做出 `InstinctMJ` 这种效果，最关键的一句话就是：

> **我要的是系统级、高保真、兼容 instinct_rl 的迁移，不是最小可用 task port。**

---

## 6. 推荐你以后固定补充的信息

每次提迁移请求时，最好同时提供：

- 源仓库路径
- 目标目录路径
- 哪些仓库只能读不能改
- 目标任务族名单
- 是否要求兼容 `instinct_rl`
- 是否要求保留 Instinct 风格 task id / CLI / logs
- 是否允许临时 proxy 实现

这样能显著提高我第一次就走对路线的概率。
