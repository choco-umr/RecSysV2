import pandas as pd

df = pd.read_csv(r"C:\Users\umr\Downloads\RECSYS_V2_ETL_PIPELINE\MINDsmall_train\behaviors.tsv"
                  , sep = '\t', header = None, names = ['impression_id', 'userid', 'Timestamp', 'History', 'impressions'])

#print(df.head(10))
df = df.assign(impressions=df["impressions"].str.split()).explode("impressions").reset_index(drop=True)
df[["itemid", "interactiontype"]] = df['impressions'].str.split("-", expand=True)

df["interactiontype"] = df["interactiontype"].astype(int)
print(df.dtypes)

df = df.drop(columns=["History", "impression_id", "impressions"])

#shuffling the columns to match schema
df = df.loc[:, ['userid', 'itemid', 'Timestamp', 'interactiontype']]


df.insert(0, "Dataset_name", "MIND")
df["Read_time"] = None
df["Scroll_percentage"] = None

df["interactiontype"] = df["interactiontype"].replace(1, "click")
df["interactiontype"] = df["interactiontype"].replace(0, "noclick")

df = df.rename(columns={"Dataset_name": "DATASET_NAME","userid": "USER_ID", "itemid": "ITEM_ID",'Timestamp': 'TIMESTAMP', "interactiontype": "INTERACTION_TYPE", "Read_time": "READ_TIME", "Scroll_percentage": "SCROLL_PERCENTAGE"})

print(df.head(10))

path = r"C:\Users\umr\Downloads\RECSYS_V2_ETL_PIPELINE\T1MindInteractionsTOP50.csv"
df.to_csv(path, index=False)