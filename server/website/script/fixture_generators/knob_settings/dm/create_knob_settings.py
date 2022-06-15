#
# OtterTune - create_knob_settings.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#
import csv
import json
import shutil
from operator import itemgetter

# Oracle Type:
# 1 - Boolean
# 2 - String
# 3 - Integer
# 4 - Parameter file
# 5 - Reserved
# 6 - Big integer


# Ottertune Type:
# STRING = 1
# INTEGER = 2
# REAL = 3
# BOOL = 4
# ENUM = 5
# TIMESTAMP = 6

# KnobResourceType
# MEMORY = 1
# CPU = 2
# STORAGE = 3
# OTHER = 4

# miss:
# OPTIMIZER_MODE
# cursor_sharing


COLNAMES = ("PARA_NAME", "PARA_VALUE", "DEFAULT_VALUE", "MIN_VALUE", "MAX_VALUE", "DESCRIPTION", "PARA_TYPE")


def process_version(version, delim=','):
    fields_list = []
    with open('dm{}.csv'.format(version), 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=delim)
        header = [h.upper() for h in next(reader)]
        idxs = [header.index(c) for c in COLNAMES]
        ncols = len(header)

        ri = 0
        for row in reader:
            assert ncols == len(row), (ri, ncols, len(row))
            fields = {}
            for i, cname in zip(idxs, COLNAMES):
                value = row[i]
                if isinstance(value, str):
                    value = value.strip()
                if cname == 'PARA_NAME':
                    fields['name'] = value.upper()
                elif cname == 'PARA_TYPE':
                    fields['vartype'] = 1
                elif cname == 'DEFAULT_VALUE':
                    fields['default'] = value
                elif cname == 'MIN_VALUE':
                    fields['minval'] = value
                elif cname == 'MAX_VALUE':
                    fields['maxval'] = value
                else:
                    fields['summary'] = value

                fields.update(
                    scope='global',
                    dbms=190,
                    category='',
                    enumvals=None,
                    context='',
                    unit=3,  # Other
                    tunable=True,
                    # description='',
                    # minval=None,
                    # maxval=None,
                )

            # set_field(fields)
            # fields['name'] = ('global.' + fields['name']).lower()
            fields['name'] = ('global.' + fields['name'])
            fields_list.append(fields)
            ri += 1

    fields_list = sorted(fields_list, key=itemgetter('name'))
    final_metrics = [dict(model='website.KnobCatalog', fields=fs) for fs in fields_list]
    filename = 'dm-{}_knobs.json'.format(version)
    with open(filename, 'w') as f:
        json.dump(final_metrics, f, indent=4)
    shutil.copy(filename, "../../../../website/fixtures/{}".format(filename))


def main():
    process_version(8)  # dm8
    # process_version(121, delim='|')  # v12.1c


if __name__ == '__main__':
    main()
