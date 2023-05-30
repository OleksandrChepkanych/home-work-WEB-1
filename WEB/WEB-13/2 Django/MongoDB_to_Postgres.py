from pymongo import MongoClient
from pymongo.server_api import ServerApi
from psycopg2 import sql
import psycopg2
import configparser
import pathlib

list_authors = []
list_quotes = []
list_tags = []

conf = configparser.ConfigParser()
conf.read("config.ini")


def from_mongodb():
    client = MongoClient(
        "mongodb+srv://user:26337@cluster0.nlkvrgn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.test
    authors = db.authors.find([])
    quotes = db.qoutes.find([])

    for el in authors:
        list_authors.append({
            'full_name': el['full_name'],
            'born_date': el['born_date'],
            'born_location': el['born_location'],
            'bio': el['bio']
        })

    for el in quotes:
        [list_tags.append(tag) for tag in el['tags']]

    index = 1
    quotes = db.qoutes.find([])
    for el in quotes:
        tags = []
        for tag in el['tags']:
            tags.append((index, list_tags.index(tag) + 1))
        try:
            author_name = db.authors.find_one(
                {"_id": el['author'][0]})['full_name']
        except:
            IndexError(print("list index out of range"))
        id_author = None
        for i in range(len(list_authors)):
            if list_authors[i]['full_name'] == author_name:
                id_author = i + 1
        list_quotes.append({
            'quote': el['qoute'],
            'author': id_author,
            'tags': tags
        })
        index += 1


def to_postgressql():

    file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
    config = configparser.ConfigParser()
    config.read(file_config)

    conn = psycopg2.connect(dbname=conf.get('postgres', 'db'), user=conf.get('postgres', 'user'),
                            password=conf.get('postgres', 'password'), host=conf.get('postgres', 'host'),
                            port=conf.get('postgres', 'port'))
    cursor = conn.cursor()

    tags = [list_tags[i] for i in range(len(list_tags))]
    insert = sql.SQL('INSERT INTO quoteapp_tag (name) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, tags))
    )
    cursor.execute(insert)
    conn.commit()

    authors = [(list_authors[i]['full_name'], list_authors[i]['born_date'], list_authors[i]
                ['born_location'], list_authors[i]['bio']) for i in range(len(list_authors))]
    insert = sql.SQL('INSERT INTO quoteapp_author (full_name, born_date, born_location, bio) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, authors))
    )
    cursor.execute(insert)
    conn.commit()

    quotes = [(list_quotes[i]['quote'], list_quotes[i]['author'])
              for i in range(len(list_quotes))]
    insert = sql.SQL(
        'INSERT INTO quoteapp_quote (quote, author_id) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, quotes))
    )
    cursor.execute(insert)
    conn.commit()

    quotes_tags = []
    for quote in list_quotes:
        for tag in quote['tags']:
            quotes_tags.append((tag[0], tag[1]))
    insert = sql.SQL(
        'INSERT INTO quoteapp_quote_tags (quote_id, tag_id) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, quotes_tags))
    )
    cursor.execute(insert)
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    from_mongodb()
    to_postgressql()
