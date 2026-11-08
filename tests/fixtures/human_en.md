# Moving the build off the old machine

We moved the build to the smaller box last Friday. It took two hours, most of it spent rebuilding the cache because I forgot to copy the keys first.

The new machine has four cores and 8 GB of RAM. It builds the site in about ninety seconds, which is slower than the old one but fine for a project this size.

Two things broke. The cron job still pointed at the old path, so the nightly deploy silently did nothing for a day. And the image upload endpoint needed the new host name in an environment variable.

I fixed both on Saturday morning. Next time I will copy the config first and read it line by line before touching anything.
