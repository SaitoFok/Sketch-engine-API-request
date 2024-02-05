import requests
import pandas as pd
import numpy as np

USERNAME = 'saitofok' # 用户名
API_KEY = '77d017d000cde5d006bc1aaa21be6150' 
base_url = 'https://api.sketchengine.eu/bonito/run.cgi' #根据要查询的语料库不同而修改

vocab_path = './input.xlsx'
output_path = './output.txt'

input_excel = pd.read_excel(vocab_path, sheet_name="B")

# 读取此表，存为list
word_list = []
for ss in input_excel.values.tolist():
    for s in ss:
        if s != None:
            word_list.append(s)
word_list = [x for x in word_list if not pd.isna(x)]
print(len(word_list))
word_list = list(set(word_list)) # 去重
print(len(word_list))

# output_result = pd.DataFrame(columns=["Word", "MI值", "Logdice值", "词频值"])
# 获取MI值
# for word in word_list:
#     data_conc = {
#     'corpname': 'preloaded/zhtenten17_simplified_stf2',
#     'format': 'json',
#     'q': 'q[word="'+ word +'"]'
#     }

#     try:
#         d_conc = requests.get(base_url + '/collx?corpname=%s' % data_conc['corpname'], params=data_conc, auth=(USERNAME, API_KEY)).json()
#         MI_value = d_conc['Items'][0]['Stats'][1]['s']
#         print(word + '的MI值为：' + d_conc['Items'][0]['Stats'][1]['s'])
#         output_result = pd.concat([output_result, pd.DataFrame({'word': word, 'MI_value': MI_value}, index=[0])], ignore_index=True)
#     except:
#         print("无法找到"+word)
#         continue

# # 获取LogDice值
# for i, word in enumerate(output_result['Word']):
#     data_conc = {
#     'corpname': 'preloaded/zhtenten17_simplified_stf2',
#     'format': 'json',
#     'q': 'q[word="'+ word +'"]'
#     }

#     try:
#         d_conc = requests.get(base_url + '/collx?corpname=%s' % data_conc['corpname'], params=data_conc, auth=(USERNAME, API_KEY)).json()
#         print(word + '的Logdice值为：' + d_conc['Items'][0]['Stats'][2]['s'])
#         logdice_value = d_conc['Items'][0]['Stats'][2]['s']
#         output_result.loc[i, 'Logdice值'] = logdice_value
#     except:
#         print("无法找到"+word)
#         continue

# 获取单个词频
# for i, word in enumerate(output_result['Word']):
for word in word_list:
    data_conc = {
    'corpname': 'preloaded/zhtenten17_simplified_stf2',
    'format': 'json',
    'q': 'q[word="'+ str(word) +'"]'
    }

    try:
        # freq
        d_conc = requests.get(base_url + '/view?corpname=%s' % data_conc['corpname'], params=data_conc, auth=(USERNAME, API_KEY)).json()
        concsize = d_conc['concsize']
        print(str(word) + "的词频为：" + str(concsize))
        with open('./output.txt', 'a') as f:
            f.write(str(word) + '\t' + str(concsize) + '\t')
        # output_result.loc[i, '词频值'] = concsize
        # MI values
        # d_conc = requests.get(base_url + '/collx?corpname=%s' % data_conc['corpname'], params=data_conc, auth=(USERNAME, API_KEY)).json()
        # MI_value = d_conc['Items'][0]['Stats'][1]['s']
        # print(word + '的MI值为：' + d_conc['Items'][0]['Stats'][1]['s'])
        # logdice values 
        d_conc = requests.get(base_url + '/collx?corpname=%s' % data_conc['corpname'], params=data_conc, auth=(USERNAME, API_KEY)).json()
        logdice_value = d_conc['Items'][0]['Stats'][2]['s']
        print(str(word) + '的Logdice值为：' + str(logdice_value))
        with open('./output.txt', 'a') as f:
            f.write(str(logdice_value))
    except:
        print("无法找到"+word)
        continue

    with open(output_path, 'a') as f:
        f.write('\n')

# output_result.to_excel('all_output_result.xlsx', index=False)

# # 获取多个词频
# data_wordlist = {
#     'corpname': 'preloaded/zhtenten17_simplified_stf2',
#     'format': 'json',
#     'wltype': 'simple',
#     'wlattr': 'word',
#     'wlfile': ['开心\n朋友\n医生']
# }

# d_wordlist = requests.get(base_url + '/wordlist?corpname=%s' % data_wordlist['corpname'], params=data_wordlist, auth=(USERNAME, API_KEY)).json()
# print(d_wordlist['Items'])
