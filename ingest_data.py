import os
import urllib

import pandas as pd
import numpy as np
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import AutoReconnect

load_dotenv()

USERNAME = os.getenv("USERNAME", "")
PWD = os.getenv("PWD", "")

uri = (
    "mongodb+srv://"
    + urllib.parse.quote_plus(USERNAME)
    + ":"
    + urllib.parse.quote_plus(PWD)
    + "@cluster0.k3qwm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(uri)
collection = client["llm_task"]["purchase_order"]

data = pd.read_csv("/home/ubuntu/aip/kotb2/PURCHASE ORDER DATA EXTRACT 2012-2015_0.csv")

date_columns = ["Creation Date", "Purchase Date"]
for col in date_columns:
    data[col] = pd.to_datetime(data[col], errors="coerce")
data = data.replace({pd.NaT: None, np.nan: None})
records = data.to_dict("records")


def batch_insert(collection, records, batch_size=1000, max_retries=5):
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        for attempt in range(max_retries):
            try:
                collection.insert_many(batch)
                print(f"Batch {i//batch_size + 1} inserted successfully.")
                break
            except AutoReconnect as e:
                print(
                    f"AutoReconnect error during batch {i//batch_size + 1}: {e}. Retrying..."
                )
                if attempt == max_retries - 1:
                    print(
                        f"Failed to insert batch {i//batch_size + 1} after {max_retries} retries."
                    )
                else:
                    import time

                    time.sleep(5)


batch_insert(collection, records, batch_size=1000)
