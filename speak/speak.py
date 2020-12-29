#import libraries
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

#import user libraries
from util.constant import Constant
from core.alice_info import Alice
from core.master_info import Master

# Text - to - speech: Chuyển đổi văn bản thành giọng nói
def speak(text):
    if(len(text.split(' ')) > 100):
        print(Alice.name + ": {}".format(text))
        text = 'Master xem nội dung bên trên nhé!'

    print(Alice.name + ": {}".format(text))
    tts = gTTS(text=text, lang=Constant.LANGUAGE, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")
    time.sleep(2)

# Speech - to - text: Chuyển đổi giọng nói bạn yêu cầu vào thành văn bản hiện ra khi máy trả lại kết quả đã nghe
def get_audio():
    print(Alice.name + ": \tĐang nghe \t --__-- ")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nMaster: ", end='')
        audio = r.listen(source, phrase_time_limit=3)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            print("...")
            return 0
    
def listen():
    text = get_audio()
    if text:
        return text.lower()
    else:
        return 0

def get_text():
    text = input('\n' + Master.name + ':')
    return text

def stop():
    speak("Hẹn gặp lại " + Master.name)
    time.sleep(1)