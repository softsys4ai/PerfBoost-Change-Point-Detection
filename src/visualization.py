import pandas as pd
import matplotlib.pyplot as plt

def read_file(fname):
    """This function is to read csv data"""
    df = pd.read_csv(fname)
    meta_columns = ["task", "variant", "test", "project", "_id"]
    task = df["task"].values
    variant = df["variant"].values
    test = df["test"].values
    project = df["project"].values
    id = df["_id"].values

    meta_df = [[task[i], variant[i], test[i], project[i], id[i]] for i in range(len(task))]
    unique_meta_df = list(set(map(tuple, meta_df)))

    return df, unique_meta_df

def visualize_ts(global_df, meta_df):
    """This function is used to visualize time series data"""
    count = 0

    for entry in meta_df:
        df = global_df.copy()
        df = df[df["task"] == entry[0]]
        df = df[df["variant"] == entry[1]]
        df = df[df["test"] == entry[2]]
        df = df[df["project"] == entry[3]]
        df = df[df["_id"] == entry[4]]
        print (df)

        count = count+1
        x = df.evg_create_date
        y = df.value
        plt.figure(figsize=(16,5), dpi=100)
        plt.plot(x, y, color='tab:red')
        #plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
        plt.show()
        if count > 2:
            break




if __name__=="__main__":
    fname = "expanded_metrics_mongodb1.csv"
    df, meta_df= read_file(fname)
    visualize_ts(df, meta_df)
