from gtts import gTTS

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='tr')
    tts.save(filename)
