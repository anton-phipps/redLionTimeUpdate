# polars to perform dataframe operations. Faster than pandas with large dataframes
import polars as pl

# the max value for the unsigned 32 bit integer which was used to keep track of 200ms clock ticks
offsetSeconds = int(2**32 / 5)

# Read in log file
df = pl.read_csv('./redlion_logs/97010100.CSV')
#combine the Date and Time columns into one
datetime_column = (df['Date'] + ' ' + df['Time']).rename('DateTime')
df = df.drop('Date').drop('Time')
df = df.insert_column(0, datetime_column)
df = df.with_columns(pl.col('DateTime').str.to_datetime('%Y-%m-%d %H:%M:%S'))
# update the time if the date is before a certain day (change according to when the redlion gets back online)
df = df.with_columns(
    pl.when(pl.col('DateTime') < pl.datetime(year= 1997, month=1, day=14))
    .then(pl.col('DateTime') + pl.duration(seconds=offsetSeconds))
    .otherwise(pl.col('DateTime')))
# Split the columns into date and time to return the original CSV format
date_column = df.select(pl.col('DateTime').cast(pl.Date).alias('Date'))
time_column = df.select(pl.col('DateTime').cast(pl.Time).alias('Time'))
df = df.insert_column(0, time_column['Time']).insert_column(0, date_column['Date']).drop('DateTime')
# A sample print for verification
print(df)
# Save the new file with a different name
df.write_csv('./redlion_logs/97010100-updated.CSV')