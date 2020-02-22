import telebot
import sqlite3

def get_db():
  def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
    return d

  db = sqlite3.connect('tgstories.db')
  db.row_factory = dict_factory
  return db

def initialize_db():
  print('initialize database')
  db = get_db()
  cursor = db.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS stories(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, name TEXT)')
  cursor.execute('''
      CREATE TABLE IF NOT EXISTS stories_tree(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_id INTEGER,
        leaf_id INTEGER,
        parent_leaf_id INTEGER,
        FOREIGN KEY(story_id) REFERENCES stories_tree(id),
        FOREIGN KEY(leaf_id) REFERENCES stories_tree_leaf(id),
        FOREIGN KEY(parent_leaf_id) REFERENCES stories_tree_leaf(id)
      )
    ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories_tree_leaf(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER,
        text TEXT,
        description TEXT
      )
  ''')
  db.commit()
  print('databse initialized')

def create_story(chat_id, name):
  db = get_db()
  cursor = db.cursor()
  cursor.execute('INSERT INTO stories (chat_id, name) VALUES(?, ?)', (chat_id, name))
  db.commit()

def get_stories(chat_id = ''):
  db = get_db()
  cursor = db.cursor()
  if chat_id == '':
    return cursor.execute('SELECT * FROM stories').fetchall()      
  return cursor.execute('SELECT * FROM stories WHERE chat_id = %d' % chat_id).fetchall()

initialize_db()

main_menu_buttons = telebot.types.ReplyKeyboardMarkup(True, True)
main_menu_buttons.row('Create new story', 'My stories', 'Global search')

bot = telebot.TeleBot('915497476:AAGDnk1DimGbiUdIwzI4sl7lhBOYxqx0ZJM')

print('bot started')

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, 'Hi in Stories adventure', reply_markup=main_menu_buttons)

@bot.message_handler(content_types=['text'])
def create_story_message(message):
  if message.text == 'Create new story':
    bot.send_message(message.chat.id, 'Send me name of your adventure')
  elif message.text == 'My stories':
    show_user_stories_list(message, can_remove=True)
  elif message.text == 'Global search':
    show_user_stories_list(message, can_remove=False)
  else:
    bot.send_message(message.chat.id, 'name of your adventure is %s' % message.text)
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
