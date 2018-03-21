import urllib.request
import json
import numpy as np
import pandas as pd
from classCompanyInfo import Company

#from ファイル名 import クラス名
#from ファイル名.クラス名 import 関数名（引数なし）

from G_Sheet import gsheet



class Row:
    def __init__(self, id, url, status, mobile, desktop):
        self.id = id
        self.url = url
        self.status = status
        self.mobile = mobile
        self.desktop = desktop
       
        
    def __repr__(self) :
        return repr((self.id, self.url, self.status, self.mobile, self.desktop))

def load_urls():
    gsheet_a = gsheet() 
    file = gsheet_a.readSheet()
    table = []
    for a in file :
        # print(a)
        row = Row(a["id"], a["url"], a["status"], a["mobile"], a["desktop"])
        table.append(row)
    return table

def define_unchecked_row(all_data) :
    """
    args: Array<row>
    return 更新した行
    Rowインスタンスの中からステータスが未実行の物の、スコアを取得する
    """
    updated_rows = []
    for row in all_data :
        if row.status == "" :
            print("checking reload time score for..." + row.url)
            row.mobile = load_score_from_url(row.url, 'mobile')
            row.desktop = load_score_from_url(row.url, 'desktop')
            updated_rows.append(row)
    return updated_rows

def load_score_from_url(target_url, device) :
    api_base = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed"
    url = api_base + "?url=" + target_url + "&strategy=" + device
    response = urllib.request.urlopen(url)
    score = response.read() # score の中身が json -> string型になってしまってる

    json_dict = json.loads(score)  # string型の json を 辞書型に変換
    score = json_dict["ruleGroups"]["SPEED"]["score"]      #例） #json_dict["ruleGroups"][0]["score"]
    print(target_url + ";" + device + ";" + str(score))
    return score


gsheet_b = gsheet()  
  
urls = load_urls()

updated_urls = define_unchecked_row(urls)
gsheet_b.override_score(updated_urls)

# print(updated_urls)








