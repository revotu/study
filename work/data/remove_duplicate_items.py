# -*- encoding: utf-8 -*-


import os
import json
import collections


def load(fname):
    with open(fname) as f:
        data = json.load(f)
        res = {item['pk']: item for item in data}
    return res


def convert1(items):
    res = {}
    for item in items:
        fields = items[item]['fields']
        res[item] = '{exercise_id}-{question_uid}-{uid}'.format(
            exercise_id=fields['exercise_id'], question_uid=fields['question_uid'], uid=fields['uid'])
    return res


def convert2(data):
    value_to_key = collections.defaultdict(list)
    for k, v in data.items():
        value_to_key[v].append(k)
    return value_to_key


def convert3(data):
    return [v for k, v in data.items() if len(v) > 1]


if __name__ == "__main__":
    dirs = '/mnt/tmp'
    for name in os.listdir(dirs):
        if name.startswith('ob_answersheetitem') and name.endswith('.json'):
            print('LOADING : %s' % name)
            items = load(name)
            len1 = len(items)
            res1 = convert1(items)
            res2 = convert2(res1)
            res3 = convert3(res2)
            for ids in res3:
                max_id = max(ids)
                for id in ids:
                    if id != max_id:
                        print('DELETE ID: %s' % id)
                        del items[id]
            len2 = len(items)
            if len1 > len2:
                print('dumping: ...')
                with open(name + '.new', 'w') as f:
                    json.dump(list(items.values()), f)
