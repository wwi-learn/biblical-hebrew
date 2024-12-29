'''
Morphology mapped to the format as per: https://www.blueletterbible.org/resources/morphology/hebrew-codes.cfm
Words extracted from: https://openbible.com
Format of morphology: https://biblehub.com/hebrewparse.htm
'''
import re

import requests
from bs4 import BeautifulSoup

from wwi.db import Word, VerseWord, get_session, WordMorphology, AddedVerse


def extract_root(strongs_number: str):
    url = f'https://openbible.com/strongs/hebrew/{strongs_number}.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    root = soup.find('span', class_='hebrew').text.strip()
    # Define a regular expression pattern to match Hebrew vowel markings
    vowel_markings_pattern = re.compile(r'[\u0591-\u05C7]')
    # Remove the vowel markings from the Hebrew word
    cleaned_word = re.sub(vowel_markings_pattern, '', root)
    return cleaned_word


def _process_morphology(morphology: str):
    result = []
    morph_raw_parts = morphology.split('\xa0')
    morphology_processed = morph_raw_parts[1] if len(morph_raw_parts) > 1 else morphology
    parts_raw = morphology_processed.split(' | ')
    parts = []
    for p in parts_raw:
        parts_parts = p.split(', ')
        parts.extend(parts_parts)
    for ix, p in enumerate(parts):
        p_parts = p.split('-')
        part_of_speech = p_parts[0]
        morphology_part = {'index': ix, 'part_of_speech': part_of_speech}
        if part_of_speech in 'Conj':
            if len(p_parts) == 2:
                morphology_part['type'] = p_parts[1]
        elif part_of_speech == 'Prep':
            if len(p_parts) == 2:
                morphology_part['type'] = p_parts[1]
        elif part_of_speech == 'Art':
            assert len(p_parts) == 1
        elif part_of_speech == 'DirObjM':
            assert len(p_parts) == 1
        elif part_of_speech == 'Adv':
            if len(p_parts) == 2:
                morphology_part['type'] = p_parts[1]
        elif part_of_speech == 'Pro' or part_of_speech.startswith(('1', '2', '3')):
            morphology_part['part_of_speech'] = 'suffix'
            if len(p_parts) == 1:
                morphology_part['word_type'] = 'p'
                assert len(p_parts[0]) in (3,4)
                if len(p_parts[0]) == 4:
                    assert p_parts[0][3] in ('e', '2'), morphology
                morphology_part['person'] = p_parts[0][0]
                morphology_part['gender'] = p_parts[0][1]
                morphology_part['number'] = p_parts[0][2]
            if len(p_parts) == 2:
                morphology_part['word_type'] = p_parts[1]
                if part_of_speech.startswith(('1', '2', '3')):
                    morphology_part['word_type'] = 'p'
                    morphology_part['person'] = p_parts[1][0]
                    morphology_part['gender'] = p_parts[1][1]
                    morphology_part['number'] = p_parts[1][2]
                else:
                    morphology_part['word_type'] = p_parts[1]
                morphology_part['word_type'] = 'p'
                assert len(p_parts[0]) == 3
            else:
                morphology_part['word_type'] = 'p'
                assert len(p_parts[0]) in (3,4), morphology
                if len(p_parts[0]) == 4:
                    assert p_parts[0][3] in ('e', '2'), morphology
                morphology_part['person'] = p_parts[0][0]
                morphology_part['gender'] = p_parts[0][1]
                morphology_part['number'] = p_parts[0][2]
        elif part_of_speech == 'Pn':
            morphology_part['part_of_speech'] = 'suffix'
            morphology_part['word_type'] = 'n'
        elif part_of_speech == 'V':
            morphology_part['stems'] = p_parts[1]
            morphology_part['word_type'] = p_parts[2]
            if len(p_parts) > 3:
                if len(p_parts[3]) == 3:
                    morphology_part['person'] = p_parts[3][0]
                    morphology_part['gender'] = p_parts[3][1]
                    morphology_part['number'] = p_parts[3][2]
                elif len(p_parts[3]) == 2:
                    morphology_part['gender'] = p_parts[3][0]
                    morphology_part['number'] = p_parts[3][1]
        elif part_of_speech in ('N', 'Adj', 'Number'):
            if p_parts[1] == 'proper':
                morphology_part['type'] = 'p'
                morphology_part['gender'] = p_parts[2][0]
                morphology_part['number'] = p_parts[2][1]
                if len(p_parts[1]) == 3:
                    morphology_part['state'] = p_parts[2][2]
            elif p_parts[1] == 'g':
                morphology_part['type'] = p_parts[1]
                morphology_part['number'] = p_parts[2][0]
                if len(p_parts[1]) == 2:
                    morphology_part['state'] = p_parts[2][1]
            elif p_parts[1] == 'o':
                morphology_part['type'] = p_parts[1]
                morphology_part['gender'] = p_parts[2][0]
                morphology_part['number'] = p_parts[2][1]
                if len(p_parts[1]) == 3:
                    morphology_part['state'] = p_parts[2][2]
            else:
                morphology_part['gender'] = p_parts[1][0]
                morphology_part['number'] = p_parts[1][1]
                if len(p_parts[1]) == 3:
                    morphology_part['state'] = p_parts[1][2]
        elif part_of_speech in ('I', 'Interrog'):
            pass
        elif part_of_speech == 'Number':
            pass
        elif part_of_speech == 'Punc':
            morphology_part['type'] = part_of_speech
        else:
            print(morphology)
            raise NotImplementedError(f'Unknown morphology part of speech: {part_of_speech}')

        result.append(morphology_part)
        word_type = p_parts[0]
        word_subtype = None
    person = None

    return result

