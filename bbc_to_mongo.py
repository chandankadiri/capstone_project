import pandas as pd
from mongo_utils import write_to_mongo

df = pd.read_csv('bbc-text.csv')
print(df.shape)
import pdb;pdb.set_trace()
write_to_mongo(df)
