import re
import os.path

import mclgrok

for pattern in mclgrok.patterns:
    pattern['cre'] = re.compile(pattern['pattern'])


def parse_line(line):
    retval = {'type': 'unknown', 'line': line}
    for p in mclgrok.patterns:
        z = p['cre'].match(line)
        if z is not None:
            retval['type'] = p['type']
            retval['data'] = z.groupdict()
    return retval


def parse_file(filepath):
    filename = os.path.basename(filepath)
    m = re.match("(?P<year>\\d\\d\\d\\d)-(?P<month>\\d\\d)-(?P<day>\\d\\d)-(?P<log_no>\\d+).log", filename)

    year = m.groupdict()['year']
    month = m.groupdict()['month']
    day = m.groupdict()['day']

    log_no = m.groupdict()['log_no']

    response = {
        'unknown_count': 0,
        'known_count': 0,
        'count': 0,
        'lines': []
    }
    with open(filepath, 'r') as f:
        for line in f:
            r = parse_line(line)
            response['count'] += 1
            if r['type'] == 'unknown':
                response['unknown_count'] += 1
                print(line)
            else:
                response['known_count'] += 1
            response['lines'].append(r)
            r['date'] = f'{year}-{month}-{day}'
            r['log_no'] = log_no
            r['filepath'] = filepath
            r['filename'] = filename
            r['index'] = response['count']

    return response