def extract_verse_data(book: str, chapter: int, verse: int):
    url = f'https://openbible.com/text/{book}/{chapter}-{verse}.htm'
    response = requests.get(url)
    if response.status_code == 404:
        return
    soup = BeautifulSoup(response.content, 'html.parser')

    tbl_heading_div = soup.find('div', string='Text Analysis')
    table = tbl_heading_div.find_next('table')
    rows = table.find_all('tr')

    data = []
    for ix, row in enumerate(rows[2:]):  # Skip the header row
        cells = row.find_all('td')
        if len(cells) == 4:
            try:
                hebrew_text = cells[1].contents[0].strip()
            except TypeError:
                continue
            strongs = cells[0].text.strip()
            root = extract_root(strongs) if strongs else None
            translit_text = cells[1].find('span', class_='translit').find('a').text
            english = cells[2].text.strip()
            morphology = _process_morphology(cells[3].text.strip())
            data.append({
                'book': book,
                'chapter': chapter,
                'verse': verse,
                'verse_position': ix,
                'strongs': strongs,
                'root': root,
                'hebrew': hebrew_text,
                'transliteration': translit_text,
                'english': english,
                'morphology': morphology
            })
    return data


def insert_verse_data(session, data):
    for d in data:
        verse_word_data = session.query(VerseWord).filter_by(
            book=d['book'],
            chapter=d['chapter'],
            verse=d['verse'],
            verse_position=d['verse_position']
        ).first()
        if verse_word_data:
            continue

        word_data = session.query(Word).filter_by(root=d['root'], hebrew=d['hebrew']).first()
        if not word_data:
            word_data = Word(
                hebrew=d['hebrew'],
                root=d['root'],
                language='Hebrew',
                strongs=d['strongs'],
                transliteration=d['transliteration']
            )
            session.add(word_data)
            session.commit()
        else:
            print(f'Word already exists: {d["hebrew"]} - {d["root"]} - {d["strongs"]}')
            print(f'In DB: {word_data.hebrew} - {word_data.root} - {word_data.strongs}')
            assert word_data.hebrew == d['hebrew'] and word_data.root == d['root'] and word_data.strongs == d['strongs']

        for m in d['morphology']:
            morphology_data = WordMorphology(
                word_id=word_data.id,
                index=m['index'],
                part_of_speech=m['part_of_speech'],
                word_type=m.get('word_type'),
                stems=m.get('stems'),
                person=m.get('person'),
                gender=m.get('gender'),
                number=m.get('number'),
                state=m.get('state')
            )
            session.add(morphology_data)

        verse_word_data = VerseWord(
            book=d['book'],
            chapter=d['chapter'],
            verse=d['verse'],
            verse_position=d['verse_position'],
            word_id=word_data.id,
            english=d['english']
        )
        session.add(verse_word_data)
        session.commit()

def extract_book_data(book: str):
    book_data = []

    session = get_session()

    for chapter in range(1, 155):
        for verse in range(1, 200):
            if session.query(AddedVerse).filter_by(book=book, chapter=chapter, verse=verse).first():
                continue
            chapter_data = extract_verse_data(book, chapter, verse)
            if not chapter_data:
                break
            insert_verse_data(session, chapter_data)
            added_verse = AddedVerse(
                book=book,
                chapter=chapter,
                verse=verse
            )
            session.add(added_verse)
            session.commit()
            book_data.extend(chapter_data)
            print(f'Finished {book}-{chapter}:{verse}')
        session.commit()

    return book_data

if __name__ == "__main__":
    data = extract_book_data('1_samuel')
    for entry in data:
        print(entry)
