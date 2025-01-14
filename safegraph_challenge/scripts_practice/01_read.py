# %%
import polars as pl
import pyarrow as pa
from pyarrow import csv
from pyarrow import dataset as ds
import pyarrow.parquet as pq


# %%
places = pl.read_parquet("../data/places.parquet")
patterns = pl.from_arrow(pq.read_table("../data/patterns.parquet"))


# %%
# with these formats we can use `explode()` to get list cells data and `unnest()` to get struct cells data.
patterns.select("placekey", "related_same_day_brand").explode("related_same_day_brand").unnest("related_same_day_brand")


# %%

# if we want to read in from the highly structured csv file
## These two should read in identical
dat_csv = pl.from_arrow(
        csv.read_csv("../data/chipotle_core_poi_and_patterns.csv"))\
    .filter(pl.col("date_range_start").is_not_null())
dcsv = pl.from_arrow(
        ds.dataset(
            "../data/chipotle_core_poi_and_patterns.csv",
            format="csv")\
        .to_table())\
    .filter(pl.col("date_range_start").is_not_null())


# Let's meet `.str.json_decode()` and use it with the `with_columns()` method
# https://docs.pola.rs/py-polars/html/reference/expressions/api/polars.Expr.str.json_decode.html
# https://docs.pola.rs/py-polars/html/reference/dataframe/api/polars.DataFrame.with_columns.html
# we need to get the json formatted strings into the right Arrow format.
dcsv_parsed = dcsv.with_columns(
    visits_by_day=pl.col("visits_by_day").str.json_decode(pl.List(pl.Int32)),
    bucketed_dwell_times=pl.col("bucketed_dwell_times").str.json_decode(),
    related_same_day_brand_4=pl.col("related_same_day_brand").str.json_decode(
        pl.Struct({
            pl.Field("Walmart", pl.Int32),
            pl.Field("McDonald's", pl.Int32),
            pl.Field("Krogers", pl.Int32),
            pl.Field("Starbucks", pl.Int32),
            }))
    # The multiple other columns
    )
