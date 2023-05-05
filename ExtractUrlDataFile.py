
import requests
import pandas as pd
from urllib.parse import urlparse
import xmltodict


class ExtractUrlData():

    #url = 'http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p=26230461585865160353650080005246131848088489|2|1|1|311263B23AA9F2062663B95C752C14D2B01DC911'

    def __init__(self, url:str):
        self.__url = url
        self.dict_type = {
            str(type([])):'list',
            str(type({})):'dict'
        }
        self.keys_flow = ['nfeProc','proc','nfeProc','NFe','infNFe','det']
        self.interest_dict = {}
        self.prods = []
        self.ref_domain = 'nfce.sefaz.pe.gov.br' #creating a reference domain to compare the url extracted from the QR Code.

    def get_Url(self):
        return self.__url
    
    def set_Url(self,url:str):
        self.__url = url

    def get_page(self):
        return requests.get(self.__url)
    
    def get_domain(self):
        return urlparse(self.__url).netloc
    
    def evaluate_domain(self):
        return (self.ref_domain == self.get_domain())

    def get_section(self,s:int):
        if (s <= 5 and s >= 1):
            section = 'ANIMAIS VIVOS E PRODUTOS DO REINO ANIMAL'
        elif (s <= 14 and s >= 6):
            section = 'PRODUTOS DO REINO VEGETAL '
        elif (s >= 15 and s <= 15):
            section = 'GORDURAS E ÓLEOS ANIMAIS, VEGETAIS OU DE ORIGEM MICROBIANA E PRODUTOS DA SUA DISSOCIAÇÃO; GORDURAS ALIMENTÍCIAS ELABORADAS; CERAS DE ORIGEM ANIMAL OU VEGETAL'
        elif (s >= 16 and s <= 24):
            section = 'PRODUTOS DAS INDÚSTRIAS ALIMENTARES; BEBIDAS, LÍQUIDOS ALCOÓLICOS E VINAGRES; TABACO E SEUS SUCEDÂNEOS MANUFATURADOS; PRODUTOS, MESMO COM NICOTINA, DESTINADOS À INALAÇÃO SEM COMBUSTÃO; OUTROS PRODUTOS QUE CONTENHAM NICOTINA DESTINADOS À ABSORÇÃO DA NICOTINA PELO CORPO HUMANO'
        elif (s >= 25 and s <= 27):
            section = 'PRODUTOS MINERAIS'
        elif (s >= 28 and s <= 38):
            section = 'PRODUTOS DAS INDÚSTRIAS QUÍMICAS OU DAS INDÚSTRIAS CONEXAS'
        elif (s >= 39 and s <= 40):
            section = 'PLÁSTICO E SUAS OBRAS; BORRACHA E SUAS OBRAS'
        elif (s >= 41 and s <= 43):
            section = 'PELES, COUROS, PELES COM PELO E OBRAS DESTAS MATÉRIAS; ARTIGOS DE CORREEIRO OU DE SELEIRO; ARTIGOS DE VIAGEM, BOLSAS E ARTIGOS SEMELHANTES; OBRAS DE TRIPA'
        elif (s >= 44 and s <= 46):
            section = 'MADEIRA, CARVÃO VEGETAL E OBRAS DE MADEIRA; CORTIÇA E SUAS OBRAS; OBRAS DE ESPARTARIA OU DE CESTARIA'
        elif (s >= 47 and s <= 49):
            section = 'PASTAS DE MADEIRA OU DE OUTRAS MATÉRIAS FIBROSAS CELULÓSICAS; PAPEL OU CARTÃO PARA RECICLAR (DESPERDÍCIOS E RESÍDUOS); PAPEL OU CARTÃO E SUAS OBRAS'
        elif (s >= 50 and s <= 63):
            section = 'MATÉRIAS TÊXTEIS E SUAS OBRAS'
        elif (s >= 64 and s <= 67):
            section = 'CALÇADO, CHAPÉUS E ARTIGOS DE USO SEMELHANTE, GUARDA-CHUVAS, GUARDA-SÓIS, BENGALAS, CHICOTES, E SUAS PARTES; PENAS PREPARADAS E SUAS OBRAS; FLORES ARTIFICIAIS; OBRAS DE CABELO'
        elif (s >= 68 and s <= 70):
            section = 'OBRAS DE PEDRA, GESSO, CIMENTO, AMIANTO, MICA OU DE MATÉRIAS SEMELHANTES; PRODUTOS CERÂMICOS; VIDRO E SUAS OBRAS'
        elif (s >= 71 and s <= 71):
            section = 'PÉROLAS NATURAIS OU CULTIVADAS, PEDRAS PRECIOSAS OU SEMIPRECIOSAS E SEMELHANTES, METAIS PRECIOSOS, METAIS FOLHEADOS OU CHAPEADOS DE METAIS PRECIOSOS (PLAQUÊ), E SUAS OBRAS; BIJUTERIAS; MOEDAS'
        elif (s >= 72 and s <= 83):
            section = 'METAIS COMUNS E SUAS OBRAS'
        elif (s >= 84 and s <= 85):
            section = 'MÁQUINAS E APARELHOS, MATERIAL ELÉTRICO, E SUAS PARTES; APARELHOS DE GRAVAÇÃO OU DE REPRODUÇÃO DE SOM, APARELHOS DE GRAVAÇÃO OU DE REPRODUÇÃO DE IMAGENS E DE SOM EM TELEVISÃO, E SUAS PARTES E ACESSÓRIOS'
        elif (s >= 86 and s <= 89):
            section = 'MATERIAL DE TRANSPORTE'
        elif (s >= 90 and s <= 92):
            section = 'INSTRUMENTOS E APARELHOS DE ÓPTICA, DE FOTOGRAFIA, DE CINEMATOGRAFIA, DE MEDIDA, DE CONTROLE OU DE PRECISÃO; INSTRUMENTOS E APARELHOS MÉDICO-CIRÚRGICOS; ARTIGOS DE RELOJOARIA; INSTRUMENTOS MUSICAIS; SUAS PARTES E ACESSÓRIOS'
        elif (s >= 93 and s <= 93):
            section = 'ARMAS E MUNIÇÕES; SUAS PARTES E ACESSÓRIOS'
        elif (s >= 94 and s <= 96):
            section = 'MERCADORIAS E PRODUTOS DIVERSOS'
        elif (s >= 97 and s <= 97):
            section = 'OBJETOS DE ARTE, DE COLEÇÃO E ANTIGUIDADES'
        else:
            section = 'NÃO DEFINIDO'
        return section

    def get_prods_from_dict(self):
      if(bool(self.interest_dict)):
        if self.dict_type[str(type(self.interest_dict))] == 'list':
            for i in self.interest_dict:
                self.prods.append({
                    'Nome':i['prod']['xProd'],
                    'Preço':i['prod']['vProd'],
                    'NCM':i['prod']['NCM'],
                    'Sessão':self.get_section(int(i['prod']['NCM'][0:2]))
                })
        elif self.dict_type[str(type(self.interest_dict))] == 'dict':
            self.prods.append({
                'Nome':self.interest_dict['prod']['xProd'],
                'Preço':self.interest_dict['prod']['vProd'],
                'NCM':self.interest_dict['prod']['NCM'],
                'Sessão':self.get_section(int(self.interest_dict['prod']['NCM'][0:2]))
            })
        return self.prods
      else:
          return self.prods
    
    def get_info_dict(self):
        page = self.get_page()
        if page.status_code == 200:
            my_dict =  xmltodict.parse(page.text)
            aux = my_dict
            for i in self.keys_flow:
                if i=='proc' and 'protNFe' in aux:
                    t = aux['protNFe']['infProt']['dhRecbto'].split("T")[0]
                    t = t.split("-")
                    self.date = t[2]+'/'+t[1]+'/'+t[0]
                    #print(date)
                if i=='det' and 'emit' in aux:
                    self.place = aux['emit']['xNome']
                if i in aux:
                    aux = aux[i]
                    self.interest_dict = aux
                else:
                    #print("The format is not valid for extracting products.")
                    self.interest_dict = {}
                    self.prods=self.get_prods_from_dict()
                    return self.date,self.place,self.prods,False
            self.prods=self.get_prods_from_dict()
            return self.date,self.place,self.prods,True
        else:
            #print("The page does not allow data extraction.")
            self.prods=self.get_prods_from_dict()
            return self.date,self.place,self.prods,False
        