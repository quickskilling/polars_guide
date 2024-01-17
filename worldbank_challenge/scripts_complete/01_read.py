# %%
import polars as pl
from pyarrow import csv
import pyarrow.parquet as pq
# %%
# %%
# Let's try to read in the csv at "../data/API_Download_DS2_en_csv_v2_5657328.csv"
# that we downloaded from the world bank about varied country metrics.
# First using native polars

# %%
# it will default to only reading in two columns as the first row has meta information in two cells.
pl.read_csv("../data/API_Download_DS2_en_csv_v2_5657328.csv", truncate_ragged_lines=True)

# %%
# now we get the data read in.  However, it isn't handling the column types correctly
pl.read_csv(
    "../data/API_Download_DS2_en_csv_v2_5657328.csv",
    truncate_ragged_lines=True,
    skip_rows=4)

# %%
# Notice that the world health leaves missing as blanks in the csv. We need to explain that blanks aren't strings but missing values.
dat = pl.read_csv("../data/API_Download_DS2_en_csv_v2_5657328.csv",
    truncate_ragged_lines=True,
    skip_rows=4,
    null_values="")
dat
# %%
# We don't like the World Banks wide format.  Let's clean it upt to long format.
dat_long = dat\
    .melt(id_vars=["Country Name", "Country Code",
                   "Indicator Name", "Indicator Code"])\
    .filter((pl.col("variable") != "") & (pl.col("value").is_not_null()))\
    .with_columns(
        pl.col("variable").cast(pl.Int32).alias("year"),
        pl.col("value").cast(pl.Float32).alias("value"))\
    .drop("variable")
dat_long
# %%
dat_long.write_csv("../data/long.csv")
dat_long.write_parquet("../data/long.parquet")

# %%
print(dat_long.estimated_size("mb"))
dat_long.select(pl.count("value"))


#### Now let's try using pyarrow
# %%
datpy = csv.read_csv(
    "../data/API_Download_DS2_en_csv_v2_5657328.csv",
    read_options = csv.ReadOptions(skip_rows = 4))
datpy = datpy.drop_columns("")


# %%
# Now if we want to get access to polars methods.
dat = pl.from_arrow(datpy)

# %%
