#!/usr/bin/env python

from __future__ import print_function
from collections import MutableSet
from operator import itemgetter

# MutableSet needs __contains__, __iter__, __len__, add, discard
class BoundedSet(MutableSet):
    def __init__(self, key=lambda x: x, maxlen=16, items=[]):
	self._maxlen = maxlen
	self._keyFunc = key
	self._store = {key(i):i for i in items}
	self.__trim()

    def __contains__(self, element):
	k = self._keyFunc(element)
	return k in self._store
    def __iter__(self):
	return self._store.values().__iter__()
    def __len__(self):
	return len(self._store)
    def __str__(self):
	return str(self._store.values())
    def add(self, element):
	k = self._keyFunc(element)
	if k not in self._store:
	    self._store[k] = element
	    self.__trim()
    def __trim(self):
	while len(self._store) > self._maxlen:
	    minkey = min(self._store.keys())
	    del self._store[minkey]

    def discardKey(self, key):
	if key in self._store:
	    del self._store[k]
    def discard(self, element):
	k = self._keyFunc(element)
	if k in self._store:
	    del self._store[k]
    @property
    def maxlen(self):
        return self._maxlen

if __name__ == '__main__':
    #obs = BoundedSet(maxlen=3, items=range(9,0,-1))
    mdict = lambda x:{'a':x}
    obs = BoundedSet(maxlen=3, items=map(mdict, range(9,0,-1)), key=itemgetter('a'))
    print(obs)
    obs.add(mdict(2))
    print(obs)
    obs.add(mdict(27))
    print(obs)
    md = mdict(13)
    obs.add(md)
    print(obs)
    print(len(obs))

    obs = BoundedSet(maxlen=3)
    print(obs)
    print(len(obs))
    obs.add(17)
    print(obs)
    print(len(obs))


