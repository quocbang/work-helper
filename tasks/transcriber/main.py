# from tasks.transcriber.openai.openai import SpeechToTextWhisperLarge3Turbo
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from tasks.transcriber.langchian.whisper_large_v3_turbo import WhisperLarge3Turbo


def main():
    print("Transcribing audio file...")
    # Initialize the SpeechToTextWhisperLarge3Turbo class
    # transcriber = SpeechToTextWhisperLarge3Turbo()
    # text = transcriber.transcribe(
    #     "/Users/teq-quocbang/go/src/github.com/quocbang/work-helper/tasks/transcriber/output_audio.wav"
    # )
    # print(text)
    # Initialize the Whisper model

    whisper_llm = WhisperLarge3Turbo(
        model_name="openai/whisper-large-v3-turbo", max_duration=30, language="chinese"
    )

    # Create a prompt template
    template = """
    Transcribe the audio file at this path:
    {audio_path}
    """

    prompt = PromptTemplate(input_variables=["audio_path"], template=template)

    # Create the chain
    chain = LLMChain(llm=whisper_llm, prompt=prompt)

    # Use the chain
    audio_path = "/Users/teq-quocbang/go/src/github.com/quocbang/work-helper/tasks/transcriber/output_audio.wav"
    result = chain.run(audio_path=audio_path)
    print("Transcription:", result)

    # Alternative direct usage
    transcription = whisper_llm._call(audio_path)
    print("Direct transcription:", transcription)


if __name__ == "__main__":
    main()
