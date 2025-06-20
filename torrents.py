#!/usr/bin/env python
# by Dominik Stanisław Suchora <hexderm@gmail.com>
# License: GNU GPLv3

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor

from reliq import RQ
import requests
import treerequests

reliq = RQ(cached=True)


def valid_directory(directory: str):
    if os.path.isdir(directory):
        return directory
    else:
        raise argparse.ArgumentTypeError('"{}" is not a directory'.format(directory))


class Torrents1337x:
    def __init__(self, path, domain, **kwargs):
        self.ses = treerequests.Session(
            requests,
            requests.Session,
            lambda x, y: treerequests.reliq(x, y, obj=reliq),
            **kwargs,
        )

        self.domain = domain

        self.workdir = Path(os.path.realpath(path))
        self.results_path = self.workdir / "torrents-results"
        self.nonexistent_path = self.workdir / "torrents-nonexistent"
        self.failed_path = self.workdir / "torrents-failed"

        self.nonexistent = self.load_nonexistent()
        self.failed = self.load_failed()

        self.nonexistent_save_counter = 0
        self.nonexistent_save_boundary = 200

        self.failed_save_counter = 0
        self.failed_save_boundary = 200

        try:
            os.mkdir(self.results_path)
        except FileExistsError:
            pass

    def load_set_from_file(self, fname, conv=int):
        ret = set()
        try:
            with open(fname, "r") as f:
                for i in f:
                    ret.add(conv(i.strip()))
        except FileNotFoundError:
            pass
        return ret

    def load_nonexistent(self):
        return self.load_set_from_file(self.nonexistent_path)

    def load_failed(self):
        return self.load_set_from_file(self.failed_path)

    def save_set_to_file(self, sett, fname, conv=str):
        with open(fname, "w") as f:
            for i in sett:
                f.write(conv(i))
                f.write("\n")

    def save_nonexistent(self):
        self.save_set_to_file(self.nonexistent, self.nonexistent_path)

    def save_failed(self):
        self.save_set_to_file(self.failed, self.failed_path)

    def save_state(self):
        self.save_nonexistent()
        self.save_failed()

    def add_nonexistent(self, p_id):
        self.nonexistent_save_counter += 1
        self.nonexistent.add(p_id)

        # if self.nonexistent_save_counter >= self.nonexistent_save_boundary:
        # nonexistent_save_counter = 0
        # self.save_nonexistent()

    def add_failed(self, p_id):
        self.failed_save_counter += 1
        self.failed.add(p_id)

        # if self.failed_save_counter >= self.failed_save_boundary:
        # self.failed_save_counter = 0
        # self.save_failed()

    def remove_failed(self, p_id):
        if p_id not in self.failed:
            return
        self.failed_save_counter += 1
        self.failed.remove(p_id)

        # if self.failed_save_counter >= self.failed_save_boundary:
        # self.failed_save_counter = 0
        # self.save_failed()

    @staticmethod
    def queryclean(text):
        return text.translate(
            str.maketrans(
                """!@#$%^&*()[]{};:'"/?.>,<=+-\\|~`\n\t""",
                "                                 ",
            )
        ).lower()

    @staticmethod
    def post_id(url):
        r = re.search(r"/torrent/(\d+)/", url)
        if r is None:
            return 0
        return int(r[1])

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

        if i == 0:
            n = 1
        else:
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
                return 0
                # raise Exception("unknown size format")
            i += 1
            if i < sizel and size[i].lower() == "b":
                i += 1

        if sizel != i:
            return 0
        return int(n)

    @staticmethod
    def conv_relative_date(date: str) -> str:
        datetime.now()
        i = 0
        datel = len(date)
        while i < datel and date[i].isdigit():
            i += 1
        n = int(date[:i])

        while i < datel and date[i].isspace():
            i += 1

        if len(date) >= 4 and date[-4:] == " ago":
            date = date[:-4]

        if date[-1] == "s":
            date = date[:-1]

        mult: float = 0
        match date[i:]:
            case "second":
                mult = 1
            case "minute":
                mult = 60
            case "hour":
                mult = 3600
            case "day":
                mult = 3600 * 24
            case "week":
                mult = 3600 * 24 * 7
            case "month":
                mult = 3600 * 24 * 30.5
            case "year":
                mult = 3600 * 24 * 365.25
            case _:
                raise Exception("unknown date format")

        return datetime.fromtimestamp(
            (datetime.now().timestamp() - int(n * mult))
        ).isoformat()

    @staticmethod
    def post_date(date):
        date = date.strip()
        if len(date) == 0:
            return ""
        date = re.sub(r" +", " ", date)
        if re.search(r"^[A-Za-z]{3}\. \d{1,2}[A-Za-z]{2} +'\d{1,2}$", date):
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
        elif re.search(r" ago$", date):
            return Torrents1337x.conv_relative_date(date)
        else:
            raise Exception("unknown date format {}".format(date))

    def post_fname(self, p_id):
        return self.results_path / str(p_id)

    def post_exists(self, p_id):
        fname = self.post_fname(p_id)
        if not os.path.exists(fname):
            return False
        if not os.path.isfile(fname):
            return True
        return os.path.getsize(fname) > 1

    def write_post(self, data):
        fname = self.post_fname(data["id"])
        with open(fname, "w") as f:
            json.dump(data, f, separators=(",", ":"))
            f.write("\n")

    def get_post(self, url, p_id=0):
        if p_id != 0:
            url = self.domain + "/torrent/" + str(p_id) + "/-/"
        else:
            p_id = self.post_id(url)

        if p_id in self.nonexistent:
            return
        if self.post_exists(p_id):
            return

        try:
            rq = self.ses.get_html(url)
        except requests.RequestException:
            self.add_failed(p_id)
            return

        if len(rq.search('[0] h1 c@[0] i@"Error 404" | "t"')):
            self.add_nonexistent(p_id)
            print("===================== 404")
            return

        r = json.loads(
            rq.search(
                r"""
                div .page-content; {
                    .title div .box-info-heading; [0] h1 | "%DT" trim,
                    .magnet [0] a i@te>"Magnet Download" | "%(href)v",
                    .tags.a [0] ul .category-name; a | "%Dt\n" / trim "\n" trim,
                    .infohash div .infohash-box; [0] span | "%i",
                    ul .list; {
                        [0] @; {
                            .category strong i@tf>"Category"; [0] span ssub@ | "%DT" trim,
                            .type strong i@tf>"Type"; [0] span ssub@ | "%DT" trim,
                            .language strong i@tf>"Language"; [0] span ssub@ | "%DT" trim,
                            .size strong i@tf>"Total size"; [0] span ssub@ | "%DT" tr "," trim,
                            strong i@tf>"Uploaded By"; [0] span ssub@; [0] a; {
                                .uploader_link.U @ | "%(href)v",
                                .uploader @ | "%DT" trim
                            }
                        },
                        [1] @; {
                            .downloads.u strong i@tf>"Downloads"; [0] span ssub@ | "%i",
                            .checked strong i@tf>"Last checked"; [0] span ssub@ | "%i",
                            .uploaded strong i@tf>"Date uploaded"; [0] span ssub@ | "%i",
                            .seeders.u strong i@tf>"Seeders"; [0] span ssub@ | "%i",
                            .leechers.u strong i@tf>"Leechers"; [0] span ssub@ | "%i",
                        }
                    },
                    .description * #description; * c@[1:] child@ | "%Di\n" / sed "s/< *(\/ *)?[Bb][rR] *>/\n/g" "E" tr "\r" " " trim "\n" trim,
                    .trackers.a * #tracker-list; li; text@ "://" child@ | trim echo "\n" / trim,
                    .files * #files; ( li )( span .head ); {
                        .type i class child@ | "%(class)v" / sed "s/^flaticon-//",
                        .name @ | "%Dt" / trim sed "s/ ([^)]* [a-zA-Z][Bb])$//",
                        .size @ | "%t" / sed 's/.* \(([^)]* [a-zA-Z][Bb])\)$/\1/; s/,//g; /^[0-9].* [a-zA-Z][bB]$/!d' "E"
                    } | ,
                    .detail [0] * .torrent-detail; {
                        .cover.U * .torrent-image; [0] img | "%(src)v",
                        .rating.u span .rating; i style | "%(style)v" / sed "s/.*width: //",
                        div .torrent-category; {
                            .title [0] B>h[1-6] spre@ | "%DT" trim,
                            .categories.a span child@ | "%DT" trim echo "\n" / trim,
                            .description [0] p ssub@ | "%DT" trim
                        }
                    }
                }
                """
            )
        )

        r["id"] = p_id
        if len(r["magnet"]) == 0 and len(r["infohash"]) == 0:
            self.add_failed(p_id)
            return
        else:
            self.remove_failed(p_id)

        r["uploaded"] = self.post_date(r["uploaded"])
        r["checked"] = self.post_date(r["checked"])
        r["size"] = self.post_size(r["size"])
        for i, j in enumerate(r["files"]):
            r["files"][i]["size"] = self.post_size(j["size"])

        self.write_post(r)

    def get_last_post_id_page(self, search):
        url = self.domain + "/sort-search/" + search + "/time/desc/1/"
        try:
            rq = self.ses.get_html(url)
        except requests.RequestException:
            return 0

        r = rq.search(
            r'table .table-list; [1:] tr; [0] td .name; [0] a -class | "%(href)v" / sed "s#.*/torrent/([0-9]+)/.*#\1#" "E"'
        )

        try:
            return int(r)
        except ValueError:
            pass
        return 0

    def get_last_post_id(self):
        r = 0
        r = max(r, self.get_last_post_id_page("and"))
        r = max(r, self.get_last_post_id_page("the"))

        return r

    def get_posts(self, start=1, end=-1, threads=1):
        if end < 0:
            end = self.get_last_post_id()
        if threads < 1:
            threads = 1

        last = end + 1

        if threads == 1:
            for i in range(start, last):
                self.get_post("", p_id=i)
        else:
            step = 800
            n = 0
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for i in range(start, last, step):
                    for j in executor.map(
                        lambda x: self.get_post("", p_id=x),
                        range(i, min(i + step, end)),
                    ):
                        pass
                    n += 1
                    if n >= 10:
                        self.save_state()
                        n = 0


def argparser():
    parser = argparse.ArgumentParser(
        description="Tool for getting torrents from 1337x. If no URLs provided scrapes the whole site",
        add_help=False,
    )

    parser.add_argument(
        "urls",
        metavar="URL",
        type=str,
        nargs="*",
        help="urls",
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
        "-t",
        "--threads",
        metavar="THREADS",
        type=int,
        help="amount of threads used for scraping",
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

    net_settings = {"logger": treerequests.simple_logger(sys.stdout)}

    threads = 1
    if args.threads is not None:
        threads = args.threads

    trs = Torrents1337x(args.directory, args.domain, **net_settings)
    treerequests.args_session(trs.ses, args)

    for i in args.urls:
        trs.get_post(i)

    if len(args.urls) == 0:
        try:
            trs.get_posts(threads=threads)
        except Exception as e:
            trs.save_state()
            raise e

if __name__ == "__main__":
    cli(sys.argv[1:])
