import librosa
from transformers import WhisperForConditionalGeneration, WhisperProcessor


class SpeechToTextWhisperLarge3Turbo:
    """
    A class to handle speech-to-text conversion using Whisper Large 3 Turbo.
    """

    def __init__(self, model_name="openai/whisper-large-v3-turbo"):
        """
        Initialize the Whisper model and processor.
        """
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe speech from an audio file to text.

        Args:
            audio_path (str): Path to the audio file.

        Returns:
            str: Transcribed text.
        """
        # Step 1: Load audio file and check sampling rate
        # Review: Ensure proper error handling for unsupported file formats or corrupted files.
        try:
            audio, original_sr = librosa.load(audio_path, sr=None)
            # Review: Add a check for empty audio data to avoid processing invalid files.
            if len(audio) == 0:
                raise ValueError(f"Audio file '{audio_path}' is empty.")
            if original_sr != 16000:
                # Review: Resampling can introduce artifacts; consider logging this step for debugging.
                audio = librosa.resample(audio, orig_sr=original_sr, target_sr=16000)
                sr = 16000
            else:
                sr = original_sr
        except Exception as e:
            # Review: Provide more specific error messages for debugging.
            raise ValueError(f"Error loading audio file '{audio_path}': {e}")

        # Step 2: Split audio into smaller chunks if it is too long
        # Review: Consider making `max_duration` a configurable parameter for flexibility.
        max_duration = 30  # seconds
        chunk_size = max_duration * sr
        transcriptions = []

        for chunk_start in range(0, len(audio), chunk_size):
            # Review: Add a check to ensure the chunk is not empty before processing.
            chunk = audio[chunk_start : chunk_start + chunk_size]
            if len(chunk) == 0:
                continue

            # Step 3: Preprocess the audio chunk into input features
            # Review: Validate the output of the processor to ensure it matches expected dimensions.
            inputs = self.processor(
                chunk, sampling_rate=sr, return_tensors="pt", padding=True
            )
            input_features = inputs.input_features

            # Step 4: Set the language to Chinese
            # Review: Make the language configurable instead of hardcoding "chinese".
            forced_decoder_ids = self.processor.get_decoder_prompt_ids(
                language="chinese", task="transcribe"
            )

            # Step 5: Generate predictions using the model
            # Review: Add a timeout or limit to the generation process to handle edge cases.
            predicted_ids = self.model.generate(
                input_features,
                forced_decoder_ids=forced_decoder_ids,
            )

            # Step 6: Decode the predictions into text
            # Review: Handle cases where decoding might fail or return unexpected results.
            transcriptions.append(
                self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            )

        # Step 7: Combine all chunk transcriptions
        # Review: Trim or clean up the final transcription to remove unnecessary whitespace.
        transcription = " ".join(transcriptions)

        return transcription
