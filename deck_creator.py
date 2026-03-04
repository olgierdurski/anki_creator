from warnings import catch_warnings

import genanki
import pandas as pd
from the_data_scraper import scrape_cambridge_dictionary, download_audio

#Utworzenie tali
my_deck = genanki.Deck(2051478910, "ANG")
my_package = genanki.Package(my_deck)

##CSS code to customize the cards
style_listening = """
/* 1. Base Card Style */
.card {
    font-family: "Segoe UI", Tahoma, sans-serif;
    font-size: 23px;
    text-align: center;
    color: #ffffff;
    background-color: #2c2c2c;
    line-height: 1.4;
}

/* 2. IPA - Forced Magenta Colour */
#ipa {
    font-family: "Lucida Sans Unicode", sans-serif;
    font-size: 24px;
    color: #bc3fbc !important; 
    margin-top: 15px;
}

/* 3. Definition - Forced Blue Colour */
#definition {
    font-size: 19px;
    color: #4a90e2 !important;
    font-style: normal;
    margin-top: 10px;
}

/* 4. Separator Lines */
hr {
    display: block;
    border: 0;
    height: 1px;
    background-color: #555;
    margin: 20px 0;
}

/* Targets strictly the top line to make it thicker */
hr:first-of-type {
    height: 3px;
    background-color: #666; /* Slightly lighter to stand out */
}

/* 5. Playback Button */
.replay-button svg {
    width: 60px;
    height: 60px;
}
.replay-button svg circle {
    fill: #2980b9;
}
.replay-button svg path {
    fill: #ffffff;
}

/* 6. Night Mode Background Fix */
.nightMode.card {
    background-color: #1c1c1c;
    color: #ffffff;
}
"""

style_cloze = """
/* 1. STYL OGÓLNY KARTY */
.card {
    font-family: "Segoe UI", Tahoma, sans-serif;
    font-size: 23px;
    text-align: center;
    color: #ffffff;           /* ZDANIE BIAŁE (Domyślne dla całej karty) */
    background-color: #2c2c2c; /* CIEMNE TŁO */
    line-height: 1.4;
}

/* 2. STYL DLA LUKI [...] */
.cloze {
    font-weight: bold;
    color: #ffffff;           /* LUKA RÓWNIEŻ BIAŁA */
}

/* 3. PODPOWIEDŹ NIEBIESKA (Definicja) */
#definition {
    font-size: 19px;      
    color: #4a90e2;
    display: block;      
    margin-top: 5px;    
}

/* 4. ODPOWIEDŹ RÓŻOWA (Słowo + IPA) */
#answer-container {
    margin-top: 25px;    
    font-size: 24px;
    color: #bc3fbc; 
}

#ipa {
    font-family: "Lucida Sans Unicode", sans-serif;
    margin-left: 12px;
}

/* 5. TRYB NOCNY - Utrzymanie bieli dla zdania */
.nightMode.card {
    background-color: #1c1c1c; /* Głębsza czerń */
    color: #ffffff !important; /* WYMUSZA BIAŁE ZDANIE */
}

.nightMode #definition {
    color: #4a90e2;           /* Utrzymujemy ten sam niebieski */
}

/* Odpowiedź w trybie nocnym pozostaje różowa */
.nightMode #answer-container {
    color: #bc3fbc;
}

/* Opcjonalna linia oddzielająca */
hr {
    border: 0;
    height: 1px;
    background-color: #555;
    margin: 15px 0;
}
"""



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
              'afmt': '{{FrontSide}}<hr><div id="ipa">{{Ipa}}</div><hr><div id="definition">{{Definition}}</div>',
            }

          ],
            css = style_listening)

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
                # Przednia strona (Pytanie)
                'qfmt': """{{cloze:Example}}<span id="definition">{{Definition}}</span><hr>
                <script>
                  var clozeElement = document.querySelector('.cloze');
                  if (clozeElement && clozeElement.innerHTML == "[...]") {
                    clozeElement.innerHTML = "____";
                  }
                </script>""",

                # Tylna strona (Odpowiedź)
                'afmt': '''
              {{FrontSide}}
              <div id="answer-container">
                  <span id="word">{{Word}}</span>
                  <span id="ipa">{{Ipa}}</span>
              </div>
              ''',
            }
          ],
        model_type=genanki.Model.CLOZE,
    css=style_cloze
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




#if __name__ == "__main__":
    #imported_word_list = pd.read_excel("lista_slowek.xlsx", header=None)
    #full_word_list = prepare_word_list(imported_word_list)
    #create_deck_file("testowy.apkg", full_word_list)

if __name__ == "__main__":
    create_deck_file("ouput.apkg", pd.read_excel("updated.xlsx"))