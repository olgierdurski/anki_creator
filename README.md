# 🎴 Anki Cards Generator

Anki is a highly effective learning application built on the principles of spaced repetition and active recall. This script automates the monotonous task of manually searching for dictionary definitions, phonetic transcriptions (IPA), and audio pronunciation recordings. 

The tool accepts a simple text file containing a list of words and outputs a fully formatted Anki deck, ready for immediate import. Originally created as a personal solution to the tedious process of preparing flashcards for learning Spanish and English, it has already been used to generate over **5,000 flashcards**. 
It operates on the uk's english pronunciation standard.

---

## 🛠 Project Structure

The script is divided into two major components:

1.  **Dataframe Preparation:** The logic engine that cleans raw input and scrapes linguistic metadata.
2.  **Deck Generation:** The module that converts the processed data into an `.apkg` file.

### Input Specification
The script requires a word list containing terms in their most basic (lemmatised) form:
* `transiented` ➔ `transient`
* `a cat` ➔ `cat`

### Output Specification
The final output is a ready-to-import Anki `.apkg` file containing:
* **Dictionary Definitions:** Primary meanings and context.
* **Phonetic Transcriptions:** IPA using Modern British Received Pronunciation (RP) /mɒd.ən rɪˈsiːvd prəˌnʌn.siˈeɪ.ʃən/.
* **Example Sentences:** Authentic usage examples.
* **Audio Recordings:** High-quality pronunciation files.

---

## 📈 Current Development

The primary focus for future updates is improving the **Dataframe Preparation** module. 

Currently, the quality of the initial input is essential for successful scraping. I am working on enhancing the script to handle **non-standard queries** to the Cambridge Dictionary (e.g., automatically handling redirects, inflections, and multi-word expressions) to make the pre-processing phase more robust and user-friendly. Another problem is creating audio as edge-tts package sometimes generates recordings with incorrect pronunciation.

---

## 🚀 Usage

1.  **Prepare List:** Place your terms in a basic text file.
2.  **Process Data:** Run the script to fetch metadata and populate the internal DataFrame.
3.  **Export:** Generate the `.apkg` file.
4.  **Import:** Open Anki and import the generated deck.

---

