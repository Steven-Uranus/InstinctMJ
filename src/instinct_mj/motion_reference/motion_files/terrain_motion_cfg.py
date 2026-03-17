from __future__ import annotations

from collections.abc import Callable  # noqa: F401
from dataclasses import MISSING, dataclass, field
from typing import Literal

import torch

from instinct_mj.motion_reference.motion_reference_cfg import MotionBufferCfg

from .amass_motion_cfg import AmassMotionCfg
from .terrain_motion import TerrainMotion


@dataclass(kw_only=True)
class TerrainMotionCfg(AmassMotionCfg):
    """Configuration for terrain motion data, which is typically terrain-dependent."""

    class_type: type = TerrainMotion

    metadata_yaml: str = MISSING
    """YAML file containing the motion matching configuration.
    Please refer to the `MotionMatchedTerrainCfg` for the expected structure.
    """

    max_origins_per_motion: int = 16
    """ Due to the subterrain design, each terrain_id will be generated to multiple subterrains. Thus, each motion
    could be put on any of these subterrains. However, to improve the sample efficiency, we need to vectorize the
    sampling of the origins. This parameter controls the maximum number of origins per motion.
    """

    motion_file_position_offsets: dict[str, tuple[float, float, float] | list[float]] = field(default_factory=dict)
    """Optional per-motion xyz offsets applied by substring match on ``motion_file`` entries in ``metadata.yaml``.

    Example:
        ``{"zd2_ring_room": (0.0, 0.8, 0.0)}``

    This is useful for mixed datasets where only a subset of motions/scenes need an additional origin shift.
    """

    def __post_init__(self) -> None:
        """Post-initialization to ensure the motion matching YAML file is set."""
        assert (
            self.filtered_motion_selection_filepath is None
        ), "TerrainMotionCfg does not support filtered_motion_selection_filepath. Please use metadata_yaml instead."
