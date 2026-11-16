# My Data Engineering Project Diary 🌷

## Day 1: Getting Things Started!

Today I finally got my hands dirty with my insurance data reconciliation project!

I started by creating synthetic data for two insurance agencies. Agency A has 1,000 records, and Agency B has 1,100. I intentionally added some messy data to Agency B, like duplicate records, missing customer names, premium mismatches, and policies that don't exist in Agency A. I wanted to create the kind of data problems a real data engineer might have to deal with.

I checked the datasets using Pandas and regenerated them to make sure I would get the same results. I also compared SHA-256 hashes to confirm that the files hadn't changed. Pretty cool!

Then came the Bronze layer! I created `bronze_ingestion.py` to read both CSV files and save them as Parquet files. I added metadata to keep track of where the data came from, which file was ingested, when it was ingested, and which batch it belonged to.

I also wanted to make sure the pipeline wouldn't ingest the same file over and over again. I used SHA-256 hashing to identify each file. If the file hasn't changed, it skips it. If it changes, it creates a new batch. That's how I got introduced to idempotency!

I checked the Parquet files, and everything looked good. Agency A had 1,000 rows, Agency B had 1,100, and both had 11 columns. The missing values and duplicate records were still there, just as they should be in the Bronze layer.

I wrote three tests using pytest, and all three passed(used agents😉)!! 🥹

I did get stuck on a Python import error while running the tests directly, but figured out that running `python -m pytest` from the project root fixed it.

I also initialized Git locally. Still need to connect everything to GitHub and make my first commit.

**Little wins today:** My synthetic data works, my first ingestion pipeline is running, and all three tests are passing. Not bad at all! 💗

**Next up:** Connect GitHub, make my first commit, and move on to the Silver layer!

