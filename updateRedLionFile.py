import polars as pl

offsetSeconds = int(2**32 / 5)

df = pl.read_csv('./redlion_logs/97010100.CSV')
datetime_column = (df['Date'] + ' ' + df['Time']).rename('DateTime')
df = df.drop('Date').drop('Time')
df = df.insert_column(0, datetime_column)
df = df.with_columns(pl.col('DateTime').str.to_datetime('%Y-%m-%d %H:%M:%S'))
df = df.with_columns(
    pl.when(pl.col('DateTime') < pl.datetime(year= 1997, month=1, day=14))
    .then(pl.col('DateTime') + pl.duration(seconds=offsetSeconds))
    .otherwise(pl.col('DateTime')))
date_column = df.select(pl.col('DateTime').cast(pl.Date).alias('Date'))
time_column = df.select(pl.col('DateTime').cast(pl.Time).alias('Time'))
df = df.insert_column(0, time_column['Time']).insert_column(0, date_column['Date']).drop('DateTime')
print(df)