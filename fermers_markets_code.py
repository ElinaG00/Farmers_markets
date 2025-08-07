import math

IN_FILE_NAME = 'Export.csv'

OUT_FILE_NAME_1 = 'markets.csv'
OUT_FILE_NAME_2 = 'states.csv'
OUT_FILE_NAME_3 = 'county.csv'
OUT_FILE_NAME_4 = 'address_market.csv'
OUT_FILE_NAME_5 = 'pay.csv'
OUT_FILE_NAME_6 = 'markets_pay.csv'
OUT_FILE_NAME_7 = 'categorias.csv'
OUT_FILE_NAME_8 = 'market_categories.csv'

file_1 = open(OUT_FILE_NAME_1, 'w', encoding='utf-8')
file_2 = open(OUT_FILE_NAME_4, 'w', encoding='utf-8')
file_3 = open(OUT_FILE_NAME_6, 'w', encoding='utf-8')
file_4 = open(OUT_FILE_NAME_8, 'w', encoding='utf-8')


id = 0
cities = set()
cities_dict = dict()
cities_dict_rev = dict()
row_count = 0
county = dict()
county_id = 0
states = dict()
states_id = 0
name_of_pay = dict()
pay_id = 0
categorias_name = dict()
categorias_id = 0
markets_pay_id = 0
pay_id_2 = 0
market_categories_id = 0
categorias_id_2 =0 
for line in open(IN_FILE_NAME, 'r', encoding='utf-8'):
    if row_count == 0:
        p = line.split(',')[23:28]
        for i in range(len(p)):
            if p[i] not in name_of_pay:
                name_of_pay[i+1] = p[i]
                pay_id += 1
        c = line.split(',')[28:58]
        for i in range(len(c)):
            if c[i] not in categorias_name:
                categorias_name[i+1] = c[i]
                categorias_id += 1       
        row_count += 1
        continue
    idx = 0
    quoted = False
    start = 0
    record = []
    while idx < len(line):
        char = line[idx]
        #print(char)
        if char == '"':
            quoted = not quoted
        if char == ',' and not quoted:
            #print()
            record.append(line[start:idx])
            start = idx + 1
        idx += 1
    row_count += 1
    record = [rec.strip() for rec in record]

    #print(record)
    if record[9] not in county:
        county[record[9]] = county_id
        county_id += 1
    if record[10] not in states:
        states[record[10]] = states_id
        states_id += 1

    fmid, market_name, website, facebook, twitter, youtube, other_media = record [:7]
    fmid = record[0].strip()
    street = record[7]
    zip = record[11]
    file_1.write(f'{fmid},{market_name},{website},{facebook},{twitter},{youtube},{other_media}\n')
    #if fmid == '1018261':
        #print('market fmid:', fmid)
    file_2.write(f'{fmid},{street},{county_id},{states_id},{zip}\n')

    #pay
    dic_1 = {record[23]: 1, record[24]: 2, record[25]: 3, record[26]: 4, record[27]:5}
    for i in record[23:28]:
        
        if i == "Y":
            markets_pay_id += 1
            pay_id_2 = dic_1[i]
            #if fmid == '1018261':
                #print('pay fmid:', fmid)
            file_3.write(f'{markets_pay_id},{fmid},{pay_id_2}\n')

  
    #market_categorias
    dic_2 = {}
    j=1
    for i in record[28:58]:
        dic_2[i] = j
        j +=1
        if i == "Y":
            market_categories_id += 1
            categorias_id_2 = dic_2[i]
            file_4.write(f'{market_categories_id},{fmid},{categorias_id_2}\n')
    # for i in record[28:58]:
    #     for categorias_id, name in categorias_name.items():
    #         if i == "Y":
    #             categorias_id_2 = categorias_id
    #             market_categories_id += 1
    #             file_4.write(f'{market_categories_id},{fmid},{categorias_id_2}\n')
    #             print(i)


    # market_categories_id += 1
    # categorias_id_2 += 1
    # file_4.write(f'{market_categories_id},{fmid},{categorias_id_2}\n')


file_1.close()
file_2.close()
file_3.close()
file_4.close()

file = open(OUT_FILE_NAME_2, 'w', encoding='utf-8')
for states, id in states.items():
    file.write(f'{id+1},{states}\n')
file.close()

file = open(OUT_FILE_NAME_3, 'w', encoding='utf-8')
for county, id in county.items():
    file.write(f'{id+1},{county}\n')
file.close()

file = open(OUT_FILE_NAME_5, 'w', encoding='utf-8')
for id, pay in name_of_pay.items():
    file.write(f'{id},{pay}\n')
file.close()

file = open(OUT_FILE_NAME_7, 'w', encoding='utf-8')
for id, categorias in categorias_name.items():
    file.write(f'{id},{categorias}\n')
file.close()



    
   




