import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ReadWriteGoogleSheet:
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self,prods=[],date=""):
        self.prods = prods
        self.date = date

        self.creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\sofia\\final_project_tecnicas_v2\\google_API_key.json",scopes=self.scopes)

        self.file = gspread.authorize(self.creds)
        self.workbook = self.file.open("Purchase_Data")
        self.sheet = self.workbook.sheet1
        self.dict_sheet = {}

    def get_dict_sheet(self):
        return self.sheet.get_all_records()
    
    def create_content_list(self,prod:dict):
         return [prod['Nome'],prod['Preço'],int(self.date.split("/")[0]),int(self.date.split("/")[1]),int(self.date.split("/")[2]),prod['Sessão']]
    
    def evaluate_input(self,prod:dict):
        prod_info = {
            "Nome":prod["Nome"],
            "Preço":float(prod["Preço"]),
            "Dia":int(self.date.split("/")[0]),
            "Mês":int(self.date.split("/")[1]),
            "Ano":int(self.date.split("/")[2]),
            "Sessão":prod["Sessão"]
        }
        #print("prod_info: ")
        #print(prod_info)
        for i in self.dict_sheet:
            #print("element from dict_sheet:")
            #print(i)
            if i == prod_info:
                return False
        return True

    def update_sheet(self):
        self.dict_sheet = self.get_dict_sheet()
        tam = len(self.dict_sheet)
        verify = 0
        for i in self.prods:
            if not self.evaluate_input(i):
                verify+=1
        if verify != len(self.prods):
            for i in self.prods:
                content_list = self.create_content_list(i)
                interval = 'A'+str(tam+2)+':F'+str(tam+2)
                tam+=1
                self.sheet.update(interval,[content_list])
            return True
        else:    
            return False
        
