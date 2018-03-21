# -*- coding:utf-8 -*-
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
#from ファイル名 (.py前) import 関数名（引数なし）

class gsheet:
    def __init__(self) :
        self.sheet = self.logIn()
    
    def logIn(self):
        doc_id = '1HIONhiBHTqlrt7lTKDa1daQ-2vowxaZ3Gdlo3d26Jws'
    
        # 先ほどDLしたJSONをロード
        json_key    = json.load(open('key.json'))
        scope       = ['https://spreadsheets.google.com/feeds']
    
        # credentialsを取得
        credentials = SignedJwtAssertionCredentials(
                        json_key['client_email'], 
                        json_key['private_key'].encode(), 
                        scope)
    #user
        gclient = gspread.authorize(credentials)
        #specify a file
        gfile   = gclient.open_by_key(doc_id)
        #sheet tab
        wsheet  = gfile.get_worksheet(0)
        return wsheet
    
    def readSheet(self):
        records = self.sheet.get_all_records() 
        return records
    
    def override_score(self, results) :
        for row in results :
            
            self.sheet.update_cell(row.id + 1, 4, row.mobile)
            self.sheet.update_cell(row.id + 1, 5, row.desktop)
            
            self.sheet.update_cell(row.id + 1, 3, 'done') 


        #self.sheet.update_cell(self.sheet.get_addr_int(row, col), 'Done')  
        #status = self.sheet.find("status")
        #self.sheet.get_addr_int(row, col)
        #self.sheet.update_cell(1,1, 'Hello, sheet.')  # 行、列、値


