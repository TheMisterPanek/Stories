import telebot
from db import create_story, get_stories

main_menu_buttons = telebot.types.ReplyKeyboardMarkup(True, True)
main_menu_buttons.row('Create new story', 'My stories', 'Global search')

bot = telebot.TeleBot('915497476:AAGDnk1DimGbiUdIwzI4sl7lhBOYxqx0ZJM')

print('bot started')

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(
    message.chat.id,
    'Hi in Stories adventure',
    reply_markup=main_menu_buttons
  )

@bot.message_handler(content_types=['text'])
def create_story_message(message):
  if message.text == 'Create new story':
    bot.send_message(message.chat.id, 'Send me name of your adventure')
  elif message.text == 'My stories':
    show_user_stories_list(message, can_remove=True)
  elif message.text == 'Global search':
    show_user_stories_list(message, can_remove=False)
  else:
    bot.send_message(
      message.chat.id,
      'name of your adventure is %s' % message.text
    )
    create_story(message.chat.id, message.text)
    print('New story "%s" is created' % message.text)

def show_user_stories_list(message, can_remove):
    markup = telebot.types.InlineKeyboardMarkup()
    stories = get_stories(message.chat.id if can_remove else '')
    for story in stories:
      if can_remove:
        markup.add(
          telebot.types.InlineKeyboardButton(text=story['name'],callback_data='1'),
          telebot.types.InlineKeyboardButton(text='X', callback_data='2'))
      else:
        markup.add(telebot.types.InlineKeyboardButton(text=story['name'],callback_data='1'))
    bot.send_message(message.chat.id, 'List of your stories:', reply_markup=markup)

@bot.message_handler(content_types=['voice'])
def get_audio(usr_msg):
  print('got audio: %s' % usr_msg.voice)
  bot.send_voice(usr_msg.chat.id, usr_msg.voice.file_id)

bot.polling()
