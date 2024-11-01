#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import codecs

import requests
from bs4 import BeautifulSoup
import pickle

class Label:
    FUTURE_TENSE: str = 'future_tense'
    PAST_TENSE: str = 'past_tense'
    PRESENT_TENSE: str = 'present_tense'
    IMPERATIVE: str = 'imperative'
    INFINITIVE: str = 'infinitive'
    MASCULINE_SINGULAR: str = 'masculine_singular'
    FEMININE_SINGULAR: str = 'feminine_singular'
    MASCULINE_PLURAL: str = 'masculine_plural'
    FEMININE_PLURAL: str = 'feminine_plural'
    SINGULAR_1ST_PERSON: str = 'singular_1st_person'
    PLURAL_1ST_PERSON: str = 'plural_1st_person'
    SINGULAR_2ND_PERSON_FEMALE: str = 'singular_2nd_person_female'
    SINGULAR_2ND_PERSON_MALE: str = 'singular_2nd_person_male'
    SINGULAR_3RD_PERSON_FEMALE: str = 'singular_3rd_person_female'
    SINGULAR_3RD_PERSON_MALE: str = 'singular_3rd_person_male'
    PLURAL_2ND_PERSON_FEMALE: str = 'plural_2nd_person_female'
    PLURAL_2ND_PERSON_MALE: str = 'plural_2nd_person_male'
    PLURAL_3RD_PERSON_FEMALE: str = 'plural_3rd_person_female'
    PLURAL_3RD_PERSON_MALE: str = 'plural_3rd_person_male'



