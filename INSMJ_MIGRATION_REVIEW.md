# InstinctMJ 迁移阅读与结构梳理

> 阅读对象：`/home/lxj/instinct/instinct/insMJ/InstinctMJ`
>
> 参考时间：2026-03-16
>
> 本文基于仓库代码、README、任务注册文件与关键配置的静态阅读整理，不代表已完成运行时验证。

---

## 1. 这个项目是什么

`InstinctMJ` 是一个**独立的 mjlab 原生任务包**，目标是把 `InstinctLab` / `Project-Instinct` 的环境侧能力迁到 MuJoCo Warp / mjlab 上，并继续接入 `instinct_rl` 训练栈。

从 `README.md`、`pyproject.toml` 和代码结构来看，它不是在 `mjlab` 仓库里直接塞任务，而是一个单独项目：

- 运行时依赖：
  - `mjlab`
  - `instinct_rl`
- 自己提供：
  - 任务注册
  - 环境封装
  - motion reference 子系统
  - 自定义传感器
  - 自定义 terrain importer / generator
  - `instinct_rl` 风格 train/play CLI

这意味着它的定位更像：

> **“面向 Project-Instinct 工作流的独立 mjlab-native 环境包”**

而不是“在 mjlab 里面临时增加几个任务”。

---

## 2. 项目整体结构

源码主目录：

- `src/instinct_mj/`

可以大致分成这些层：

### 2.1 核心运行层

- `envs/`
  - `manager_based_rl_env.py`
  - `manager_based_rl_env_cfg.py`
  - `scene.py`

### 2.2 任务层

- `tasks/`
  - `locomotion/`
  - `shadowing/`
  - `parkour/`
  - `registry.py`

### 2.3 训练对接层

- `rl/`
  - `config.py`
  - `module_cfg.py`
  - `vecenv_wrapper.py`

### 2.4 运动参考与感知层

- `motion_reference/`
- `sensors/noisy_camera/`
- `sensors/volume_points/`
- `sensors/grouped_ray_caster/`

### 2.5 terrain 与几何支持层

- `terrains/`
  - `height_field/`
  - `trimesh/`
  - `virtual_obstacle/`
  - `terrain_importer_cfg.py`

### 2.6 辅助能力

- `monitors/`
- `managers/`
- `assets/`
- `scripts/`

这个结构说明：它迁移的不是单个 task，而是一整套**任务运行生态**。

---

## 3. 任务覆盖范围

从 `README.md` 和各个 `config/g1/__init__.py` 注册文件看，当前已经迁移并注册的任务 ID 包括：

### 3.1 Locomotion

- `Instinct-Locomotion-Flat-G1-v0`
- `Instinct-Locomotion-Flat-G1-Play-v0`

### 3.2 Shadowing / Tracking 家族

#### BeyondMimic
- `Instinct-BeyondMimic-Plane-G1-v0`
- `Instinct-BeyondMimic-Plane-G1-Play-v0`

#### Whole-body shadowing
- `Instinct-Shadowing-WholeBody-Plane-G1-v0`
- `Instinct-Shadowing-WholeBody-Plane-G1-Play-v0`

#### Perceptive shadowing
- `Instinct-Perceptive-Shadowing-G1-v0`
- `Instinct-Perceptive-Shadowing-G1-Play-v0`

#### Perceptive VAE
- `Instinct-Perceptive-Vae-G1-v0`
- `Instinct-Perceptive-Vae-G1-Play-v0`

### 3.3 Parkour

- `Instinct-Parkour-Target-Amp-G1-v0`
- `Instinct-Parkour-Target-Amp-G1-Play-v0`

也就是说，`InstinctMJ` 当前覆盖的是：

- locomotion
- shadowing（多分支）
- parkour

总计 **12 个 train/play task id**。

---

## 4. 它的迁移方式：不是“做几个配置”，而是“迁一套框架语义”

从 `AGENTS.md` 可以看出，这个项目的迁移原则非常明确：

- 尽量按原 `InstinctLab` 结构一一对应
- 不随意压缩原逻辑
- 不增加 compat shim / adapter layer
- 任务命名、职责划分尽量贴原版
- manager 配置改成 mjlab 形式，但语义尽量不改

这在代码中体现得很明显：

### 4.1 自己做了 `InstinctRlEnv`

文件：

- `src/instinct_mj/envs/manager_based_rl_env.py`

它不是直接用 mjlab 原版 env 就结束，而是加了：

- `InstinctScene`
- `MultiRewardManager`
- `MonitorManager`
- 额外日志 / monitor 机制

