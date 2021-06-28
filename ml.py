import pandas as pd
from comtrade import Comtrade
class DetectPhase:

    @staticmethod
    def process_data(faza):
        for column in faza:
            faza[column] = pd.to_numeric(faza[column].str.replace(',', '.'))
        return faza

    @staticmethod
    def time_1_faza(faza_1):
        start = 0
        st_bool = True
        end = 0
        A = 0.5
        short_type = '1_faza'
        for index, row in faza_1.iterrows():
            if abs(row['Ub']) < 20 and abs(row['Ib']) > 1 or abs(row['Ua']) < 20 and abs(row['Ia']) > 1 or abs(row['Uc']) < 20 and abs(row['Ic']) > 1:
                if st_bool:
                    start = row['t']
                    st_bool = False
                end = row['t']
        return [short_type, start, end]

    @staticmethod
    def time_2_faza(faza_2):
        start = 0
        st_bool = True
        end = 0
        A = 0.5
        short_type = '2_faza'
        for index, row in faza_2.iterrows():
            a = abs(row['Ia']) > A
            b = abs(row['Ib']) > A
            c = abs(row['Ic']) > A
            if ((a and b and not c) or (a and c and not b) or (b and c and not a)):
                if st_bool:
                    start = row['t']
                    st_bool = False
                end = row['t']
        return [short_type, start, end]

    @staticmethod
    def time_3_faza(faza_3):
        start = 0
        st_bool = True
        end = 0
        A = 0.5
        short_type = '3_faza'
        for index, row in faza_3.iterrows():
            a = abs(row['Ia']) > A
            b = abs(row['Ib']) > A
            c = abs(row['Ic']) > A
            if a and b and c:
                if st_bool:
                    start = row['t']
                    st_bool = False
                end = row['t']
        return [short_type, start, end]

    @staticmethod
    def detect(path_to_cff, k_stat=1):
        rec = Comtrade()
        rec.load(path_to_cff)
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
            res = DetectPhase.time_1_faza(phase)
            if res[1] != 0 and res[2] != 0 :
              if rec.digital[79] != 0:
                res.append(0)
              else:
                res.append(1)
            if res[1] == 0  and res[2] == 0:
                res = DetectPhase.time_3_faza(phase)
                if rec.digital[3] != 0:
                  res.append(0)
                else:
                  res.append(1)
                if res[1] == 0  and res[2] == 0:
                    res = DetectPhase.time_2_faza(phase)
                    if rec.digital[3] != 0:
                      res.append(0)
                    else:
                      res.append(1)
            results.append(res)
        return results
