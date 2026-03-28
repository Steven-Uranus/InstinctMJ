# InstinctMJ 板端部署详细说明（locomotion + perceptive tracking）

本文面向你当前这条技术路线：

- 在 `insMJ/InstinctMJ` 里训练 / 导出策略；
- 在 `instinct_onboard` 里把策略部署到机器人板子上；
- 希望实现：
  1. 先进入 locomotion（walk）；
  2. 人工把机器人走到障碍前；
  3. 再触发某个 reference motion 做越障；
  4. 做完后回到 locomotion，再把机器人走回来。

---

## 0. 结论先说

你当前最适合的板端部署组合是：

1. **WalkAgent** 作为 locomotion 策略  
   - 对应板端脚本里的 `--walk_logdir`
2. **PerceptiveTrackerAgent** 作为越障策略  
   - 对应板端脚本里的 `--logdir`
3. **motion_dir** 里放 reference motion 文件  
   - 比如你的 `zd-2-retargeted.npz`

板端主入口建议使用：

```bash
python instinct_onboard/scripts/g1_perceptive_track.py \
  --logdir <perceptive_tracking_logdir> \
  --motion_dir <motion_dir> \
  --walk_logdir <locomotion_logdir>
```

---

## 1. 机器人板子上需要什么环境

根据 `instinct_onboard/README.md`，建议环境为：

- Ubuntu 22.04
- ROS2 Humble
- Jetson Orin NX（作者当前测试平台）
- Python 虚拟环境

### 1.1 Jetson / 系统依赖

#### JetPack

```bash
sudo apt-get update
sudo apt install nvidia-jetpack
```

#### rosbag mcap（建议）

```bash
sudo apt install ros-${ROS_DISTRO}-rosbag2-storage-mcap
```

> 如果你用的是 Humble：
>
> ```bash
> sudo apt install ros-humble-rosbag2-storage-mcap
> ```

---

### 1.2 Python 虚拟环境

```bash
sudo apt-get install python3-venv
python3 -m venv ~/instinct_venv
source ~/instinct_venv/bin/activate
```

---

### 1.3 安装 `instinct_onboard`

假设你把仓库放到：

```text
/home/unitree/workspaces/instinct_onboard
```

安装：

```bash
cd /home/unitree/workspaces/instinct_onboard
pip install -e .[all]
```

说明：

- `setup.py` 会自动检测 GPU，并安装：
  - `onnxruntime-gpu`
  - 或 `onnxruntime`
- 如果你想强制 GPU：

```bash
FORCE_GPU=1 pip install -e .[all]
```

- 如果想强制 CPU：

```bash
FORCE_CPU=1 pip install -e .[all]
```

---

### 1.4 需要额外准备的依赖

#### `crc_module.so`

`instinct_onboard/README.md` 明确要求：

- 按 `g1_crc` / `crc_module` 的说明编译出 `crc_module.so`
- 并把它放到**运行 Python 脚本时的工作目录**里，或者 Python 能找到的目录里

一个简单做法是：

```text
/home/unitree/workspaces/instinct_onboard/crc_module.so
```

然后运行脚本时就在这个目录下执行。

#### Unitree ROS 消息

需要安装并 source：

- `unitree_hg`
- `unitree_go`

否则：

- `/lowstate`
- `/lowcmd`
- `/wirelesscontroller`

这些消息类型没法用。

#### OpenCV

确认当前 Python 环境里 `cv2` 可用：

```bash
python -c "import cv2; print(cv2.__version__)"
```

#### RealSense

perceptive tracking 需要：

- `pyrealsense2`
- RealSense D435（或兼容）

脚本默认分辨率 / 频率：

- `480 x 270`
- `60 FPS`

对应：

- `instinct_onboard/scripts/g1_perceptive_track.py`
- `instinct_onboard/instinct_onboard/ros_nodes/realsense.py`

---

## 2. 需要从训练机拷贝哪些文件到机器人端

### 2.1 总原则

**不要只拷单个 ONNX 文件。**

建议直接拷：

- 整个 `logdir`
- 整个 `motion_dir`

这样最稳。

---

## 3. 推荐的机器人端目录结构

下面给一个建议路径，你也可以换成你自己的路径，只要命令行参数对应即可。

