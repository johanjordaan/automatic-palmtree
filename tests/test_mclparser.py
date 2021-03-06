from unittest import TestCase

import os

import mclparser


class TestParser(TestCase):
    def test_parse_file(self):
        for filename in os.listdir('fixtures'):
            r = mclparser.parse_file(f'fixtures/{filename}')
            print(f'fixtures/{filename} ->  Total: {r["count"]}, Unknown: {r["unknown_count"]}, Known: {r["known_count"]}')

    def test_parse_line(self):
        unknown_total = 0
        known_total = 0
        count = 0

        with open('fixtures/2021-11-30-1.log', 'r') as f:
            for line in f:
                r = mclparser.parse_line(line)
                count = count + 1
                if r['type'] == 'unknown':
                    unknown_total = unknown_total + 1
                    print(line)
                else:
                    known_total = known_total +1
            print(f'Total: {count}, Unknown: {unknown_total}, Known: {known_total}')

