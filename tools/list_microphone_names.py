import speech_recognition as sr


microphone_names = sr.Microphone.list_microphone_names()
for i in range(len(microphone_names)):
    name = microphone_names[i]
    print(i, name)
