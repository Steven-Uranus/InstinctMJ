board_debug_bundle_20260319

Contents:
- onboard_code/agents/: onboard runtime agent code used for comparison
- train_export_script/play.py: training-side export/play entrypoint
- locomotion_run/: exported locomotion model + params used for walk_logdir
- perceptive_run/: params from latest perceptive shadowing run  param已经在parkour中，请参考
- motion_examples/zd-2-retargeted.npz: your ringroom motion example

Source paths:
- Onboard code from /home/lxj/instinct/instinct/instinct_onboard
- Training/export/config/model files from /home/lxj/instinct/instinct/insMJ/InstinctMJ

Notes:
- No perceptive exported ONNX was found under insMJ/InstinctMJ/logs/instinct_rl/g1_perceptive_shadowing on this machine, so only params are bundled for perceptive_run.
- locomotion_run/exported includes actor.onnx.data and must stay with actor.onnx.
