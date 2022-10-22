import pandas as pd
# %% Soil Classes
def soil_classes(sand, silt, clay):

    # Conditions of soil texture classes
    SAND = (sand > 85) and (silt+1.5*clay <= 15)
    LOAMY_SAND_UPPER = (80 <= sand <= 90) and (silt+1.5*clay >= 15)
    LOAMY_SAND_LOWER = (70 <= sand <= 85) and (silt+2*clay <= 30)
    SANDY_LOAM_A = (clay <= 20) and (sand >= 52) and (silt+2*clay > 30)
    SANDY_LOAM_B = (clay < 7) and (silt < 50) and (43 <= sand <= 52)
    LOAM = (7 <= clay <= 27) and (28 <= silt <= 50) and (sand < 52)
    SILT_LOAM_A = (silt >= 50 ) and (12 <= clay <= 27)
    SILT_LOAM_B = (50 <= silt <= 80) and (clay < 12)
    SILT = (silt >= 80) and (clay < 12)
    SANDY_CLAY_LOAM = (20 <= clay <= 35) and (silt <= 28) and (sand >= 45)
    CLAY_LOAM = (27 <= clay <= 40) and (20 <= sand <= 45)
    SILTY_CLAY_LOAM = (27 <= clay <= 40) and (sand < 20)
    SANDY_CLAY = (clay >= 35) and (sand >= 45)
    SILTY_CLAY = (clay >= 40) and (silt >= 40)
    CLAY = (clay >= 40) and (sand <= 45) and (silt < 40)   
   
    if (SAND):
        return "SAND"
    elif (LOAMY_SAND_UPPER) or (LOAMY_SAND_LOWER):
        return "LOAMY SAND" 
    elif (SANDY_LOAM_A) or (SANDY_LOAM_B):
        return "SANDY LOAM"
    elif (LOAM):
        return "LOAM"
    elif (SILT_LOAM_A) or (SILT_LOAM_B):
        return "SILT LOAM"
    elif (SILT):
        return "SILT"
    elif (SANDY_CLAY_LOAM):
        return "SANDY CLAY LOAM"
    elif (CLAY_LOAM):
        return "CLAY LOAM"
    elif (SILTY_CLAY_LOAM):
        return "SILTY CLAY LOAM"
    elif (SANDY_CLAY):
        return "SANDY CLAY"
    elif (SILTY_CLAY):
        return "SILTY CLAY"
    elif (CLAY):
        return "CLAY"
    else:
        return "N/A"



#%%
def soil_texture_classification(df):

    df["temp_id"] = [f'TID_{i}' for i in range(len(df))]
    col_find = ['temp_id','sand','silt','clay']
    selected_cols = [c2 for c1 in col_find for c2 in df.columns if c1 in c2.lower()]
    temp_df = df[selected_cols]
    temp_df.iloc[:,1:] = temp_df.iloc[:,1:].apply(pd.to_numeric, errors='coerce')
    temp_fn = lambda row: soil_classes(row[selected_cols[1]], row[selected_cols[2]], row[selected_cols[3]])
    temp_df.loc[:,"Texture_Class"] = temp_df.apply(temp_fn, axis=1)
    df = df.merge(temp_df, on='temp_id', suffixes=('', '_y'))
    df.drop(df.filter(regex='temp_id|_y$').columns, axis=1, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    del temp_fn, temp_df
    
    return df
