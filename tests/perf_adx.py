"""Performance testing script for exports/adx.py"""

import os
import time
import sys
sys.path.append("..")
from exports.adx import ADXFile

exp_iters = 13  # number of entries will be 2**exp_iters
test_path = "test_export.adx"

# some bogus test data,  literally
test_data = [
    {
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
        "bogus16": "123",
        "bogus17": "123",
        "bogus18": "123",
        "bogus19": "123",
        "bogus20": "123",
        "bogus21": "123",
        "bogus22": "123",
        "bogus23": "123",
        "bogus24": "123",
        "bogus25": "123",
        "bogus26": "123",
        "bogus27": "123",
        "bogus28": "123",
        "bogus29": "123",
        "bogus30": "123",
        "bogus31": "123",
        "bogus32": "123",
        "bogus33": "123",
        "bogus34": "123",
        "bogus35": "123",
        "bogus36": "123",
        "bogus37": "123",
        "bogus38": "123",
        "bogus39": "123",
        "bogus40": "123",
        "bogus41": "123",
        "bogus42": "123",
        "bogus43": "123",
        "bogus44": "123",
        "bogus45": "123",
        "bogus46": "123",
        "bogus47": "123",
        "bogus48": "123",
        "bogus49": "123",
        "bogus50": "123",
        "bogus51": "123",
        "bogus52": "123",
        "bogus53": "123",
        "bogus54": "123",
        "bogus55": "123",
        "bogus56": "123",
        "bogus57": "123",
        "bogus58": "123",
        "bogus59": "123",
        "bogus60": "123",
        "bogus61": "123",
        "bogus62": "123",
        "bogus63": "123",
        "bogus64": "123",
        "bogus65": "123",
        "bogus66": "123",
        "bogus67": "123",
        "bogus68": "123",
        "bogus69": "123",
        "bogus70": "123",
        "bogus71": "123",
        "bogus72": "123",
        "bogus73": "123",
        "bogus74": "123",
        "bogus75": "123",
        "bogus76": "123",
        "bogus77": "123",
        "bogus78": "123",
        "bogus79": "123",
        "bogus80": "123",
        "bogus81": "123",
        "bogus82": "123",
        "bogus83": "123",
        "bogus84": "123",
        "bogus85": "123",
        "bogus86": "123",
        "bogus87": "123",
        "bogus88": "123",
        "bogus89": "123",
        "bogus90": "123",
        "bogus91": "123",
        "bogus92": "123",
        "bogus93": "123",
        "bogus94": "123",
        "bogus95": "123",
        "bogus96": "123",
        "bogus97": "123",
        "bogus98": "123",
        "bogus99": "123",
        "bogus100": "123",
    },
]

# make the dataset exponentially larger
for i in range(exp_iters):
    test_data.extend(test_data)

n_entries = len(test_data)
n_fields = len(test_data[0].items())
n_data_points = n_entries * n_fields

if os.path.exists(test_path):
    os.remove(test_path)  # remove any existing data

# now we can start timing
start = time.perf_counter()

file = ADXFile(test_path)
file.write_header()
for x in test_data:
    file.write_record(x)
file.write_file()

end = time.perf_counter()
exec_time = end - start

print(f"Data export complete! Statistics:\n")
print(f"Entries in list: {n_entries}")
print(f"Fields per entry: {n_fields}")
print(f"Total data points: {n_data_points}")
print(f"Total export time: {exec_time:0.9f} seconds")
print(f"Time per entry: {(exec_time/n_entries)*1000:0.6f} ms")
print(f"Time per data point: {(exec_time/n_data_points)*1000000:0.4f} us")
