import telegram
from bs4 import BeautifulSoup as bs
import requests as req
from time import sleep
import re

def get_sessions():
    '''
    TODO write doc
    '''

    # get ilug page html
    r = req.get(ilugurl)

    if r.ok:
        # get groups' this week session
        r.encoding = 'utf-8'
        source_code = bs(r.text, 'html.parser')
        main_group = source_code.find(id='main-group')
        sub_groups = source_code.find(id='sub-groups')

        # print [main_group.get_text().encode('utf8'), sub_groups.get_text().encode('utf8')]

        return [main_group.get_text().encode('utf8'), sub_groups.get_text().encode('utf8')]
    # TODO else


if __name__ == '__main__':
    # assign bot and ilug url
    global bot, ilugurl
    bot = telegram.Bot(token=open('ilugbot.token').read())
    ilugurl = 'http://drupal.isfahanlug.org/'

    commands = [
        {
            'match': r'^/sessions',
            'func': get_sessions
        }
    ]

    last_update_id_file = open('last-update.id', 'r+')
    last_update_id = int(last_update_id_file.read())

    # listen for command
    while True:
        # get updates
        updates = bot.getUpdates(offset=last_update_id)

        # update offset of last update
        if updates:
            last_update_id_file.seek(0)
            last_update_id = updates[-1].update_id + 1
            last_update_id_file.write(str(last_update_id))
            last_update_id_file.truncate()

        for update in updates:
            print update
            for command in commands:
                if re.search(command['match'], update.message.text):
                    for message in command['func']():
                        bot.sendMessage(update.message.chat.id, message)
                    break
            sleep(3)
