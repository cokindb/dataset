#!/usr/bin/env python3
# pylint: disable=line-too-long, missing-function-docstring, logging-fstring-interpolation
# pylint: disable=too-many-locals, broad-except, too-many-arguments,
# pylint: disable=raise-missing-from

import json

dataset_v700g_filename = "v700g/cokin-p-dataset-v700g.json"
dataset_cokinfilter_com_filename = "cokinfilter.com/cokin_products_concise.json"

consolidated_filename = "consolidated.json"


def fetch_dataset_v700g():
    result = []
    with open(dataset_v700g_filename, 'r') as fh:
        content_json = json.loads(fh.read())

        for item in content_json:
            result.append({
                "ref": f"P{item['REF']}",
                "factor": item['FILTER FACTOR'],
                "correction": item['F-STOP'],
                "title": item['DESIGNATION'],
            })

    return result


def fetch_dataset_cokinfilter_com():
    result = []
    with open(dataset_cokinfilter_com_filename, 'r') as fh:
        content_json = json.loads(fh.read())

        for item in content_json:
            result.append({
                "ref": item['model'],
                "url": item['url'],
                "image_url": item['image_url'],
                "title": item['title'],
            })

    return result


if __name__ == '__main__':

    consolidated = {}

    dataset_v700g = fetch_dataset_v700g()
    dataset_cokinfilter_com = fetch_dataset_cokinfilter_com()

    for item in dataset_v700g:
        if item['ref'] not in consolidated:
            consolidated[item['ref']] = {}

        if 'titles' not in consolidated[item['ref']]:
            consolidated[item['ref']]['titles'] = []

        consolidated[item['ref']]['factor'] = item['factor']
        consolidated[item['ref']]['correction'] = item['correction']

        if item['title'] not in consolidated[item['ref']]['titles']:
            consolidated[item['ref']]['titles'].append(item['title'])

    for item in dataset_cokinfilter_com:
        if item['ref'] not in consolidated:
            consolidated[item['ref']] = {}

        if 'urls' not in consolidated[item['ref']]:
            consolidated[item['ref']]['urls'] = []

        if 'image_urls' not in consolidated[item['ref']]:
            consolidated[item['ref']]['image_urls'] = []

        if 'titles' not in consolidated[item['ref']]:
            consolidated[item['ref']]['titles'] = []

        if item['url'] not in consolidated[item['ref']]['urls']:
            consolidated[item['ref']]['urls'].append(item['url'])

        if item['image_url'] not in consolidated[item['ref']]['image_urls']:
            consolidated[item['ref']]['image_urls'].append(item['image_url'])

        if item['title'] not in consolidated[item['ref']]['titles']:
            consolidated[item['ref']]['titles'].append(item['title'])

    with open(consolidated_filename, "w") as fh:
        fh.write(json.dumps(consolidated, indent=2))

    print("Done")