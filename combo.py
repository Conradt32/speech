import vosk
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyautogui # For simulating keyboard presses


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

 #   print("Listening for speech. Say 'Terminate' to stop.")
    # Start streaming and recognize speech
while True:
        data = stream.read(4096)#read in chunks of 4096 bytes
        if rec.AcceptWaveform(data):#accept waveform of input voice
            # Parse the JSON result and get the recognized text
            result = json.loads(rec.Result())
            recognized_text = result['text']
		

            #print(recognized_text)
	  
	    # Check for enter
            #if "enter" in recognized_text.lower():
		#break  
	    
            if "enter" in recognized_text:
                pyautogui.press('enter')
                print(f"{recognized_text} hit.")
			
            elif "back space" in recognized_text:
                pyautogui.press('backspace')
                print(f"{recognized_text} hit.")

            else:
                #pyautogui.typewrite(recognized_text) # Type the recognized text
                print(f"{recognized_text}")
	    
	    
            
            # Check for the termination keyword
            if "terminate" in recognized_text.lower():
                print("Termination keyword detected. Stopping...")
                break




# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
p.terminate()

