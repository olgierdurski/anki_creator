from bs4 import BeautifulSoup
import requests
import os
from soupsieve.util import lower


##The code below was mostly created by AI, it was only implemented and adjusted accordingly to my needs


def scrape_cambridge_dictionary(word):

    word = lower(word).strip()
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to retrieve page. HTTP Status: {response.status_code}"}

    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. Phonetic form - IPA
    ipa_nodes = soup.select('.uk .ipa')
    ipa = ipa_nodes[0].text.strip() if ipa_nodes else None
    ipa = f"/{ipa}/"
    # 2. Definition
    def_nodes = soup.select('.def.ddef_d')
    definition = def_nodes[0].text.strip() if def_nodes else None

    # 3. Example sentence
    ex_nodes = soup.select('.eg.deg')
    example = ex_nodes[0].text.strip() if ex_nodes else None

    # 4. Voice recording
    audio_nodes = soup.select('.uk audio source[type="audio/mpeg"]')
    audio_url = None
    if audio_nodes and 'src' in audio_nodes[0].attrs:
        audio_url = f"https://dictionary.cambridge.org{audio_nodes[0]['src']}"

    # 5. File name
    file_name = f"{word}_uk.mp3"
    return word, definition, ipa, file_name, example, audio_url


def download_audio(audio_url, filename, save_directory):

    #Downloads the audio into pointed location
    if not audio_url:
        print("Error: No audio URL provided.")
        return False

    # Create the target directory if it does not already exist
    os.makedirs(save_directory, exist_ok=True)

    file_path = os.path.join(save_directory, filename)

    # A User-Agent is required to prevent the download request from being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(audio_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Success: Audio saved to {file_path}")
        return True
    else:
        print(f"Error: Failed to download audio. HTTP Status: {response.status_code}")
        return False
