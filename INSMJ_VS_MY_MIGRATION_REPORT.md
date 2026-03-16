# InstinctMJ 与我此前迁移版本的差异报告

> 对比对象：
>
> 1. `InstinctMJ`：`/home/lxj/instinct/instinct/insMJ/InstinctMJ`
> 2. 我此前的迁移 workspace：`/home/lxj/instinct/mjlab_parkour_workspace`
>
> 本报告基于静态代码阅读与我此前的修改记录整理。

---

## 1. 一句话结论

### InstinctMJ

更像：

> **完整的、独立的、Instinct 生态优先的 mjlab-native 环境项目**

### 我此前的迁移版本

更像：

> **在 mjlab 副本里做的一个 parkour 定向端口与实验性迁移工作区**

所以两者不是简单“谁好谁坏”，而是**目标不同、范围不同、策略不同**。

---

## 2. 范围差异

### InstinctMJ 迁了什么

它已经覆盖：

- locomotion
- beyondmimic
- whole-body shadowing
- perceptive shadowing
- perceptive vae
- parkour

并且配套迁了：

- motion reference
- noisy camera
- volume points
- terrain importer / virtual obstacle
- multi reward
- monitor
- instinct_rl train/play CLI

### 我此前迁了什么

我主要在 `mjlab_parkour_workspace` 里迁了：

- `Mjlab-Parkour-Target-Unitree-G1`

并围绕这个任务补了：

- target-aware command
- terrain cfg
- depth history
- AMP-style lightweight discriminator
- 一批 reward parity
- `--motion-file` 训练入口

**本质上，我迁的是一个 task；而 InstinctMJ 迁的是一个 task suite + runtime stack。**

---

## 3. 训练栈差异

### InstinctMJ

训练栈是：

- `InstinctRlEnv`
- `InstinctRlVecEnvWrapper`
- `instinct_rl.runners.OnPolicyRunner`
- `InstinctRlOnPolicyRunnerCfg`
- `WasabiPPO` / MoE / VAE / encoder actor-critic 等原始 Instinct 算法体系

也就是说：

> **它保留了 Project-Instinct 的算法栈。**

### 我此前的版本

训练栈是：

- mjlab 原生 env
- mjlab/rsl_rl 风格 runner
- 我额外补的 `ParkourAmpPPO`

虽然我已经做了 AMP-style discriminator，但仍然是：

> **基于 mjlab 默认训练链路的近似改造版**

因此在训练语义上：

- `InstinctMJ` 更接近原 Instinct
- 我的版本更接近 mjlab 原生 + 局部增强

---

## 4. 迁移策略差异

### InstinctMJ 的策略

从 `AGENTS.md` 和代码组织看，它的策略是：

- 尽量一一对应原 InstinctLab 结构
- 尽量保留原任务职责划分
- 在 mjlab 上重建 Instinct 风格子系统
- 命名和接口尽量维持 Instinct 习惯

可以理解为：

> **高保真迁移**

### 我此前的策略

我的策略更偏：

- 先在独立 workspace 中落地
- 优先让一个 task 能被表达
- 能用 mjlab 原生能力的地方尽量用原生能力
- 不足的地方做最小补齐
- 对缺失能力先做 proxy 或 lightweight 近似

可以理解为：

> **最小可用迁移 + 渐进补齐**

---

## 5. 系统深度差异

### InstinctMJ

它迁的是整套系统：

- custom env wrapper
- custom scene
- custom terrain importer
- custom motion reference manager
- custom noisy camera
- custom volume points
- custom reward manager
- custom monitor manager
- custom train/play/list CLI

### 我此前的版本

我没有在 mjlab 外再做一套完整运行时系统，而是更多复用：

- mjlab 原生 registry
- mjlab 原生 env config 体系
- mjlab 原生 train/play 入口（只补局部）
- 原生 sensor / terrain 尽量复用

所以在系统层：

- `InstinctMJ` 更完整、更重
- 我的版本更轻、更依赖上游 mjlab

---

## 6. 任务保真度差异

### Shadow / Perceptive / BeyondMimic

