import pandas


class DetectPhase:

    def process_data(self, faza):
        for column in faza:
            faza[column] = pd.to_numeric(faza[column].str.replace(',','.'))
        return faza


    def time_1_faza(self, faza_1):
        start = 0
        st_bool = True
        end = 0
        A = 1
        short_type = '1_faza'
        try:
            for index, row in faza_1.iterrows():
                if row['3U0 ВЛ-330-09 330 kV'] > 100:
                    if st_bool:
                        start = row['t, сек.']
                        st_bool = False
                    end = row['t, сек.']
            return (short_type, start, end)
        except:
            return (0,0,0)


    def time_2_faza(self, faza_2):
        start = 0
        st_bool = True
        end = 0
        A = 1
        short_type = '2_faza'
        try:
            for index, row in faza_2.iterrows():
                if (row['Ia ВЛ-29 токи'] > A ) | (row['Ia ВЛ-29 токи'] < -A):
                    if st_bool:
                        start = row['t, сек.']
                        st_bool = False
                    end = row['t, сек.']
            return (short_type, start, end)
        except:
            return (0,0,0)


    def time_3_faza(self, faza_3):
        start = 0
        st_bool = True
        end = 0
        A = 1
        short_type = '3_faza'
        try:
            for index, row in faza_3.iterrows():
                if (row['Ia ВЛ-330-Дерб. 330 kV'] > A ) | (row['Ia ВЛ-330-Дерб. 330 kV'] < -A):
                    if st_bool:
                        start = row['t, сек.']
                        st_bool = False
                    end = row['t, сек.']
            return (short_type, start, end)
        except:
            return (0, 0, 0)


    def detect(self, path_to_csv):
        data = pd.read_csv(path_to_csv)
        res = self.time_1_faza(data)
        if res[1] == 0  and res[2] == 0:
            res = self.time_2_faza(data)
            if res[1] == 0  and res[2] == 0:
                res = self.time_3_faza(data)
        return res