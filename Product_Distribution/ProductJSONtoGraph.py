import json
import pandas as pd
import matplotlib.pyplot as plt
  
def generate_graph(m:list,col:list,text:str):
    print(text)
    print(m)
    print(col)
    
    df = pd.DataFrame(
        { 'Month' : m , 
        'Price': col })

    fig = df.plot(x = 'Price' , y = 'Month', title = text,  figsize=(20, 16), fontsize=26).get_figure()
    fig.savefig(text+'.png')

    
def read_JSON(data:list):
    labels = []
    values = []
    for i in data:
        labels.append(i['month'])
        values.append(i['price'])
    return labels,values

with open('Gasoline.json') as json_file:
    data = json.load(json_file)

labels,values = read_JSON(data.values())

generate_graph(values,labels,"Gasolina_por_litro")


with open('Bread Roll.json') as json_file:
    data = json.load(json_file)

data = data['prices']
labels,values = read_JSON(data)

generate_graph(values,labels,"Pão_Francês_por_kg")


with open('Electricity.json') as json_file:
    data = json.load(json_file)

data = data['prices']
labels,values = read_JSON(data)

generate_graph(values,labels,"Eletricidade_por_watt")


with open('Medicine.json') as json_file:
    data = json.load(json_file)

data = data['prices']
labels,values = read_JSON(data)

generate_graph(values,labels,"Medicamentos_por_ml")


with open('Cosmetics.json') as json_file:
    data = json.load(json_file)


labels = [i for i in data.keys()]
values = [i for i in data.values()]

generate_graph(values,labels,"Cosméticos_por_unidade")