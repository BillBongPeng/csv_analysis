import pandas as pd
import Test as test
import numpy as np

ds = pd.read_csv('test.csv',index_col = None, header = 0, engine='python')
# q = ds['Ch1 Amplitude'].quantile(0.99)
# ds = ds[ds['Ch1 Amplitude'] < q]
test1 = test.Test()
test2 = test.Test()
ds.sort_values('Ch1 Amplitude')
print_value, position, z1_max, normalized_list, z1_list, cv1_list = test1.feed_frame(ds,'Ch1 Amplitude')
df = ds.drop(ds.index[0:position])
print("cv1_list")
print(cv1_list[1:10])
print(cv1_list[-10:-1])
del cv1_list[0:position]
#print_value.index[0]+29
# del z_list[0:print_value.index[0]]
# print(len(z_list))
z2_list = test2.determine_with_cv(cv1_list, df)
print("z2_list")
# print(z2_list[1:10])
# print(z2_list[-1])
print(max(z2_list))
print2_value, position, z2_max, normalized_list = test2.determine_dip(df, z2_list,'Ch1 Amplitude')
print("norm_list")
print(normalized_list[1])
print(normalized_list[-1])
print("z2")
print(z2_max)
print("p1")
print(print_value)
print("p2")
print(print2_value)
