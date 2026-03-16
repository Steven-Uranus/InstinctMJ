# 自采数据集：zd-2 + 钻圈切割 + 简易房间

> 目标：在不影响默认 `50cm_kneeClimbStep` 数据集配置的前提下，新建一个可选的数据集，用于先在 MuJoCo 里可视化你的自采动作和自定义障碍效果。

---

## 1. 默认配置没有被改坏

我已经把 `Perceptive Shadowing` / `Perceptive VAE` 的默认数据集恢复为：

```bash
/home/lxj/instinct/instinct/Instinct/data/20251116_50cm_kneeClimbStep1
```

也就是说：

- 你平时不加任何额外参数时，还是走默认的 `50cm_kneeClimbStep1` 数据集。

现在额外支持通过环境变量切换数据集：

```bash
INSTINCT_MJ_PERCEPTIVE_MOTION_FOLDER=/path/to/your_dataset
```

---

## 2. 新建的数据集在哪里

我新建的“带房间版本”的数据集在：

```bash
/home/lxj/instinct/instinct/Instinct/data/20260316_zd2_ring_room_dataset
```

结构如下：

```text
20260316_zd2_ring_room_dataset/
  metadata.yaml
  zd2_ring_room/
    zd2_ring_room.stl
    zd-2-retargeted.npz
    metadata.yaml
    README.txt
```

---

## 3. 数据来源

### 动作来源

- 原始动作：
  - `/home/lxj/resource/GMR/data/zd-2.pkl`
- 转换后动作：
  - `zd2_ring_room/zd-2-retargeted.npz`

### 障碍来源

- 原始障碍：
  - `/home/lxj/instinct/instinct/assets/obstacle/钻圈切割.STL`

---

## 4. 我怎么处理了你的 STL

你说得对：

- 作者原来的 STL 往往自带整个房间/场景
- 你的 `钻圈切割.STL` 只有障碍物本体

所以如果直接拿来当 terrain，会缺少：

- 地面
- 房间边界
- 完整场景参照

### 我对你的障碍做的处理是：

1. **先把原始板件居中**
2. **重新按“上下翻转后开口朝上”的方向做姿态变换**
3. **让障碍底边落在地面上**
4. **把它放到机器人前方的中线位置**
5. **让障碍更靠近机器人，适合“向前走然后跨过去”的参考序列**
5. **额外构造了一个简易房间**：
   - floor
   - 四面墙
6. **让开口朝前后方向（不再埋到地板下面）**

### 最终生成的场景 mesh

```bash
/home/lxj/instinct/instinct/Instinct/data/20260316_zd2_ring_room_dataset/zd2_ring_room/zd2_ring_room.stl
```

### 当前摆放效果（近似）

当前障碍被摆成：

- **开口朝上**
- **底边接地**
- **位于机器人前方中线**
- 位置按 `zd-2` 参考动作的前进方向重新对齐
- 障碍中心约在：
  - `x = -1.13`
  - `y = 0.60`
  - `z = 0.495`

这更符合“机器人沿自己的参考前进方向走向障碍，然后跨过去”的序列假设。

### 场景尺寸（近似）

生成后的 room mesh bounds / extents 约为：

- bounds:
  - `x: [-3.13, 0.87]`
  - `y: [-2.70, 3.30]`
  - `z: [-0.04, 1.20]`
- extents:
  - `4.0 x 6.0 x 1.24`

也就是说这是一个沿机器人前进方向拉长的“房间 + 地板 + 环形障碍”场景。

---

## 5. 如何切换到这个新数据集（不改默认）

### 推荐方式：环境变量切换

进入项目：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
export WARP_CACHE_DIR=/tmp/warp
export MPLCONFIGDIR=/tmp/mpl
export XDG_CACHE_HOME=/tmp/xdg
source .venv/bin/activate
```

然后用这个环境变量切换：

```bash
export INSTINCT_MJ_PERCEPTIVE_MOTION_FOLDER=/home/lxj/instinct/instinct/Instinct/data/20260316_zd2_ring_room_dataset
```

这样当前 shell 下再运行 `Perceptive Shadowing` / `Perceptive VAE`，就会使用你的自采数据集。

---

## 6. 如何只做可视化，不训练

### 方案 A：直接在 MuJoCo 场景里看

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
export WARP_CACHE_DIR=/tmp/warp
export MPLCONFIGDIR=/tmp/mpl
export XDG_CACHE_HOME=/tmp/xdg
export INSTINCT_MJ_PERCEPTIVE_MOTION_FOLDER=/home/lxj/instinct/instinct/Instinct/data/20260316_zd2_ring_room_dataset
source .venv/bin/activate
instinct-play Instinct-Perceptive-Shadowing-G1-Play-v0 \
  --agent zero \
  --viewer native \
  --num-envs 1 \
  --no-terminations True
```

### 这个命令会看到什么

你会在 MuJoCo 里看到：

- 自建房间 `zd2_ring_room.stl`
- 地面 + 墙体
- 你的环形障碍物（已经竖起来，底边落地，位于房间前方）
- 当前 motion reference 对应的 perceptive shadowing 场景

### 为什么用 `--agent zero`

因为你现在只是想：

> 先看场景、障碍、动作是不是对得上

不用训练，`zero` 会让主机器人更安静，便于观察。

---

## 7. 如果你只想看 STL 场景本身

可以直接查看生成后的 room mesh：

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
source .venv/bin/activate
PYTHONPATH=src .venv/bin/python - <<'PY'
import pyvista as pv
mesh = pv.read('/home/lxj/instinct/instinct/Instinct/data/20260316_zd2_ring_room_dataset/zd2_ring_room/zd2_ring_room.stl')
p = pv.Plotter()
p.add_mesh(mesh, color='lightgray', show_edges=True)
p.show()
PY
```

---

## 8. 如果你只想看动作文件本身

```bash
cd /home/lxj/instinct/instinct/insMJ/InstinctMJ
export MPLCONFIGDIR=/tmp/mpl
export XDG_CACHE_HOME=/tmp/xdg
source .venv/bin/activate
PYTHONPATH=src .venv/bin/python -m instinct_mj.scripts.amass_visualize \
  --motion-path /home/lxj/instinct/instinct/Instinct/data/20260316_zd2_ring_room_dataset/zd2_ring_room/zd-2-retargeted.npz \
  --viewer native
```

---

## 9. 这个版本当前适合做什么

适合：

- 验证你的自采 GMR 数据能不能接到 InstinctMJ
- 验证自定义障碍物能不能进入 perceptive shadowing 场景
- 先用 MuJoCo 原生 viewer 看大致效果

不适合：

- 直接拿来做高质量泛化训练
- 直接作为最终正式数据集

因为它现在还是一个：

> **单障碍 + 单动作的最小可视化数据集**

---

## 10. 如果你后面要继续扩展

后续可以继续往这个目录里加：

- 更多 motion：
  - `zd-3-retargeted.npz`
  - `zd-4-retargeted.npz`
- 更多障碍：
  - `zd2_ring_room_variant/`
  - `zd2_box_room/`
  - `zd2_ramp_room/`

然后更新 `metadata.yaml`，逐步把它变成一个真正能训练的小型 perceptive 数据集。
