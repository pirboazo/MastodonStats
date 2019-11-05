"""
Usage: mastodonStats.py  PATH FILE... [--hashtag=N]  [--mention=N]

Arguments:
  FILE     input file
  PATH     out directory
Options:
  --hashtag=N   Valeur du filtre nombre de citation entre 1 & 10
  --mention=N Filtre mention % de citation entre 1 & 10
  -v --version
  -h --help
"""

# Astuce pour rendre le JSON lisible: python -m json.tool outbox.json > pretty.json

import json
import sys
import os

from docopt import docopt

try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
    exit('This example requires that `schema` data-validation library'
         ' is installed: \n    pip install schema\n'
         'https://github.com/halst/schema')


class Lespouets:

    def __init__(self, json_pouets, UserMention, UserInstance, Filtre_mention, Filtre_hashtag):
        """

        :rtype: object
        """
        self.Filtre_mention = Filtre_mention
        self.Filtre_hashtag = Filtre_hashtag
        self.pouets = json_pouets["orderedItems"]
        self.UserMention = UserMention
        self.UserInstance = UserInstance
        self.stats = {"directs": 0, "privés": 0, "nonlistés": 0, "publics": 0, "repouets": 0, "mfailed": 0, "mentions": {},
                 "hashtag": {}}

    def calcul(self):
        for pouet in self.pouets:

            if pouet["to"] == []:
                self.stats["mfailed"] += 1

            elif pouet["to"][0] == PUBLIC_STREAM:
                if pouet["type"] == "Announce":
                    self.stats["repouets"] += 1
                else:
                    self.stats["publics"] += 1

            elif pouet["to"][0] == "https://{0}/users/{1}/followers".format(INSTANCE, USER):
                if pouet["cc"] == []:
                    self.stats["privés"] += 1
                else:
                    if PUBLIC_STREAM in pouet["cc"][0]:
                        self.stats["nonlistés"] += 1
                    else:
                        self.stats["privés"] += 1

            elif not "/followers" in pouet["to"][0]:
                self.stats["directs"] += 1

            else:
                print("y'a des oubliés: ", pouet["id"], pouet["to"])

            if "tag" in pouet["object"] and type(pouet["object"]) == dict:
                for tag in pouet["object"]["tag"]:

                    if tag["type"] == "Mention":
                        if tag["name"] in self.stats["mentions"]:
                            self.stats["mentions"][tag["name"]] += 1
                        else:
                            self.stats["mentions"][tag["name"]] = 1

                    elif tag["type"] == "Hashtag":
                        if tag["name"] in self.stats["hashtag"]:
                            self.stats["hashtag"][tag["name"]] += 1
                        else:
                            self.stats["hashtag"][tag["name"]] = 1

    def stat_global(self):

        nb_msg_total = self.stats["publics"] + self.stats["nonlistés"] + self.stats["privés"] + self.stats["directs"] + self.stats["repouets"] + \
                       self.stats["mfailed"]
        proportions_pouets = (round(self.stats["publics"] / nb_msg_total * 100, 1),
                              round(self.stats["nonlistés"] / nb_msg_total * 100, 1),
                              round(self.stats["privés"] / nb_msg_total * 100, 1),
                              round(self.stats["directs"] / nb_msg_total * 100, 1),
                              round(self.stats["repouets"] / nb_msg_total * 100, 1),
                              round(self.stats["mfailed"] / nb_msg_total * 100, 1))

        #print(("Nombre de messages total : {0} ").format(nb_msg_total))

        print((
            "\n Nombre de messages \n \r\r total : {0} (100%) \n \r\r publics : {1} ({2}%); \n \r\r non listés : {3} ({4}%); \n \r\r privés : {5} ({6}%); \n \r\r directs : {7} ({8}%);"
            " \n \r\r repouets : {9} ({10}%) ; \n \r\r MentionFail : {11} ({12}%) ").format(
            nb_msg_total,
            self.stats["publics"],
            proportions_pouets[0],
            self.stats["nonlistés"],
            proportions_pouets[1],
            self.stats["privés"],
            proportions_pouets[2],
            self.stats["directs"],
            proportions_pouets[3],
            self.stats["repouets"],
            proportions_pouets[4],
            self.stats["mfailed"],
            proportions_pouets[5])
        )

    def stat_mention(self):

        mentions_tri = sorted(self.stats["mentions"].items(), key=lambda kv: kv[1])
        mentions_tri.reverse()
        total_mentions = sum(self.stats["mentions"].values())

        print(("Pseudos mentionnés : {0}").format(total_mentions))
        if self.Filtre_mention < 100 :
            print("Pseudos mentionnés (par quantité décroissante):")
            for mention in mentions_tri:
                if (round(mention[1] / total_mentions * 100, 1) > self.Filtre_mention):
                    print("{0} : {1} ({2}%)".format(mention[0], mention[1], round(mention[1] / total_mentions * 100, 1)))

    def stat_hashtag(self):
        hashtag_tri = sorted(self.stats["hashtag"].items(), key=lambda kv: kv[1])
        hashtag_tri.reverse()
        total_hashtag = sum(self.stats["hashtag"].values())

        print()
        print(("Hashtag utilisés : {0}").format(total_hashtag))
        if self.Filtre_hashtag < 100:
            print("Hashtag utilisés (par quantité décroissante):")
            for hashtag in hashtag_tri:
                if hashtag[1] >= self.Filtre_hashtag:
                    print("{0} : {1} ({2}%)".format(hashtag[0],hashtag[1],round(hashtag[1] / total_hashtag * 100, 1)))


if __name__ == '__main__':
    args = docopt(__doc__, version='0.9')

    schema = Schema({
        'FILE': [Use(open, error='FILE should be readable')],
        'PATH': And(os.path.exists, error='PATH should exist'),
        '--hashtag': Or(None, And(Use(int), lambda n: 0 < n < 11), error='--count=N should be integer 0 < N < 11'),
        '--mention': Or(None, And(Use(int), lambda n: -1 < n < 11), error='--count=N should be integer 0 < N < 11')
    }
    )
    try:
        args_valid = schema.validate(args)
    except SchemaError as e:
        exit(e)


# Chargement du fichier open par schema:
d = json.load(args_valid['FILE'][0])

USER = d["id"].split('/')[-2]
INSTANCE = d["id"].split('/')[2]
PUBLIC_STREAM = "https://www.w3.org/ns/activitystreams#Public"

print(("Statistiques sur une archive de @{0}@{1}").format(USER,INSTANCE))

Fmention=100
Fhashtag=100

if args_valid['--mention'] :
    Fmention=args_valid['--mention']

if args_valid['--hashtag'] :
    Fhashtag=args_valid['--hashtag']

analyze = Lespouets(d, USER, INSTANCE, Fmention, Fhashtag)

analyze.calcul()
analyze.stat_global()
analyze.stat_hashtag()
analyze.stat_mention()

exit(0)
