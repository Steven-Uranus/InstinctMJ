# InstinctMJ 使用说明（详细版）

> 项目根目录：`/home/lxj/instinct/instinct/insMJ/InstinctMJ`
>
> 本文基于当前仓库代码、README 与任务配置整理，目标是告诉你“最新的 InstinctMJ 怎么用”。

---

## 1. 先认识这个项目

`InstinctMJ` 是一个独立的 Python 包，不是直接在 `mjlab` 仓库里改 task。

当前目录结构里相关项目分别是：

- `insMJ/InstinctMJ`：环境与任务包（你真正要用的主项目）
- `insMJ/mjlab`：上游 mjlab 参考/依赖
- `insMJ/instinct_rl`：训练算法仓库参考/依赖

主项目根目录：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
```

---

## 2. 入口脚本有哪些


## 2.1 如果命令提示 `command not found`

如果你在项目根目录执行：

```bash
instinct-list-envs
```

但出现：

```bash
zsh: command not found: instinct-list-envs
```

说明**当前 shell 没有把 `InstinctMJ/.venv/bin` 放进 PATH**。

你有三种常用解决方式：

### 方式 A：临时激活虚拟环境（推荐）

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
source .venv/bin/activate
```

激活后再执行：

```bash
instinct-list-envs
```

### 方式 B：直接调用脚本绝对路径

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
.venv/bin/instinct-list-envs
```

### 方式 C：用模块方式运行

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
PYTHONPATH=src .venv/bin/python -m instinct_mj.scripts.list_envs
```

---

## 2.2 如果继续遇到 Warp / cache 只读错误

在当前机器环境下，`InstinctMJ` 的脚本还可能进一步报错：

- `Read-only file system: '/home/lxj/.cache/warp/...'`
- `matplotlib` / `fontconfig` cache 不可写

这是因为默认缓存目录不可写，不是 `InstinctMJ` 命令本身不存在。

当前可用的临时运行方式是：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
WARP_CACHE_DIR=/tmp/warp MPLCONFIGDIR=/tmp/mpl XDG_CACHE_HOME=/tmp/xdg .venv/bin/instinct-list-envs
```

我已验证，上面这条在你当前环境里可以正常列出任务。

如果你想每次都不用重复写，可以先执行：

```bash
export WARP_CACHE_DIR=/tmp/warp
export MPLCONFIGDIR=/tmp/mpl
export XDG_CACHE_HOME=/tmp/xdg
```

然后再：

```bash
source /home/lxj/instinct/instinct/insMJ/InstinctMJ/.venv/bin/activate
instinct-list-envs
```


`pyproject.toml` 中定义了这些常用命令：

- `instinct-train`
- `instinct-play`
- `instinct-list-envs`
- `instinct-format`
- `instinct-depth-probe`
- `instinct-perceptive-p0-1-7`
- `instinct-amass-filter`
- `instinct-amass-visualize`
- `instinct-gmr-to-instinct`
- `instinct-motion-metadata`
- `instinct-phalp-to-amass`

如果命令没进 PATH，也可以直接用模块方式：

```bash
python -m instinct_mj.scripts.instinct_rl.train <TASK_ID>
python -m instinct_mj.scripts.instinct_rl.play <TASK_ID> --load-run <run_name>
python -m instinct_mj.scripts.list_envs
```

---

## 3. 如何安装

### 3.1 推荐目录关系

推荐三者作为同级目录：

```text
<workspace_dir>/
  mjlab/
  instinct_rl/
  InstinctMJ/
```

### 3.2 在当前环境中的实际路径

你现在的本地路径就是：

```text
/home/lxj/instinct/instinct/insMJ/
  mjlab/
  instinct_rl/
  InstinctMJ/
```

### 3.3 安装步骤

进入主项目：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
```

如果使用 `uv`：

```bash
uv sync
```

如果使用 pip editable：

```bash
pip install -e .
```

前提通常是你已经能导入：

- `mjlab`
- `instinct_rl`

---

## 4. 怎么列出全部任务

