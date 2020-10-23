import pandas as pd


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
        short_type = '1_faza'
        try:
            for index, row in faza_1.iterrows():
                if row['3U0 ВЛ-330-09 330 kV'] > 100:
                    if st_bool:
                        start = row['t, сек.']
                        st_bool = False
                    end = row['t, сек.']
            return short_type, start, end
        except:
            return 0, 0, 0

    @staticmethod
    def time_2_faza(faza_2):
        start = 0
        st_bool = True
        end = 0
        a = 1
        short_type = '2_faza'
        try:
            for index, row in faza_2.iterrows():
                if (row['Ia ВЛ-29 токи'] > a) | (row['Ia ВЛ-29 токи'] < -a):
                    if st_bool:
                        start = row['t, сек.']
                        st_bool = False
                    end = row['t, сек.']
            return short_type, start, end
        except:
            return 0, 0, 0

    @staticmethod
    def time_3_faza(faza_3):
        start = 0
        st_bool = True
        end = 0
        a = 1
        short_type = '3_faza'
        try:
            for index, row in faza_3.iterrows():
                if (row['Ia ВЛ-330-Дерб. 330 kV'] > a) | (row['Ia ВЛ-330-Дерб. 330 kV'] < -a):
                    if st_bool:
                        start = row['t, сек.']
                        st_bool = False
                    end = row['t, сек.']
            return short_type, start, end
        except:
            return 0, 0, 0

    @staticmethod
    def detect(path_to_csv):
        data = pd.read_csv(path_to_csv)
        res = DetectPhase.time_1_faza(data)
        if res[1] == 0 and res[2] == 0:
            res = DetectPhase.time_2_faza(data)
            if res[1] == 0 and res[2] == 0:
                res = DetectPhase.time_3_faza(data)
        return res
