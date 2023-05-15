"""
根据输入的文字，获取以下几个信息：
1）字音
2）新华字典释义
3）古诗词按时间历排序结果
4）古诗词该字韵意
"""
import json
from pypinyin import pinyin, Style
from hanzidentifier import identify
import zhon.hanzi as hanzi

# https://github.com/pwxcoo/chinese-xinhua
# https://github.com/chinese-poetry/chinese-poetry.git

class NameWord():
    def __init__(self):
        # 加载笔画数所需数据
        chinese_cnt_map = {}
        chinese_structure_map = {}
        with open('./chinese_unicode_table.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for line in lines[6:]:  # 前6行是表头，去掉
                line_info = line.strip().split()
                # 处理后的数组第一个是文字，第7个是笔画数量
                chinese_cnt_map[line_info[0]] = line_info[6]
                chinese_structure_map[line_info[0]] = line_info[7]

        self.chinese_cnt_map = chinese_cnt_map
        self.chinese_structure_map = chinese_structure_map
        # 加载新华字典
        with open('word.json', 'r') as f:
            content = json.load(f)
        self.word_xinhuacontent = dict(zip([c['word'] for c in content], content))

    def get_word_yin(self, word):
        """获取字音
        """
        pinyin_list = pinyin(word)
        return pinyin_list[0][0]

    def get_word_cnt(self, word):
        words = list(word)
        strokes = 0
        for word in words:
            if 0 <= ord(word) <= 126:  # 数字，英文符号范围
                continue
            elif 0x4E00 <= ord(word) <= 0x9FA5:  # 常用汉字Unicode编码范围4E00-9FA5，20902个字
                strokes += int(self.chinese_cnt_map.get(word, 1))
            else:  # 特殊符号字符一律排在最后
                continue
        return strokes

    def get_word_xing(self, word):
        """
            获取中文字符的结构和部首信息
            :param char: 中文字符
            :return: 包含结构和部首信息的字典
            """
        structure = self.chinese_structure_map.get(word, '无')
        return {'偏旁': structure, '结构': ''}

    def get_word_infos(self, word):
        """获取字的韵意
        """
        # 1. 获取字音
        word_yin = self.get_word_yin(word)
        # 2. 获取笔画
        word_cnt = self.get_word_cnt(word)
        # 3. 获取结构部首
        word_xing = self.get_word_xing(word)
        # 4. 获取新华字典释义
        meaning = self.word_xinhuacontent.get(word, {})
        res = meaning.get('explanation', '').strip('').split('\n\n')

        return {
            word: {
                "笔画": word_cnt,
                "音": word_yin,
                "形": word_xing,
                "字义": res,
                "古义": []
            }
        }


if __name__ == '__main__':
    from pprint import pprint
    w = NameWord()
    pprint(w.get_word_infos('澄'))
