# RingRoom 混合训练问题分析与板端部署说明

本文整理两个问题：

1. 为什么把 `ringroom` 混进 perceptive shadowing 数据集后，训练出来的机器人会“原地摆跨越姿态”，而不是先前进两步再跨过去。
2. `instinct_onboard` 在机器人板子上如何部署当前这类策略，以及其中是否存在 locomotion 策略。

---

## 1. 现象复述

你当前观察到的现象是：

- 参考序列（play 时的白色参考机器人 / 参考点）本身没有问题，可以过障碍。
- 原始已有场景（项目里已有的几类 motion / terrain）都能很好复现。
- 唯独你新加入的 `ringroom` 场景训练后不对：
  - 机器人不会真正先走到障碍前；
  - 而是原地做出“跨过去”的姿态；
  - 随后摔倒。

这说明：

- **reference motion 本身是可行的**；
- 但当前训练目标并没有足够强地逼着策略把**全局 root / base 的平面位置**跟到正确障碍位置；
- 它更容易学到“姿态像”而不是“真的走到正确位置再越障”。

---

## 2. 为什么 ringroom 更容易失败

### 2.1 reward 更偏向“姿态模仿”，不够偏向“全局推进”

在：

- `src/instinct_mj/tasks/shadowing/perceptive/perceptive_env_cfg.py`

可看到 perceptive shadowing 的主 reward：

- `base_position_imitation_gauss` 权重 `0.5`
- `base_rot_imitation_gauss` 权重 `0.5`
- `link_pos_imitation_gauss` 权重 `1.0`
- `link_rot_imitation_gauss` 权重 `1.0`

其中 `link_pos_imitation_gauss` 和 `link_rot_imitation_gauss` 还使用了：

- `in_relative_world_frame=True`

这会带来一个重要后果：

> 策略更容易通过“局部身体姿态像”来拿分，而不一定需要把机器人真的推进到障碍前的正确位置。

对于普通场景，这种 reward 结构往往还能工作。  
但对于 `ringroom` 这种**必须精确走到孔前再穿过**的任务，这种设计就容易塌成：

- 不真正前进；
- 但开始做跨越姿态；
- 最后摔倒。

---

### 2.2 termination 对 XY 偏差不敏感

同一个文件里可以看到 termination：

- `base_pos_too_far`
- `link_pos_too_far`

这两项目前都用了：

- `height_only=True`

也就是说：

> 它主要关注高度方向是否偏得太离谱，而不是严格检查平面 XY 是否真的对齐。

这进一步放大了上面的 reward 问题：

- 机器人即使没有真正“走到位”；
- 也不会因为 XY 偏太多而立刻被强力惩罚。

---

### 2.3 训练时 reset 随机化比 play 时更难

在训练配置里，`reset_robot` 默认有：

- `x/y` 随机扰动
- 关节初值扰动

而 play 里为了看参考序列，通常会把这些随机化收紧甚至关掉。

因此你看到：

- **play 参考序列完全没问题**
- **训练学不出来**

并不矛盾。

原因是：

> play 看的通常是“理想条件下的参考动作”；  
> 训练里策略面对的是“带随机偏差的自身状态 + 困难障碍 + 相对宽松的全局位移约束”。

对 `ringroom` 这种窄开口障碍，这种差异会特别明显。

---

### 2.4 ringroom 在 mixed dataset 里仍然是困难少数样本

当前混合数据集里：

- 普通 motion/terrain 占大头；
- `ringroom` 虽然加了权重，但仍然是一个更难、更窄容错的子分布。

所以策略很容易学到一种“对大部分普通样本都还行”的解，而不是专门学会 ringroom 这种更苛刻的时空对齐。

---

## 3. 为什么会出现“原地不动，只做跨越姿态”

一句话总结：

> 当前 perceptive shadowing 的训练目标，更像是在学“参考姿态序列”，而不是强制学“把 root/base 精确送到障碍正确位置再穿过去”。

所以对 ringroom 来说，最容易出现的局部最优就是：

1. 不真正往前推进；
2. 只模仿参考动作里的抬腿/跨越姿态；
3. 由于根部位置不对，最后摔倒。

---

## 4. 当前代码中已经做的 ringroom 特殊处理

为了让 ringroom 在 mixed dataset 下对齐更合理，当前仓库里已经做了：

### 4.1 ringroom motion 的 reference 原点单独加偏移

不是按整个数据集目录判断，而是按 motion 文件名匹配：

- `src/instinct_mj/motion_reference/motion_files/terrain_motion_cfg.py`
- `src/instinct_mj/motion_reference/motion_files/terrain_motion.py`

当前逻辑是：

- 对 `motion_file` 路径里包含 `zd2_ring_room` 的样本，
- 单独给 reference motion 加 `(0.0, +0.8, 0.0)` 偏移。

这意味着：

- 只有 ringroom 的 env 会偏移；
- 其它普通场景不会偏移；
- 机器人 reset 和 future reference 也会一起跟着这个 reference 原点走。

### 4.2 为什么是 `+Y 0.8`

因为当前 ringroom 这条 motion 的主要前进方向是 `-Y`，  
所以“往后挪 0.8m”就是 `+Y 0.8`。

---

## 5. 如果想让 ringroom 真正学会，建议的下一步

### 5.1 最优先：做 ringroom-only fine-tune

建议在 mixed 训练之后，再做一段：

- `ringroom-only dataset`
- perceptive shadowing fine-tune

因为 ringroom 的容错比普通场景窄很多，单独微调通常更有效。

---

### 5.2 收紧 ringroom 的训练随机化

尤其是：