也就是说它在 mjlab 上重新实现了一层**更贴近 InstinctLab 行为的环境外壳**。

### 4.2 自己做了 `InstinctRlVecEnvWrapper`

文件：

- `src/instinct_mj/rl/vecenv_wrapper.py`

这层不是为 rsl_rl，而是为了：

- 直接对接 `instinct_rl.env.VecEnv`
- 暴露 `obs_format`
- 输出 `policy` / `critic` / 其他 observation groups
- 支持 `instinct_rl` 所需的 observation packing 约定

这意味着它不是走 mjlab 默认训练栈，而是走：

> `InstinctMJ env` + `InstinctRlVecEnvWrapper` + `instinct_rl runner`

### 4.3 自己做了 `InstinctRlOnPolicyRunnerCfg`

文件：

- `src/instinct_mj/rl/config.py`

这里的配置字段明显是为 `instinct_rl` 设计的，而不是 mjlab 原生 rsl_rl。

比如：

- `policy_observation_group`
- `critic_observation_group`
- `teacher_policy_class_name`
- `discriminator_*`
- `advantage_mixing_weights`
- `distillation_loss_coef`
- `actor_state_key`
- `reference_state_key`

这说明它不仅迁了环境，还把**原始算法接口习惯**也保住了。

---

## 5. 它额外迁了哪些“重”子系统

这是 `InstinctMJ` 和一般“只迁 task config”项目差别最大的地方。

### 5.1 Motion Reference 子系统

目录：

- `src/instinct_mj/motion_reference/`

关键文件：

- `motion_reference_cfg.py`
- `motion_reference_manager.py`
- `motion_buffer.py`

作用：

- 管理参考动作 buffer
- 支持 link-of-interest
- 支持 symmetric augmentation
- 支持多 motion buffer
- 支持 debug visualization / reference robot 语义

这不是简单“读一个 motion.npz”，而是把 InstinctLab 的 motion reference 管理逻辑整体迁了过来。

### 5.2 Noisy Camera / Grouped RayCaster

目录：

- `src/instinct_mj/sensors/noisy_camera/`
- `src/instinct_mj/sensors/grouped_ray_caster/`

作用：

- 支持更接近 InstinctLab 的 depth pipeline
- 支持 grouped ray caster camera
- 支持 image noise / transform pipeline

这比我之前在 mjlab workspace 中做的“depth crop + history”要完整得多。

### 5.3 Volume Points 传感器

目录：

- `src/instinct_mj/sensors/volume_points/`

这点非常关键，因为原始 parkour / obstacle 系列里：

- `volume_points_penetration`

是一个真实存在的重要 reward。

`InstinctMJ` 是真的把这类传感器一起迁了；不是简单用 contact proxy 替代。

### 5.4 自定义 Terrain Importer / Hacked Generator / Virtual Obstacles

目录：

- `src/instinct_mj/terrains/`

关键文件：

- `terrain_importer_cfg.py`
- `terrain_importer.py`
- `terrain_generator_cfg.py`
- `virtual_obstacle/*`

它支持：

- `terrain_type="hacked_generator"`
- `virtual_obstacles`
- `mesh` / `heightfield` 两种 virtual obstacle 来源
- 直接从 terrain collision / hfield 推边界

这说明它不是“把 rough terrain 换成一个差不多的 mjlab terrain”，而是把 InstinctLab 里的 terrain 语义扩展到了 mjlab。

### 5.5 MultiReward / Monitor 体系

文件：

- `managers/reward_manager.py`
- `monitors/monitor_manager.py`

作用：

- 输出更接近 InstinctLab 风格的 reward 日志
- 支持 term-wise episodic reward logging
- 支持 monitor term / monitor sensor

这使得：

- 训练日志结构
- 诊断信号
- step/episode monitor

都更接近原始 Project-Instinct 工作流。

---

## 6. 训练与回放工作流

`InstinctMJ` 没有直接复用 mjlab 的 `uv run train/play` 入口，而是单独提供了：

- `instinct-train`
- `instinct-play`
- `instinct-list-envs`

对应脚本在：

- `src/instinct_mj/scripts/instinct_rl/train.py`
- `src/instinct_mj/scripts/instinct_rl/play.py`
- `src/instinct_mj/scripts/list_envs.py`

### 6.1 train.py 特点

- 用的是 `instinct_rl.runners.OnPolicyRunner`
- 支持 `motion_file` / `registry_name`
- 支持 dot-overrides 到 `env.*` / `agent.*`
- 支持 video / native viewer / torchrunx
- 支持 tracking motion file 校验

### 6.2 play.py 特点

