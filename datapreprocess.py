#!/usr/bin/python


def process_data(file):
    headers = [
        'shopId',
        'shopName',
        'shopGlng',
        'shopGlat',
        'shopPower',
        'shopType',
        'mainCategoryName',
        'categoryURLName',
        'shopGroupId',
        'categoryName',
        'comNum']
    outfile = './data_processed/%s_processed.csv' % file[:-4]
    output = open(outfile, 'w')
    for header in headers:
        if header == 'comNum':
            output.write(header + '\n')
        else:
            output.write(header + ',')
    infile = './data/%s' % file
    with open(infile) as f:
        for line in f.readlines():
            # print(line)
            words = line.split(',')
            if len(words) != 11:
                continue
            for word in words:
                ws = word.split(':')
                ws[1] = ws[1].replace('"', '').strip()
                if ws[0] == 'comNum':
                    ws[1] = ws[1].replace('条评论', '')
                    output.write(ws[1] + '\n')
                else:
                    if ws[1] == '':
                        ws[1] = 'NULL'
                    output.write(ws[1] + ',')
            # output.write('\n')
    output.close()


files = ['gshopInfoK歌.txt', 'gshopInfo休闲娱乐.txt',
         'gshopInfo医疗健康.txt', 'gshopInfo宠物.txt', 'gshopInfo学习培训.txt',
         'gshopInfo爱车.txt', 'gshopInfo生活服务.txt',
         'gshopInfo运动健身.txt', 'gshopInfo美食.txt', 'gshopInfo电影演出赛事.txt',
         'gshopInfo购物.txt', 'gshopInfo周边游.txt']
for file in files:
    process_data(file)