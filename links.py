#!/usr/bin/env python
# by Dominik Stanisław Suchora <hexderm@gmail.com>
# License: GNU GPLv3

import os
import sys
import time
import json
import re
from datetime import datetime
from pathlib import Path
import argparse

from reliq import RQ
import requests
import treerequests

reliq = RQ(cached=True)


def valid_directory(directory: str):
    if os.path.isdir(directory):
        return directory
    else:
        raise argparse.ArgumentTypeError('"{}" is not a directory'.format(directory))


def valid_file(file: str):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError('"{}" is not a file'.format(file))


class Links1337x:
    def __init__(self, path, domain, **kwargs):
        self.ses = treerequests.Session(
            requests,
            requests.Session,
            lambda x, y: treerequests.reliq(x, y, obj=reliq),
            **kwargs,
        )

        self.domain = domain

        self.workdir = Path(os.path.realpath(path))
        self.found_path = self.workdir / "links-keys-found"
        self.used_path = self.workdir / "links-keys-used"
        self.saved_path = self.workdir / "links-saved"
        try:
            os.mkdir(self.saved_path)
        except FileExistsError:
            pass

        self.found = self.load_found()
        self.used = self.load_used()
        self.saved = self.load_saved()

        self.found_save_counter = 0
        self.found_save_bound = 100

    def load_set_from_file(self, fname):
        ret = set()
        try:
            with open(fname, "r") as f:
                for i in f:
                    n = i.strip()
                    if len(n) == 0:
                        pass
                    ret.add(n)
        except FileNotFoundError:
            pass
        return ret

    def load_found(self):
        return self.load_set_from_file(self.found_path)

    def load_used(self):
        return self.load_set_from_file(self.used_path)

    def load_saved(self):
        ret = set()
        for i in os.scandir(self.saved_path):
            if not i.is_file():
                continue
            ret.add(int(i.name))
        return ret

    @staticmethod
    def queryclean(text):
        return text.translate(
            str.maketrans(
                """!@#$%^&*()[]{};:'"/?.>,<=+-\\|~`\n\t""",
                "                                 ",
            )
        ).lower()

    def feed(self, text):
        text = self.queryclean(text)
        for i in filter(lambda x: x != "", text.split(" ")):
            self.found.add(i)

    def feedfile(self, fname):
        with open(fname, "r") as f:
            for i in f:
                self.feed(i)

    def scan(self):
        new = 0
        for i in list(self.found):
            if i in self.used:
                continue

            self.getkey(i)
            new += 1

        return True if new > 0 else False

    def scanall(self):
        try:
            while self.scan():
                pass
        except Exception as e:
            self.save_state()
            raise e

    @staticmethod
    def post_id(url):
        r = re.search(r"/torrent/(\d+)/", url)
        if r is None:
            return 0
        return int(r[1])

    def post_save(self, post):
        p_id = post["id"]
        if p_id == 0:
            return False
        if p_id in self.saved:
            return False

        self.feed(post["title"])

        path = self.saved_path / str(p_id)
        with open(path, "w") as f:
            json.dump(post, f)
            f.write("\n")

        self.saved.add(p_id)
        return True

    @staticmethod
    def post_size(size):
        sizel = len(size)
        if sizel == 0:
            return 0
        i = 0
        hasdot = 0
        while i < sizel and (size[i].isdigit() or (size[i] == "." and not hasdot)):
            if size[i] == ".":
                hasdot = 1
            i += 1
        n = float(size[:i])

        while i < sizel and size[i].isspace():
            i += 1

        if i < sizel:
            c = size[i].lower()
            if c == "k":
                n *= 2**10
            elif c == "m":
                n *= (2**10) ** 2
            elif c == "g":
                n *= (2**10) ** 3
            elif c == "t":
                n *= (2**10) ** 4
            else:
                raise Exception("unknown size format")
            i += 1
            if i < sizel and size[i].lower() == "b":
                i += 1

        assert sizel == i
        return int(n)

    @staticmethod
    def post_date(date):
        if re.search(r"^[A-Za-z]{3}\. \d{1,2}[A-Za-z]{2} +'\d{1,2}$", date):
            date = re.sub(r" +", " ", date)
            date = re.sub(r" (\d{1,2})(st|nd|rd|th) ", r" \1 ", date)
            return datetime.strptime(date, "%b. %d '%y").isoformat()
        elif re.search(r"^\d{1,2}:\d{2} ?[a-z]{2}$", date):
            now = datetime.now()
            ref = datetime.strptime(date, "%OI:%M%p")

            return datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=ref.hour,
                minute=ref.minute,
            ).isoformat()
        else:
            raise Exception("unknown date format {}".format(date))

    def get_page_posts(self, rq):
        p = json.loads(
            rq.search(
                r"""
            .posts table .table-list; [1:] tr; {
                [0] td .name; {
                    .icon [0] a .icon | "%(href)v",
                    [0] a -class; {
                        .link.U @ | "%(href)v",
                        .title @ | "%DT" trim
                    },
                },
                .seeds.u [0] td .seeds | "%i",
                .leeches.u [0] td .leeches | "%i",
                .date [0] td .coll-date | "%i",
                .size [0] td .size | "%i",
                [0] td .uploader; [0] a; {
                    .uploader_link.U @ | "%(href)v",
                    .uploader @ | "%DT" trim
                }
            } |
        """
            )
        )
        new = 0
        for i in p["posts"]:
            i["size"] = self.post_size(i["size"])
            i["date"] = self.post_date(i["date"])
            i["id"] = self.post_id(i["link"])
            if self.post_save(i):
                new += 1
        return new

    def get_page(self, url, page):
        rq = self.ses.get_html(url)

        newposts = self.get_page_posts(rq)
        pagination = rq.filter(r"[0] div .pagination")

        lastpage = 1
        nexturl = ""

        if len(pagination) > 0:
            lastpage = int(pagination.search(r'[-] a i@B>"[0-9]" | "%i"').strip())
            nexturl = pagination.json(r'.u.U a i@tf>">>" | "%(href)v"')["u"]

        if len(nexturl) == 0 and page != lastpage:
            print("================== retrying")
            time.sleep(2)
            return

        return {"newposts": newposts, "lastpage": lastpage, "nexturl": nexturl}

    def get_pages(self, key, category, sort, direction):
        nexturl = ""
        if len(category) == 0:
            nexturl = "{}/sort-search/{}/{}/{}/1/".format(
                self.domain, key, sort, direction
            )
        else:
            nexturl = "{}/sort-category-search/{}/{}/{}/{}/1/".format(
                self.domain, key, category, sort, direction
            )

        lastpage = 0
        page = 1
        bcount = 0
        while nexturl is not None and len(nexturl) > 0:
            r = self.get_page(nexturl, page)
            bcount += 1
            if r is None:
                if bcount > 10:
                    if page + 1 >= lastpage:
                        break
                    nexturl = re.sub(r"/\d+/$", "/", nexturl) + str(page + 1) + "/"
                    bcount = 0
                continue
            nexturl = r["nexturl"]
            if lastpage == 0:
                lastpage = r["lastpage"]
            page += 1
            bcount = 0

        return lastpage

    def get_pages_both(self, key, category, sort):
        lp = self.get_pages(key, category, sort, "desc")
        if lp == 50:
            self.get_pages(key, category, sort, "asc")
        return lp

    def get_pages_sorts(self, key, category):
        lp = self.get_pages_both(key, category, "seeders")
        if lp != 50:
            return lp
        self.get_pages_both(key, category, "leechers")
        self.get_pages_both(key, category, "time")
        self.get_pages_both(key, category, "size")
        return lp

    def get_pages_categories(self, key):
        lp = self.get_pages_sorts(key, "")
        if lp != 50:
            return lp
        self.get_pages_sorts(key, "Movies")
        self.get_pages_sorts(key, "TV")
        self.get_pages_sorts(key, "Games")
        self.get_pages_sorts(key, "Music")
        self.get_pages_sorts(key, "Apps")
        return lp

    def getkey(self, key):
        key = self.queryclean(key)
        key = "-".join(filter(lambda x: x != "", key.split(" ")))
        self.found.add(key)
        self.found_save_counter += 1
        if self.found_save_counter >= self.found_save_bound:
            self.save_state()
            self.found_save_counter = 0

        self.get_pages_categories(key)

        self.used.add(key)

    def save_set_to_file(self, sett, fname):
        with open(fname, "w") as f:
            for i in sett:
                f.write(i)
                f.write("\n")

    def save_found(self):
        self.save_set_to_file(self.found, self.found_path)

    def save_used(self):
        self.save_set_to_file(self.used, self.used_path)

    def save_state(self):
        self.save_found()
        self.save_used()


def argparser():
    parser = argparse.ArgumentParser(
        description="Tool for getting links from 1337x",
        add_help=False,
    )

    parser.add_argument(
        "keys",
        metavar="KEY",
        type=str,
        nargs="*",
        help="key to feed the crawler",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="append",
        metavar="FILE",
        type=valid_file,
        help="Load keys from file",
        default=[],
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit",
    )
    parser.add_argument(
        "-d",
        "--directory",
        metavar="DIR",
        type=valid_directory,
        help="Use DIR as working directory",
        default=".",
    )
    parser.add_argument(
        "-D",
        "--domain",
        metavar="DOMAIN",
        type=str,
        help="set DOMAIN, by default set to https://www.1337xx.to",
        default="https://www.1337xx.to",
    )

    treerequests.args_section(parser)

    return parser


def cli(argv: list[str]):
    args = argparser().parse_args(argv)

    directory = args.directory
    domain = args.domain

    net_settings = {
        "logger": treerequests.simple_logger(sys.stdout),
    }

    lns = Links1337x(directory, domain, **net_settings)

    for i in args.keys:
        lns.feed(i)
    for i in args.file:
        lns.feedfile(i)

    lns.scanall()


cli(sys.argv[1:] if sys.argv[1:] else ["-h"])