```text
/home/unitree/instinct_deploy/
  logs/
    locomotion/
      2026-03-19_12-13-05/
        exported/
          actor.onnx
          actor.onnx.data
          policy_normalizer.npz
          metadata.json
        params/
          env.yaml
          agent.yaml

    perceptive_ringroom/
      <your_perceptive_run>/
        exported/
          actor.onnx
          actor.onnx.data
          0-depth_image.onnx
          0-depth_image.onnx.data   # 如果导出器拆分外部权重
          policy_normalizer.npz
          metadata.json
        params/
          env.yaml
          agent.yaml

  motions/
    ringroom/
      zd-2-retargeted.npz
      # 可选再放其他动作：
      diveroll4-ziwen-0-retargeted.npz
      jumpsit2-ziwen-retargeted.npz
      rollVault11-ziwen-retargeted.npz
```

---

## 4. locomotion（walk）策略需要拷哪些文件

你现在已经导出了一份 locomotion ONNX，例如：

```text
insMJ/InstinctMJ/logs/instinct_rl/g1_locomotion_flat/2026-03-19_12-13-05/
```

至少要拷：

```text
<walk_logdir>/
  exported/
    actor.onnx
    actor.onnx.data
    policy_normalizer.npz
  params/
    env.yaml
```

说明：

- `WalkAgent` 明确读取：
  - `exported/actor.onnx`
  - `exported/policy_normalizer.npz`（如果存在）
- `OnboardAgent` 会读取：
  - `params/env.yaml`

对应代码：

- `instinct_onboard/instinct_onboard/agents/walk_agent.py`
- `instinct_onboard/instinct_onboard/agents/base.py`

虽然 `agent.yaml` 对 `WalkAgent` 不是强制必须，但建议一起保留整个 `params/` 目录。

---

## 5. perceptive tracking / shadowing 策略需要拷哪些文件

如果你用的是：

- `g1_perceptive_track.py`
- `PerceptiveTrackerAgent`

则至少要拷：

```text
<tracking_logdir>/
  exported/
    actor.onnx
    actor.onnx.data
    0-depth_image.onnx
    0-depth_image.onnx.data   # 若存在
    policy_normalizer.npz
  params/
    env.yaml
```

说明：

- `PerceptiveTrackerAgent` 读取：
  - `exported/actor.onnx`
  - `exported/0-depth_image.onnx`
  - `exported/policy_normalizer.npz`
- `OnboardAgent` 读取：
  - `params/env.yaml`

对应代码：

- `instinct_onboard/instinct_onboard/agents/tracking_agent.py`
- `instinct_onboard/instinct_onboard/agents/base.py`

同样建议直接把整个 run 目录都拷过去。

---

## 6. motion_dir 需要放什么

`g1_perceptive_track.py` 还需要：

```bash
--motion_dir <path>
```

这里必须放的是：

- 要执行的 `.npz` motion 文件

例如你的 ringroom：

```text
/home/unitree/instinct_deploy/motions/ringroom/zd-2-retargeted.npz
```

当前 `TrackerAgent` 会直接扫描这个目录下所有 motion 文件：

- 每个 `.npz` 都会被加载
- 按按钮切换时按文件名选对应 motion

对应代码：

- `instinct_onboard/instinct_onboard/agents/tracking_agent.py`

---

## 7. 板端启动命令（推荐）

### 7.1 使用 locomotion + perceptive tracking

推荐命令：

```bash
cd /home/unitree/workspaces/instinct_onboard
source ~/instinct_venv/bin/activate
source /opt/ros/humble/setup.bash

python instinct_onboard/scripts/g1_perceptive_track.py \
  --logdir /home/unitree/instinct_deploy/logs/perceptive_ringroom/<your_perceptive_run> \
  --motion_dir /home/unitree/instinct_deploy/motions/ringroom \
  --walk_logdir /home/unitree/instinct_deploy/logs/locomotion/2026-03-19_12-13-05 \
  --nodryrun
```

如果只是先在板子上做不发命令测试，把 `--nodryrun` 去掉即可。

---

## 8. 当前脚本里的 agent 状态机

`g1_perceptive_track.py` 当前有三种状态：

