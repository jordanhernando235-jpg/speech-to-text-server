from deep_translator import GoogleTranslator

text = input("Enter text: ")

translated = GoogleTranslator(
    source='auto',
    target='id'
).translate(text)

print("\nTranslated:")
print(translated)