def _get_word_links(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {page_url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    toc = {}

    # Find the table with the class 'dict-table-t'
    table = soup.find('table', {'class': 'dict-table-t'})
    if not table:
        raise Exception("Dictionary table not found")

    for row in table.find_all('tr'):
        first_td = row.find('td')
        if not first_td:
            continue
        a_tag = first_td.find('a', href=True)
        if not a_tag:
            print('NO A TAG FOUND!')
            continue
        links.append(a_tag['href'])
        menakud_tag = a_tag.find('div').find('div').find('span')
        if not menakud_tag:
            print('NO menakud TAG FOUND!')
            continue
        toc[menakud_tag.text] = {
            'link': a_tag['href'],
            'menakud': menakud_tag.text
        }
        dict_toc = toc[menakud_tag.text]
        transcription_tag = first_td.find('span', {'class': 'dict-transcription'})
        if transcription_tag:
            dict_toc['transcription'] = transcription_tag.text

        # Get root
        root_td = first_td.find_next('td')
        if root_td:
            root_a_tag = root_td.find('a', href=True)
            if root_a_tag:
                dict_toc['root'] = root_a_tag.text
            else:
                dict_toc['root'] = root_td.text

        # Get part of speech
        part_of_speech_td = root_td.find_next('td')
        dict_toc['part_of_speech'] = part_of_speech_td.text

        # Get meaning
        meaning_td = part_of_speech_td.find_next('td')
        dict_toc['meaning'] = meaning_td.text

        toc[dict_toc['menakud']] = dict_toc
    return toc


def read_and_print_file(file_path):
    try:
        with codecs.open(file_path, 'rb') as f:
            content = f.read()
            result = json.loads(content)
        for k, v in result.items():
            print(f'{k}: {v}')
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_words(file_path):
    word_list = {}
    try:
        for i in range(1, 610):  # 610
            print(i)
            page_url = f"https://www.pealim.com/dict/?page={i}"
            word_list.update(_get_word_links(page_url))
    except Exception as e:
        print(e)
    for k, v in word_list.items():
        print(f'{k}: {v}')
    with codecs.open(file_path, "wb", encoding='utf-8') as f:
        json.dump(word_list, f, ensure_ascii=False)
    print(f'Word links saved to {file_path}')

def _fetch_verb(url) -> dict:
    def _extract_details(cell):
        result = {
            'menakud': cell.find('span', {'class': 'menukad'}).text,
            'transcription': cell.find('div', {'class': 'transcription'}).text,
            'meaning': cell.find('div', {'class': 'meaning'}).text
        }
        return result

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    result = {}
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section containing the active and passive forms
    forms_div = soup.find('div', {'class': 'horiz-scroll-wrapper'})
    tables = forms_div.find_all('table')
    active_tenses = {}

    rows = tables[0].find('tbody').find_all('tr')

    pt_cells = rows[0].find_all('td')
    # Present tense / Participle
    active_tenses[Label.PRESENT_TENSE] = {
        Label.MASCULINE_SINGULAR: _extract_details(pt_cells[0]),
        Label.FEMININE_SINGULAR: _extract_details(pt_cells[1]),
        Label.MASCULINE_PLURAL: _extract_details(pt_cells[2]),
        Label.FEMININE_PLURAL: _extract_details(pt_cells[3])
    }
    # Past Tense
    past_t_1_cells = rows[1].find_all('td')
    past_t_2_cells = rows[2].find_all('td')
    past_t_3_cells = rows[3].find_all('td')
    active_tenses[Label.PAST_TENSE] = {
        Label.SINGULAR_1ST_PERSON: _extract_details(past_t_1_cells[0]),
        Label.PLURAL_1ST_PERSON: _extract_details(past_t_1_cells[1]),
        Label.SINGULAR_2ND_PERSON_MALE: _extract_details(past_t_2_cells[0]),
        Label.SINGULAR_2ND_PERSON_FEMALE: _extract_details(past_t_2_cells[1]),
        Label.PLURAL_2ND_PERSON_MALE: _extract_details(past_t_2_cells[2]),
        Label.PLURAL_2ND_PERSON_FEMALE: _extract_details(past_t_2_cells[3]),
        Label.SINGULAR_3RD_PERSON_MALE: _extract_details(past_t_3_cells[0]),
        Label.SINGULAR_3RD_PERSON_FEMALE: _extract_details(past_t_3_cells[1]),
        Label.PLURAL_3RD_PERSON_MALE: _extract_details(past_t_3_cells[2]),
        Label.PLURAL_3RD_PERSON_FEMALE: _extract_details(past_t_3_cells[2]),
    }
    # Future Tense
    ft_1_cells = rows[4].find_all('td')
    ft_2_cells = rows[5].find_all('td')
    ft_3_cells = rows[6].find_all('td')
    active_tenses[Label.FUTURE_TENSE] = {
        Label.SINGULAR_1ST_PERSON: _extract_details(ft_1_cells[0]),
        Label.PLURAL_1ST_PERSON: _extract_details(ft_1_cells[1]),
        Label.SINGULAR_2ND_PERSON_MALE: _extract_details(ft_2_cells[0]),
        Label.SINGULAR_2ND_PERSON_FEMALE: _extract_details(ft_2_cells[1]),
        Label.PLURAL_2ND_PERSON_MALE: _extract_details(ft_2_cells[2]),
        Label.PLURAL_2ND_PERSON_FEMALE: _extract_details(ft_2_cells[3]),
        Label.SINGULAR_3RD_PERSON_MALE: _extract_details(ft_3_cells[0]),
        Label.SINGULAR_3RD_PERSON_FEMALE: _extract_details(ft_3_cells[1]),
        Label.PLURAL_3RD_PERSON_MALE: _extract_details(ft_3_cells[2]),
        Label.PLURAL_3RD_PERSON_FEMALE: _extract_details(ft_3_cells[3]),
    }
    # Imperative
    active_tenses[Label.IMPERATIVE] = {
        Label.MASCULINE_SINGULAR: _extract_details(pt_cells[0]),
        Label.FEMININE_SINGULAR: _extract_details(pt_cells[1]),
        Label.MASCULINE_PLURAL: _extract_details(pt_cells[2]),
        Label.FEMININE_PLURAL: _extract_details(pt_cells[3])
    }
    result['active_forms'] = active_tenses
    if len(tables) < 2:
        return result

    # Passive Form
    passive_tenses = {}
    p_rows = tables[1].find('tbody').find_all('tr')

    pt_cells = p_rows[0].find_all('td')
    # Present tense / Participle
    passive_tenses[Label.PRESENT_TENSE] = {
        Label.MASCULINE_SINGULAR: _extract_details(pt_cells[0]),
        Label.FEMININE_SINGULAR: _extract_details(pt_cells[1]),
        Label.MASCULINE_PLURAL: _extract_details(pt_cells[2]),
        Label.FEMININE_PLURAL: _extract_details(pt_cells[3])
    }
    # Past Tense
    past_t_1_cells = p_rows[1].find_all('td')
    past_t_2_cells = p_rows[2].find_all('td')
    past_t_3_cells = p_rows[3].find_all('td')
    passive_tenses[Label.PAST_TENSE] = {
        Label.SINGULAR_1ST_PERSON: _extract_details(past_t_1_cells[0]),
        Label.PLURAL_1ST_PERSON: _extract_details(past_t_1_cells[1]),
        Label.SINGULAR_2ND_PERSON_MALE: _extract_details(past_t_2_cells[0]),
        Label.SINGULAR_2ND_PERSON_FEMALE: _extract_details(past_t_2_cells[1]),
        Label.PLURAL_2ND_PERSON_MALE: _extract_details(past_t_2_cells[2]),
        Label.PLURAL_2ND_PERSON_FEMALE: _extract_details(past_t_2_cells[3]),
        Label.SINGULAR_3RD_PERSON_MALE: _extract_details(past_t_3_cells[0]),
        Label.SINGULAR_3RD_PERSON_FEMALE: _extract_details(past_t_3_cells[1]),
        Label.PLURAL_3RD_PERSON_MALE: _extract_details(past_t_3_cells[2]),
        Label.PLURAL_3RD_PERSON_FEMALE: _extract_details(past_t_3_cells[2]),
    }
    # Future Tense
    ft_1_cells = p_rows[4].find_all('td')
    ft_2_cells = p_rows[5].find_all('td')
    ft_3_cells = p_rows[6].find_all('td')
    passive_tenses[Label.FUTURE_TENSE] = {
        Label.SINGULAR_1ST_PERSON: _extract_details(ft_1_cells[0]),
        Label.PLURAL_1ST_PERSON: _extract_details(ft_1_cells[1]),
        Label.SINGULAR_2ND_PERSON_MALE: _extract_details(ft_2_cells[0]),
        Label.SINGULAR_2ND_PERSON_FEMALE: _extract_details(ft_2_cells[1]),
        Label.PLURAL_2ND_PERSON_MALE: _extract_details(ft_2_cells[2]),
        Label.PLURAL_2ND_PERSON_FEMALE: _extract_details(ft_2_cells[3]),
        Label.SINGULAR_3RD_PERSON_MALE: _extract_details(ft_3_cells[0]),
        Label.SINGULAR_3RD_PERSON_FEMALE: _extract_details(ft_3_cells[1]),
        Label.PLURAL_3RD_PERSON_MALE: _extract_details(ft_3_cells[2]),
        Label.PLURAL_3RD_PERSON_FEMALE: _extract_details(ft_3_cells[3]),
    }
    result['passive_forms'] = passive_tenses

    return result


def fetch_conjugates(from_file_path):
    result = {}
    # url = 'https://www.pealim.com/dict/58-leabed/'
    base_url = 'https://www.pealim.com'
    with codecs.open(from_file_path, 'rb') as f:
        content = f.read()
        word_list = json.loads(content)
    for k, v in word_list.items():
        try:
            url = f"{base_url}{v['link']}"
            if v['part_of_speech'].startswith('Verb'):
                print(f'Fetching verb for {k} from {url}')
                conjugate = _fetch_verb(url)
                result[k] = conjugate
                result[k].update(v)
                result[k]['word_type'] = 'verb'
                result[k]['word_pattern'] = v['part_of_speech'].split(' – ')[1]
        except Exception as e:
            print(f'ERROR: {k}-{v['link']}: {e}')
    with codecs.open('verbs.dat', 'wb', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
    print(result)

if __name__ == "__main__":
    file_path = 'word_links.dat'
    #fetch_words(file_path)
    #read_and_print_file(file_path)
    fetch_conjugates(file_path)
