# %%
# %%
import polars as pl
dat_long = pl.read_parquet("../data/long.parquet")

# %%
# Can we split out the information in the indicator Code
indicator_columns = dat_long.select(
    # pick columns
    pl.col("Indicator Code")\
    # split string: example VC.IDP.TOCV into list object ["VC", "IDP", "TOCV"]
        .str.split(".")\
        .list.to_struct(n_field_strategy="max_width"))  # convert to struct object {"VC","IDP","TOCV",null,null,null,null}

# %%
# now display the difference
dat_long.select(pl.col("Indicator Code"))
indicator_columns


# %%
dat_columns = indicator_columns.unnest("Indicator Code")
dat_columns

# %%
# What should we call these columns?
# https://datahelpdesk.worldbank.org/knowledgebase/articles/201175-how-does-the-world-bank-code-its-indicators
new_names = {"field_0":"topic", "field_1":"general_subj", "field_2":"specific_subj",
        "field_3":"ext_1", "field_4":"ext_2", "field_5":"ext_3", "field_6":"ext_4"}
dat_columns = dat_columns.rename(new_names)

# %%
# now we need to finalize our munge and write our data
# https://stackoverflow.com/questions/71654966/how-can-i-append-or-concatenate-two-dataframes-in-python-polars
dat_final = dat_long.hstack(dat_columns)

names = dat_final.columns
new_order = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 0]
name_order = [names[i] for i in new_order]
dat_final = dat_final.select(name_order)
dat_final
# %%
# write data
dat_final.write_parquet("../data/dat_munged.parquet")
dat_final.write_csv("../data/dat_munged.csv")
# %%
