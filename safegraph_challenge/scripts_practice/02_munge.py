# %%
import polars as pl
import pyarrow as pa
from pyarrow import csv
from pyarrow import dataset as ds
import pyarrow.parquet as pq

# %%
patterns = pl.read_parquet("../data/patterns.parquet")
places = pl.read_parquet("../data/places.parquet")
# %%
# notice how "related_same_day_brand" is handled differently.
patterns.select("placekey", "related_same_day_brand")\
    .explode("related_same_day_brand")\
    .unnest("related_same_day_brand")
# We don't have nulls now.


# %%
# Now lets try to join patterns and places to get a table similar to the csv file

dat = patterns.join(places, on=["placekey"], how="left")


# %%
# what is a unique row? How can we check our join meets our assumptions
dat.group_by("placekey", "date_range_start").count().sort("count", descending=True)

# %%
# now let's create a better join and save our data as `patterns_places.parquet`