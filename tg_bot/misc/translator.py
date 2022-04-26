from googletrans import Translator

def trans(origin_text: str) -> str:
    return Translator().translate(origin_text, dest='ru', src='en').text