1. `cold_start`
2. `walk`（如果传了 `--walk_logdir`）
3. `tracking`

启动时默认流程：

### Step 1：cold_start 自动开始

- 节点启动后自动进入 `cold_start`
- 作用：把机器人缓慢带到目标初始姿态

### Step 2：冷启动完成后

如果你提供了 `--walk_logdir`：

- 提示你按 `L1`
- 切到 `walk`

当前代码里这一段见：

- `instinct_onboard/scripts/g1_perceptive_track.py`

### Step 3：进入 walk

进入 `walk` 后，你可以用摇杆让机器人移动。

### Step 4：在 walk 模式下按按钮，切到 tracking

按钮会触发不同 motion：

- `up`
- `down`
- `left`
- `right`
- `X`

切到 `tracking` 后，会执行对应 motion。

### Step 5：tracking 做完后

如果存在 `walk` agent：

- 自动回到 `walk`

否则：

- 关电机并退出

---

## 9. Walk 模式（locomotion）怎么控制

`WalkAgent` 是一个连续 locomotion 策略。

它不是 reference motion，而是直接吃摇杆速度命令：

- 左摇杆 `ly`：前后速度
- 左摇杆 `lx`：横移（代码里用了负号）
- 右摇杆 `rx`：yaw 转向（代码里用了负号）

对应代码：

- `instinct_onboard/instinct_onboard/agents/walk_agent.py`

### 实际理解

大体可理解为：

- 左摇杆上下：前进 / 后退
- 左摇杆左右：左右平移
- 右摇杆左右：转向

---

## 10. 当前 `g1_perceptive_track.py` 的按钮流程

### A 按钮

- 作用：重新把当前 tracking motion 对齐到机器人当前朝向

对应：

- `match_to_current_heading()`

注意：

- `TrackerAgent.reset(motion_name)` 本身就会调用一次 `match_to_current_heading()`
- 所以按方向键切换 motion 时，通常已经自动做了初始对齐
- `A` 更多是一个手动重新对齐按钮

---

### L1 按钮

- 冷启动完成后：
  - `L1` 切到 `walk`
- tracking 执行过程中：
  - `L1` 强制回到 `walk`

---

### 方向键 / X

当前默认映射是：

- `up` → `diveroll4-ziwen-0-retargeted.npz`
- `down` → `kneelClimbStep1-x-0.1-ziwen-retargeted.npz`
- `left` → `rollVault11-ziwen-retargeted.npz`
- `right` → `jumpsit2-ziwen-retargeted.npz`
- `X` → `superheroLanding-retargeted.npz`

这意味着：

> 同一个 tracking/perceptive tracking 策略，  
> 可以由不同按钮触发不同 motion 文件。

---

## 11. 如果你要部署自己的 ringroom motion

你当前的目标 motion 是：

- `zd-2-retargeted.npz`

但是当前脚本里没有这个按钮映射。

所以你需要把某一个按钮改成：

```python
self.available_agents[self.current_agent_name].reset("zd-2-retargeted.npz")
```

例如你可以把：

- `X`

改成你的 ringroom motion。

### 改完后的推荐交互流程

1. 启动节点
2. `cold_start` 自动开始
3. 冷启动完成后，按 `L1` 进入 `walk`
4. 用摇杆把机器人走到 ringroom 障碍前
5. 按你映射的按钮（比如 `X`）
6. 进入 `tracking`
7. 执行 `zd-2-retargeted.npz`
8. 执行完自动回 `walk`
9. 你再用摇杆把机器人走回来

---

## 12. 当前实现下，如何开始 locomotion、如何开始越障

### 开始 locomotion

前提：

- 启动命令里传了 `--walk_logdir`

然后：

1. 节点启动
2. `cold_start` 自动进行
3. 冷启动完成后
4. **按 `L1`**
5. 进入 `walk`

---

### 开始越障

前提：

- 当前已经在 `walk` 模式
- `motion_dir` 里有对应的 motion 文件
- 脚本里该按钮已经映射到你的 motion 文件

然后：

1. 用摇杆把机器人走到障碍前
2. 按对应按钮（例如你把 `X` 改成 ringroom）
3. 进入 `tracking`
4. 执行 reference motion 越障

---

