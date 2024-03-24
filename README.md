# redLionTimeUpdate
 Due to the manner in which RedLion tracked time, logs started to contain time errors beginning 2024-03-22.

 To correct the error in the logs, for dates in 1997, which is the 0 time for Redlion devices, time can be added in the order of the maximum value of an unsigned 32 bit integer divided by 5 (for 200 ms increments). This does not take into account those whom are using subsecond data.

 Feel free to use this code however you like, as we do not know the full results of this error, the code may not work as intended and is designed as an example solution.

 This code is written in Python and uses the polars library.
