"""Script to test the adx.py module."""
# TODO: Convert to actual unit test!

from exports.adx import ADXFile
import time

exp_iters = 12

start = time.time()
export_file = ADXFile("../export.adx")
data = [
    {
        "name": "Galen Gold",
        "call": "KB6EE",
        "frequency": 32.1532,
        "signal": "59",
        "snr": 26,
        "mode": "LSB",
        "start": "1234-56-78 90:12:34",
        "end": "0987-65-43 21:09:87",
        "qsos": 123456,
        "contest-name": "CQ WPX",
        "bogus1": "123",
        "bogus2": "123",
        "bogus3": "123",
        "bogus4": "123",
        "bogus5": "123",
        "bogus6": "123",
        "bogus7": "123",
        "bogus8": "123",
        "bogus9": "123",
        "bogus10": "123",
        "bogus11": "123",
        "bogus12": "123",
        "bogus13": "123",
        "bogus14": "123",
        "bogus15": "123",
    },
]

# make the data like 100000 times larger, to stress test performance
for i in range(exp_iters):
    data.extend(data)

export_file.write_header()
for x in data:
    export_file.write_record(x)
export_file.write_file()
end = time.time()
print(f"done! ({end-start}) len: {len(data)}")