## 13. 如果你不传 `--walk_logdir` 会怎样

那就没有 locomotion 模式。

这时只剩：

- `cold_start`
- `tracking`

从当前代码看，**最稳定、最符合你的使用方式的流程是传入 `--walk_logdir`**。

否则你就失去了：

- 先走到位
- 做完再走回来

这一整套工作流。

---

## 14. 是否需要一起拷 `agent.yaml`

对 `g1_perceptive_track.py` / `PerceptiveTrackerAgent` 来说，核心必须的是：

- `params/env.yaml`
- `exported/actor.onnx`
- `exported/0-depth_image.onnx`
- `exported/policy_normalizer.npz`

但为了减少遗漏，**推荐直接拷整个 run 目录**，包括：

- `params/env.yaml`
- `params/agent.yaml`
- `exported/*`

同理，walk 模型目录也直接拷整个 run 目录。

---

## 15. 推荐的实际拷贝命令（示例）

假设训练机上：

- locomotion logdir：

```text
/home/lxj/instinct/instinct/insMJ/InstinctMJ/logs/instinct_rl/g1_locomotion_flat/2026-03-19_12-13-05
```

- perceptive tracking / shadowing logdir：

```text
/home/lxj/instinct/instinct/insMJ/InstinctMJ/logs/instinct_rl/g1_perceptive_shadowing/<your_run>
```

### 拷 locomotion

```bash
rsync -av \
  /home/lxj/instinct/instinct/insMJ/InstinctMJ/logs/instinct_rl/g1_locomotion_flat/2026-03-19_12-13-05 \
  unitree@<robot_ip>:/home/unitree/instinct_deploy/logs/locomotion/
```

### 拷 perceptive tracking

```bash
rsync -av \
  /home/lxj/instinct/instinct/insMJ/InstinctMJ/logs/instinct_rl/g1_perceptive_shadowing/<your_run> \
  unitree@<robot_ip>:/home/unitree/instinct_deploy/logs/perceptive_ringroom/
```

### 拷 motion 文件

```bash
mkdir -p /tmp/ringroom_motion_dir
cp /home/lxj/instinct/instinct/insMJ/InstinctMJ/data/20251116_50cm_kneeClimbStep1/20260316_zd2_ring_room/zd-2-retargeted.npz /tmp/ringroom_motion_dir/

rsync -av \
  /tmp/ringroom_motion_dir/ \
  unitree@<robot_ip>:/home/unitree/instinct_deploy/motions/ringroom/
```

---

## 16. 部署前最终 checklist

在机器人端确认：

- [ ] Ubuntu 22.04
- [ ] ROS2 Humble 已 source
- [ ] `instinct_venv` 已激活
- [ ] `instinct_onboard` 已 `pip install -e .[all]`
- [ ] `cv2` 可 import
- [ ] `pyrealsense2` 可 import
- [ ] `unitree_hg` / `unitree_go` message 已安装并 source
- [ ] `crc_module.so` 已放到运行目录 / Python 可见目录
- [ ] `walk_logdir` 里存在：
  - [ ] `params/env.yaml`
  - [ ] `exported/actor.onnx`
  - [ ] `exported/actor.onnx.data`
  - [ ] `exported/policy_normalizer.npz`
- [ ] `tracking logdir` 里存在：
  - [ ] `params/env.yaml`
  - [ ] `exported/actor.onnx`
  - [ ] `exported/actor.onnx.data`
  - [ ] `exported/0-depth_image.onnx`
  - [ ] `exported/policy_normalizer.npz`
- [ ] `motion_dir` 里存在：
  - [ ] `zd-2-retargeted.npz`
- [ ] `g1_perceptive_track.py` 按钮映射已经改成你的 ringroom motion

---

## 17. 你当前最推荐的使用方式

对你当前这条 reference-conditioned 策略，板端最推荐工作流是：

1. `WalkAgent` 负责 locomotion
2. `PerceptiveTrackerAgent` 负责 ringroom 越障
3. `motion_dir` 提供 `zd-2-retargeted.npz`
4. 通过手柄按钮切 motion

这条路线最接近你描述的作者工作流：

> 进入 locomotion → 走到位 → 启动越障 → 做完后回 locomotion → 再走回来

