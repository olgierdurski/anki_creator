from warnings import catch_warnings

import genanki
import pandas as pd
from the_data_scraper import scrape_cambridge_dictionary, download_audio

#Utworzenie tali
my_deck = genanki.Deck(2051478910, "ANG")
my_package = genanki.Package(my_deck)

#Deklaracja modeli - struktury fiszek:
model_listening = genanki.Model(
          212634552,
          'Model recording to definition',
          #Definiuje pola na fiszce
          fields=[
            {'name': 'MyMedia'},
            {'name': 'Definition'},
            {'name': 'Ipa'},

          ],
          #Układam pola w układzie jaki mi pasuje
          templates=[
            {
              'name': 'Card sound_practice',
              #Przednia strona - plik dzwiekowy
              'qfmt': '{{MyMedia}}',

              #Tylnia strona - definicja i IPA
              'afmt': '{{FrontSide}}<hr id="ipa">{{Ipa}}<hr id="definition">{{Definition}}',
            },
          ])

model_cloze = genanki.Model(
          9126562512,
          'Model sentence to word',

          fields=[
            {'name': 'Example'},
            {'name': 'Definition'},
            {'name': 'Ipa'},
            {'name': 'Word'},
            {'name': 'emptystring'}

          ],
          #Układam pola w układzie jaki mi pasuje
          templates=[
            {
              'name': 'Card cloze',
              #Przednia strona
              'qfmt': '{{cloze:Example}}<hr id="definition">{{Definition}}',
                #Tylnia strona
              'afmt': '{{FrontSide}}<br id="word">{{Word}}<hr id="ipa">{{Ipa}}',
            }
          ],
        model_type=genanki.Model.CLOZE
)


#wygenerowanie fiszki - petla - potrzebuje string string oraz nazwa pliku
def create_deck_file(deck_file_name, word_list):
    lista = word_list
    recordings_files = []

    for index, row in lista.iterrows():
        word = row["Word"]
        definition = row["Definition"]
        recording = row["Recording"]
        ipa = row["Ipa"]
        example = cloze_creator(row["Example"], word)


        my_note_recording = genanki.Note(
            model=model_listening,
            fields=[f"[sound:{recording}]",definition, ipa])

        my_deck.add_note(my_note_recording)
        recordings_files.append(f'audio_files/{recording}')

        my_note_cloze = genanki.Note(
            model=model_cloze,
            fields=[example, definition, ipa, word, ""],
        )
        my_deck.add_note(my_note_cloze)

    my_package.media_files = recordings_files
    my_package.write_to_file(f'{deck_file_name}.apkg')

#Supporting function for creating cloze flashcards
def cloze_creator(sentence, word):
        return sentence.replace(word, f"{{{{c1::{word}}}}}")

def prepare_word_list(word_list):
    word_list = word_list
    full_word_list = pd.DataFrame(columns = ["Word", "Definition", "Ipa", "Recording", "Example"])
    for current_row in range(0, len(word_list)):
        current_word = word_list.iloc[current_row, 0]

        #Scraping data from the dictionary
        word, definition, ipa, recording_file_name, example, audio_url = scrape_cambridge_dictionary(current_word)

        #Assiging the elements
        full_word_list.loc[current_row, ["Word", "Definition", "Ipa", "Recording", "Example"]] = [word, definition, ipa, recording_file_name, example]

        #Downloading audio file to the chosen directory
        download_audio(audio_url, recording_file_name, r"path")

    full_word_list.to_excel("updated.xlsx")
    return full_word_list




if __name__ == "__main__":
    imported_word_list = pd.read_excel("lista_slowek.xlsx", header=None)
    full_word_list = prepare_word_list(imported_word_list)
    create_deck_file("testowy.apkg", full_word_list)