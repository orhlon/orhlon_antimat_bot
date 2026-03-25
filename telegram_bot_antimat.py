#t.me/orhlon_antimat_bot
import csv
import telebot
from config import TOKEN


TRUSTED_GROUP=['orhlon_antimat_group',]
TRUSTED_PEOPLE=['orhlon']
bot = telebot.TeleBot(TOKEN)
print('bot accepted the token')

#СФОРМИРОВАТЬ ИЗ ФАЙЛА СЕТ
csv_file = 'word_black_list.csv'

the_set={''}
the_set.remove('')
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        the_set.add(row[0])
f.close()

#ПРИМИВНАЯ ПРОВЕРКА НА ОСНОВЫ
def primitive_check(s):
    pristavki = ['с', 'вы', 'на', 'под', 'по', 'о', 'от', 'у', 'долбо']
    korni = ['хуй', 'хуе', 'хуё', 'хуи', 'хул', 'пизд', 'пезд', 'пёзд', 'сук', 'суч', 'ебл', 'еба', 'ебу', 'бляд', 'блят', 'пидр', 'пидор', 'шлюх', 'шлюш']
    #s = "Ах вы, ебанные пидорасы! Выблядки, блять! Ебать вас, шлюхи пиздохуевы, хуями, да до одолбоебения! Хулиганы!"
    s = s.lower()
    splited = s.split()
    for i in splited:
        for a in korni:
            if a in i:
                return True
    return False

#ПРОВЕРИТЬ НА НАЛИЧИЕ ЛИШНЕГО
def is_it_fit_for_set(s):
    s=s.lower()
    unfit_chars=' ,./)(\\@?<>$!#%^&*-_=+`|:;\'][}{1234567890"'
    for i in s:
        if i in unfit_chars:
            return False
    if len(s)>30:
        return False
    return True

#ПРОВЕРИТЬ НА ПЛОХИЕ СЛОВА
def contains_curse_words(s, the_set):
    def listate(s):
        listik=[]
        ctr = 0
        temp_str=''
        for i in s:
            if i not in unfit_chars:
                temp_str+=i
            else:
                listik.append(temp_str)
                listik.append(i)
                temp_str=''
            ctr +=1
        return listik
    unfit_chars=' ,./)(\\@?<>$!#%^&*-_=+`|:;\'][}{\124567890"'
    result_string=''
    orig_str=s+' '
    s=s.lower()+' '
    orig_str_list=listate(orig_str)
    s_list=listate(s)

    ctr=0
    for i in orig_str_list:
        if s_list[ctr] in the_set:
            orig_str_list[ctr]='(beep)'
        ctr+=1

    for i in orig_str_list:
        result_string += i
    return result_string


@bot.message_handler(content_types=['text', ])
def watch_messages(message: telebot.types.Message):
    CHATID = message.chat.id
    POSTID = message.id
    POSTTEXT=message.text
    CHATNAME=message.chat.title
    ISBOT=message.from_user.is_bot
    WHO=message.from_user.username
    print('message: ', POSTTEXT, CHATNAME, WHO)
    if primitive_check(POSTTEXT):
        bot.reply_to(message, 'сообщение ' + WHO + ' удалено by orhlon_antimat_bot')
        bot.delete_message(CHATID, POSTID)
    else:
        filtered = contains_curse_words(POSTTEXT, the_set)
        if POSTTEXT+' ' != filtered:
            bot.reply_to(message, 'сообщение ' + WHO + ' удалено by orhlon_antimat_bot')
            bot.delete_message(CHATID, POSTID)

    if POSTTEXT =='ligma_help':
        bot.reply_to(message, 'Доступные команды:\nligma_forbid "слово"\nligma_allow "слово"\nligma_list "п"')
    if Ture: #CHATNAME in TRUSTED_GROUP or CHATID in TRUSTED_GROUP:

#ПОКАЗАТЬ КОМАНДЫ
#ДОБВАИТЬ СЛОВО В СПИСОК
        if POSTTEXT[:13] =='ligma_forbid ':
            toadd=POSTTEXT[13:]
            toadd=toadd.lower()
            if is_it_fit_for_set(toadd):
                if toadd not in the_set:
                    the_set.add(toadd)
                    bot.reply_to(message, 'Слово добавлено в чёрный список')
                    with open(csv_file, 'a', encoding='utf-8') as f:
                        f.write(toadd+'\n')
                        print('ЗАПИСАНО В ФАЙЛ')
                    f.close()
            else:
                bot.reply_to(message, 'В слове недопустимые знаки или пробелы')
#УДАЛИТЬ СЛОВО ИЗ СПИСКА
        if POSTTEXT[:12] =='ligma_allow ':
            listik=[]
            todelete=POSTTEXT[12:]
            todelete=todelete.lower()
            if todelete not in the_set:
                bot.reply_to(message, 'Такого слова нет в чёрном списке')
            else:
                the_set.remove(todelete)
                with open(csv_file, 'r', encoding='utf-8') as f:
                    for i in f:
                        if i != todelete+'\n':
                            listik.append(i)

                with open(csv_file, 'w', encoding='utf-8') as f:
                    f.writelines(listik)
                f.close()
                print('УДАЛЕНО ИЗ ФАЙЛА')


                bot.reply_to(message, 'Слово удалено из чёрного списка')
#ПОКАЗАТЬ ЧЕРНЫЙ СПИСОК
        if POSTTEXT[:10] =='ligma_list':

            if POSTTEXT=='ligma_list':
                bot.reply_to(message, 'Нужно добавить букву для поиска')
            else:

                toshow=POSTTEXT[11:]
                toshow=toshow.lower()
                if len(toshow)==1:
                    toshow_str=''
                    for i in the_set:
                        if i[0]==toshow:
                            toshow_str+=i
                            toshow_str+=', '
                    bot.reply_to(message, toshow_str)

                else:
                    bot.reply_to(message, 'Должна быть лишь одна буква')
#ПРИВЕТСТВИЕ
        if POSTTEXT.lower() =='/start':
            bot.reply_to(message, '@orhlon_antimat_bot - это уникальный "антимат" бот с изменяемым чёрным списком. Любой пользователь может добавлять и убирать слова из списка. Для инструкции напишите /help.')

#ХЕЛП
        if POSTTEXT.lower() =='/help':
            bot.reply_to(message, 'Для фильтрации сообщений групп, добавьте бота в администраторы своей группы с правами на управление сообщениями.\n\nДля того, чтобы изменить базу черного списка, необходимо вводить команды в группе @orhlon_antimat_group.\n\nДоступные команды:\nligma_forbid слово (добавить слово в чёрный список)\nligma_allow слово (удалить слово из черного списка)\nligma_list п (отобразить слова черного списка на данную букву)')


bot.infinity_polling()
