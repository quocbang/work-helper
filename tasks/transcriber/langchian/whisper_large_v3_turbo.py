from typing import Any, Dict, List, Optional

import librosa
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from transformers import WhisperForConditionalGeneration, WhisperProcessor


class WhisperLarge3Turbo(LLM):
    """
    Langchain implementation of Whisper Large 3 Turbo for speech-to-text conversion.
    """

    model_name: str = "openai/whisper-large-v3-turbo"
    max_duration: int = 30
    target_sampling_rate: int = 16000
    language: str = "chinese"

    def __init__(
        self,
        model_name: str = "openai/whisper-large-v3-turbo",
        max_duration: int = 30,
        target_sampling_rate: int = 16000,
        language: str = "chinese",
        **kwargs,
    ):
        """Initialize the Whisper model and processor."""
        super().__init__(**kwargs)
        self.model_name = model_name
        self.max_duration = max_duration
        self.target_sampling_rate = target_sampling_rate
        self.language = language

        # Initialize model and processor
        self.processor = WhisperProcessor.from_pretrained(self.model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(self.model_name)

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "whisper_large_v3_turbo"

    def _load_audio(self, audio_path: str) -> tuple:
        """
        Load and preprocess audio file.

        Args:
            audio_path (str): Path to audio file

        Returns:
            tuple: (audio_data, sampling_rate)
        """
        try:
            audio, original_sr = librosa.load(audio_path, sr=None)

            if len(audio) == 0:
                raise ValueError(f"Audio file '{audio_path}' is empty.")

            if original_sr != self.target_sampling_rate:
                audio = librosa.resample(
                    audio, orig_sr=original_sr, target_sr=self.target_sampling_rate
                )
                sr = self.target_sampling_rate
            else:
                sr = original_sr

            return audio, sr

        except Exception as e:
            raise ValueError(f"Error loading audio file '{audio_path}': {e}")

    def _process_audio_chunk(self, chunk: List[float], sr: int) -> str:
        """
        Process a single chunk of audio data.

        Args:
            chunk (List[float]): Audio chunk data
            sr (int): Sampling rate

        Returns:
            str: Transcribed text
        """
        if len(chunk) == 0:
            return ""

        # Preprocess audio chunk
        inputs = self.processor(
            chunk, sampling_rate=sr, return_tensors="pt", padding=True
        )

        # Set language and generate predictions
        forced_decoder_ids = self.processor.get_decoder_prompt_ids(
            language=self.language, task="transcribe"
        )

        predicted_ids = self.model.generate(
            inputs.input_features,
            forced_decoder_ids=forced_decoder_ids,
        )

        # Decode predictions
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Process audio file and return transcription.

        Args:
            prompt (str): Path to audio file
            stop (Optional[List[str]]): Stop sequences (not used)
            run_manager (Optional[CallbackManagerForLLMRun]): Callback manager
            **kwargs: Additional arguments

        Returns:
            str: Transcribed text
        """
        try:
            # Load audio
            audio, sr = self._load_audio(prompt)

            # Split audio into chunks
            chunk_size = self.max_duration * sr
            transcriptions = []

            # Process chunks
            for chunk_start in range(0, len(audio), chunk_size):
                chunk = audio[chunk_start : chunk_start + chunk_size]
                transcription = self._process_audio_chunk(chunk, sr)
                if transcription:
                    transcriptions.append(transcription)

            # Combine transcriptions
            return " ".join(transcriptions).strip()

        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "max_duration": self.max_duration,
            "target_sampling_rate": self.target_sampling_rate,
            "language": self.language,
        }
