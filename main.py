import telebot
import markups


TOKEN = "5546042303:AAGQkF395NZbfG3WnwtMBh-5ArO3Gojha1o"
bot = telebot.TeleBot(TOKEN)
admin = 805404632  # указать id администратора в tg,
# в моем случае id чата и id аккаунта телеграм это одно и тоже значение,
# если у вас не так скину иструкцию, как получить chat id чата с админом
apeeals = {}


# обработчик комманды start, вызываем меню
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Здравствуй, <b>{message.from_user.first_name} '
                                      f'{message.from_user.last_name}</b>! Тебя приветствует ППОС КемГУ! '
                                      f'\nВыбери кнопку, чтобы продолжить:',
                     parse_mode='html',
                     reply_markup=markups.menu_markup(message.chat.id, admin))


# обрабатываем ввод с клавиатуры
@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == "private":
        if message.text == "Материальная помощь":
            msg = bot.send_message(message.chat.id, "Материальная помощь", reply_markup=markups.MAT_HELP_MARKUP)
            bot.register_next_step_handler(msg, mat_help_button)
        elif message.text == "СКС Бонус":
            msg = bot.send_message(message.chat.id, 'CКС Бонус', reply_markup=markups.CKC_BONUS_MARKUP)
            bot.register_next_step_handler(msg, ckc_bonus)
        elif message.text == "Частые вопросы":
            bot.send_message(message.chat.id, "МАТЕРИАЛЬНАЯ ПОМОЩЬ\n1. Как написать заявление на мат.помощь?\n2. Я написал заявление, что дальше?\n"
                                              "3. Нужно ли прикреплять ИНН?\n4. Что делать, если я забыл прикрепить к письму документ или какой-то документ случайно не прикрепился?\n"
                                              "5. Я отправил документы на материальную помощь на почту. Как узнать, дошло ли письмо?\n"
                                              "6. Моему другу пришел ответ, а мне нет, что делать?\n7. Как узнать, будет ли мне назначена мат.помощь в апреле?\n"
                                              "8. Кто такой председатель профбюро моего института/факультета?\n9. Когда "
                                              "можно будет подавать документы на материальную помощь на май?")
            bot.send_message(message.chat.id, "СОЦИАЛЬНАЯ СТЕПЕНДИЯ\n1. Я получил уведомление в соц.защите. Как мне передать его в профком?\n"
                                              "2. У меня закончилась социальная стипендия, как мне собрать документы для оформления новой справки?\n"
                                              "3. У меня закончилась социальная стипендия, но возможности оформить новую справку нет, как быть?\n"
                                              "4. Если у меня закончилась социальная стипендия в марте, но я не успел подать заявление до 15 апреля?\n"
                                              "5. Могу ли я оформить мат.помощь как «социальщик», если моя социальная стипендия закончилась, "
                                              "но я не предоставил новую справку и написал заявление на продление выплат соц.стипендии?\n"
                                              "6. Я написал заявление на мат.помощь для продления выплат соц.стипендии, "
                                              "будет ли учитываться мат. помощь в мой доход при оформлении новой справки на соц. стипендию?")
            msg = bot.send_message(message.chat.id, "Выберете тему интересующего вас вопроса:", reply_markup=markups.QUESTION_TORIC_MARKUP)
            bot.register_next_step_handler(msg, question_topic)
        elif message.text == 'Льготы':
            msg = bot.send_message(message.chat.id, 'Льготы', reply_markup=markups.PRIVILEGES_MARKUP)
            bot.register_next_step_handler(msg, privileges)
        elif message.text =='Вита':
            msg = bot.send_message(message.chat.id, 'Вита', reply_markup=markups.VITA_MARKUP)
            bot.register_next_step_handler(msg, vita)
        elif message.text == 'Контакты':
            bot.send_message(message.chat.id, 'Вы можете связаться с нами, позвонив по номеру телефона 8(3842) 58-33-03,'
                                              ' написав нам в VK или Telegram', reply_markup=markups.PHONE_NUMBER_MARKUP)
            bot.send_message(message.chat.id, 'А так же через кнопку "Связаться с председателем ППОС" в главном меню',
                                   reply_markup=markups.menu_markup(message.chat.id, admin))
        elif message.text == 'Связаться с председателем ППОС':
            bot.send_message(message.chat.id, "Председателю ППОС будет доставлено ваше сообщение. Если вы уже ранее"
                                              " делали обращение, но вам не ответили, то ваше страое обращение будет заменено новым")
            msg = bot.send_message(message.chat.id, "Введите текст обращения:")
            bot.register_next_step_handler(msg, appeal_to_admin)
        elif message.text == "Ответить на обращение" and message.chat.id == admin:
            msg = bot.send_message(message.chat.id, "Введите id чата пользывателя которому нужно ответить:")
            bot.register_next_step_handler(msg, respond_to_a_request)
        elif message.text == "Прочитать обращения" and message.chat.id == admin:
            bot.send_message(message.chat.id, "Выводим обращения")
            i = 0
            for id, message_text in apeeals.items():
                bot.send_message(message.chat.id, f"ID чата: <code>{id}</code>\nСообщение: {message_text}", parse_mode="html")
                i += 1
                if i >= 10:
                    break
            if i == 0:
                bot.send_message(message.chat.id, "У вас пока нет обращений")


