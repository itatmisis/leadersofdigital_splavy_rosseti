import pandas as pd
from comtrade import Comtrade


def time_1_faza(faza_1):
    start = 0
    st_bool = True
    end = 0
    A = 0.5
    short_type = '1_faza'
    #print(faza_1)
    for index, row in faza_1.iterrows():
        if -20 < row['Ub'] < 20 and abs(row['Ib']) > 1 or -20 < row['Ua'] < 20 and abs(row['Ia']) > 1 or -20 < row['Uc'] < 20 and abs(row['Ic']) > 1:
            if st_bool:
                start = row['t']
                st_bool = False
            end = row['t']
    return (short_type, start, end)


def time_2_faza(faza_2):
    start = 0
    st_bool = True
    end = 0
    A = 0.5
    short_type = '2_faza'
    #print(faza_2)
    for index, row in faza_2.iterrows():
        a = (row['Ia'] > A ) | (row['Ia'] < -A)
        b = (row['Ib'] > A ) | (row['Ib'] < -A)
        c = (row['Ic'] > A ) | (row['Ic'] < -A)
        if ((a and b and not c) or (a and c and not b) or (b and c and not a)):
            if st_bool:
                start = row['t']
                st_bool = False
            end = row['t']
    return (short_type, start, end)


def time_3_faza(faza_3):
    start = 0
    st_bool = True
    end = 0
    A = 0.5
    short_type = '3_faza'
    a = False
    b = False
    c = False
    for index, row in faza_3.iterrows():
        a = ((row['Ia'] > A ) or (row['Ia'] < -A))
        b = ((row['Ib'] > A ) or (row['Ib'] < -A))
        c = ((row['Ic'] > A ) or (row['Ic'] < -A))
        if a and b and c:
            if st_bool:
                start = row['t']
                st_bool = False
            end = row['t']
    return (short_type, start, end)


def detect(path_to_сff, k_stat=1):
    rec = Comtrade()
    rec.load(path_to_сff)
    keys = ['t'] + rec.analog_channel_ids 
    values = [rec.time] + rec.analog
    d = dict(zip(keys,values))
    data = pd.DataFrame(data = d)
    col_pref = ['Ua', 'Ub', 'Uc', '3U0', 'Ia', 'Ib', 'Ic', '3I0']
    col_name  = ['t']
    col_name += k_stat * col_pref
    data.columns = col_name
    data = data.dropna()
    results = []
    for i in range(k_stat):
        phase = pd.concat([data.iloc[:, 0], data.iloc[:, 1 + i * 8: 9 + i * 8]], axis=1, sort=False)
        res = time_1_faza(phase)
        if res[1] == 0  and res[2] == 0:
            res = time_3_faza(phase)
            if res[1] == 0  and res[2] == 0:
                res = time_2_faza(phase)
        results.append(res)
    return results
###

#detect('/content/1_faza_perv.cff', 2)

#detect('/content/2_faza_VL.cff', 1)

#detect('/content/3_faza_VL.cff', 2)

