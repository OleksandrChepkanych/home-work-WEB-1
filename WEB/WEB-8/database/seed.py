import json
import pathlib

from database.models import Author, Quote
import connect


def json_read(file_name: str, encoding: str = 'utf-8'):
    files = pathlib.Path(__file__).parent.parent.joinpath(file_name)
    with open(files, 'r', encoding=encoding) as f:
        data = json.load(f)
    return data


def authors_file() -> None:
    authors_f = json_read('authors.json')
    [Author(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    ).save()
     for author in authors_f]


def quotes_file() -> None:
    quotes = json_read('quotes.json')
    for quote in quotes:
        author = Author.objects(fullname=quote['author']).first()
        if author.id:
            Quote(
                tags=quote['tags'],
                author=author.id,
                quote=quote['quote']
                ).save()
        else:
            print(f'{quote["author"]}" is unknown!')


if __name__ == '__main__':
    if not Quote.objects():
        authors_file()
        quotes_file()