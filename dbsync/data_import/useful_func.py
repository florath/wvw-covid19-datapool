''' A collection of functions, which are mainly used to convert datatypes.'''
import dateutil.parser


def convert2int(s):
    '''Convert the given string to int. If the string is empty, return 0.'''
    if s == '':
        return 0
    return int(s)


def convert2float(s):
    '''Converts the given string to a Floating-Point Number.
    If the string is empty, return 0.
    This is necessary for longitude and latitude.'''
    if s == '':
        return 0.0
    return float(s)


def convert_ts(ts_str):
    '''A generic date / time converter.

    This is needed because the data set uses (at least) three
    different ways of specifying date / times.'''
    return dateutil.parser.parse(ts_str).timestamp()