在项目根目录执行：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
instinct-list-envs
```

按关键词筛选：

```bash
instinct-list-envs shadowing
instinct-list-envs parkour
instinct-list-envs locomotion
```

模块方式：

```bash
python -m instinct_mj.scripts.list_envs
```

---

## 5. 当前已注册任务列表

### 5.1 Locomotion

- `Instinct-Locomotion-Flat-G1-v0`
- `Instinct-Locomotion-Flat-G1-Play-v0`

配置路径：

- 任务注册：
  - `src/instinct_mj/tasks/locomotion/config/g1/__init__.py`
- 环境配置：
  - `src/instinct_mj/tasks/locomotion/config/g1/flat_env_cfg.py`
- RL 配置：
  - `src/instinct_mj/tasks/locomotion/config/g1/rl_cfgs.py`

### 5.2 Shadowing / BeyondMimic

- `Instinct-BeyondMimic-Plane-G1-v0`
- `Instinct-BeyondMimic-Plane-G1-Play-v0`

配置路径：

- 注册：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/beyondmimic_plane_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/rl_cfgs.py`

### 5.3 Shadowing / WholeBody

- `Instinct-Shadowing-WholeBody-Plane-G1-v0`
- `Instinct-Shadowing-WholeBody-Plane-G1-Play-v0`

配置路径：

- 注册：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/plane_shadowing_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/rl_cfgs.py`

### 5.4 Shadowing / Perceptive

- `Instinct-Perceptive-Shadowing-G1-v0`
- `Instinct-Perceptive-Shadowing-G1-Play-v0`

配置路径：

- 注册：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/perceptive_shadowing_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/rl_cfgs.py`

### 5.5 Shadowing / Perceptive VAE

- `Instinct-Perceptive-Vae-G1-v0`
- `Instinct-Perceptive-Vae-G1-Play-v0`

配置路径：

- 注册：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/perceptive_vae_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/rl_cfgs.py`

### 5.6 Parkour

- `Instinct-Parkour-Target-Amp-G1-v0`
- `Instinct-Parkour-Target-Amp-G1-Play-v0`

配置路径：

- 注册：
  - `src/instinct_mj/tasks/parkour/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/parkour/config/g1/g1_parkour_target_amp_cfg.py`
- 公共 parkour env：
  - `src/instinct_mj/tasks/parkour/config/parkour_env_cfg.py`
- RL：
  - `src/instinct_mj/tasks/parkour/config/g1/agents/instinct_rl_amp_cfg.py`

---

## 6. 基础命令怎么用

以下命令默认都在项目根目录运行：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
```

### 6.1 训练

通用形式：

```bash
instinct-train <TASK_ID>
```

例如：

```bash
instinct-train Instinct-Locomotion-Flat-G1-v0
instinct-train Instinct-BeyondMimic-Plane-G1-v0
instinct-train Instinct-Shadowing-WholeBody-Plane-G1-v0
instinct-train Instinct-Perceptive-Shadowing-G1-v0
instinct-train Instinct-Perceptive-Vae-G1-v0
instinct-train Instinct-Parkour-Target-Amp-G1-v0
```

### 6.2 回放

通用形式：

```bash
instinct-play <PLAY_TASK_ID> --load-run <run_name_or_run_path>
```

例如：

```bash
instinct-play Instinct-Locomotion-Flat-G1-Play-v0 --load-run <run_name>
instinct-play Instinct-BeyondMimic-Plane-G1-Play-v0 --load-run <run_name>
instinct-play Instinct-Shadowing-WholeBody-Plane-G1-Play-v0 --load-run <run_name>
instinct-play Instinct-Perceptive-Shadowing-G1-Play-v0 --load-run <run_name>
instinct-play Instinct-Perceptive-Vae-G1-Play-v0 --load-run <run_name>
instinct-play Instinct-Parkour-Target-Amp-G1-Play-v0 --load-run <run_name>
```

### 6.3 录视频

训练时：

```bash
instinct-train <TASK_ID> --video True
```

回放时：

```bash
instinct-play <PLAY_TASK_ID> --load-run <run_name> --video True
```

### 6.4 使用随机策略或零策略看环境

```bash
instinct-play <PLAY_TASK_ID> --agent random
instinct-play <PLAY_TASK_ID> --agent zero
```

---

## 7. 日志和输出在哪

训练日志目录遵循：

```text
logs/instinct_rl/<experiment_name>/<timestamp_run>/
```

