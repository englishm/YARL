"""Performance testing script for exports/adx.py"""

import os
import time
import sys
sys.path.append("..")
from exports.adx import ADXFile

exp_iters = 13  # number of entries will be 2**exp_iters
test_path = "test_export.adx"

# some bogus test data,  literally
test_data = [{"bogus" + str(n): "123" for n in range(1, 101)}, ]

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
