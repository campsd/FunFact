#!/usr/bin/env python
# -*- coding: utf-8 -*-


def flatten(iterable):
    def _flatten(_iterable):
        for item in _iterable:
            try:
                yield from _flatten(item)
            except TypeError:
                yield item
    return list(_flatten(iterable))


def flatten_if(iterable, pred):
    def _flatten_if(_iterable):
        for item in _iterable:
            if pred(item):
                yield from _flatten_if(item)
            else:
                yield item
    return list(_flatten_if(iterable))


def map_or_call(iterable, mapping):
    for item in iterable:
        try:
            yield mapping[item]
        except TypeError:
            yield mapping(item)
