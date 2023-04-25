import json
from mongoengine import disconnect
from models import Author, Quote


if __name__ == '__main__':

    with open("authors.json", "r", encoding='utf-8') as fh:
        authors = json.load(fh)

    with open("quotes.json", "r",encoding='utf-8') as fh:
        quotes = json.load(fh)

    for person in authors:
        author = Author(fullname=person["fullname"], born_date=person["born_date"], born_location=person["born_location"],
                        description=person["description"])
        author.save()


        for quote in quotes:
            if quote["author"] == person["fullname"]:
                record = Quote(tags=quote["tags"], author=author, quote=quote["quote"])
                record.save()

    disconnect()

