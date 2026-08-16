"""
Common functionality for generator scripts.
"""

import collections
import csv
import re
from datetime import datetime
from os import path
from uuid import uuid4

from typing import Any, Dict, List, OrderedDict, Union




class UuidCache:
    def __init__(self, filename: str):
        self.filename = filename
        self.data: OrderedDict[str, str] | None = None

    def __enter__(self) -> 'UuidCache':
        print('Loading cache: {}'.format(self.filename))
        self.data = collections.OrderedDict()
        try:
            with open(self.filename, 'r') as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                for row in reader:
                    self.data[row[0]] = row[1]
        except FileNotFoundError:
            pass
        return self

    def __exit__(self, exception: Any, value: Any, traceback: Any) -> None:
        if not exception:
            assert self.data is not None, 'Exiting non-entered generator'
            self.save_cache()

    def save_cache(self):
        print('Saving cache: {}'.format(self.filename))
        with open(self.filename, 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
            for k, v in sorted(self.data.items()):
                writer.writerow([k, v])
        print('Done, cached {} UUIDs'.format(len(self.data)))

    def get(self, *args: Any) -> str:
        key = '-'.join(str(a).lower().replace(' ', '~') for a in args)
        assert self.data is not None, 'Using non-entered generator'
        if key not in self.data:
            self.data[key] = str(uuid4())
        return self.data[key]


def now() -> str:
    """
    Return current timestamp as string.
    """
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def format_ipc_dimension(number: float, decimal_places: int = 2) -> str:
    """
    Format a dimension (e.g. lead span or height) according to IPC rules.

    Note: Unfortunately the IPC naming conventions do not specify whether
          decimals shall be rounded or truncated. But it seems usually they
          are truncated, even in the "Footprint Expert" software from
          https://www.pcblibraries.com/. So let's do it the same way to
          get consistent names.
    """
    number *= pow(10, decimal_places)
    # Note: Round to 1nm before truncating to avoid wrong results due to
    # inaccurate calculations leading in numbers like 0.79999999999999.
    return str(int(round(number, 6 - decimal_places)))


def sign(val: Union[int, float]) -> int:
    """
    Return 1 for positive or zero values, -1 otherwise.
    """
    if val >= 0.0:
        return 1
    else:
        return -1


def get_pad_uuids(base_lib_path: str, pkg_uuid: str) -> Dict[str, str]:
    """
    Return a mapping from pad name to pad UUID.
    """
    with open(path.join(base_lib_path, 'pkg', pkg_uuid, 'package.lp'), 'r') as f:
        lines = f.readlines()
    opt_matches = [re.match(r' \(pad ([^\s]*) \(name "([^"]*)"\)\)$', line) for line in lines]
    matches = list(filter(None, opt_matches))
    mapping = {}
    for match in matches:
        uuid = match.group(1)
        name = match.group(2)
        mapping[name] = uuid
    assert len(matches) == len(mapping)
    return mapping


def human_sort_key(key: str) -> List[Any]:
    """
    Function that can be used for natural sorting, where "PB2" comes before
    "PB10" and after "PA3".
    """

    def _convert(text: str) -> Union[int, str]:
        return int(text) if text.isdigit() else text

    return [_convert(x) for x in re.split(r'(\d+)', key) if x]
