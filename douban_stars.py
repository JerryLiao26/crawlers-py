#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, requests

def get_total():
    if len(sys.argv) >= 2:
        return int(sys.argv[1])
    else:
        return 100

def get_start():
    if len(sys.argv) >= 3:
        return int(sys.argv[2]) + 1000000
    else:
        return 1000000

def grep_page(URL):
    r = requests.get(URL)
    r.encoding = 'utf-8'
    return r.text

def get_content(stream):
    s_tag = '<div id="headline" class="item">'
    e_tag = '</div>'
    prev = stream.find(s_tag)
    latt = stream.find(e_tag, prev)
    latt = stream.find(e_tag, latt + 1)
    latt = stream.find(e_tag, latt + 1)
    return stream[prev + len(s_tag): latt]

def get_image(content, path):
    e_flag = '点击看大图'
    index = content.find(e_flag)
    if index != -1:
        prev = content.find('src=', index)
        latt = content.find('>', prev)
        img_url = content[prev + 5: latt - 1]
        img_url = img_url.replace('medium', 'large') # Get large image
        r = requests.get(img_url)
        with open(path, 'wb') as img:
            img.write(r.content)
        return True
    else:
        return False

def get_gender(content):
    index = content.find('性别')
    if index != -1:
        gender = ''
        prev = content.find('男', index)
        if prev == -1:
            gender = 'F'
        else:
            gender = 'M'
        return True, gender
    else:
        return False, None

def calc_age(content): # Get approximate age
    index = content.find('<ul')
    prev = content.find('<li>', index)
    prev = content.find('<li>', prev + 1)
    prev = content.find('<li>', prev + 1)
    prev = content.find('</span>', prev)
    latt = content.find('</li>', prev)
    date = content[prev + 8: latt - 1]
    if content.find('出生日期') != -1:
        li = date.split('-')
        b_year = int(li[0])
        c_year = int(time.strftime('%Y', time.localtime(time.time())))
        return True, c_year - b_year
    elif content.find('生卒日期'):
        li = date.split(' 至 ')
        b_year = int(li[0].split('-')[0])
        d_year = int(li[1].split('-')[0])
        return True, d_year - b_year
    else:
        return False, None

def list2str(li, sep=':', end='\n'):
    string = ''
    for i in li[:-1]:
        string += i + sep
    string += li[-1] + end
    return string

def main():
    NUM = 0
    COUNT = 0
    TOTAL = get_total()
    START_FROM = get_start()
    CURRENT_PATH = os.path.abspath(os.curdir)
    DATA_DIR = CURRENT_PATH + os.sep + 'stars' + os.sep
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    URL = 'https://movie.douban.com/celebrity/'
    while COUNT < TOTAL:
        CURR_DATA = list()
        NO = START_FROM + NUM
        NUM += 1
        IMG_PATH = DATA_DIR + str(NO) + '.jpg'
        stream = grep_page(URL + str(NO))
        content = get_content(stream)
        # Get gender
        e_gender, gender = get_gender(content)
        if e_gender:
            CURR_DATA.append(str(NO)) # Append number
            CURR_DATA.append(gender)
            e_age, age = calc_age(content)
            # Get age
            if e_age:
                CURR_DATA.append(str(age))
                # Get image
                e_image = get_image(content, IMG_PATH) # If image exists
                if e_image:
                    COUNT += 1
                    print('Getting star No.' + str(COUNT) + '...') # Command line hint
                    CURR_DATA.append(IMG_PATH)
                    with open(DATA_DIR + 'stars.dat', 'a') as data:
                        data.write(list2str(CURR_DATA))
                    
        else:
            continue
    # After run
    print(str(COUNT) + ' stars got, ' + str(NUM - COUNT) + ' stars skipped. Script finished.')

if __name__ == "__main__":
    main()