在 `play.py` 中还能看到这些默认输出逻辑：

- play 视频默认写到：
  - `<checkpoint_parent>/videos/play/`
- ONNX 默认导出到：
  - `<checkpoint_parent>/exported/`

因此一个典型 run 目录可能长这样：

```text
logs/instinct_rl/g1_parkour/2026-03-16_12-34-56_some_run/
  model_1000.pt
  model_2000.pt
  params/
  videos/play/
  exported/
```

---

## 8. `--load-run` / checkpoint 怎么理解

回放时最常见用法是：

```bash
instinct-play <PLAY_TASK_ID> --load-run <run_name>
```

也可以更显式：

```bash
instinct-play <PLAY_TASK_ID>   --load-run <run_name>   --checkpoint-pattern 'model_.*.pt'
```

或者直接指定 checkpoint：

```bash
instinct-play <PLAY_TASK_ID>   --checkpoint-file /absolute/path/to/model_30000.pt
```

如果你已经下载了一个 run 目录，也可以直接把 `--load-run` 指向绝对路径。

---

## 9. 设备、viewer、并行环境常用参数

### 9.1 训练常用

在 `train.py` 里你可以用这些：

- `--num-envs`
- `--device cuda:0`
- `--video True`
- `--viewer native`
- `--gpu-ids "[0,1]"`

例如：

```bash
instinct-train Instinct-Locomotion-Flat-G1-v0   --num-envs 4096   --device cuda:0
```

多 GPU：

```bash
instinct-train Instinct-Locomotion-Flat-G1-v0   --gpu-ids "[0,1]"
```

### 9.2 回放常用

在 `play.py` 里常用这些：

- `--device cuda:0`
- `--viewer native`
- `--viewer viser`
- `--num-envs 1`
- `--video True`
- `--no-terminations True`
- `--max-steps 1000`

例如：

```bash
instinct-play Instinct-Locomotion-Flat-G1-Play-v0   --load-run <run_name>   --viewer native   --device cuda:0
```

---

## 10. 各任务具体怎么用

---

## 10.1 Locomotion 任务怎么用

### 任务

- `Instinct-Locomotion-Flat-G1-v0`
- `Instinct-Locomotion-Flat-G1-Play-v0`

### 关键配置路径

- 注册：
  - `src/instinct_mj/tasks/locomotion/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/locomotion/config/g1/flat_env_cfg.py`
- RL：
  - `src/instinct_mj/tasks/locomotion/config/g1/rl_cfgs.py`

### 是否需要改本地数据路径

- **不需要**
- 这是最简单的任务，可以直接跑

### 训练

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
instinct-train Instinct-Locomotion-Flat-G1-v0
```

### 回放

```bash
instinct-play Instinct-Locomotion-Flat-G1-Play-v0 --load-run <run_name>
```

---

## 10.2 BeyondMimic 任务怎么用

### 任务

- `Instinct-BeyondMimic-Plane-G1-v0`
- `Instinct-BeyondMimic-Plane-G1-Play-v0`

### 关键配置路径

- 注册：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/beyondmimic_plane_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/rl_cfgs.py`

### 你必须先改的本地路径

在文件：

```text
src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/beyondmimic_plane_cfg.py
```

要关注这些变量：

- `MOTION_NAME`
- `_hacked_selected_file_`
- `path=os.path.expanduser("...")`

当前代码里数据根路径示例是：

```python
path=os.path.expanduser("~/Xyk/Datasets/UbisoftLAFAN1_GMR_g1_29dof_torsoBase_retargetted_instinctnpz")
```

你需要改成你机器上的真实路径。

### 训练

```bash
instinct-train Instinct-BeyondMimic-Plane-G1-v0
```

### 回放

```bash
instinct-play Instinct-BeyondMimic-Plane-G1-Play-v0 --load-run <run_name>
```

---

## 10.3 Whole-body Shadowing 任务怎么用

### 任务

- `Instinct-Shadowing-WholeBody-Plane-G1-v0`
- `Instinct-Shadowing-WholeBody-Plane-G1-Play-v0`

### 关键配置路径

