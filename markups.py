import telebot
from telebot import types


def menu_markup(chat_id, admin):
    MENU_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
    MENU_MARKUP.add(types.KeyboardButton('Частые вопросы'), types.KeyboardButton('Льготы'), types.KeyboardButton('Материальная помощь'),
                    types.KeyboardButton('Вита'), types.KeyboardButton('СКС Бонус'),
                    types.KeyboardButton('Контакты'), types.KeyboardButton('Связаться с председателем ППОС'))
    if chat_id == admin:
        MENU_MARKUP.add(types.KeyboardButton("Прочитать обращения"), types.KeyboardButton("Ответить на обращение"))
    return MENU_MARKUP


ADMIN_MENU_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
ADMIN_MENU_MARKUP.add(types.KeyboardButton('Частые вопросы'), types.KeyboardButton('Льготы'),
                      types.KeyboardButton('Материальная помощь'), types.KeyboardButton('Вита'),
                      types.KeyboardButton('СКС Бонус'), types.KeyboardButton('Контакты'),
                      types.KeyboardButton('Связаться с председателем ППОС'), types.KeyboardButton('Ответить на обращение'),
                      types.KeyboardButton('Прочитать обращения'))


MAT_HELP_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
MAT_HELP_MARKUP.add(types.KeyboardButton('Инструкция'), types.KeyboardButton('В начало'))


CHOICE_EXAMPLE_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
CHOICE_EXAMPLE_MARKUP.add(types.KeyboardButton('Для бюджета'), types.KeyboardButton('Для контракта'),
                          types.KeyboardButton('В начало'))


CKC_BONUS_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
CKC_BONUS_MARKUP.add(types.KeyboardButton('Что это?'), types.KeyboardButton('Где скачать?'),
                     types.KeyboardButton('Как зарегистрироваться?'), types.KeyboardButton('В начало'))

INLINE_KEYBOARD_LINKS = types.InlineKeyboardMarkup()
INLINE_KEYBOARD_LINKS.add(types.InlineKeyboardButton(text='Google Play',
                                                     url='https://play.google.com/store/apps/details?id=com.gorbin.sks&hl=ru&gl=US'),
                          types.InlineKeyboardButton(text='App Store',
                                                     url='https://apps.apple.com/ru/app/%D1%81%D0%BA%D1%81-%D1%80%D1%84/id1473711942'))

QUESTION_TORIC_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
QUESTION_TORIC_MARKUP.add(types.KeyboardButton('Материальная помощь'), types.KeyboardButton('Социальная степендия'),
                          types.KeyboardButton('В начало'))

MAT_QUESTIONS_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
MAT_QUESTIONS_MARKUP.add(types.KeyboardButton('1'), types.KeyboardButton('2'), types.KeyboardButton('3'),
                              types.KeyboardButton('4'), types.KeyboardButton('5'), types.KeyboardButton('6'),
                              types.KeyboardButton('7'), types.KeyboardButton('8'), types.KeyboardButton('9'))
MAT_QUESTIONS_MARKUP1 = types.ReplyKeyboardMarkup()
MAT_QUESTIONS_MARKUP1.add(types.KeyboardButton('Примеры заявлений'), types.KeyboardButton('К вопросам'))
MAT_QUESTIONS_MARKUP9 = types.InlineKeyboardMarkup()
MAT_QUESTIONS_MARKUP9.add(types.InlineKeyboardButton(text='Алгоритм', url='https://vk.com/pos_kemsu?w=wall-776924_4793'))

SOC_QUESTIONS_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
SOC_QUESTIONS_MARKUP.add(types.KeyboardButton('1'), types.KeyboardButton('2'), types.KeyboardButton('3'),
                         types.KeyboardButton('4'), types.KeyboardButton('5'), types.KeyboardButton('6'))

SOC_QUESTIONS_MARKUP1 = types.InlineKeyboardMarkup()
SOC_QUESTIONS_MARKUP1.add(types.InlineKeyboardButton(text='Председатель профкома', url='https://vk.com/id42695847'))
SOC_QUESTIONS_MARKUP5 = types.InlineKeyboardMarkup()
SOC_QUESTIONS_MARKUP5.add(types.InlineKeyboardButton(text='Положение',
                                                     url='https://kemsu.ru/upload/university/document/student_support_statute.pdf'))

