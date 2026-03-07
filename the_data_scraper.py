from bs4 import BeautifulSoup
import requests
from soupsieve.util import lower
import edge_tts
import asyncio
import edge_tts
import os
import re


##The code below was mostly created by AI, it was only implemented and adjusted accordingly to my needs





def scrape_cambridge_dictionary(query):

    query = query.lower().strip()

    url_query = query.replace(' ', '-')
    url = f"https://dictionary.cambridge.org/dictionary/english/{url_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page. HTTP Status: {response.status_code} for {query}")
        return None, None, None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. Phonetic form - IPA
    ipa_nodes = soup.select('.uk .ipa')

    if ipa_nodes:
        ipa = ipa_nodes[0].text.strip()
        ipa = f"/{ipa}/"
    else:
        words = query.split()
        if len(words) > 1:
            return scrape_cambridge_dictionary(words[0])
        else:
            return None, None, None, None, None

    # 2. Definition
    def_nodes = soup.select('.def.ddef_d')
    definition = def_nodes[0].text.strip() if def_nodes else None

    # 3. Example sentence
    ex_nodes = soup.select('.eg.deg')
    example = ex_nodes[0].text.strip() if ex_nodes else None

    # 5. File name
    file_name = f"{query.replace(' ', '_')}_uk.mp3"
    return query, definition, ipa, file_name, example



async def process_single_word(word, save_directory):
    voice = "en-GB-SoniaNeural"
    word_str = str(word)

    safe_text = re.sub(r'[\\/*?:"<>|]', "", word_str).strip()
    filename = f"{safe_text.replace(' ', '_')}_uk.mp3"
    file_path = os.path.join(save_directory, filename)

    try:
        communicate = edge_tts.Communicate(word_str, voice)
        await communicate.save(file_path)
        print(f"Success: '{word_str}' saved.")
    except Exception as e:
        print(f"Error for '{word_str}': {e}")


#Main function that  manages creating the recordings
async def create_audio(words, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    #Task list
    tasks = [process_single_word(word, save_directory) for word in words]

    #simultaneously realizing the task defined above
    await asyncio.gather(*tasks)