- `reset_robot.randomize_pose_range["x"]`
- `reset_robot.randomize_pose_range["y"]`

对于 ringroom，可以先缩到：

- `±0.02 ~ ±0.05`

甚至最开始直接设成：

- `0`

先让它学会“对孔和推进”，再慢慢加随机化。

---

### 5.3 增强全局推进约束

建议考虑：

1. 提高 `base_position_imitation_gauss` 权重；
2. 把 `base_pos_too_far.height_only` 改成 `False`；
3. 把 `link_pos_too_far.height_only` 改成 `False`；
4. 如有需要，再加更直接的 root/base 前进约束。

这些改动的共同目标都是：

> 让策略不能只在原地“摆姿态”，而必须真的把身体送到正确位置。

---

## 6. instinct_onboard 里有没有 locomotion 策略？

有。

### 6.1 `WalkAgent`

文件：

- `instinct_onboard/instinct_onboard/agents/walk_agent.py`

特点：

- 只加载 `actor.onnx`
- 用遥控器摇杆给速度命令
- 连续 walking
- 没有 motion reference

控制方式：

- `ly`：前后速度
- `-lx`：横移速度
- `-rx`：yaw 角速度

更像：

> 一个简单的 locomotion / walk 策略。

---

### 6.2 `ParkourAgent`

文件：

- `instinct_onboard/instinct_onboard/agents/parkour_agent.py`
- `instinct_onboard/scripts/g1_parkour.py`

特点：

- 也是一种 locomotion / parkour 策略；
- 带 depth encoder；
- 用摇杆控制速度；
- 用于连续移动和越障；
- 更自主，但不是基于 reference motion。

所以如果你说“作者先进入 locomotion，再走到某个地方，再启动越障策略”，
这在代码里通常对应：

- `walk` 或 `parkour`
- 再切到 `tracking`

---

## 7. `g1_perceptive_track.py` 的按钮映射是什么

`g1_perceptive_track.py` 读的是 Unitree 无线遥控器：

- `up/down/left/right`
- `A/B/X/Y`
- `L1/R1`

在当前脚本里，不同按钮对应不同 motion 文件：

- `up` → `diveroll4-ziwen-0-retargeted.npz`
- `down` → `kneelClimbStep1-x-0.1-ziwen-retargeted.npz`
- `left` → `rollVault11-ziwen-retargeted.npz`
- `right` → `jumpsit2-ziwen-retargeted.npz`
- `X` → `superheroLanding-retargeted.npz`

也就是说：

> 同一个 tracking / perceptive tracking 策略，  
> 配合不同 reference motion，由不同按钮触发不同动作。

---

## 8. 板端部署你的策略，应该选哪条线

### 8.1 如果你的策略是“带 reference 的 perceptive shadowing / tracking”

最接近现成入口的是：

- `instinct_onboard/scripts/g1_perceptive_track.py`

这条线适合：

- `depth + future reference motion`
- 执行具体 motion 文件

它需要：

- `logdir`
  - 内含 `exported/actor.onnx`
  - `exported/0-depth_image.onnx`
  - `exported/policy_normalizer.npz`
  - `params/env.yaml`
- `motion_dir`
  - 放 `.npz` motion 文件

---

### 8.2 典型工作流

在板端通常是这样：

1. `cold_start`
2. 切到 `walk`（如果提供了 `--walk_logdir`）
3. **你用摇杆把机器人走到障碍附近**
4. 按某个按钮切到 `tracking`
5. 执行对应的 motion reference
6. 执行完毕后，如果有 `walk`，会自动切回 `walk`
7. **你再用 walk 把机器人走回来**

所以你说作者是：

> 先进入 locomotion，再位移到相应地方，然后启动策略，做完越障，再控制他走回来

这和代码逻辑是一致的。

---

## 9. 如果你要在板端部署 ringroom motion，需要改什么

因为当前 `g1_perceptive_track.py` 里按钮映射没有你的：

- `zd-2-retargeted.npz`

所以你需要把某个按钮改成：

```python
self.available_agents[self.current_agent_name].reset("zd-2-retargeted.npz")
```

比如把：

- `X` 按钮

改成你的 ringroom 动作。

---

## 10. 推荐的板端部署路线

### 方案 A：最贴合你当前策略

使用：

- `g1_perceptive_track.py`

流程：

1. 从 `InstinctMJ` 导出 perceptive tracking/shadowing ONNX
2. 把整个 logdir 拷到板端
3. 准备一个 `motion_dir`，放：
   - `zd-2-retargeted.npz`
4. 修改 `g1_perceptive_track.py` 按钮映射
5. 启动脚本：

```bash
python instinct_onboard/scripts/g1_perceptive_track.py \
  --logdir <your_logdir> \
  --motion_dir <your_motion_dir> \
  --walk_logdir <optional_walk_logdir>
```

这样就是：

- `walk` 负责走到位
- `tracking` 负责执行 ringroom 参考动作

---

### 方案 B：如果最终你不想依赖 reference motion

那最终板端更适合部署：

- `parkour_agent`
- 或者 student / VAE 之类的策略

因为这些更像：

> 只看 depth + proprio，自主连续运动。

但这已经不是当前这条 reference-conditioned perceptive tracking 的直接部署方式了。

---

## 11. 建议的下一步

如果继续围绕 ringroom 做：

1. 先把 mixed dataset 训练问题解决：
   - 收紧 ringroom 随机化
   - 提高全局推进约束
   - 做 ringroom-only fine-tune
2. 再做板端部署：
   - 用 `g1_perceptive_track.py`
   - 增加 `zd-2-retargeted.npz` 的按钮映射
   - 搭配 `walk_agent` 先走到位再触发 tracking

