import pandas as pd
from google.cloud import storage

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "assignment1-data"
    res = []
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        # print(blob.name)
        if blob.name.startswith("data") and blob.name.endswith(".h5"):
            res.append(blob.name[5:])
    
    return res

dirs = list_blobs("assignment1-data")

def valEvent(eventId, fileName, h5List, valEventId):
    if eventId.startswith("R") and fileName in h5List:
        return 1
    elif eventId in valEventId and fileName in h5List:
        return 1
    else:
        return 0

def eventWith5h5(eventId, valEventId):
    if eventId in valEventId:
        return 1
    else:
        return 0

stormEvents_df = pd.read_csv("gs://assignment1-data/StormEvents_details-ftp_v1.0_d2018_c20210604.csv.gz")
stormEvents_df["EVENT_ID"] = stormEvents_df["EVENT_ID"].map(lambda x: "S" + str(x))
valEventId = stormEvents_df.EVENT_ID.to_list()

catalog_df = pd.read_csv("gs://assignment1-data/CATALOG.csv")
catalog_df["ifVal"] = catalog_df.apply(lambda x: valEvent(x["id"], x["file_name"], dirs, valEventId), axis=1)
catalog_df = catalog_df[catalog_df["ifVal"] == 1]

# Desired image types
types = set(['vis','ir069','ir107','vil','lght'])

# Group by event id, and filter to only events that have all desired img_types
events = catalog_df.groupby('id').filter(lambda x: types.issubset(set(x['img_type']))).groupby('id')
event_ids = list(events.groups.keys())
print('Found %d events matching' % len(event_ids),types)

catalog_df["ifVal"] = catalog_df.apply(lambda x: eventWith5h5(x["id"], event_ids), axis=1)
catalog_df = catalog_df[catalog_df["ifVal"] == 1]
del catalog_df["ifVal"]

# catalog_df.to_csv("gs://assignment1-data/CATALOG_cleaned.csv", index = False)
catalog_df.to_csv("gs://assignment1-data/CATALOG_cleaned.csv", index = False, header = None)