- 注册：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/plane_shadowing_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/rl_cfgs.py`

### 你必须先改的本地路径

在：

```text
src/instinct_mj/tasks/shadowing/whole_body/config/g1/plane_shadowing_cfg.py
```

主要改：

- `MOTION_NAME`
- `_hacked_selected_files_`
- 当前 active motion buffer 所使用的 `path=...`

README 中也特别提醒：

- `_path_` 在一些 preset block 里存在
- 但你真正要改的是**当前 active motion_buffers 里正在用的 path**

### 训练

```bash
instinct-train Instinct-Shadowing-WholeBody-Plane-G1-v0
```

### 回放

```bash
instinct-play Instinct-Shadowing-WholeBody-Plane-G1-Play-v0 --load-run <run_name>
```

---

## 10.4 Perceptive Shadowing 怎么用

### 任务

- `Instinct-Perceptive-Shadowing-G1-v0`
- `Instinct-Perceptive-Shadowing-G1-Play-v0`

### 关键配置路径

- 注册：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/perceptive_shadowing_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/rl_cfgs.py`

### 你必须先改的本地路径

在：

```text
src/instinct_mj/tasks/shadowing/perceptive/config/g1/perceptive_shadowing_cfg.py
```

主要变量：

```python
MOTION_FOLDER = "/home/lxj/instinct/instinct/Instinct/data/20251116_50cm_kneeClimbStep1"
```

你需要保证：

- `MOTION_FOLDER` 指向真实存在目录
- 目录下有 `metadata.yaml`

当前这台机器上，我已经把配置改成了这个实际存在的目录：

```bash
/home/lxj/instinct/instinct/Instinct/data/20251116_50cm_kneeClimbStep1
```

### 训练

```bash
instinct-train Instinct-Perceptive-Shadowing-G1-v0
```

### 回放

```bash
instinct-play Instinct-Perceptive-Shadowing-G1-Play-v0 --load-run <run_name>
```

### 使用已下载 checkpoint 回放

```bash
instinct-play Instinct-Perceptive-Shadowing-G1-Play-v0   --load-run <downloaded_run_dir>   --checkpoint-file <checkpoint_file>
```

---

## 10.5 Perceptive VAE 怎么用

### 任务

- `Instinct-Perceptive-Vae-G1-v0`
- `Instinct-Perceptive-Vae-G1-Play-v0`

### 关键配置路径

- 注册：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/__init__.py`
- 环境：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/perceptive_vae_cfg.py`
- RL：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/rl_cfgs.py`

### 你必须先改的本地路径

同样关注：

```python
MOTION_FOLDER = "/home/lxj/instinct/instinct/Instinct/data/20251116_50cm_kneeClimbStep1"
```

并确认 `metadata.yaml` 存在。

---

## 10.4.1 如果你想翻越不同障碍物，应该如何建立数据集

Perceptive Shadowing 依赖的是 **terrain-matched motion dataset**，也就是：

- 一个障碍物地形文件
- 配套的一组 motion 文件
- 根目录 `metadata.yaml` 负责把二者关联起来

### 目录结构建议

推荐把数据集组织成这样：

```text
<DATASET_ROOT>/
  metadata.yaml
  obstacle_a/
    obstacle_a.stl
    motion_1-retargeted.npz
    motion_2-retargeted.npz
  obstacle_b/
    obstacle_b.stl
    motion_1-retargeted.npz
  obstacle_c/
    obstacle_c.ply
    motion_1-retargeted.npz
```

### 每个障碍目录里应该有什么

根据 `instinct_mj.scripts.motion_matched_metadata_generator` 当前实现：

- 每个子目录应当包含 **一个** terrain 文件：
  - `.stl`
  - 或 `.ply`
- 以及 **一个或多个** motion 文件：
  - 文件名以 `retargeted.npz` 结尾
  - 或 `poses.npz` 结尾

### retargeted motion 文件的最低要求

从 `motion_reference/motion_files/amass_motion.py` 当前读取逻辑看，`retargeted.npz` 至少要有：

- `framerate`
- `joint_names`
- `joint_pos`
- `base_pos_w`
- `base_quat_w`

因此最稳妥的方式是继续沿用你现在已有的 `*-retargeted.npz` 风格文件。

### metadata.yaml 是什么

根目录的 `metadata.yaml` 会长这样：

```yaml
terrains:
  - terrain_id: 0
    terrain_file: obstacle_a/obstacle_a.stl
  - terrain_id: 1
    terrain_file: obstacle_b/obstacle_b.stl

