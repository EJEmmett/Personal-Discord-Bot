import json
import textwrap
import uuid
from collections import Iterable


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))


def line_wrap(text, wrap_at=1990):
    blocks = []
    for chunk in textwrap.wrap(text, wrap_at, replace_whitespace=False, drop_whitespace=False,
                               break_on_hyphens=False, tabsize=4):
        blocks.append(chunk)
    return blocks


def is_valid_uuid(val, version=4):
    try:
        uuid.UUID(str(val), version=version)
        return True
    except ValueError:
        return False


def comma_separator(seq):
    if not seq:
        return ''
    if len(seq) == 1:
        return seq[0]
    return f"{', '.join(seq[:-1])} and {seq[-1]}"


def flatten(lst):
    flat = []
    for item in lst:
        if isinstance(item, Iterable):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


# Unused, replaced by metaprogramming
def override_cls(obj: object, cls):
    if issubclass(cls, obj.__class__):
        obj.__class__ = cls
