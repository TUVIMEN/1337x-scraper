#!/usr/bin/env python

import os
import sys
import tempfile
import json
from pathlib import Path

from biggusdictus import isdict, uint, Or, Isodate, Https, Uri

import torrents


def intemp(func):
    prev = os.getcwd()

    with tempfile.TemporaryDirectory() as dir:
        os.chdir(dir)

        func()

    os.chdir(prev)


def post_verify(data):
    isdict(
        data,
        ("title", str, 1),
        ("magnet", str, 20),
        ("tags", list, (str, 1)),
        ("infohash", str, 40, 40),
        ("category", str),
        ("type", str),
        ("language", str),
        ("size", uint),
        ("uploader_link", Or, (str, 0, 0), Https),
        ("uploader", str),
        ("downloads", uint),
        ("checked", Isodate),
        ("uploaded", Isodate),
        ("seeders", uint),
        ("leechers", uint),
        ("description", str),
        ("trackers", list, Uri),
        (
            "files",
            list,
            (
                dict,
                ("type", str),
                ("name", str, 1),
                ("size", uint),
            ),
        ),
        (
            "detail",
            dict,
            ("cover", Or, (str, 0, 0), Https),
            ("rating", uint),
            ("title", str),
            ("categories", list, str),
            ("description", str),
        ),
        ("id", uint),
    )


def post_test(p_id):
    def t():
        leet = torrents.Torrents1337x(".", "https://www.1337xx.to")

        leet.get_post("", p_id=p_id)
        path = Path("torrents-results/" + str(p_id))
        data = path.read_text()

        js = json.loads(data)
        post_verify(js)

    intemp(t)


def test_posts_1():
    post_test(6424662)


def test_posts_2():
    post_test(6419201)


def test_posts_3():
    post_test(4711160)


def test_posts_4():
    post_test(6424050)


def test_posts_5():
    post_test(6423799)


def test_posts_6():
    post_test(122701)


def test_posts_7():
    post_test(5378664)


def test_posts_8():
    post_test(1761419)
