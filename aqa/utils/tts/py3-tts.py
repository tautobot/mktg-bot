import pyttsx3

vietnamese = None
voice_id = None
engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty('rate')  # getting details of current speaking rate
print(rate)  # printing current voice rate
engine.setProperty('rate', 182)  # setting up new voice rate
rate = engine.getProperty('rate')  # getting details of current speaking rate
print(rate)  # printing current voice rate
#
"""VOLUME"""
volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
print(volume)  # printing current volume level
engine.setProperty('volume', 0.8)  # setting up volume level  between 0 and 1
volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
print(volume)  # printing current volume level

#
# """VOICE"""
# voices = engine.getProperty('voices')  # getting details of current voice
# # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

for voice in engine.getProperty('voices'):
    if 'vi' in voice.languages[0]:
        print(voice)
        vietnamese = voice.languages[0]
        voice_id = voice.id

engine.setProperty('voice', 'com.apple.voice.enhanced.vi-VN.Linh')
# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

change_voice(engine, vietnamese, "VoiceGenderFemale")
engine.say("Khi Bellingham rời sân ở phút 86, <break time='1s'/> nhường vị trí cho Kobbie Mainoo, <break time='1s'/> khán giả tuyển Anh đồng loạt đứng dậy vỗ tay tán thưởng tiền vệ số 10. <break time='3s'> Không chỉ ghi bàn duy nhất, break time='1s'> anh còn chơi xông xáo, break time='1s'> liên tiếp bị phạm lỗi và cũng khiêu khích đối thủ. break time='3s'> Tài năng của tiền vệ CLB Real Madrid là điểm khác biệt của trận cầu khan hiếm cơ hội, break time='1s'> khi mỗi đội chỉ dứt điểm năm lần.")
engine.runAndWait()
engine.stop()
