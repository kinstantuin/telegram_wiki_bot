import requests
from bs4 import BeautifulSoup
import pandas as pd

import telebot


def get_image(wiki_site): 
    url = f"https://ru.wikipedia.org/wiki/{wiki_site}"
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    
    # check standart image in table
    r = soup.select('table.infobox img')
    if not r: 
        print('none 1')
        # if standart is missing, try check anoter imgage
        r = soup.select('div.thumbinner img')
        if not r: 
            print('none 2')
            list_of_kinds = list()
            lst_ul = soup.select('div.mw-parser-output ul > li > a')
            if lst_ul: 
                print('not none 1')
                try: 
                    for i in lst_ul:
                        list_of_kinds.append(i['title'])
                
                    return [str(make_message_from_list(list_of_kinds)), False]
                except:
                    return ["Попробуйте ввести название по-другому", False]
            else: 
                return ["Попробуйте ввести название по-другому", False]
        else:
            print('r2:')
            img = r[0]['src']
            r.clear()
            # print(img)
            return [f"https:{img}", True]
    else: 
        print('r1')
        img = r[0]['src']
        r.clear()
        # print(img)
        return [f"https:{img}", True]
    # print(r)
    
    # return f"https:{img}"

def get_describe(wiki_site): 
    url = f"https://ru.wikipedia.org/wiki/{wiki_site}"
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    describe_parse = soup.find('div', {'class':'mw-parser-output'})
    describe_parse = soup.find('p')
    # describe_parse = soup.select_one('div.mw-parser-output > p')
    
    # print(i)
    # print('i ===========')
    print()
    print('describe parse====================')
    print(describe_parse.get_text())
    print('describe parse====================')
    describe_parse = describe_parse.get_text()
    describe_parse = str(describe_parse)
    describe_parse.strip(' ')
    
    
    # for i in describe_parse: 
    #     print('=================')
    #     print(i['text'])
    # print(describe['text'])
    
    return describe_parse

def make_message_from_list(lst): 
    message = str("Попробуйте следующие запросы: \n ================================== \n")
    for i in lst: 
        message += f"{i} \n"
    return message


bot = telebot.TeleBot("5778347962:AAFAPihRl3t-sy0BQv8YEs2dXKTyRgGuNik");

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    describe = get_describe(message.text)
    print('|',describe, '|')
    img = get_image(message.text)

    if img[1] == True:
        print('from true')
        if describe: 
            bot.send_message(message.from_user.id, describe)
        elif describe == 'В Википедии нет статьи с таким названием.': 
            return
        bot.send_photo(message.from_user.id, img[0])
    else: 
        print("from false")
        bot.send_message(message.from_user.id, img[0])
    return

bot.polling(none_stop=True, interval=0, timeout=False)