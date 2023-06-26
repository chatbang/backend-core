# -*- coding: utf-8 -*-
import datetime
import decimal
import json
from functools import partial


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        super(JsonEncoder, self).default(o)


json_dumps = partial(json.dumps, cls=JsonEncoder, ensure_ascii=False)

if __name__ == "__main__":
    data = json_dumps({"a": decimal.Decimal(12)})
    print(data)