motion_files:
  - terrain_id: 0
    motion_file: obstacle_a/motion_1-retargeted.npz
  - terrain_id: 0
    motion_file: obstacle_a/motion_2-retargeted.npz
  - terrain_id: 1
    motion_file: obstacle_b/motion_1-retargeted.npz
```

也就是说：

- `terrain_id` 定义障碍物类型
- `motion_files` 指出哪些 motion 属于这个障碍物

### 如何自动生成 metadata.yaml

项目已经带了脚本：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
PYTHONPATH=src .venv/bin/python -m instinct_mj.scripts.motion_matched_metadata_generator \
  --path <DATASET_ROOT>
```

或者如果命令在 PATH 中：

```bash
instinct-motion-metadata --path <DATASET_ROOT>
```

这个脚本会：

- 遍历 `<DATASET_ROOT>`
- 读取每个子目录中的 terrain 文件和 motion 文件
- 自动在根目录生成 `metadata.yaml`

### 如果你想支持“不同障碍物”

建议按障碍物类型或参数拆目录，不要混在同一个文件夹里。

例如：

#### 不同几何类型

```text
roadRamp/
step50cm/
boxVault/
simpleLab/
```

#### 同一种障碍不同尺寸

```text
step30cm/
step50cm/
step70cm/
```

#### 同一障碍的有墙/无墙版本

```text
roadRamp/
roadRamp_noWall/
simpleLab/
simpleLab_noWall/
```

### 你当前已有的数据集就是一个模板

你现在机器上已有的这个目录就是标准示例：

```bash
/home/lxj/instinct/instinct/Instinct/data/20251116_50cm_kneeClimbStep1
```

它当前已经包含：

- 根目录 `metadata.yaml`
- 多个障碍子目录
- 每个子目录里有：
  - 一个 `.stl`
  - 一个或多个 `*-retargeted.npz`

你以后要做新的障碍数据集，直接照这个结构扩展是最稳妥的。

### 训练

```bash
instinct-train Instinct-Perceptive-Vae-G1-v0
```

### 回放

```bash
instinct-play Instinct-Perceptive-Vae-G1-Play-v0 --load-run <run_name>
```

---

## 10.6 Parkour 任务怎么用

### 任务

- `Instinct-Parkour-Target-Amp-G1-v0`
- `Instinct-Parkour-Target-Amp-G1-Play-v0`

### 关键配置路径

- 注册：
  - `src/instinct_mj/tasks/parkour/config/g1/__init__.py`
- 主环境：
  - `src/instinct_mj/tasks/parkour/config/g1/g1_parkour_target_amp_cfg.py`
- 公共 terrain/env：
  - `src/instinct_mj/tasks/parkour/config/parkour_env_cfg.py`
- RL：
  - `src/instinct_mj/tasks/parkour/config/g1/agents/instinct_rl_amp_cfg.py`

### 你必须先改的本地路径

在：

```text
src/instinct_mj/tasks/parkour/config/g1/g1_parkour_target_amp_cfg.py
```

最关键变量：

```python
_PARKOUR_DATASET_DIR = os.path.expanduser("~/Xyk/Datasets/data&model/parkour_motion_reference")
```

如果你的 motion 过滤文件不在默认位置，也要改：

- `filtered_motion_selection_filepath`

### 训练

```bash
instinct-train Instinct-Parkour-Target-Amp-G1-v0
```

### 回放

```bash
instinct-play Instinct-Parkour-Target-Amp-G1-Play-v0 --load-run <run_name>
```

### 导出 ONNX

```bash
instinct-play Instinct-Parkour-Target-Amp-G1-Play-v0   --load-run <run_name>   --export-onnx
```

### 使用导出的 ONNX 回放

```bash
instinct-play Instinct-Parkour-Target-Amp-G1-Play-v0   --load-run <run_name>   --use-onnx
```

---

## 11. motion file / registry_name 怎么用

从 `train.py` / `play.py` 逻辑看，**tracking 类任务**支持：

- `--motion-file /path/to/motion.npz`
- `--registry-name your-org/motions/name`

也就是说 motion 来源优先顺序一般是：