# при нажатии кнопки "Материальная помощь" будет выполнен следующий сценарий
def mat_help_button(message):
    if message.text == "Инструкция":
        msg = ""
        messages = [f'<b>Шаг 1</b>',
                    f'Написать заявление, подробно расписывая свою ситуацию, на основании которой вы хотите '
                    f'получить мат. помощь (прикладывая к нему чеки, справки и другие документы, подтверждающие, что вы действительно нуждаетесь в мат.помощи)',
                    f'<b>Шаг 2</b>',
                    f'Отдать заявление профоргу своей группы, либо принести в профком (ауд.2116, ауд.7345)'
                    f' \n При первом написании заявления на материальную помощь необходимо предоставить копию ИНН.']
        for i in messages:
            msg = bot.send_message(message.chat.id, i, parse_mode='html', reply_markup=markups.CHOICE_EXAMPLE_MARKUP)
        bot.register_next_step_handler(msg, send_example)
    elif message.text == "В начало":
        bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))


# по аналогии с mat_help_button
def send_example(message):
    if message.text == "Для бюджета":
        photo1 = open('1.jpg', 'rb')
        msg = bot.send_photo(message.chat.id, photo1, reply_markup=markups.CHOICE_EXAMPLE_MARKUP)
        bot.register_next_step_handler(msg, send_example)
    elif message.text == "Для контракта":
        photo2 = open('2.jpg', 'rb')
        msg = bot.send_photo(message.chat.id, photo2, reply_markup=markups.CHOICE_EXAMPLE_MARKUP)
        bot.register_next_step_handler(msg, send_example)
    elif message.text == "В начало":
        bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))

# при нажатии кнопки "СКС Бонус" будет выполнен следующий сценарий
def ckc_bonus(message):
    if message.text == "Что это?":
        msg = ""
        messages = ['<b>СКС Бонус — бонусная программа для членов Профсоюза</b>',
                    'Для всех членов Профсоюза доступна одна из крупнейших бонусных программ в России.',
                    f'Скидки и промокоды от наших партнеров в специальном приложении — СКС. '
                    f'Скачать можно в Google play или AppStore. \n \n'
                    f' <i>Список партнеров постоянно пополняется.</i>']
        for i in messages:
            msg = bot.send_message(message.chat.id, i, parse_mode='html')
        bot.register_next_step_handler(msg, ckc_bonus)  # остаёмся в этой функции
    elif message.text == "Где скачать?":
        msg = bot.send_message(message.chat.id, 'Ссылки на приложение', reply_markup=markups.INLINE_KEYBOARD_LINKS)
        bot.register_next_step_handler(msg, ckc_bonus)  # остаёмся в этой функции
    elif message.text == "Как зарегистрироваться?":
        msg = ""
        messages = ['1. Скачать приложение по ссылке.',
                    '2. Пройти регистрацию.',
                    '<i>Заполнить личные данные, выбрав вуз и загрузив фотографию. Заявка на регистрацию может'
                    'быть отклонена по причине «Фото пользователя» (не видно лицо, фотография не Ваша).</i> ',
                    '3. Подтвердить свою учетную запись в профкоме студентов (ауд. 2116)',
                    '<i>После регистрации в профиле будет указан статус «Ждём Вас в профкоме».</i>',
                    '<b>Проверка профилей проходит через Первичную профсоюзную организацию студентов КемГУ (необходимо личное присутствие).</b>',
                    'Как только профиль будет подтверждён, в приложении будет указан ваш индивидуальный баркод.']
        for i in messages:
            msg = bot.send_message(message.chat.id, i, parse_mode="html")
        bot.register_next_step_handler(msg, ckc_bonus)  # остаёмся в этой функции
    elif message.text == "В начало":
        bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))

