import base64
import sys
from threading import Lock, Thread

import cv2
from cv2 import VideoCapture
import numpy as np
from speech_recognition import (
    Microphone,
    Recognizer,
    UnknownValueError,
)
from AppKit import NSSpeechSynthesizer
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from pyaudio import PyAudio, paInt16

load_dotenv()


class WebcamStream:
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        if not self.stream.isOpened():
            print("Error: Could not access webcam.")
            print("Please grant camera permissions in System Settings > Privacy & Security > Camera")
            sys.exit(1)
            
        self.grabbed, self.frame = self.stream.read()
        if not self.grabbed or self.frame is None:
            print("Error: Failed to get frame from webcam.")
            print("Please check your camera connection and permissions.")
            sys.exit(1)
            
        self.running = False
        self.lock = Lock()
        self.thread = None

    def start(self):
        self.running = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True  # Make thread daemon so it exits when main thread exits
        self.thread.start()
        return self

    def update(self):
        while self.running:
            grabbed, frame = self.stream.read()
            if grabbed:
                with self.lock:
                    self.frame = frame

    def read(self, encode=False):
        with self.lock:
            if self.frame is None:
                return None
            if encode:
                _, buffer = cv2.imencode(".jpg", self.frame)
                return base64.b64encode(buffer).decode("utf-8")
            return self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)  # Wait up to 1 second for thread to finish
        if self.stream is not None:
            self.stream.release()


class Assistant:
    def __init__(self, model=None):
        self.recognizer = Recognizer()
        self.microphone = Microphone()
        
        # Initialize NSSpeechSynthesizer
        self.synthesizer = NSSpeechSynthesizer.alloc().init()
        self.synthesizer.setRate_(175)  # Set speech rate (default is 175)
        self.synthesizer.setVolume_(0.8)  # Set volume (0.0 to 1.0)
        
        # Set voice to Samantha
        self.synthesizer.setVoice_("com.apple.speech.synthesis.voice.daniel")
        
        self.chain = self._create_inference_chain(model)
        self.is_listening = False

    def listen(self):
        """Listen for a single voice command"""
        if self.is_listening:
            print("Already listening! Please wait...")
            return
            
        try:
            self.is_listening = True
            print("\nListening... Speak your command!")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5.0, phrase_time_limit=15.0)
                
            print("Processing your command...")
            try:
                text = self.recognizer.recognize_whisper(audio, model="base", language="english")
                print(f"You said: {text}")
                return text
            except UnknownValueError:
                print("Sorry, I couldn't understand that.")
                return None
            
        except Exception as e:
            print(f"Error while listening: {e}")
            return None
        finally:
            self.is_listening = False

    def answer(self, prompt, image=None):
        """Generate and speak a response"""
        if not prompt:
            return
            
        try:
            print("Generating response...")
            response = self.chain.invoke(
                {"prompt": prompt, "image_base64": image},
                config={"configurable": {"session_id": "unused"}},
            ).strip()
            
            print("Assistant:", response)
            self._tts(response)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            self._tts("I'm sorry, I encountered an error while processing your request.")

    def _tts(self, response):
        """Convert text to speech using NSSpeechSynthesizer"""
        try:
            if self.synthesizer.isSpeaking():
                self.synthesizer.stopSpeaking()
            self.synthesizer.startSpeakingString_(response)
            
            # Wait for speech to complete
            while self.synthesizer.isSpeaking():
                continue
                
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are a passionate baseball stats guru and analyst who lives and breathes America's favorite pastime. 
        You'll use chat history, images, and available tools to provide insightful baseball analysis and stats.
        
        Your knowledge covers:
        - MLB historical and current statistics
        - Player performance metrics and comparisons
        - Team records and achievements
        - Baseball strategies and analytics
        - Game situations and rules
        
        Keep your responses concise but informative. Talk like a true baseball insider - use common baseball 
        terminology but avoid being too technical. Feel free to throw in classic baseball expressions when appropriate.
        
        Remember:
        - Stick to baseball-related queries only
        - Use provided tools and data to support your analysis
        - Reference chat history for context
        - Analyze any baseball-related images shared
        - Be direct and to the point, but maintain that ballpark enthusiasm
        
        You're like the veteran scout in the press box - knowledgeable, approachable, and always ready 
        to dive into the numbers and share insights about the game.
        """
        

        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{image_base64}",
                        },
                    ],
                ),
            ]
        )

        chain = prompt_template | model | StrOutputParser()

        chat_message_history = ChatMessageHistory()
        return RunnableWithMessageHistory(
            chain,
            lambda _: chat_message_history,
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )


if __name__ == "__main__":
    webcam_stream = None
    stop_listening = None
    
    try:
        # Initialize the webcam stream
        webcam_stream = WebcamStream()
        webcam_stream.start()

        # Initialize the assistant
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
        assistant = Assistant(model)

        recognizer = Recognizer()
        microphone = Microphone()
        
        # Initialize microphone
        print("Initializing microphone...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
        print("Microphone initialized!")

        def audio_callback(recognizer, audio):
            try:
                if not assistant.is_listening:  # Only process if not in manual listening mode
                    prompt = recognizer.recognize_whisper(audio, model="base", language="english")
                    print(f"Recognized: {prompt}")
                    assistant.answer(prompt, webcam_stream.read(encode=True))
            except UnknownValueError:
                print("There was an error processing the audio.")
            except Exception as e:
                print(f"Error in audio callback: {e}")

        print("Starting background listener...")
        stop_listening = recognizer.listen_in_background(microphone, audio_callback)
        print("Background listener started!")
        print("\nPress Ctrl+C to exit or 'q' to quit")

        while True:
            frame = webcam_stream.read()
            if frame is None:
                print("Error: No frame available from webcam")
                break
                
            cv2.imshow("webcam", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('r'):
                # Manual recording mode
                prompt = assistant.listen()
                if prompt:
                    assistant.answer(prompt, webcam_stream.read(encode=True))
                    
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        print("Cleaning up resources...")
        if stop_listening:
            stop_listening(wait_for_stop=False)
        if webcam_stream:
            webcam_stream.stop()
        cv2.destroyAllWindows()
        print("Cleanup complete!")
