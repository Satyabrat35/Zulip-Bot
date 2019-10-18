from googletrans import Translator


def translate_message(msg):
    result = ""
    translator = Translator()
    data = translator.translate(msg)
    if(data.text):
        result += "**Text** : "+data.text
        result += '\n'
    if(data.pronunciation):
        result += "**Pronunciation** : "+data.pronunciation
    if((data.text==None) and (data.pronunciation==None)):
        result += "Couldn't translate :("
    return result

