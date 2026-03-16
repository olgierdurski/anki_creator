import asyncio
import genanki
import pandas as pd
from the_data_scraper import scrape_cambridge_dictionary, create_audio


#Deck creation - deck_id should be unique
my_deck = genanki.Deck(2051478910, "Eng")
my_package = genanki.Package(my_deck)

##CSS code to customize the cards - 95% AI generated!!!
##Html and css parts of the code below are mostly AI generated!
style_listening = """
/* 1. Base Card Style */
.card {
    font-family: "Segoe UI", Tahoma, sans-serif;
    font-size: 23px;
    text-align: center;
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

"""

style_cloze = """
/* 1. STYL OGÓLNY KARTY */
.card {
    font-family: "Segoe UI", Tahoma, sans-serif;
    font-size: 23px;
    text-align: center;
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


#Declaration of 2 different types of flashcards:
model_listening = genanki.Model(
          212134552,
          'Model recording to definition',
          #Fields of the flashcard
          fields=[
            {'name': 'MyMedia'},
            {'name': 'Definition'},
            {'name': 'Ipa'},

          ],
          #Ordering the fields into desired combination
          templates=[
            {
              'name': 'Card sound_practice',
              #Przednia strona - plik dzwiekowy
              'qfmt': '{{MyMedia}}',

              #Tylnia strona - definicja i IPA
              'afmt': '{{FrontSide}}<hr><div id="ipa">{{Ipa}}</div><hr><div id="definition">{{Definition}}</div>',
            }

          ],
            #Defining visual aspect
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

          templates=[
            {
              'name': 'Card cloze',

                #Front side
                'qfmt': '{{Example}}<span id="definition">{{Definition}}</span><hr>',

                #Back side
                'afmt': '''
              {{FrontSide}}
              <div id="answer-container">
                  <span id="word">{{Word}}</span>
                  <span id="ipa">{{Ipa}}</span>
              </div>
              ''',
            }
          ],
    css=style_cloze
)


#Basically a loop that organizes all the elements into ready anki flashcard
def create_deck_file(deck_file_name, word_list):
    lista = word_list
    recordings_files = []

    for index, row in lista.iterrows():
        word = row["Word"]
        definition = row["Definition"]
        recording = row["Recording"]
        ipa = row["Ipa"]


        if pd.isna(definition) or ipa == "/None/":
            continue
        example = cloze_creator(str(row["Example"]), word)

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
    my_package.write_to_file(f"{deck_file_name}.apkg")

#String operation required to create html code for cloze card type
def cloze_creator(sentence, word):
        return sentence.replace(word, "______")


#The function takes a raw DataFrame of words and appends the definition, IPA, audio recording, and an example sentence for each word from the Cambridge Dictionary.
def prepare_word_list(word_list):
    word_list = word_list
    full_word_list = pd.DataFrame(columns = ["Word", "Definition", "Ipa", "Recording", "Example"])
    for current_row in range(0, len(word_list)):
        current_word = word_list.iloc[current_row, 0]

        #Scraping data from the dictionary
        word, definition, ipa, recording_file_name, example = scrape_cambridge_dictionary(current_word)

        #Assiging the elements
        full_word_list.loc[current_row, ["Word", "Definition", "Ipa", "Recording", "Example"]] = [word, definition, ipa, recording_file_name, example]

        #Creating audio file to the chosen directory - "path" shall be the directory location

    asyncio.run(create_audio(full_word_list["Word"], r"./audio_files"))

    full_word_list.to_excel(r"word_lists/updated.xlsx")
    return full_word_list



if __name__ == "__main__":
    imported_word_list = pd.read_excel(r"word_lists/updated.xlsx")
    create_deck_file("ready_to_import.apkg", imported_word_list)