# при нажатии кнопки "Частые вопросы" будет выполнен следующий сценарий
def question_topic(message):
    if message.text == 'Материальная помощь':
        msg = bot.send_message(message.chat.id, 'Выберете номер интересующего вас вопроса:', reply_markup=markups.MAT_QUESTIONS_MARKUP)
        bot.register_next_step_handler(msg, mat_questions)
    elif message.text == 'Социальная степендия':
        msg = bot.send_message(message.chat.id, 'Выберете номер интересующего вас вопроса:', reply_markup=markups.SOC_QUESTIONS_MARKUP)
        bot.register_next_step_handler(msg, soc_questions)
    elif message.text == 'В начало':
        bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))

def mat_questions(message):
    if message.text == '1':
        msg = bot.send_message(message.chat.id, 'Заявление на материальную помощь пишется ОТ РУКИ на имя ректора КемГУ с просьбой'
                                          ' о выделении мат.помощи, с указанием причины обращения. Пример заявления '
                                          'смотрите ниже (причину обращения пишите в зависимости от Вашей ситуации). '
                                          'Обязательно нужно поставить дату и подпись, иначе заявление не будет принято.',
                         reply_markup=markups.MAT_QUESTIONS_MARKUP1)
        bot.register_next_step_handler(msg, mat_question1)
    elif message.text == '2':
        msg = bot.send_message(message.chat.id, 'Далее нужно выслать полный комплект документов на электронную почту '
                                                'prof.kemsu@yandex.ru , в теме письма указать свой институт, ФИО, группу и курс.',
                               reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '3':
        msg = bot.send_message(message.chat.id, 'Фото или скан ИНН нужно прикреплять только тем студентам, которые '
                                                'оформляют мат.помощь впервые за весь период обучения.',
                               reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '4':
        msg = bot.send_message(message.chat.id, 'Если Вы отправили неполный пакет документов, то он не будет принят к рассмотрению.'
                                          ' Поэтому нужно создать новое письмо, прикрепить все необходимые документы '
                                          '(включая заявление!) и отправить ещё раз.', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '5':
        msg = bot.send_message(message.chat.id, 'По мере поступления и обработки заявлений придет ответ на ту '
                                          'электронную почту, с которой отправляли документы.', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '6':
        msg = bot.send_message(message.chat.id, 'Написать председателю профбюро своего института/факультета, либо в '
                                                'сообщения группы ВКонтакте.', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '7':
        msg = bot.send_message(message.chat.id, 'Всем студентам был отправлен ответ на почту. Если по каким-то причинам '
                                                'вам не ответили, нужно обратиться к председателю профбюро своего '
                                                'института/факультета.', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '8':
        msg = bot.send_message(message.chat.id, 'Председатель профбюро вашего института/факультета – это ответственный студент,'
                                          ' который сможет ответить вам на все вопросы, касающиеся профсоюзной деятельности,'
                                          ' а также оформления мат.помощи, соц. стипендии и иных выплат.',
                               reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '9':
        msg1 = bot.send_message(message.chat.id, 'Документы на мат.помощь на май будут приниматься до 4 мая включительно в '
                                          'электронном виде. Заявления, поступившие на почту после 4 мая, будут перенесены'
                                          ' на июнь. После окончания дистанционного обучения ОБЯЗАТЕЛЬНО нужно принести '
                                          'эти документы в бумажном виде, поэтому подготовьте пакет документов заранее и'
                                          ' ожидайте объявления о приеме документов в нашей группе.',
                                reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.send_message(message.chat.id, 'ПОЛНЫЙ АЛГОРИТМ ПОДАЧИ ДОКУМЕНТОВ НА МАТЕРИАЛЬНУЮ ПОМОЩЬ МОЖНО ПОСМОТРЕТЬ ЗДЕСЬ',
                         reply_markup=markups.MAT_QUESTIONS_MARKUP9)
        bot.register_next_step_handler(msg1, question_topic)

def mat_question1(message):
    if message.text == 'Примеры заявлений':
        msg = bot.send_message(message.chat.id, 'Выберете тип заявления:', reply_markup=markups.CHOICE_EXAMPLE_MARKUP)
        bot.register_next_step_handler(msg, send_example)
    elif message.text == 'К вопросам':
        msg = bot.send_message(message.chat.id, 'Выберете тему интересующего вас вопроса:', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)

def soc_questions(message):
    if message.text == '1':
        bot.send_message(message.chat.id, 'Вам нужно отправить в личные сообщения председателю профкома '
                                          'скан либо фотографию уведомления.', reply_markup=markups.SOC_QUESTIONS_MARKUP1)
        bot.send_message(message.chat.id, 'Указать номер телефона и учебную группу.')
        msg = bot.send_message(message.chat.id, 'Принести оригинал уведомления в кабинет профкома после снятия режима '
                                                '«повышенная готовность».', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '2':
        msg = ""
        messages = ['Для того, чтобы заказать справку о стипендии, вам нужно написать на почту бухгалтерии, указав ФИО, '
                    'учебную группу и срок, за который нужна справка (kemgu_buh@mail.ru)', 'Для того, чтобы заказать справку '
                    'с места учебы, вам нужно обратиться в дирекцию своего института/факультета.', 'Также нужно обратиться '
                    'в отдел социальной защиты по месту жительства и узнать режим работы.']
        for i in messages:
            msg = bot.send_message(message.chat.id, i, reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '3':
        photo3 = open('3.jpg', 'rb')
        messages = ['Если у вас закончилась соц.стипендия в период с 15 марта по 15 мая 2020 года, вам будет назначена '
                    'ежемесячная материальная помощь в размере не ниже получаемой ГСС. Это касается тех студентов, которые'
                    ' не могут подтвердить право на получение ГСС в электронном виде.', 'Для этого вам нужно написать ОТ'
                    ' РУКИ заявление (образец прикреплен ниже), обязательно поставить дату и подпись. Отправить заявление'
                    ' на почту (prof.kemsu@yandex.ru ) с пометкой «Социальная стипендия».']
        for i in messages:
            bot.send_message(message.chat.id, i)
        msg = bot.send_photo(message.chat.id, photo3, reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '4':
        msg = bot.send_message(message.chat.id, 'Если вы не успели подать заявление до 15 апреля 2020 г., то вы можете подать '
                                          'его позже в течение месяца и получить в майскую стипендию материальную помощь'
                                          ' в двойном размере (за апрель и май).', reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)
    elif message.text == '5':
        msg1 = bot.send_message(message.chat.id, 'Нет, по такому основанию вы не можете оформить материальную помощь, '
                                                 'так как не предоставили справку. Но вы можете оформить материальную '
                                                 'помощь по другому основанию, согласно положению.',
                                reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.send_message(message.chat.id,'Ссылку на положение об оказании материальной помощи прикрепляем ниже.',
                               reply_markup=markups.SOC_QUESTIONS_MARKUP5)
        bot.register_next_step_handler(msg1, question_topic)
    elif message.text == '6':
        msg = bot.send_message(message.chat.id, 'Да, материальная помощь будет учитываться в ваш доход.',
                               reply_markup=markups.QUESTION_TORIC_MARKUP)
        bot.register_next_step_handler(msg, question_topic)

# при нажатии кнопки "Льготы" будет выполнен следующий сценарий
def privileges(message):
    if message.text == 'ДМС':
        bot.send_message(message.chat.id, 'Благодаря полису добровольного медицинского страхования мы частично или '
                                          'полностью возместим траты на сложное лечение или дорогостоящие анализы.')
        bot.send_message(message.chat.id, 'Условия для получения услуги по ДМС:\n\n- быть членом Общероссийского Профсоюза'
                                          ' образования не менее шести месяцев;\n- не иметь задолженности по профсоюзным'
                                          ' взносам за все время обучения.')
        bot.send_message(message.chat.id, 'Чтобы воспользоваться нашей новой льготой, необходимо заполнить гугл форму',
                         reply_markup=markups.PRIVILEGES_DMS_MARKUP)
        bot.send_message(message.chat.id, 'Обращаем ваше внимание, что мы будем одобрять заявки только на те медицинские'
                                          ' услуги, которые не входят в перечень полису ОМС (например, посещение терапевта,'
                                          ' стоматолога, сдача общего анализа крови и тд). Сюда же не входят и косметические'
                                          ' услуги, косметическая стоматология. Также обязательно необходимо направление'
                                          ' врача на определенную медицинскую услугу.', parse_mode='html')
        bot.send_message(message.chat.id, 'Все заявки рассматриваются на заседании президиума ППОС КемГУ, после чего на'
                                          ' указанный адрес почты направляется ответ.')
        msg = bot.send_message(message.chat.id, 'Все дополнительные вопросы можно задать лично (ауд. 2116) или через кнопку '
                                          '"Связаться с председателем ППОС" в главном меню.',
                               reply_markup=markups.PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, privileges)
    elif message.text == 'Целевая субсидия':
        msg = bot.send_message(message.chat.id, 'Выберете интересующий вас пункт:', reply_markup=markups.TARGET_SUBSIDY_MARKUP)
        bot.register_next_step_handler(msg, target_subsidy)
    elif message.text == 'Проезд':
        msg = bot.send_message(message.chat.id, 'Выберте интересующую вас скидку:', reply_markup=markups.DISCOUNT_MARKUP)
        bot.register_next_step_handler(msg, discount)
    elif message.text == 'Общежития':
        msg = bot.send_message(message.chat.id, 'Порой, жизнь в общежитии отягощается определенными проблемами. Но не всегда '
                                          'понятно, куда обращаться за их решением.\n\nСпециально для таких случаев мы, '
                                          'совместно со Студенческим советом обучающихся КемГУ, создали гугл-форму, в '
                                          'которой вы можете сообщить нам о них. А далее, мы уже свяжемся с вами, чтобы '
                                          'помочь в их решении', reply_markup=markups.HOSTEL_MARKUP)
        bot.register_next_step_handler(msg, privileges)
    elif message.text == 'Прочие льготы':
        msg = bot.send_message(message.chat.id, 'Выберете интересующую вас льготу', reply_markup=markups.OTHER_PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, other_privileges)
    elif message.text == 'В начало':
        bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))

def target_subsidy(message):
    if message.text == 'Что это?':
        msg = bot.send_message(message.chat.id, 'Целевая субсидия — это огромная скидка на оплату обучения! Размер данной скидки'
                                          ' зависит от результатов сессии:\n\nвсе оценки «хорошо» или «хорошо» и '
                                          '«отлично» — 75%\nвсе оценки «отлично» — 90%.', reply_markup=markups.TARGET_SUBSIDY_MARKUP)
        bot.register_next_step_handler(msg, target_subsidy)
    elif message.text == 'Условия для получения':
        msg = ""
        messages = ['— Обучаться на 2-5 курсе бакалавриата или 1-2 курса магистратуры на контрактной основе',
                    '— Иметь доход на 1 члена семьи ниже прожиточного минимума, установленного в Кемеровской области '
                    '(13 081 рубль на 2023 год)', '— Обучаться на «хорошо» и «отлично» или только «отлично»',
                    'Все пункты должны быть соблюдены.']
        for i in messages:
            msg = bot.send_message(message.chat.id, i, reply_markup=markups.TARGET_SUBSIDY_MARKUP)
            if i == messages[0]:
                bot.send_message(message.chat.id, 'Примечания к этому пункту:\n\nЕсли ты студент 1 курса, закончивший '
                                                  'школу с золотой или серебряной медалью, то смело можешь претендовать '
                                                  'на субсидию с 1 семестра!\n\nДля магистрантов 1 года обучения при '
                                                  'оформлении субсидии в 1 семестре важно, чтобы в дипломе были только '
                                                  '«отлично»!\n\nЕсли ты студент 1 курса, но у тебя нет медали, но есть '
                                                  'диплом с отличием о получении среднего профессионального образования,'
                                                  ' то ты также имеешь право оформить субсидию!')
        bot.register_next_step_handler(msg, target_subsidy)
    elif message.text == 'Какие необходимы документы':
        msg = bot.send_message(message.chat.id, 'Выберете тип гражданства:', reply_markup=markups.CITIZENSHIP_MARKUP)
        bot.register_next_step_handler(msg, citizenship)
    elif message.text == 'Ограничения':
        msg = bot.send_message(message.chat.id, '— Студенты, обучающиеся в Юридическом институте и Институте экономики и управления,'
                                                ' а также по направлениям «Политология» «Международные отношения», '
                                                '«Социология», к сожалению, не имеют права на оформление целевой субсидии;\n\n'
                                                '— За весь период обучения субсидию можно оформить не более 6 раз;\n\n'
                                                '— В последнем семестре выпускного курса оформить субсидию нельзя.',
                               reply_markup=markups.TARGET_SUBSIDY_MARKUP)
        bot.register_next_step_handler(msg,target_subsidy)
    elif message.text == 'Оформление':
        bot.send_message(message.chat.id, 'Оформить субсидию можно только по адресу: пр. Советский, 73, ауд. 2116 '
                                          '— профком студентов КемГУ')
        msg = bot.send_message(message.chat.id, 'По всем вопросам, касающимся оформления субсидии, обращайтесь лично в '
                                                'профком или звоните по тел. 58-33-03!',
                               reply_markup=markups.TARGET_SUBSIDY_MARKUP)
        bot.register_next_step_handler(msg, target_subsidy)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Льготы', reply_markup=markups.PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, privileges)

def citizenship(message):
    if message.text == 'РФ':
        bot.send_message(message.chat.id, '— Справка об успеваемости за последний семестр — ее можно получить в '
                                                'дирекции/деканате института/факультета;\n\n— Копия договора об оказании'
                                                ' платных образовательных услуг;\n\n— Справка из управления социальной '
                                                'защиты о признании семьи или одиноко проживающего гражданина малоимущими.')
        msg = bot.send_message(message.chat.id, 'Это общий перечень документов, но в каждом конкретном случае может '
                                                'возникнуть необходимость дополнительных сведений. Все вопросы уточняйте'
                                                ' лично в профкоме студентов КемГУ (2 корпус, ауд. 2116)',
                               reply_markup=markups.TARGET_SUBSIDY_MARKUP)
        bot.register_next_step_handler(msg, target_subsidy)
    elif message.text == 'Иностранный':
        bot.send_message(message.chat.id, '— Справка об успеваемости за последний семестр — ее можно получить в '
                                                'дирекции/деканате института/факультета;\n\n— Копия договора об оказании'
                                                ' платных образовательных услуг;\n\n— Справка о составе семьи с указанием'
                                                ' года рождения — получить такую справку можно в ЖЭКе. Если проживаете в'
                                                ' частном доме, то необходима копия домовой книги;\n\n— Справка о доходах'
                                                ' всех членов семьи за последние 6 месяцев.')
        msg = bot.send_message(message.chat.id, 'Это общий перечень документов, но в каждом конкретном случае может '
                                                'возникнуть необходимость дополнительных сведений. Все вопросы уточняйте'
                                                ' лично в профкоме студентов КемГУ (2 корпус, ауд. 2116)',
                               reply_markup=markups.TARGET_SUBSIDY_MARKUP)
        bot.register_next_step_handler(msg, target_subsidy)

def discount(message):
    if message.text == '50%':
        msg = bot.send_message(message.chat.id, 'Скидка 50% на междугородний проезд', reply_markup=markups.DISCOUNT50_MARKUP)
        bot.register_next_step_handler(msg, discount50)
    elif message.text == '100%':
        msg = bot.send_message(message.chat.id, 'Скидка 100% на междугородний проезд',
                               reply_markup=markups.DISCOUNT100_MARKUP)
        bot.register_next_step_handler(msg, discount100)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Льготы', reply_markup=markups.PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, privileges)

def discount50(message):
    if message.text == 'Как получить':
        msg = bot.send_message(message.chat.id, '— Быть иногородним студентом;\n\n— Учиться на очной форме обучения '
                                                '(бюджет или контракт);\n\n— Жить на расстоянии не менее 50 километров '
                                                'от города Кемерово;\n\n— Проверить, продлён ли студенческий '
                                                '(для студентов 2 — 5 курсов);\n\n— Прийти в ППОС КемГУ (ауд. 2116 или ауд. 7345)'
                                                ' с паспортом и студенческим за вкладышем.', reply_markup=markups.DISCOUNT50_MARKUP)
        bot.register_next_step_handler(msg, discount50)
    elif message.text == 'Примечания':
        bot.send_message(message.chat.id, '1. Вкладыш работает только на территории Кемеровской области')
        bot.send_message(message.chat.id, '2. Билеты удобнее покупать на e-traffic.ru', reply_markup=markups.TICKETS_BUY_MARKUP)
        msg = bot.send_message(message.chat.id, '3. Аспиранты очной формы могут для скидки пользоваться проездными',
                               reply_markup=markups.DISCOUNT50_MARKUP)
        bot.register_next_step_handler(msg, discount50)
    elif message.text == 'Выдача':
        msg = bot.send_message(message.chat.id, 'Выберете ваш кампус:', reply_markup=markups.ADDRESS_DISCOUNT50)
        bot.register_next_step_handler(msg, address_discount50)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберете интересующую вас скидку', reply_markup=markups.DISCOUNT_MARKUP)
        bot.register_next_step_handler(msg, discount)

def discount100(message):
    if message.text == 'Кто может получить':
        msg = bot.send_message(message.chat.id, 'Студенты контрактной или бюджетной очной формы обучения, у которых член'
                                                ' семьи (отец, отчим или опекун) является участником специальной военной'
                                                ' операции, имеют право на получение скидки в размере 100 процентов от '
                                                'стоимости проезда в междугороднем транспорте Кузбасса (автобусы, электрички)'
                                                ' от места обучения до дома.', reply_markup=markups.DISCOUNT100_MARKUP)
        bot.register_next_step_handler(msg, discount100)
    elif message.text == 'Оформление':
        msg = bot.send_message(message.chat.id,'Для оформления специального вкладыша необходимо обратиться в профком студентов (ауд. 2116)'
                               ' со студенческим билетом и паспортом. Дополнительно необходимо предоставить заверенную '
                               'копию документа, подтверждающего участие отца, опекуна или отчима в СВО.',
                               reply_markup=markups.DISCOUNT100_MARKUP)
        bot.register_next_step_handler(msg, discount100)
    elif message.text == 'Когда предоставляется':
        msg = bot.send_message(message.chat.id,'Данная льгота предоставляется ежегодно в период с 30 августа по 30 июня включительно.',
                               reply_markup=markups.DISCOUNT100_MARKUP)
        bot.register_next_step_handler(msg, discount100)
    elif message.text == 'Выдача':
        msg = bot.send_message(message.chat.id,'Выдача вкладышей начнется с 1 февраля.', reply_markup=markups.DISCOUNT100_MARKUP)
        bot.register_next_step_handler(msg, discount100)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберете интересующую вас скидку', reply_markup=markups.DISCOUNT_MARKUP)
        bot.register_next_step_handler(msg, discount)

def address_discount50(message):
    if message.text == 'Восточный':
        msg = bot.send_message(message.chat.id, 'Бульвар строителей 47, ауд. 7345', reply_markup=markups.DISCOUNT50_MARKUP)
        bot.register_next_step_handler(msg, discount50)
    elif message.text == 'Западный':
        msg = bot.send_message(message.chat.id, 'пр. Советский 73, ауд. 2116', reply_markup=markups.DISCOUNT50_MARKUP)
        bot.register_next_step_handler(msg, discount50)

def other_privileges(message):
    if message.text == 'Пособие за рождение ребенка':
        msg = bot.send_message(message.chat.id, 'Единоразовое пособие студенческим семьям за рождение ребенка',
                               reply_markup=markups.ALLOWANCE_MARKUP)
        bot.register_next_step_handler(msg, allowance)
    elif message.text == 'Доплата студенческим семьям':
        msg = bot.send_message(message.chat.id, 'Полные студенческие семьи, имеющие детей, или неполные студенческие '
                                                'семьи, где ребенка воспитывает один родитель-студент, имеют возможность'
                                                ' оформить доплату к академической стипендии', reply_markup=markups.SUPPLEMENT_MARKUP)
        bot.register_next_step_handler(msg, supplement)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Льготы', reply_markup=markups.PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, privileges)

def allowance(message):
    if message.text == 'Кто может получить':
        msg = bot.send_message(message.chat.id, 'Студенческие семьи или одинокие родители имеют право на единоразовое '
                                                'социальное пособие в рамках региональной льготы.',
                               reply_markup=markups.ALLOWANCE_MARKUP)
        bot.register_next_step_handler(msg, allowance)
    elif message.text == 'Оформление':
        msg = bot.send_message(message.chat.id, 'Для его оформления в профком студентов необходимо предоставить '
                                                'следующие документы:\n\n— согласие на обработку персональных данных\n\n'
                                                '— копии паспортов родителей (родителя) ребенка\n\n— копию свидетельства'
                                                ' о браке (при наличии)\n\n— копию свидетельства о рождении ребенка '
                                                '(в случае, если отец ребенка в свидетельство о рождении вписан со слов '
                                                'матери необходимо подтвердить данный факт справкой из органов ЗАГС)\n\n'
                                                '— копию свидетельства о расторжении брака (при наличии)\n\n— копию ИНН '
                                                'и копию пенсионного страхового свидетельства (СНИЛС) родителя, на счет '
                                                'которого будет перечислено пособие\n\n— копию пенсионного страхового '
                                                'свидетельства (СНИЛС) ребенка\n\n— копию реквизитов личного банковского'
                                                ' счета родителя\n\n— справки (оригинал) из образовательных организаций '
                                                'о том, что родители (родитель) ребенка являются студентами с указанием '
                                                'специальности, курса обучения и формы обучения', reply_markup=markups.ALLOWANCE_MARKUP)
        bot.register_next_step_handler(msg, allowance)
    elif message.text == 'Период подачи':
        msg = bot.send_message(message.chat.id, 'Документы на получение пособия необходимо подать в течение 6 месяцев '
                                                'после рождения ребенка', reply_markup=markups.ALLOWANCE_MARKUP)
        bot.register_next_step_handler(msg, allowance)
    elif message.text == 'Выплата':
        msg = bot.send_message(message.chat.id, 'Выплата пособия происходит в течение 3 месяцев с момента предоставления'
                                                ' документов.', reply_markup=markups.ALLOWANCE_MARKUP)
        bot.register_next_step_handler(msg, allowance)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Льготы', reply_markup=markups.PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, privileges)


def supplement(message):
    if message.text == 'Условия':
        msg = bot.send_message(message.chat.id, '- Средний душевой доход в семье не выше прожиточного минимума. '
                                                'Напоминаем, что в 2023 году он составляет 13081 рубль\n\n- Учеба на '
                                                '«хорошо» и «отлично»\n\n- Обучение в вузе Кузбасса',
                               reply_markup=markups.SUPPLEMENT_MARKUP)
        bot.register_next_step_handler(msg,supplement)
    elif message.text == 'Оформление':
        msg = bot.send_message(message.chat.id, 'Для оформления доплаты в Профком студентов необходимо предоставить '
                                                'следующие документы до 8 февраля включительно',
                               reply_markup=markups.SUPPLEMENT_DOCUMENTS_MARKUP)
        bot.register_next_step_handler(msg, supplement_documents)
    elif message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Льготы', reply_markup=markups.PRIVILEGES_MARKUP)
        bot.register_next_step_handler(msg, privileges)

def supplement_documents(message):
    if message.text == 'Для полных студенческих семей':
        msg = bot.send_message(message.chat.id, '- копия свидетельства о заключении брака\n\n- копия свидетельства о '
                                                'рождении ребенка\n\n- справка об обучении (для студентов, обучающихся в'
                                                ' разных вузах Кузбасса)\n\n- копия паспорта\n\n- копия СНИЛСа\n\n- '
                                                'подтверждающий документ, что ребенок живет с родителями\n\n- реквизиты '
                                                'карты МИР с печатью банка\n\n- справка о доходах всех членов семьи за '
                                                'последние 6 месяцев', reply_markup=markups.SUPPLEMENT_MARKUP)
        bot.register_next_step_handler(msg, supplement)
    elif message.text == 'Для неполных студенческих семей':
        msg = bot.send_message(message.chat.id, '- копия свидетельства о заключении брака\n\n- копия свидетельства о '
                                                'разводе\n\n- копия свидетельства о рождении ребенка\n\n- копия '
                                                'паспорта\n\n- копия СНИЛСа\n\n- подтверждающий документ, что ребенок '
                                                'живет с родителем\n\n- реквизиты карты МИР с печатью банка\n\n- справка'
                                                ' о доходах всех членов семьи за последние 6 месяцев',
                               reply_markup=markups.SUPPLEMENT_MARKUP)
        bot.register_next_step_handler(msg, supplement)

# при нажатии кнопки "Вита" будет выполнен следующий сценарий
def vita(message):
    if message.text == 'Что это':
        msg = bot.send_message(message.chat.id, 'Санаторий-профилакторий КемГУ – место, где можно пройти профилактическое'
                                                ' лечение с помощью массажа, физиотерапии, кислородных коктейлей и других'
                                                ' процедур. Вы получаете талоны на комплексное питание суммой 180 рублей'
                                                ' в день. И в дополнение ко всему этому комплекс необходимых витаминов и'
                                                ' медикаментов!', reply_markup=markups.VITA_MARKUP)
        bot.register_next_step_handler(msg, vita)
    elif message.text == 'Инструкция':
        bot.send_message(message.chat.id, 'Пошаговая инструкция для оформления и получения путевки в санаторий-профилакторий:')
        msg = bot.send_message(message.chat.id, '1. Записаться на приём к терапевту в межвузовскую поликлинику №10. '
                                                'Получить справку для оформления санаторно-курортной путевки.\n2. При '
                                                'необходимости сдать анализы.\n3. Прийти в ППОС КемГУ (ауд. 2116 или ауд.'
                                                ' 7345), написать заявление на получение санаторно-курортной путевки.\n4.'
                                                ' Записаться снова на приём к терапевту. По путевке получить санаторно-'
                                                'курортную карту.\n5. Прийти в с/п КемГУ (ауд. 2502) и получить талоны на'
                                                ' питание, медикаменты и назначение на лечение.', reply_markup=markups.VITA_MARKUP)
        bot.register_next_step_handler(msg, vita)
    elif message.text == 'В начало':
        bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))

def appeal_to_admin(message):
    bot.send_message(message.chat.id, "Ваше сообщение будет доставлено представителю ППОС,"
                                      " в ближайшее время вам придёт ответ, ожидайте.")
    apeeals[message.chat.id] = message.text
    bot.send_message(message.chat.id, "Возвращаемся в главное меню", reply_markup=markups.menu_markup(message.chat.id, admin))


def respond_to_a_request(message):
    if message.text.isdecimal():
        if int(message.text) in apeeals:
            msg = bot.send_message(message.chat.id, "Напишите ответ на обращение:")
            bot.register_next_step_handler(msg, send_respond_to_user, int(message.text))
        else:
            bot.send_message(message.chat.id, "обращение от данного пользывателя не поступало")
    else:
        bot.send_message(message.chat.id, "введённый id чата невалиден")


def send_respond_to_user(message, chat_id):
    bot.send_message(chat_id, f"Ответ председателя ППОС: {message.text}")
    bot.send_message(message.chat.id, f"Ваше сообщение доставлено пользователю: {chat_id}",
                     reply_markup=markups.menu_markup(message.chat.id, admin))
    apeeals.pop(chat_id)


if __name__ == "__main__":
    bot.polling()