1. `--motion-file`
2. `--registry-name`
3. env config 内已写好的 `motion_file`

如果是 tracking/shadowing 类任务，你还可以这样指定：

```bash
instinct-train Instinct-BeyondMimic-Plane-G1-v0   --motion-file /absolute/path/to/motion.npz
```

或：

```bash
instinct-play Instinct-BeyondMimic-Plane-G1-Play-v0   --motion-file /absolute/path/to/motion.npz   --agent random
```

但对很多当前任务来说，项目本身更偏向**直接在 cfg 文件中固定数据根路径**，然后让配置去构造 motion buffer。

所以更稳妥的做法通常是：

- 先改 cfg 里的本地路径
- 再 train/play

---

## 12. 推荐实际使用顺序

如果你第一次上手，我建议：

### 第一步：进入项目根目录

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
```

### 第二步：确认任务列表

```bash
instinct-list-envs
instinct-list-envs shadowing
instinct-list-envs parkour
```

### 第三步：先跑最简单的 locomotion

```bash
instinct-train Instinct-Locomotion-Flat-G1-v0
instinct-play Instinct-Locomotion-Flat-G1-Play-v0 --load-run <run_name>
```

### 第四步：再跑 shadow / parkour

先去对应 cfg 改本地数据路径，再运行：

```bash
instinct-train Instinct-BeyondMimic-Plane-G1-v0
instinct-train Instinct-Shadowing-WholeBody-Plane-G1-v0
instinct-train Instinct-Perceptive-Shadowing-G1-v0
instinct-train Instinct-Parkour-Target-Amp-G1-v0
```

### 第五步：需要部署时再做 ONNX

```bash
instinct-play Instinct-Parkour-Target-Amp-G1-Play-v0   --load-run <run_name>   --export-onnx
```

---

## 13. 你现在最应该记住的几个文件

### 项目入口

- `pyproject.toml`
- `README.md`

### 任务注册

- `src/instinct_mj/tasks/registry.py`
- `src/instinct_mj/tasks/__init__.py`

### CLI

- `src/instinct_mj/scripts/list_envs.py`
- `src/instinct_mj/scripts/instinct_rl/train.py`
- `src/instinct_mj/scripts/instinct_rl/play.py`

### 重点任务配置

- locomotion：
  - `src/instinct_mj/tasks/locomotion/config/g1/flat_env_cfg.py`
- beyondmimic：
  - `src/instinct_mj/tasks/shadowing/beyondmimic/config/g1/beyondmimic_plane_cfg.py`
- whole-body：
  - `src/instinct_mj/tasks/shadowing/whole_body/config/g1/plane_shadowing_cfg.py`
- perceptive：
  - `src/instinct_mj/tasks/shadowing/perceptive/config/g1/perceptive_shadowing_cfg.py`
- parkour：
  - `src/instinct_mj/tasks/parkour/config/g1/g1_parkour_target_amp_cfg.py`

---

## 14. 当前最现实的注意事项

### 14.1 先改本地数据路径再训练

当前多个任务不是完全开箱即用，必须先把 cfg 里的：

- dataset root
- metadata path
- filtered motion list path

改成你本机真实路径。

### 14.2 `--load-run` 一般必须给

对于 play 来说，通常你需要：

```bash
--load-run <run_name>
```

否则它不会知道去哪找 checkpoint。

### 14.3 Parkour 的 ONNX 是特化支持的

`play.py` 里明确写了：

- `--use-onnx` 当前主要支持 parkour

所以 ONNX 相关流程，优先按 parkour 理解。

---

## 15. 一句话总结

如果你要“最新的 InstinctMJ 怎么用”，最简单的理解是：

1. 进入：
   ```bash
   cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
   ```
2. 列任务：
   ```bash
   instinct-list-envs
   ```
3. 先改对应 task cfg 里的本地数据路径
4. 训练：
   ```bash
   instinct-train <TASK_ID>
   ```
5. 回放：
   ```bash
   instinct-play <PLAY_TASK_ID> --load-run <run_name>
   ```
6. parkour 导出 ONNX：
   ```bash
   instinct-play Instinct-Parkour-Target-Amp-G1-Play-v0 --load-run <run_name> --export-onnx
   ```