- `InstinctMJ`：已经迁入并形成正式任务家族
- 我的版本：**没有正式迁这些任务**，我只做了 parkour

### Parkour

`InstinctMJ` 的 parkour：

- shoe G1
- volume points 真传感器
- noisy grouped raycaster camera
- hacked terrain importer
- WasabiPPO
- Instinct 风格 CLI / export / onnx 使用链路

我的 parkour：

- 没有 shoe G1
- volume points 目前是 proxy 版
- depth noise 是近似版
- AMP 是 lightweight 近似版
- 训练入口是补在 mjlab train.py 上的

所以 parkour 保真度上：

> **InstinctMJ 明显更高。**

---

## 7. 工程形态差异

### InstinctMJ

是一个可以单独安装的包：

- `pyproject.toml`
- `project.scripts`
- `project.entry-points."mjlab.tasks"`

这意味着它是：

> **正式工程化包**

### 我的版本

是一个研究型 workspace：

- 通过复制 mjlab 到新目录改 task
- 主要目的是快速迁移 / 快速验证

这意味着它是：

> **实验性工作区**

---

## 8. 与上游 mjlab 的关系差异

### InstinctMJ

它与上游 mjlab 的关系是：

- 以 mjlab 为底座
- 但重建了很多 Instinct 语义层
- 更像一个“mjlab 上层框架”

### 我的版本

它与上游 mjlab 的关系是：

- 尽量直接在 mjlab 现有 abstractions 上做 task port
- 只在必要处做少量自定义

所以：

- `InstinctMJ`：偏“框架再封装”
- 我的版本：偏“任务层扩展”

---

## 9. 日志与工作流差异

### InstinctMJ

日志和工作流明显贴近 Project-Instinct：

- `logs/instinct_rl/<experiment_name>/<timestamp_run>/`
- `instinct-train`
- `instinct-play`
- `instinct-list-envs`
- monitor / episodic reward 结构接近原系统

### 我的版本

更偏 mjlab 默认工作流：

- `logs/rsl_rl/...`
- `uv run train ...`
- `uv run play ...`

虽然我补了 `--motion-file` 等功能，但整体 workflow 并没有切换成 Instinct 风格。

---

## 10. 成本与风险差异

### InstinctMJ 的优点

- 更完整
- 更接近原系统
- 多任务可用
- 对 shadow / perceptive / AMP 更成熟

### InstinctMJ 的代价

- 更重
- 更复杂
- 和上游 mjlab 偏离更大
- 更依赖本地数据路径与 `instinct_rl`

### 我的版本的优点

- 轻量
- 改动集中
- 便于快速试验
- 更容易看清单任务迁移过程

### 我的版本的代价

- 覆盖面小
- 保真度不如 InstinctMJ
- 很多高级子系统没有完全迁
- 仍需较多后续补齐

---

## 11. 我对两者的总体评价

### 如果目标是“尽快得到一个高保真的 Instinct 迁移版本”

更应该看：

- `InstinctMJ`

### 如果目标是“在 mjlab 原生语义里一步步看清单任务怎么迁”

更适合看：

- 我此前的 `mjlab_parkour_workspace`

### 如果只看当前完成度

`InstinctMJ` 比我此前的迁移结果：

- **范围更大**
- **深度更深**
- **保真度更高**
- **更接近正式项目**

而我的版本：

- **更像一个可控、渐进式的端口实验**

---

## 12. 最终结论

### InstinctMJ 的本质

它不是“另一个 parkour workspace”，而是：

> **一个面向 Project-Instinct 工作流的完整 mjlab-native 任务包。**

### 我此前迁移版本的本质

它不是“完整替代 InstinctLab 的系统”，而是：

> **一个围绕 parkour 的逐步迁移工作区。**

### 所以二者的关系

不是简单的“同一个东西谁更好”，而是：

- `InstinctMJ`：系统级迁移
- 我的版本：任务级迁移

如果你后面要继续深入，建议把 `InstinctMJ` 作为主参考；
而我的 `mjlab_parkour_workspace` 更适合作为“我之前做了哪些简化、哪些近似、哪些步骤需要补齐”的对照样本。
