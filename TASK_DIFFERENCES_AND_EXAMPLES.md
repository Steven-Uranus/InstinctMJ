# InstinctMJ 各任务区别与示例说明

> 目标：直接回答“不同任务到底差在哪、机器人到底要干嘛”。
>
> 特别关注：
>
> - `instinct-train Instinct-Shadowing-WholeBody-Plane-G1-v0`
> - `instinct-train Instinct-Perceptive-Shadowing-G1-v0`

---

## 1. 先给结论：WholeBody Shadowing 和 Perceptive Shadowing 的核心区别

### `Instinct-Shadowing-WholeBody-Plane-G1-v0`

这是：

> **平地上的全身动作模仿任务**

机器人主要依赖：

- 动作参考（motion reference）
- 本体状态（关节、姿态、速度等）

它的环境重点是：

- **平地**
- **没有深度感知参与决策**
- 目标是把给定动作在平地上尽量模仿出来

你可以把它理解成：

- “让机器人在平地上模仿一段打拳/奔跑/翻滚/武术动作”

### 一个直观例子

如果 motion 是 `LafanFight5Files` 或 `LafanFiltered` 里的某段动作，机器人要做的是：

- 在**平地**上
- 尽量跟上参考动作的躯干、四肢、关节运动
- 不摔倒、不偏差太大

它更像：

> **动作跟随 / 动作复现**

而不是“看着障碍去过障碍”。

---

### `Instinct-Perceptive-Shadowing-G1-v0`

这是：

> **带深度感知的障碍相关动作模仿任务**

机器人不仅要模仿动作，还要：

- 读取 depth image
- 在与 motion 匹配的 terrain 上执行动作
- 处理障碍物几何

它的环境重点是：

- **motion-matched terrain**
- **深度相机输入**
- **障碍与动作成对出现**

你可以把它理解成：

- “让机器人看到障碍，再去做与该障碍对应的跨越/翻越/钻过动作”

### 一个直观例子

你当前机器上的 perceptive 数据集里，实际就有这些场景：

- `50cm_kneeClimbStep`
- `50cm_kneeClimbStep_noWall`
- `20251106_diveroll4_roadRamp`
- `20251106_diveroll4_roadRamp_noWall`
- `20251106_diveroll4_simpleLab`
- `20251106_diveroll4_simpleLab_noWall`

所以这个任务里的机器人可能要做的就是：

- **爬 50cm 箱体/台阶**（`50cm_kneeClimbStep`）
- **在 road ramp 上做 dive roll**（`diveroll4_roadRamp`）
- **在 simpleLab 障碍上翻滚通过**

它更像：

> **越障动作模仿 / 感知驱动的动作执行**

---

## 2. 一句话区别（最重要）

### WholeBody Shadowing

- 平地
- 不靠 depth
- 重点是“模仿动作本身”

### Perceptive Shadowing

- 障碍地形
- 用 depth
- 重点是“模仿与障碍配对的动作，并处理障碍”

所以如果你问：

> “Perceptive Shadowing 好像是越障的？”

答案是：

> **对，基本可以这么理解。**

它比 WholeBody Shadowing 更接近“感知驱动越障模仿”。

---

## 3. InstinctMJ 当前各任务的区别总览

下面按“任务目标”给你一个直观分类。

---

## 3.1 `Instinct-Locomotion-Flat-G1-v0`

### 它是什么

> **平地命令跟踪 locomotion**

### 机器人要干嘛

- 接收速度命令
- 在平地走路/转向/站立
- 保持稳定，不摔倒

### 输入特点

- 本体状态
- 命令
- 没有复杂障碍物感知

### 典型示例任务

- **在平地上向前走**
- **原地站立**
- **边走边转向**

### 你可以把它理解成

> “基础移动能力训练”

---

## 3.2 `Instinct-BeyondMimic-Plane-G1-v0`

### 它是什么

> **平地上的 BeyondMimic 风格全身动作模仿**

### 机器人要干嘛

- 跟踪参考动作
- 模仿 link-level 的全身运动
- 在平地上完成整段动作

### 输入特点

- 参考动作
- 本体状态
- 没有障碍感知

### 当前默认动作示例

从配置看，当前 active motion 例子是：

- `LafanSprint1`
- 文件：`sprint1_subject2_retargetted.npz`

### 典型示例任务

- **在平地上模仿冲刺动作**
- **模仿一段武术或攻击动作**

### 你可以把它理解成

> “平地上的高保真全身模仿”

---

## 3.3 `Instinct-Shadowing-WholeBody-Plane-G1-v0`

### 它是什么

> **平地 whole-body shadowing**

### 机器人要干嘛

- 跟随一整段参考动作
- 关节、肢体、躯干姿态都尽量贴近参考
- 在平地上完整复现动作

### 输入特点

- 参考动作
- 本体状态
- 没有 depth 图
- 没有障碍依赖

### 当前配置里常见动作示例

从配置中的 motion preset 看，示例动作包括：

- `LafanFight5Files`
- `LafanFiltered`
- `LafanKungfu1`
- `LafanSprint1`

### 典型示例任务

- **在平地上模仿一段格斗动作**
- **模仿一段翻滚或奔跑动作**
- **模仿包含上肢和下肢协同的全身动作**

### 你可以把它理解成

> “不看障碍，只专注把整个人体动作模仿出来”

---

## 3.4 `Instinct-Perceptive-Shadowing-G1-v0`

### 它是什么

> **带深度感知的障碍动作 shadowing**

### 机器人要干嘛

- 看深度图
- 在 motion-matched terrain 上执行参考动作
- 处理障碍几何
- 把动作模仿和越障感知结合起来

