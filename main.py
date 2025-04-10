import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Force CPU usage

import IPython.display as ipd
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.dataclass.utils import convert_namespace_to_omegaconf
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface

# Create config override dictionary
cfg_overrides = {
    "vocoder": "hifigan",
    "fp16": False,
    "cpu": True,
}

# Load model with modified configuration
models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/tts_transformer-vi-cv7",
    arg_overrides=convert_namespace_to_omegaconf(cfg_overrides),
)

# Move model to CPU explicitly
model = models[0].cpu()

# Update configuration
TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
generator = task.build_generator(model, cfg)

# Test text
text = "Xin chào, đây là một cuộc chạy thử nghiệm."

# Generate audio
sample = TTSHubInterface.get_model_input(task, text)
wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)

# Play audio
ipd.Audio(wav, rate=rate)
