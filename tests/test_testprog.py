# -*- coding: utf-8 -*-
import time


def test_foo():
    time.sleep(2)
    assert True


def test_bar():
    time.sleep(2)
    assert True


def test_baz():
    time.sleep(2)
    assert False


def test_bubz():
    time.sleep(2)
    assert True
