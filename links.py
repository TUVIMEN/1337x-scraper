#!/usr/bin/env python
# by Dominik Stanisław Suchora <hexderm@gmail.com>
# License: GNU GPLv3

import os
import sys
import random
import time
import json
import re
from datetime import datetime
from typing import Tuple
from pathlib import Path
import argparse
import ast

from reliq import RQ
import requests
from urllib.parse import urljoin

reliq = RQ(cached=True)


def conv_curl_header_to_requests(src: str):
    r = re.search(r"^\s*([A-Za-z0-9_-]+)\s*:(.*)$", src)
    if r is None:
        return None
    return {r[1]: r[2].strip()}


def conv_curl_cookie_to_requests(src: str):
    r = re.search(r"^\s*([A-Za-z0-9_-]+)\s*=(.*)$", src)
    if r is None:
        return None
    return {r[1]: r[2].strip()}


def valid_header(src: str) -> dict:
    r = conv_curl_header_to_requests(src)
    if r is None:
        raise argparse.ArgumentTypeError('Invalid header "{}"'.format(src))
    return r


def valid_cookie(src: str) -> dict:
    r = conv_curl_cookie_to_requests(src)
    if r is None:
        raise argparse.ArgumentTypeError('Invalid cookie "{}"'.format(src))
    return r


def valid_directory(directory: str):
    if os.path.isdir(directory):
        return directory
    else:
        raise argparse.ArgumentTypeError('"{}" is not a directory'.format(directory))


def valid_file(directory: str):
    if os.path.isfile(directory):
        return directory
    else:
        raise argparse.ArgumentTypeError('"{}" is not a file'.format(directory))


class RequestError(Exception):
    pass


def bool_get(obj: dict, name: str, otherwise: bool = False) -> bool:
    x = obj.get(name)
    if x is None:
        return otherwise
    return bool(x)


def int_get(obj: dict, name: str, otherwise: int = 0) -> int:
    x = obj.get(name)
    if x is None:
        return otherwise
    return int(x)


def float_get(obj: dict, name: str, otherwise: float = 0) -> float:
    x = obj.get(name)
    if x is None:
        return otherwise
    return float(x)


def dict_get(obj: dict, name: str) -> dict:
    x = obj.get(name)
    if not isinstance(x, dict):
        return {}
    return x


class Session(requests.Session):
    def __init__(self, **kwargs):
        super().__init__()

        self.proxies.update(dict_get(kwargs, "proxies"))
        self.headers.update(dict_get(kwargs, "headers"))
        self.cookies.update(dict_get(kwargs, "cookies"))

        self.timeout = int_get(kwargs, "timeout", 30)
        self.verify = bool_get(kwargs, "verify", True)
        self.allow_redirects = bool_get(kwargs, "allow_redirects", False)

        t = kwargs.get("user_agent")
        self.user_agent = (
            t
            if t is not None
            else "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"
        )

        self.headers.update({"User-Agent": self.user_agent})

        self.retries = int_get(kwargs, "retries", 3)
        self.retry_wait = float_get(kwargs, "retry_wait", 60)
        self.wait = float_get(kwargs, "wait")
        self.wait_random = int_get(kwargs, "wait_random")

        self.logger = kwargs.get("logger")

    def r_req_try(self, url: str, method: str, retry: bool = False, **kwargs):
        if not retry:
            if self.wait != 0:
                time.sleep(self.wait)
            if self.wait_random != 0:
                time.sleep(random.randint(0, self.wait_random + 1) / 1000)

        if self.logger is not None:
            print(url, file=self.logger)

        if method == "get":
            return self.get(url, timeout=self.timeout, **kwargs)
        elif method == "post":
            return self.post(url, timeout=self.timeout, **kwargs)
        elif method == "delete":
            return self.delete(url, timeout=self.timeout, **kwargs)
        elif method == "put":
            return self.put(url, timeout=self.timeout, **kwargs)

    def r_req(self, url: str, method: str = "get", **kwargs):
        tries = self.retries
        retry_wait = self.retry_wait

        instant_end_code = [400, 401, 402, 403, 404, 410, 412, 414, 421, 505]

        i = 0
        while True:
            try:
                resp = self.r_req_try(url, method, retry=(i != 0), **kwargs)
            except (
                requests.ConnectTimeout,
                requests.ConnectionError,
                requests.ReadTimeout,
                requests.exceptions.ChunkedEncodingError,
                RequestError,
            ):
                resp = None

            if resp is None or not (
                resp.status_code >= 200 and resp.status_code <= 299
            ):
                if resp is not None and resp.status_code in instant_end_code:
                    raise RequestError(
                        "failed completely {} {}".format(resp.status_code, url)
                    )
                if i >= tries:
                    raise RequestError(
                        "failed {} {}".format(
                            "connection" if resp is None else resp.status_code, url
                        )
                    )
                i += 1
                if retry_wait != 0:
                    time.sleep(retry_wait)
            else:
                return resp

    def get_html(
        self, url: str, return_cookies: bool = False, **kwargs
    ) -> Tuple[reliq, str] | Tuple[reliq, str, dict]:
        resp = self.r_req(url, **kwargs)

        rq = reliq(resp.text, ref=url)
        ref = rq.ref

        if return_cookies:
            return (rq, ref, resp.cookies.get_dict())
        return (rq, ref)

    def get_json(self, url: str, **kwargs) -> dict:
        resp = self.r_req(url, **kwargs)
        return resp.json()

    def post_json(self, url: str, **kwargs) -> dict:
        resp = self.r_req(url, method="post", **kwargs)
        return resp.json()

    def delete_json(self, url: str, **kwargs) -> dict:
        resp = self.r_req(url, method="delete", **kwargs)
        return resp.json()

    def put_json(self, url: str, **kwargs) -> dict:
        resp = self.r_req(url, method="put", **kwargs)
        return resp.json()