### 输入特点

- depth image
- 本体状态
- 参考动作
- terrain-matched metadata

### 当前真实数据集示例（你机器上已有）

路径：

```bash
/home/lxj/instinct/instinct/Instinct/data/20251116_50cm_kneeClimbStep1
```

其中包含的障碍场景示例：

- `50cm_kneeClimbStep`
- `50cm_kneeClimbStep_noWall`
- `20251106_diveroll4_roadRamp`
- `20251106_diveroll4_roadRamp_noWall`
- `20251106_diveroll4_simpleLab`
- `20251106_diveroll4_simpleLab_noWall`

### 典型示例任务

- **爬 50cm 的箱体 / 台阶**
- **在 road ramp 上做翻滚通过**
- **面对 simpleLab 里的障碍做 dive roll**

### 你可以把它理解成

> “看着障碍做动作模仿”

---

## 3.5 `Instinct-Perceptive-Vae-G1-v0`

### 它是什么

> **Perceptive Shadowing 的 VAE 版本**

### 机器人要干嘛

本质任务目标和 Perceptive Shadowing 很接近：

- 也是看 depth
- 也是在障碍地形上执行与障碍匹配的动作

不同的是算法层：

- 不是普通 perceptive shadowing policy
- 而是 **VAE 风格策略结构**

### 典型示例任务

和 Perceptive Shadowing 相同，例如：

- **爬箱子 / 台阶**
- **翻滚越过路障**
- **在特定障碍布局里做预定义动作**

### 你可以把它理解成

> “任务和 perceptive shadowing 类似，但模型结构换成了 VAE 版本”

---

## 3.6 `Instinct-Parkour-Target-Amp-G1-v0`

### 它是什么

> **命令驱动 + 深度感知 + AMP motion prior 的跑酷任务**

### 机器人要干嘛

它不是单纯模仿某一条动作，而是：

- 接收速度/目标命令
- 读取 depth
- 在 rough terrain / stairs / gaps / boxes / slope 上移动
- 同时借助 AMP / motion prior 学出更自然的身体控制

### 输入特点

- 命令
- depth image
- 本体状态
- AMP / motion prior

### 典型示例任务

- **沿命令向前跑过台阶**
- **跨过 gap**
- **越过 box 障碍**
- **在坡面和粗糙地形上继续前进**

### 你可以把它理解成

> “不是照着一个动作表演，而是学会在复杂障碍上跑酷前进”

---

## 4. 这些任务的关系图（直观理解）

你可以这样记：

### A. 基础移动

- `Locomotion-Flat`

关键词：
- 平地
- 跟命令走

---

### B. 平地动作模仿

- `BeyondMimic`
- `Shadowing-WholeBody`

关键词：
- 平地
- 模仿动作
- 不靠深度感知

其中：
- BeyondMimic 更偏 imitation/beyondmimic 风格
- WholeBody Shadowing 更偏 shadowing 体系

---

### C. 障碍动作模仿

- `Perceptive-Shadowing`
- `Perceptive-Vae`

关键词：
- 有障碍
- 用 depth
- motion 与 terrain 匹配
- 更像越障模仿

---

### D. 跑酷控制

- `Parkour-Target-Amp`

关键词：
- 有障碍
- 用 depth
- 不是单条动作模仿
- 更像“自主运动 through obstacles”

---

## 5. 如果你现在要做“翻越不同障碍物”，应该选哪个任务

### 如果你要：

#### 只是想让机器人学会“基础走路/跑步”
选：
- `Instinct-Locomotion-Flat-G1-v0`

#### 想在平地上模仿复杂全身动作
选：
- `Instinct-Shadowing-WholeBody-Plane-G1-v0`
- 或 `Instinct-BeyondMimic-Plane-G1-v0`

#### 想让机器人“看着障碍去模仿翻越动作”
选：
- `Instinct-Perceptive-Shadowing-G1-v0`

#### 想在障碍场景里用 VAE 形式做感知动作模仿
选：
- `Instinct-Perceptive-Vae-G1-v0`

#### 想让机器人“自己在复杂障碍上跑酷前进”
选：
- `Instinct-Parkour-Target-Amp-G1-v0`

---

## 6. 对你当前问题的直接回答

你问的是：

> `instinct-train Instinct-Shadowing-WholeBody-Plane-G1-v0`
> 和
> `instinct-train Instinct-Perceptive-Shadowing-G1-v0`
> 有什么区别？

最直接的回答就是：

### WholeBody Shadowing

- 平地
- 不看 depth
- 专注模仿动作本身

示例：
- **平地模仿格斗动作**
- **平地模仿翻滚动作**

### Perceptive Shadowing

- 有障碍地形
- 看 depth
- 专注模仿“与障碍匹配的动作”

示例：
- **爬 50cm 台阶/箱子**
- **在 road ramp 上 dive roll**
- **在 simpleLab 场景中越障翻滚**

所以如果你现在的目标是：

> **“让机器人翻越不同障碍物”**

那你应该优先看：

- `Instinct-Perceptive-Shadowing-G1-v0`
- 以及如果以后想更自主一些，再看 `Instinct-Parkour-Target-Amp-G1-v0`

---

## 7. 你当前最推荐的入口

对你现在来说，我建议：

### 先跑这个

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
export WARP_CACHE_DIR=/tmp/warp
export MPLCONFIGDIR=/tmp/mpl
export XDG_CACHE_HOME=/tmp/xdg
source .venv/bin/activate
instinct-train Instinct-Perceptive-Shadowing-G1-v0
```

因为它最符合你现在的目标：

> **越障 + 感知 + 动作模仿**
