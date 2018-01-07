#!/usr/bin/env python

from __future__ import print_function
import fanfou, json, shelve
from random import shuffle

def get_client():
    with open('config.json') as f:
        config = json.load(f)
    consumer = {'key': config['CLIENT_KEY'], 'secret': config['CLIENT_SECRET']}
    access = {'key': config['ACCESS_TOKEN'], 'secret': config['ACCESS_SECRET']}
    return fanfou.OAuth(consumer, access)

def get_status():
    db = shelve.open('vocabs.dbm')
    indices = db.get('indices') or reindex_shelve(db)
    status = db[indices.pop()]
    db['indices'] = indices
    db.close()
    return status

def reindex_shelve(db):
    db.clear()
    with open('vocabs.txt') as f:
        i = 0
        while 1:
            l = f.readline().strip()
            if not l: break
            db[str(i)] = l
            i += 1
    indices = db.keys()
    shuffle(indices)
    db['indices'] = indices
    return indices

def main():
    client = get_client()
    fanfou.bound(client)
    status = get_status()
    # print(status)
    resp = client.statuses.update({'status': status})
    # print(resp.code)
    assert resp.code == 200

if __name__ == '__main__':
    main()
