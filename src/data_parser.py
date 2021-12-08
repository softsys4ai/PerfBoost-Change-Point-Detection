import bson
import datetime
import pandas as pd
import json
from bson.objectid import ObjectId


def parse_change_points():
    """This function is used to parse change points data"""
    with open('change_points.bson','rb') as f:
        data = bson.decode_all(f.read())

    columns = ["percent_change", "repo_full_name", "evg_create_date",
           "author", "author_email", "commit_date",
           "version","build_failures","calculated_on",
           "branch", "commit", "cedar_perf_result_id",
           "message", "_id", "z_score_change",
           "order"]
    triage_columns=["triage_status", "triaged_on"]
    algorithm_columns = ["version","name"]
    time_series_info_columns=["task","variant","project",
                         "measurement","test"]
    cols = []
    cols.extend(columns)
    cols.extend(triage_columns)
    cols.extend(["alg_version", "name"])
    cols.extend(time_series_info_columns)

    ldf = []
    rec = data[0]
    for col in columns:
        try:
            ldf.append(rec[col])
        except KeyError:
            ldf.append(-5000)

    cur = rec["triage"]
    for t_col in triage_columns:
        ldf.append(cur[t_col])

    cur = rec["algorithm"]
    for a_col in algorithm_columns:
        ldf.append(cur[a_col])

    cur = rec["time_series_info"]
    for ts_col in time_series_info_columns:
        ldf.append(cur[ts_col])


    df = pd.DataFrame([ldf])
    df.columns = cols
    df.to_csv("change_points_processed.csv")

    counter=0
    for rec in data:
        ldf = []
        for col in columns:
            try:
                ldf.append(rec[col])
            except KeyError:
                ldf.append(-5000)

        cur = rec["triage"]
        for t_col in triage_columns:
             ldf.append(cur[t_col])

        cur = rec["algorithm"]
        for a_col in algorithm_columns:
            ldf.append(cur[a_col])

        cur = rec["time_series_info"]
        for ts_col in time_series_info_columns:
            ldf.append(cur[ts_col])

        df = pd.DataFrame([ldf])
        try:
            df.to_csv("change_points_processed.csv",mode="a",header=None)
        except UnicodeEncodeError:
            pass

def parse_time_series():
    """This function is used to parse time series data"""
    with open('time_series.bson','rb') as f:
        data = bson.decode_file_iter(open('time_series.bson'))


    columns = ['task', 'updateFailuers', 'args',
              'variant', 'project','test',
              '_id','evg_create_date','commit_date',
              'value', 'version', 'commit',
              'cedar_perf_result_id', 'order']
    df=[]
    index = 0
    num=0
    for row in data:
        num=num+1
        for ts in row['data']:
            cur = [row['task'], row['updateFailures'], row['args'],
                   row['variant'], row['project'], row['test'],
                   row['_id'], ts['evg_create_date'], ts['commit_date'],
                   ts['value'], ts['version'], ts['commit'],
                   ts['cedar_perf_result_id'], ts['order']]
            df.append(cur)
        if num > 10000:
            index = index+1
            df = pd.DataFrame(df)
            df.columns = columns
            df.to_csv("expanded_metrics_mongodb"+str(index)+".csv")
            num = 0
            df = []
            if index > 50:
                break


if __name__=="__main__":
    parse_time_series()