- 支持 trained / random / zero agent
- 支持 `load_run` / `checkpoint_file` / `checkpoint_pattern`
- 支持 `export_onnx`
- 支持 `use_onnx`
- 支持 native / viser viewer

也就是说，它复现的是**Instinct 风格 CLI 体验**，而不是 mjlab 的原生 CLI 体验。

---

## 7. Parkour 迁移完成度

从 `tasks/parkour/config/g1/g1_parkour_target_amp_cfg.py` 和 `config/parkour_env_cfg.py` 看，parkour 迁移完成度相当高。

### 已迁的关键能力

- rough terrain curriculum
- `PoseVelocityCommandCfg`
- 复杂 terrain generator（Perlin/stairs/gaps/boxes/slope）
- shoe 版 G1 (`g1_parkour_target_amp_cfg.py` 中有 shoe MJCF)
- motion reference manager
- noisy grouped raycaster camera
- volume points
- height scanner
- parkour reward / termination / curriculum
- Instinct-RL AMP runner config

而且 parkour 的算法配置不是“近似 AMP”，而是明确写了：

- `class_name = "WasabiPPO"`

也就是它直接依赖 `instinct_rl` 里的原始训练算法家族。

---

## 8. Shadowing 迁移完成度

这部分也是明显比“只靠 mjlab tracking”更完整。

已经迁的分支包括：

- BeyondMimic
- whole-body shadowing
- perceptive shadowing
- perceptive VAE

从代码和 README 来看，这些都不是 placeholder，而是有：

- 任务注册
- env cfg
- motion reference / terrain / camera / monitor
- instinct_rl cfg
- train/play 使用说明

特别是 perceptive shadowing：

- 有 motion-matched terrain
- 有 metadata.yaml 驱动的数据目录
- 有 reference visualization 逻辑
- 有更复杂的 play overrides

因此 shadowing 家族在 `InstinctMJ` 里是**实质性迁移完成**的，不是仅有名字。

---

## 9. 这个项目的优势

### 9.1 迁移范围大

它不是只迁一个 parkour，而是迁了：

- locomotion
- shadowing
- parkour

### 9.2 迁移深度深

它不只是配置层迁移，而是把下面这些都一起迁了：

- env wrapper
- task registry
- instinct_rl interface
- motion reference
- noisy camera
- volume points
- terrain importer / virtual obstacle
- multi reward / monitor

### 9.3 与原 Instinct 生态兼容更强

它保留了：

- Instinct 风格 task naming
- Instinct 风格 CLI
- instinct_rl 算法入口
- 更像原版的日志 / monitor 结构

### 9.4 对 shadow / perceptive / AMP 更友好

如果目标是“尽量保持原任务定义和训练方式”，它比直接在 mjlab 里做简化版迁移更有优势。

---

## 10. 这个项目的代价 / 风险

### 10.1 系统更重

因为它迁了一整套子系统，所以：

- 维护成本更高
- 和上游 mjlab 的偏离更大
- 学习成本更高

### 10.2 更依赖本地数据与本地路径

大量任务 README / cfg 里都要求手动改：

- dataset root
- metadata 路径
- motion file 选择

这说明它目前更偏“研究工作区版本”，而不是开箱即用版本。

### 10.3 对 `instinct_rl` 依赖更深

一旦 `instinct_rl` 版本变动较大，`InstinctMJ` 的训练链路也更容易受影响。

### 10.4 并不是纯上游 mjlab 风格

虽然它基于 mjlab，但它为了贴近 InstinctLab，引入了很多自定义层。

所以它的风格更像：

> **Instinct 语义优先，mjlab 作为底座**

而不是：

> **mjlab 原生最简风格优先**

---

## 11. 我对它的整体判断

如果只从“迁移完整度”看，`InstinctMJ` 明显已经走得比我之前做的 parkour workspace 更远。

它的状态更接近：

- **一个可长期使用的独立迁移项目**

而不是：

- **一个任务级实验性端口**

它最大的特点不是“某一个 task 做得多完整”，而是：

> **它把 InstinctLab → mjlab 的“任务框架语义”整体迁过去了。**

---

## 12. 当前结论（简版）

### 已经迁移了什么

- locomotion
- shadowing（BeyondMimic / whole-body / perceptive / perceptive-vae）
- parkour
- motion reference 系统
- noisy camera
- volume points
- hacked terrain / virtual obstacle
- multi reward / monitor
- instinct_rl train/play workflow

### 它最像什么

- 一个“mjlab-native 的 InstinctLab 替身 / 环境侧实现”

### 它相对于普通 mjlab task port 的本质区别

- 它迁的是**系统**，不只是**任务配置**。
