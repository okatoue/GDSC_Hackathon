from dotenv import load_dotenv
import logging, verboselogs
from time import sleep

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()


def main():
    try:
        deepgram = DeepgramClient("c254b94530fcfc64076e6d850f0c61d536ff5098")
        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            for channel in result.channel.alternatives:   # Iterate through channels
                for transcript in channel.transcript:  # Iterate over transcripts
                     for word in transcript.words:       # Iterate over words
                        print(f"speaker: {word.punctuated_word}")  # Print each word

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


if __name__ == "__main__":
    main()