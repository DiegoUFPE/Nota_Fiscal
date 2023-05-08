import openai
import time


API_KEY = open("chatgpt_API_key","r").read()
openai.api_key = API_KEY

#Os principais grupos de gasto referentes ao IPCA:
#Transporte; Alimentação e bebidas; Habitação; Saúde e cuidados pessoais; Despesas Pessoais.

#Foi selecionado um representante de cada uma dessas classes 

prods_dict = {
            "Gasoline":"liter",
            "Bread Roll":"kg",
            "Electricity":"watt",
            "Medicine":"ml",
            "Cosmetics":"unit"
              }

chat_log = []

for i,j in prods_dict.items():
    user_message = "can you generate a json code with the medium price of the " +j+ " of "+i+ " in pernambuco in each month from january to april 2023 with only the keys 'month' and 'price'? If there are no real informations yet, please generate a simulation to these values."
    chat_log.append({"role":"user","content":user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']
    start = assistant_response.find("{")
    end = assistant_response.rfind("}")
    json_string = assistant_response[start:end+1]
    with open(i+'.json', 'w') as outfile:
        outfile.write(json_string)
    time.sleep(20)
