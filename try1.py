import pandas as pd

ds = pd.read_csv('test.csv',index_col = None, header = 0, engine='python')
print_value = self.feed_frame(ds,'Ch1 Amplitude')
print(print_value)

def feed_frame(self, frame, column):
    results_list = []
    cv_list = []
    avg_list = []
    stdv_list = []
    total_length = len(frame.index)
    for i in total_length-20:
        cv, avg, stdv, current_value = self.calculate_cv_value(frame.iloc[i:i+20], column)
        cv_list.append(cv)
        avg_list.append(avg)
        stdv_list.append(stdv)
        z = self.calculate_z_by_cv(cv, cv_list, stdv_list, current_value)
        z_list.append(z)
    z_max = z_list.max()
    for i in list(frame[column]):
        results_list.append(i/z_max)
    results_list.insert(0,0)
    frame['Normalized_Value'] = results_list
    result_frame = frame['Nomralized_Value'] > self.glob_z_filter
    norm_max = frame['Normalized_Value'].max()
    if norm_max != 1:
        dip_series = result_frame.iloc(frame['Normalized_Value'] == 1)
    else:
        dip_series = result_frame.iloc(frame['Normalized_Value'] == norm_max)
    value = dip_series.get(column) + self.glob_base_value
    return value

def calculate_cv_value(self, frame, column):
    #Column is 'Ch1 Amplitude' or 'Ch2 Amplitude'
    values = list(frame[column])
    stdv = np.sqrt((2/(np.mean(sum(values)))))	
    avg = sum(values)/len(values)
    cv = stdv/avg
    return cv, avg, stdv, values[0]

def calculate_z_by_cv(self, cv, cv_list, stdv_list, current_value): 
    z = (current_value-(sum(cv_list)/len(cv_list)))/sum(stdv_list)
    return z
