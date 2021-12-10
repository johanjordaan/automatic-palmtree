import re

import mclgrok

for pattern in mclgrok.patterns:
    pattern['cre'] = re.compile(pattern['pattern'])


def parse_line(line):
    retval = {'type': 'unknown', 'line': line}
    for pattern in mclgrok.patterns:
        z = pattern['cre'].match(line)
        if z is not None:
            retval['type'] = pattern['type']
            retval['data'] = z.groupdict()
    return retval
