import numpy as np
import scipy.io.wavfile
import torch
from transformers import AutoTokenizer, VitsModel

# Load model and tokenizer
model = VitsModel.from_pretrained("facebook/mms-tts-vie")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-vie")

# Prepare input text
text = "Chiều 30.3, Bộ Quốc phòng tổ chức hội nghị giao nhiệm vụ cho các lực lượng tham gia khắc phục hậu quả động đất tại Myanmar. Đại tướng Nguyễn Tân Cương, Tổng tham mưu trưởng Quân đội nhân dân Việt Nam, Thứ trưởng Bộ Quốc phòng chủ trì hội nghị."
inputs = tokenizer(text, return_tensors="pt")

# Generate waveform
with torch.no_grad():
    output = model(**inputs).waveform

# Convert output tensor to numpy array
output_np = output.squeeze().cpu().numpy()

# Ensure proper type (float32 is common for models like VITS)
output_np = output_np.astype(np.float32)

# Save as .wav file
scipy.io.wavfile.write("techno.wav", rate=model.config.sampling_rate, data=output_np)