PRIVILEGES_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
PRIVILEGES_MARKUP.add(types.KeyboardButton('ДМС'), types.KeyboardButton('Целевая субсидия'), types.KeyboardButton('Проезд'),
                      types.KeyboardButton('Общежития'), types.KeyboardButton('Прочие льготы'), types.KeyboardButton('В начало'))
PRIVILEGES_DMS_MARKUP = types.InlineKeyboardMarkup()
PRIVILEGES_DMS_MARKUP.add(types.InlineKeyboardButton(text='гугл форма', url='https://vk.com/away.php?to=https%3A%2F%2Fforms.gle%2Fxk1fNJnwHSdZH8vCA&cc_key='))

TARGET_SUBSIDY_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
TARGET_SUBSIDY_MARKUP.add(types.KeyboardButton('Что это?'), types.KeyboardButton('Условия для получения'),
                   types.KeyboardButton('Какие необходимы документы'), types.KeyboardButton('Ограничения'),
                   types.KeyboardButton('Оформление'), types.KeyboardButton('Назад'))

CITIZENSHIP_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
CITIZENSHIP_MARKUP.add(types.KeyboardButton('РФ'), types.KeyboardButton('Иностранный'))

DISCOUNT_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
DISCOUNT_MARKUP.add(types.KeyboardButton('50%'), types.KeyboardButton('100%'), types.KeyboardButton('Назад'))

DISCOUNT50_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
DISCOUNT50_MARKUP.add(types.KeyboardButton('Как получить'), types.KeyboardButton('Примечания'),
                      types.KeyboardButton('Выдача'), types.KeyboardButton('Назад'))

TICKETS_BUY_MARKUP = types.InlineKeyboardMarkup()
TICKETS_BUY_MARKUP.add(types.InlineKeyboardButton(text='Сайт', url='https://vk.com/away.php?to=http%3A%2F%2Fe-traffic.ru&cc_key='))

ADDRESS_DISCOUNT50 = types.ReplyKeyboardMarkup(resize_keyboard=True)
ADDRESS_DISCOUNT50.add(types.KeyboardButton('Восточный'), types.KeyboardButton('Западный'))

DISCOUNT100_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
DISCOUNT100_MARKUP.add(types.KeyboardButton('Кто может получить'), types.KeyboardButton('Оформление'),
                       types.KeyboardButton('Когда предоставляется'), types.KeyboardButton('Выдача'),
                       types.KeyboardButton('Назад'))

HOSTEL_MARKUP = types.InlineKeyboardMarkup()
HOSTEL_MARKUP.add(types.InlineKeyboardButton(text='гугл форма', url='https://vk.com/away.php?to=https%3A%2F%2Fforms.gle%2FcvpYX68ZTD645urF8&post=-776924_8676&cc_key='))

OTHER_PRIVILEGES_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
OTHER_PRIVILEGES_MARKUP.add(types.KeyboardButton('Пособие за рождение ребенка'), types.KeyboardButton('Доплата студенческим семьям'),
                            types.KeyboardButton('Назад'))

ALLOWANCE_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
ALLOWANCE_MARKUP.add(types.KeyboardButton('Кто может получить'), types.KeyboardButton('Оформление'),
                       types.KeyboardButton('Период подачи'), types.KeyboardButton('Выплата'), types.KeyboardButton('Назад'))

SUPPLEMENT_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
SUPPLEMENT_MARKUP.add(types.KeyboardButton('Условия'), types.KeyboardButton('Оформление'), types.KeyboardButton('Назад'))

SUPPLEMENT_DOCUMENTS_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
SUPPLEMENT_DOCUMENTS_MARKUP.add(types.KeyboardButton('Для полных студенческих семей'),
                                types.KeyboardButton('Для неполных студенческих семей'))

VITA_MARKUP = types.ReplyKeyboardMarkup(resize_keyboard=True)
VITA_MARKUP.add(types.KeyboardButton('Что это'), types.KeyboardButton('Инструкция'), types.KeyboardButton('В начало'))

PHONE_NUMBER_MARKUP = types.InlineKeyboardMarkup()
PHONE_NUMBER_MARKUP.add(types.InlineKeyboardButton(text='Сообщество в VK', url='https://vk.com/ppos_kemsu'),
                        types.InlineKeyboardButton(text='Группа в Telegram', url='http://t.me/ppos_kemsu'))