# crawlers-py
Python crawlers of different usage written by me :)

## college_major.py
Crawl college major list from the [site](http://www.fengup.com). Will output to ```major_data.json``` after command line run.

## douban_stars.py
Crawl stars' images, age and gender from douban movie celebrity page. Output images and formatted data file to ```./stars```. Configurable through a few command line options:
For example, running ```python3 douban_stars.py 100 50``` will crawl 100 images from 50th star. Note that stars without image, age or gender info will be skipped.
