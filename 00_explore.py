#%%
# preprocess DisGeNET(Disease-Gene) dataset into biggraph edge format
import pandas as pd
import sqlite3
#%%

# Connect to the SQLite database
conn = sqlite3.connect('./db/disgenet_2020.db')
#%%
### check tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()
[table[0] for table in tables]
#%%
# Read data into a DataFrame
df_gd = pd.read_sql_query("SELECT * FROM geneDiseaseNetwork", conn)
#%%
df_gd.shape
#%%
df_gd.head()
#%%
df_gd.source.unique()
df_gd.association.unique()
#%%
df_gd.association.sum()
#%%
df_gd.associationType.unique()
#%%
df_gd.score.min()
df_gd.score.max()
#%%
df_gd.EL.unique()
#%%
df_gd.EI.min()
df_gd.EI.max()
#%%
for ue in df_gd.EL.unique():
    print(f'{ue} :: min : {df_gd.loc[df_gd.EL==ue].score.min()} max :{df_gd.loc[df_gd.EL==ue].score.max()}')
    print(f'{ue} :: min : {df_gd.loc[df_gd.EL==ue].EI.min()} max :{df_gd.loc[df_gd.EL==ue].EI.max()}')
#%%
df_gd.loc[~pd.isna(df_gd.EL)].shape
df_gd.loc[pd.isna(df_gd.EL)].shape
#%%
df_gd.loc[~pd.isna(df_gd.EL)][['diseaseNID', 'geneNID', 'NID']].shape
df_gd.loc[~pd.isna(df_gd.EL)][['diseaseNID', 'geneNID', 'NID']].drop_duplicates(subset=['diseaseNID', 'geneNID'], inplace=False).shape
#%%
df_gd.loc[~pd.isna(df_gd.EL)][['diseaseNID', 'geneNID', 'NID']].groupby(['geneNID', 'diseaseNID']).count()
#%%
for gr, rows in df_gd.loc[~pd.isna(df_gd.EL)][['geneNID', 'diseaseNID', 'NID']].groupby(['geneNID', 'diseaseNID']):
    # print(gr)
    print(rows.diseaseNID.values)
#%%
# Close the connection
conn.close()


#%%
### what disease to do quality check
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name like '%disease%';")

tables = cursor.fetchall()
tns = [table[0] for table in tables]
#%%
for tn in tns:
    print(tn)
    df_t = pd.read_sql_query(f'SELECT * FROM {tn} LIMIT 5;', conn)
    print(df_t.head())
#%%
df_d = pd.read_sql_query(f'SELECT diseaseNID, diseaseName FROM diseaseAttributes;', conn)
df_d.shape
#%%
df_d.loc[df_d.diseaseName.str.find('dementia')>=0].diseaseNID.values
#%%
df_d.loc[df_d.diseaseNID==7897]
#%%
df_d.loc[df_d.diseaseNID==135]