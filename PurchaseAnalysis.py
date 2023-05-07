import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt
import numpy as np 

class PurchaseAnalysis:

    def __init__(self) -> None:
        pass

    def func(pct, allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return "{:.1f}%\n({:d} g)".format(pct, absolute)

    def generate_pie_graph(self,out:dict,text:str):
        plt.figure(figsize =(20, 8)) 
        labels = [i.split(";")[0] for i in out.keys()]
        plt.pie(out.values(), labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')

        plt.savefig(text+'.png')

    def get_analysis(self,purchase_dict:dict,isYearly:bool,isMonthly:bool):
        df = pd.DataFrame(data = purchase_dict)
        if isYearly:
            for i in set(set(df["Ano"])):
                filter = df['Ano'] == i
                df_grouped = df[filter]
                df_grouped = dict(df_grouped.groupby(by="Sessão")["Preço"].sum())
                dict_sorted = {item:round(df_grouped[item],2) for item in sorted(df_grouped, key = df_grouped.get, reverse = True)}
                out = dict(islice(dict_sorted.items(), 4))

                sum = 0.0
                for j,k in zip(dict_sorted.values(),range(len(dict_sorted.values()))):
                    if k > 4:
                        sum += j
                if sum != 0:
                    out['Outros'] = round(sum,2)
                print(out)

                self.generate_pie_graph(out,"purchase_analysis_"+str(i))

        elif isMonthly: 
            lastyear = max(set(df["Ano"]), key=int)
            filter = df['Ano'] == lastyear
            df_aux = df[filter]
            for i in set(df_aux["Mês"]):
                filter = df_aux['Mês'] == i
                df_grouped = df_aux[filter]
                df_grouped = dict(df_grouped.groupby(by="Sessão")["Preço"].sum())
                dict_sorted = {item:round(df_grouped[item],2) for item in sorted(df_grouped, key = df_grouped.get, reverse = True)}
                out = dict(islice(dict_sorted.items(), 4))

                sum = 0.0
                for j,k in zip(dict_sorted.values(),range(len(dict_sorted.values()))):
                    if k > 4:
                        sum += j
                if sum != 0:
                    out['Outros'] = round(sum,2)

                self.generate_pie_graph(out,"purchase_analysis_"+str(lastyear)+"month_"+str(i))

        else:
            df_grouped = dict(df.groupby(by="Sessão")["Preço"].sum())
            dict_sorted = {item:round(df_grouped[item],2) for item in sorted(df_grouped, key = df_grouped.get, reverse = True)}
            out = dict(islice(dict_sorted.items(), 4))

            sum = 0.0
            for j,k in zip(dict_sorted.values(),range(len(dict_sorted.values()))):
                if k > 4:
                    sum += j
            if sum != 0:        
                out['Outros'] = round(sum,2)

            self.generate_pie_graph(out,"purchase_analysis_general")
  

        
        
