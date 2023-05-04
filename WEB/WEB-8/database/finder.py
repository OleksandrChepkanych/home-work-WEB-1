import sys
from pprint import pprint

from database.models import Author, Quote
import connect


def command_line(command, value):
    match command:
        case 'name':
            name_author(value)
        case 'tag':
            find_tag(value)
        case 'tags':
            tags = value.strip().split(',')
            for tag in tags:
                find_tag(tag.strip())
        case _:
            print(f'Wrong command "{command}"')


def c_parser(value):
    com, val = value.strip().split(' ')
    return com, val


def name_author(author):
    author_id = Author.objects(fullname__icontains=author).first()
    if author_id:
        author_id = author_id.id
    information = Quote.objects(author=author_id)
    if information:
        for text in information:
            pprint(text.quote)
    else:
        print('Not found')


def find_tag(tag):
    information = Quote.objects(tags__icontains=tag)
    if information:
        for item in information:
            pprint(item.quote)
    else:
        print('Not found')


if __name__ == '__main__':
    print('Possible commands: name, tag, tags, exit')
    while True:
        inputted = input('Command: ')
        if inputted != 'exit':
            try:
                com, val = c_parser(inputted)
                command_line(com, val)
            except ValueError:
                print('Wrong command')
        else:
            sys.exit(0)