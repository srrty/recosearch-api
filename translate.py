from googletrans import Translator

translator = Translator()

def translate_to_korean(text):
    translated = translator.translate(text, dest='ko')
    return translated.text