class Links1337x:
    def __init__(self, path, domain, **kwargs):
        self.ses = Session(
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

    def get_page_posts(self, rq, ref):
        p = json.loads(
            rq.search(
                r"""
            .posts table .table-list; [1:] tr; {
                [0] td .name; {
                    .icon [0] a .icon | "%(href)v",
                    [0] a -class; {
                        .link @ | "%(href)v",
                        .title @ | "%DT" trim
                    },
                },
                .seeds.u [0] td .seeds | "%i",
                .leeches.u [0] td .leeches | "%i",
                .date [0] td .coll-date | "%i",
                .size [0] td .size | "%i",
                [0] td .uploader; [0] a; {
                    .uploader_link @ | "%(href)v",
                    .uploader @ | "%DT" trim
                }
            } |
        """
            )
        )
        new = 0
        for i in p["posts"]:
            i["link"] = urljoin(ref, i["link"])
            i["uploader_link"] = urljoin(ref, i["uploader_link"])
            i["size"] = self.post_size(i["size"])
            i["date"] = self.post_date(i["date"])
            i["id"] = self.post_id(i["link"])
            if self.post_save(i):
                new += 1
        return new

    def get_page(self, url, page):
        rq, ref = self.ses.get_html(url)

        newposts = self.get_page_posts(rq, ref)
        pagination = rq.filter(r"[0] div .pagination")

        lastpage = 1
        nexturl = ""

        if len(pagination) > 0:
            lastpage = int(pagination.search(r'[-] a i@B>"[0-9]" | "%i"').strip())
            nexturl = pagination.search(r'a i@tf>">>" | "%(href)v"')
            if len(nexturl) > 0:
                nexturl = urljoin(ref, nexturl)

        if len(nexturl) == 0 and page != lastpage:
            print("================== retrying")
            time.sleep(2)
            return None

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

    request_set = parser.add_argument_group("Request settings")
    request_set.add_argument(
        "-w",
        "--wait",
        metavar="SECONDS",
        type=float,
        help="Sets waiting time for each request to SECONDS",
    )
    request_set.add_argument(
        "-W",
        "--wait-random",
        metavar="MILISECONDS",
        type=int,
        help="Sets random waiting time for each request to be at max MILISECONDS",
    )
    request_set.add_argument(
        "-r",
        "--retries",
        metavar="NUM",
        type=int,
        help="Sets number of retries for failed request to NUM",
    )
    request_set.add_argument(
        "--retry-wait",
        metavar="SECONDS",
        type=float,
        help="Sets interval between each retry",
    )
    request_set.add_argument(
        "-m",
        "--timeout",
        metavar="SECONDS",
        type=float,
        help="Sets request timeout",
    )
    request_set.add_argument(
        "-k",
        "--insecure",
        action="store_false",
        help="Ignore ssl errors",
    )
    request_set.add_argument(
        "-L",
        "--location",
        action="store_true",
        help="Allow for redirections, can be dangerous if credentials are passed in headers",
    )
    request_set.add_argument(
        "-A",
        "--user-agent",
        metavar="UA",
        type=str,
        help="Sets custom user agent",
    )
    request_set.add_argument(
        "-x",
        "--proxies",
        metavar="DICT",
        type=lambda x: dict(ast.literal_eval(x)),
        help='Set requests proxies dictionary, e.g. -x \'{"http":"127.0.0.1:8080","ftp":"0.0.0.0"}\'',
    )
    request_set.add_argument(
        "-H",
        "--header",
        metavar="HEADER",
        type=valid_header,
        action="append",
        help="Set header, can be used multiple times e.g. -H 'User: Admin' -H 'Pass: 12345'",
    )
    request_set.add_argument(
        "-b",
        "--cookie",
        metavar="COOKIE",
        type=valid_cookie,
        action="append",
        help="Set cookie, can be used multiple times e.g. -b 'auth=8f82ab' -b 'PHPSESSID=qw3r8an829'",
    )

    return parser


def cli(argv: list[str]):
    args = argparser().parse_args(argv)

    headers = {}
    cookies = {}
    if args.cookie is not None:
        for i in args.cookie:
            cookies.update(i)

    if args.header is not None:
        for i in args.header:
            headers.update(i)
        cookie = headers.get("Cookie")
        if cookie is not None:
            headers.pop("Cookie")
            for i in cookie.split(";"):
                pair = i.split("=")
                name = pair[0].strip()
                val = None
                if len(pair) > 1:
                    val = pair[1].strip()
                cookies.update({name: val})

    directory = args.directory
    domain = args.domain

    net_settings = {
        "logger": sys.stdout,
        "wait": args.wait,
        "wait_random": args.wait_random,
        "retries": args.retries,
        "retry_wait": args.retry_wait,
        "timeout": args.timeout,
        "location": args.location,
        "user_agent": args.user_agent,
        "verify": args.insecure,
        "proxies": args.proxies,
        "headers": headers,
        "cookies": cookies,
    }

    lns = Links1337x(directory, domain, **net_settings)

    for i in args.keys:
        lns.feed(i)
    for i in args.file:
        lns.feedfile(i)

    lns.scanall()


cli(sys.argv[1:] if sys.argv[1:] else ["-h"])
