# %%
import polars as pl
import pyarrow as pa
from pyarrow import csv
from pyarrow import dataset as ds
import pyarrow.parquet as pq

# Now we can explore the relationships using unnest and explode

dcsv_parsed = pl.read_parquet("../data/chipotle_core_poi_and_patterns.parquet")
# %%
# explore the brands
day_brand = dcsv_parsed\
    .select("placekey", "related_same_day_brand")\
    .unnest("related_same_day_brand")\
    .melt(id_vars="placekey")\
    .drop_nulls()

month_brand = dcsv_parsed\
    .select("placekey", "related_same_month_brand")\
    .unnest("related_same_month_brand")\
    .melt(id_vars="placekey")\
    .drop_nulls()

# %%
# explore the home cbgs
dcsv_parsed.select("placekey", "visitor_home_cbgs")\
    .unnest("visitor_home_cbgs")\
    .melt(id_vars="placekey")\
    .drop_nulls()
# %%
# Popularity by hour
# https://docs.pola.rs/py-polars/html/reference/expressions/api/polars.Expr.cum_count.html
dcsv_parsed\
    .select("placekey", "popularity_by_hour")\
    .explode("popularity_by_hour")\
    .with_columns(hour=pl.col("popularity_by_hour")\
        .cum_count()\
        .over("placekey") - 1)
# %%
# explore the day of the month
# Are Fridays at the end of the month more attended than Friday at the beginning of the month?
dcsv_parsed\
    .select("placekey", "date_range_start", "visits_by_day")\
    .explode("visits_by_day")\
    .with_columns(
        day_number=pl.col("visits_by_day")\
            .cum_count()\
            .over("placekey", "date_range_start") - 1)\
    .with_columns(day_date=(pl.col("date_range_start") + pl.duration(days="day_number")))\
    .with_columns(day_week=pl.col("day_date").dt.weekday())\
    .with_columns(day_week_name=pl.col("day_week").replace([1,2,3,4,5,6, 7], ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]))
# %%
