from pprint import pprint

def get_stroke_map():
    chinese_char_map = {}
    with open('./chinese_unicode_table.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines[6:]:  # 前6行是表头，去掉
            line_info = line.strip().split()
            # 处理后的数组第一个是文字，第7个是笔画数量
            chinese_char_map[line_info[0]] = line_info[6]
    return chinese_char_map

def get_strokes(words, chinese_char_map) -> int:
    strokes = 0
    for word in words:
        if 0 <= ord(word) <= 126:  # 数字，英文符号范围
            continue
        elif 0x4E00 <= ord(word) <= 0x9FA5:  # 常用汉字Unicode编码范围4E00-9FA5，20902个字
            strokes += int(chinese_char_map.get(word, 1))
        else:  # 特殊符号字符一律排在最后
            continue
    # print(strokes)
    return strokes

if __name__ == '__main__':
    chinese_char_map = get_stroke_map()
    # get_strokes('芃(peng)', chinese_char_map)
    """
    滨：水边；取自朱熹 《春日》    胜日寻芳泗水滨，无边光景一时新。等闲识得东风面，万紫千红总是春。 
    潮：海水涨落；取自王湾《次北固山下》潮平两岸阔，风正一帆悬。
    澄：水清澈而宁静；取自王维《青溪》  漾漾泛菱荇，澄澄映葭苇。
    潇：水清而深；
    """
    first_list = ['芃(peng)', '菲(fei)', '蓁(zhen)', '莀(chen)']
    second_list = ['滨(bin)', '潮(chao)', '澄(cheng)', '潇(xiao)']
    word_meaning = {
        '芃(peng)': {'Meaning': "芃: 草木茂盛繁密，茁壮生长的意思；",
                     'From': "取自《礼记》：我行其野，其麦芃芃。"},
        '菲(fei)': {'Meaning': "菲: 形容花草美，香味浓郁；",
                    'From': "取自刘禹锡《尝茶》 今宵更有湘江月，照出菲菲满碗花。"},
        '蓁(zhen)': {'Meaning': "形容草木茂盛的样子；",
                     'From': "取自《诗经》-《桃夭》桃之夭夭，其叶蓁蓁。"},
        '莀(chen)': {'Meaning': "莀: 草多的样子；",
                     'From': ""},
        '滨(bin)': {'Meaning': "滨: 水边；",
                    'From': "取自朱熹《春日》:胜日寻芳泗水滨，无边光景一时新。等闲识得东风面，万紫千红总是春。"},
        '潮(chao)': {'Meaning': "潮: 海水涨落；",
                    'From': "取自王湾《次北固山下》:潮平两岸阔，风正一帆悬。"},
        '澄(cheng)': {'Meaning': "澄: 水清澈而宁静；",
                    'From': "取自王维《青溪》:漾漾泛菱荇，澄澄映葭苇。"},
        '潇(xiao)': {'Meaning': "潇: 水清而深；",
                    'From': ""},
    }

    names = []
    name_meaning = {}

    for first_name in first_list + second_list:
        for second_name in second_list if first_name in first_list else first_list:
            this_name = f'李 {first_name + second_name}'
            name_count = get_strokes(this_name, chinese_char_map)
            name_meaning[this_name] = {
                '笔画数': name_count,
                '字义': f"{''.join(word_meaning.get(first_name, {}).values())}" 
                       f"{''.join(word_meaning.get(second_name, {}).values())}",
                # '名义': '',
            }

    pprint(name_meaning)
