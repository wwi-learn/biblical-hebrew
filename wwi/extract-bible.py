import requests
from bs4 import BeautifulSoup

def extract_verse_data(book: str, chapter: int, verse: int):
    url = f'https://openbible.com/text/{book}/{chapter}-{verse}.htm'
    print(f'Extracting data from {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tbl_heading_div = soup.find('div', string='Text Analysis')
    table = tbl_heading_div.find_next('table')
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        if len(cells) == 4:
            strongs = cells[0].text.strip()
            hebrew = cells[1].text.strip()
            english = cells[2].text.strip()
            morphology = cells[3].text.strip()
            data.append({
                'book': book,
                'chapter': chapter,
                'verse': verse,
                'strongs': strongs,
                'hebrew': hebrew,
                'english': english,
                'morphology': morphology
            })
    return data

def extract_book_data(book: str):
    book_data = []

    for chapter in range(1, 155):
        for verse in range(1, 200):
            chapter_data = extract_verse_data(book, chapter, verse)
            if not chapter_data:
                return book_data
            book_data.extend(chapter_data)
            return book_data

    return book_data

if __name__ == "__main__":
    data = extract_book_data('1_samuel')
    for entry in data:
        print(entry)
