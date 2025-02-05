import pandas as pd
import datetime

PERIODE = 8
VAK = 'wiskunde A'
NIVEAU = 'vwo'
CURSUSREEKS = 'examencursus'

class Teacher:
    def __init__(self, name, subject, job, email, phone):
        self.name = name
        self.subject = subject
        self.job = job
        self.email = email
        self.phone = phone
        pass
    
PAUZE_TIJDEN = {"vroeg" : [["10:30","11:00"],["13:00","13:45"],["15:45","16:15"]],
                "laat"  : [["11:00","11:30"],["13:30","14:15"],["16:15","16:45"]]}
AVONDETEN = ["18:15","19:15"]

HEADER_LENGTH = 8
DAY_HEADER_LENGTH = 5
DAY_BODY_LENGTH = 55
DAY_LENGTH = DAY_HEADER_LENGTH + DAY_BODY_LENGTH

excel_file = pd.read_excel('presentatierooster.xlsx', skiprows=1, sheet_name="Indeling")

teachers_info = excel_file.iloc[305:,3]

def read_dag(dag_df : pd.DataFrame):
    dag_body = dag_df.iloc[DAY_HEADER_LENGTH:,1:].fillna("").reset_index(drop=True)
    dag_events = dag_body.iloc[:,2:]
    time_col = dag_body.iloc[:,0]
    pauze_schema = dag_df.iloc[2,3]
    
    new_dag_columns = ["time", "event", "docent", "training", "observatie"]
    
    new_dag = pd.DataFrame("", index = range(len(time_col)), columns = new_dag_columns)
    new_dag["time"] = time_col

    # Pauzes
    for pauze in PAUZE_TIJDEN[pauze_schema]:
        start = new_dag[new_dag["time"] == datetime.datetime.strptime(pauze[0], "%H:%M").time()].index[0]
        end = new_dag[new_dag["time"] == datetime.datetime.strptime(pauze[1], "%H:%M").time()].index[0] - 1
        new_dag.loc[start:end,"event"] = "Pauze"

    # Avondeten
    start_dinner = new_dag[new_dag["time"] == datetime.datetime.strptime(AVONDETEN[0], "%H:%M").time()].index[0]
    end_dinner = new_dag[new_dag["time"] == datetime.datetime.strptime(AVONDETEN[1], "%H:%M").time()].index[0] - 1
    new_dag.loc[start_dinner:end_dinner,"event"] = "Avondeten"

    # Wie presenteert
    new_dag["docent"] = dag_events.apply(lambda row: "".join(row[row.str.startswith('p')].index.tolist()), axis=1)
    # Alle trainingen
    new_dag["training"] = dag_events.apply(lambda row: row[row.str.startswith('t')].index.tolist(), axis=1)


    present_mask = new_dag["docent"].ne("") # We zoeken nu alleen nog uitleggen van docenten buiten de klas
    external_mask = pd.Series(False, new_dag.index) # 
    external_mask.loc[~present_mask] = dag_events.loc[~present_mask].apply(lambda row: "".join(row[row.str.startswith('x')].index.tolist()), axis=1).ne("") # Pas alleen plekken aan waar geen docent uit de klas uitlegt, vind daar alles wat met x begint

    def lookup(p_col):
        def f(row):
            i = row.name
            if row[p_col[i]].startswith("p="):
                return " ".join(row[p_col[i]].split(" ")[1:])
            else:
                return " ".join(row[p_col[i]].split(" ")[2:])
        return f
    
    def find_external(row):
        a = row.loc[row.str.startswith('x')]
        
        if a.empty:
            return ""
        else:
            return " ".join(a.head(1).iloc[0].split(" ")[1:])
        
    def find_observatie(p_col):
        def f(row):
            i = row.name
            if row[p_col[i]].startswith("p:"):
                return row[p_col[i]].split(" ")[1]
            else:
                return ""
        return f

    # Check aan de hand van wie presenteert welke uitleg gegeven wordt
    new_dag.loc[present_mask, "event"] = dag_events.loc[present_mask].apply(lookup(new_dag["docent"]), axis = 1)
    # Doe dat ook in het geval dat iemand van een andere klas presenteert
    new_dag.loc[external_mask, "event"] = dag_events.loc[external_mask].apply(find_external, axis = 1)
    # Check of er observeerders zijn, alleen als iemand uit de klas presenteert
    new_dag.loc[present_mask, "observatie"] = dag_events.loc[present_mask].apply(find_observatie(new_dag["docent"]), axis = 1)

    return new_dag

dag_start_indices = excel_file[excel_file.iloc[:,0].str.contains(f"Periode {PERIODE}", na=False)].index
dag_dfs = []
datums = []

for dag_start in dag_start_indices:
    datums.append(excel_file.iloc[dag_start + 1, 0])
    dag_dfs.append(read_dag(excel_file.iloc[dag_start:dag_start + DAY_LENGTH,:]))

dagen = pd.concat(dag_dfs, keys = range(1,len(dag_dfs) + 1), axis=1)
datums_col = pd.DataFrame(datums, columns = pd.MultiIndex.from_tuples([('datums','')]))
periode_col = pd.DataFrame([], columns = pd.MultiIndex.from_tuples([('periode',PERIODE)]))
niveau_col = pd.DataFrame([], columns = pd.MultiIndex.from_tuples([('niveau',NIVEAU)]))
vak_col = pd.DataFrame([], columns = pd.MultiIndex.from_tuples([('vak',VAK)]))
reeks_col = pd.DataFrame([], columns = pd.MultiIndex.from_tuples([('reeks',CURSUSREEKS)]))

final = dagen.join([datums_col,periode_col,niveau_col,vak_col,reeks_col])

final.to_csv(f"cursusplanning.csv")