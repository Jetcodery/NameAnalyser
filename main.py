import json
import yaml
import math
import ganzhi
from pprint import pprint
from itertools import product
from pathlib import Path
from word_infos import NameWord
from NameAnalyseClient import get_name_score

word_meaning = {
        '芃': {'Meaning': "芃: 草木茂盛繁密，茁壮生长的意思；",
                     'From': "取自《礼记》：我行其野，其麦芃芃。"},
        '菲': {'Meaning': "菲: 形容花草美，香味浓郁；",
                    'From': "取自刘禹锡《尝茶》 今宵更有湘江月，照出菲菲满碗花。"},
        '蓁': {'Meaning': "形容草木茂盛的样子；",
                     'From': "取自《诗经》-《桃夭》桃之夭夭，其叶蓁蓁。"},
        '莀': {'Meaning': "莀: 草多的样子；",
                     'From': ""},
        '滨': {'Meaning': "滨: 水边；",
                    'From': "取自朱熹《春日》:胜日寻芳泗水滨，无边光景一时新。等闲识得东风面，万紫千红总是春。"},
        '潮': {'Meaning': "潮: 海水涨落；",
                    'From': "取自王湾《次北固山下》:潮平两岸阔，风正一帆悬。"},
        '澄': {'Meaning': "澄: 水清澈而宁静；",
                    'From': "取自王维《青溪》:漾漾泛菱荇，澄澄映葭苇。"},
        '潇': {'Meaning': "潇: 水清而深；",
                    'From': ""},
        '浚': {'Meaning': "浚: 疏通，深挖；", 'From': "《起义堂颂》源浚者流长，根深者叶茂。"},
    }

tiangans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
wuxingNames = ["金", "木", "水", "火", "土"]

wuxingDicForTiangan = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水"
}
wuxingDicForDizhi = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水"
}

def calculateTime(tianganOfDay, time):  # tiangan%10 : 10
    tianganIndex = (2 * tianganOfDay - 1) % 10
    if time == 23 or time == 0 or time == 24:
        dizhi = dizhis[0]
        dizhiIndex = 0
    else:
        dizhiIndex = time / 2
        if dizhiIndex >= 0.5:
            dizhiIndex = math.ceil(dizhiIndex)
        else:
            dizhiIndex = round(dizhiIndex)
        dizhi = dizhis[dizhiIndex]
    return tiangans[(tianganIndex - 1 + dizhiIndex) % 10] + dizhi


class Config():
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

class Runner():
    def __init__(self, config):
        self.config = config
        # 处理输出目录
        self.output_dir = self.config['Runner']['OutputDir']
        if not Path(self.output_dir).exists():
            Path(self.output_dir).mkdir(parents=True)

        # 初始化文字分析器
        self.NameWordAnalyser = NameWord()
        # 计算生辰八字
        self.eight_words = self.getShenChenBaZi(self.config['BirthInfo']['Year'],
                                                self.config['BirthInfo']['Month'],
                                                self.config['BirthInfo']['Day'],
                                                self.config['BirthInfo']['Hour'])
        print(self.eight_words)

    @staticmethod
    def getShenChenBaZi(year, month, day, time):
        data = ganzhi.day(year, month, day)
        tianganOfDay = data[2]
        tianganOfDaySymbol = tiangans.index(tianganOfDay) + 1
        ganzhiOfTime = calculateTime(tianganOfDaySymbol, time)
        return data[0] + '-' + ganzhiOfTime

    @staticmethod
    def getWuXing(bazi):
        bazilist = str(bazi).split("-")
        wuxingList = []
        countForJin = 0
        countForMu = 0
        countForShui = 0
        countForHuo = 0
        countForTu = 0
        for bazi in bazilist:
            wuxingList.append(wuxingDicForTiangan[bazi[0]])
            wuxingList.append(wuxingDicForDizhi[bazi[1]])
        for wuxing in wuxingList:
            if wuxing == "金":
                countForJin = countForJin + 1
            elif wuxing == "木":
                countForMu = countForMu + 1
            elif wuxing == "水":
                countForShui = countForShui + 1
            elif wuxing == "火":
                countForHuo = countForHuo + 1
            else:
                countForTu = countForTu + 1
        scoreForJin = round(countForJin / 8, 2)
        scoreForMu = round(countForMu / 8, 2)
        scoreForShui = round(countForShui / 8, 2)
        scoreForHuo = round(countForHuo / 8, 2)
        scoreForTu = round(countForTu / 8, 2)
        return (scoreForJin, scoreForMu, scoreForShui, scoreForHuo, scoreForTu)

    def get_combinations(self):
        last_name = self.config['NameInfo']['LastName']
        first_list = self.config['NameInfo']['FirstName0']
        second_list = self.config['NameInfo']['FirstName1']
        # 根据config获得所有名字组合
        names = {}
        name_list = []
        combinations = list(product(first_list, second_list))
        if len(combinations) == 0:
            name_list = [last_name + i for i in first_list + second_list]
        else:
            for first_name, second_name in combinations:
                name_list.append(last_name + first_name + second_name)
                name_list.append(last_name + second_name + first_name)

        name_list = list(set(name_list))
        for this_name in name_list:
            name_count = self.NameWordAnalyser.get_word_cnt(this_name)
            if len(this_name) == 2:
                first_name = this_name[-1]
                second_name = ''
            else:
                first_name, second_name = this_name[1], this_name[2]

            names[this_name] = {
                '名字拼音': ' '.join([self.NameWordAnalyser.get_word_yin(w) for w in this_name]),
                '名字笔画数': name_count,
                '自定义源引': f"{''.join(word_meaning.get(first_name, {}).values())}"
                            f"{''.join(word_meaning.get(second_name, {}).values())}",
                '字义': [],
                '名字剖析': {},
                '生辰八字': self.eight_words,
                '五行指数': "金：%.2f,木：%.2f,水：%.2f,火：%.2f,土:%.2f" % (self.getWuXing(self.eight_words))
            }
        return names

    def get_name_meaning(self, names):
        for name in names:
            for nameword in name[1:]:
                names[name]['字义'].append(self.NameWordAnalyser.get_word_infos(nameword))

        return names

    def check_cache(self, now_files, name):
        for ff in now_files:
            if name in str(ff):
                print(f'{name} 已分析完毕: {ff}')
                return True
        else:
            return False

    def get_name_score(self, names):
        _names = list(names.keys())
        now_files = list(Path(self.output_dir).glob('*.json'))

        for name in _names:
            print(f'===================== {name} =====================')
            if self.check_cache(now_files, name):
                continue

            response = get_name_score(name, postconfig=self.config['BirthInfo'])
            names[name]['名字剖析'] = response
            score = response['五格评分']

            # 写文件
            with open(Path(self.output_dir).joinpath(f'{name}_{score}.json'), 'w') as f:
                json.dump(names[name], f, ensure_ascii=False, indent=2)

    def run(self):
        names = self.get_combinations()
        names = self.get_name_meaning(names)
        names = self.get_name_score(names)


if __name__ == '__main__':
    c = Config('config.yaml')
    pprint(c.config)
    r = Runner(config=c.config)
    r.run()
