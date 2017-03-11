#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import codecs
import os
import re
import sys
import requests

re_font_url = re.compile(r'url\((http[^\)]+/([^/\)]+))\)')


def download_css(url):
    print('Downloading CSS:', url)
    r = requests.get(url)
    r.raise_for_status()

    content = r.content.decode('utf-8')

    if '@font-face' not in content:
        raise RuntimeError('Downloaded CSS file is in the expected format')

    return content


def download_font(url, fname):
    print('Downloading font:', url, '->', 'fonts/%s' % fname)
    r = requests.get(url)
    r.raise_for_status()
    dest_file = os.path.join('fonts', fname)
    if not os.path.isdir('fonts'):
        os.makedirs('fonts')
    with open(dest_file, 'wb') as fp:
        fp.write(r.content)


def get_font_urls(content):
    for r in re_font_url.finditer(content):
        yield r.groups()


def patch_css(content):
    print('Generating patched CSS: fonts.css')
    with codecs.open('fonts.css', 'w', encoding='utf-8') as fp:
        fp.write(re_font_url.sub(r'url(fonts/\2)', content))


def main(argv):
    if len(argv) != 1:
        raise RuntimeError('Please provide a Google Fonts CSS url')

    content = download_css(argv[0])
    for url, fname in get_font_urls(content):
        download_font(url, fname)
    patch_css(content)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
