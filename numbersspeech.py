import vosk
from vosk import Model, KaldiRecognizer
import pyaudio
import json


#model = vosk.Model("./model/vosk-model-small-en-us-0.15/")
#model = vosk.Model("./model/vosk-model-en-us-0.22/")
#model = vosk.Model("./model/vosk-model-en-us-daanzu-20200905/")
#model = vosk.Model("./model/model1")
model = Model("./model/model1")

word_list = ["enter", "back space", "terminate", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "double", "triple", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "bulls eye"]
grammar = json.dumps(word_list)


# Create a recognizer
rec = vosk.KaldiRecognizer(model, 16000, grammar)

# Open the microphone stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)

# Specify the path for the output text file
output_file_path = "recognized_text.txt"

# Open a text file in write mode using a 'with' block
with open(output_file_path, "w") as output_file:
    print("Listening for speech. Say 'Terminate' to stop.")
    # Start streaming and recognize speech
    while True:
        data = stream.read(4096)#read in chunks of 4096 bytes
        if rec.AcceptWaveform(data):#accept waveform of input voice
            # Parse the JSON result and get the recognized text
            result = json.loads(rec.Result())
            recognized_text = result['text']
            
            # Write recognized text to the file
            output_file.write(recognized_text + "\n")
            print(recognized_text)
            
            # Check for the termination keyword
            if "terminate" in recognized_text.lower():
                print("Termination keyword detected. Stopping...")
                break

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
p.terminate()

