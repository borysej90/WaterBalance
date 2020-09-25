DRINK = {
    'en': "It's time to drink a glass of water",
    'ru': "Время выпить стакан воды"
}

REMIND = {
    'en': "I will remind you to drink water every {} minutes.",
    'ru': "Я буду напоминать тебе пить воду каждые {} минут."
}

START = {
    'en': "Hello, I'm bot that will remind you to *drink water regularly*\n\nTo start type /remind command\nAlso I "
          "recomend you to set time period when notifications are turned off\. See /silence command\nTo see all "
          "available commands type /help\n\nBe healthy\!",
    'ru': "Привет, я бот, который будет тебе напоминать *пить воду регулярно*\n\nЧтобы начать напиши команду "
          "/remind\nТакже я рекомендую вам установить временной отрезок, когда напоминания отключены\. Используй "
          "команду /silence\nЧтобы посмотреть все доступные команды, напиши /help\n\nБудьте здоровы\! "
}

STOP = {
    'en': "Remindings turned off.",
    'ru': "Напоминания отключены."
}

STOP_NOT_EXiST = {
    'en': "You don't have active remindings.",
    'ru': "Нету активных напоминаний."
}

HELP = {
    'en': "Here is a list of commands which I know:\n\n/remind \<minutes\> \- I will remind you to drink water every "
          "*n*\-minutes \(or every *30*, if you don't pass any parameters\)\n/silence \- you can set time period when "
          "no notifications will be sent \(e\.g\. 23:00\-08:00\)\n/stop \- If there is active remindings, I will stop "
          "them",
    'ru': "Вот список команд, которые я умею:\n\n/remind \<минуты\> \- Я буду напоминать тебе пить воду каждые "
          "*n*\-минут \(или каждые *30*, если не передавать никаких параметров\)\n/silence \- вы можете установить "
          "период времени, когда напоминания не будуть отправляться \(например 23:00\-08:00\)\n/stop \- Если есть "
          "активные напоминания, то я перестану это делать "
}

CALIBRATION = {
    'en': "First of all, we need to calibrate your local timezone\.\nSo please, write your current time \(*only* "
          "hours\) in 24h format\.\nOr type /cancel if you want to exit",
    'ru': "Сперва нам надо откалибровать твой местный часовой пояс\.\nПоэтому пожалуйста напиши своё текущее время \("
          "*только* часы\) в 24\-часовом формате\.\nИли напиши /cancel если хочешь выйти "
}

TIMEZONE_ERROR = {
    'en': "Sorry, that's not time format\. Please write your current time \(*only* hours\) in 24h format\.\nOr type "
          "/cancel if you want to exit",
    'ru': "Извини, но это не часовой формат\. Пожалуйста напиши своё текущее время (*только* часы) в 24-часовом "
          "формате\.\nИли напиши /cancel если хочешь выйти "
}

TIMEZONE_OK = {
    'en': "Great, your timezone is set\! Now you need to specify your local time when to pause remindings _\(format: "
          "*hh:mm* or *hh*\)_",
    'ru': "Отлично, твой часовой пояс установлен\! Тепер нужно указать твое местное время когда приостанавливать "
          "напоминания _\(формат: *чч:мм* или *чч*\)_ "
}

START_SILENCE = {
    'en': "Perfect, one more left: now write your local time when to resume remindings _\(format: *hh:mm* or *hh*\)_",
    'ru': "Прекрасно, теперь последнее: напиши свое местное время когда возобновить напоминания _\(формат: *чч:мм* "
          "или *чч*\)_ "
}

END_SILENCE = {
    'en': "All done\! Now you can use /remind with silence period",
    'ru': "Все готово\! Тепер ты можешь использовать /remind вместе с промежутком тишини"
}

CANCEL = {
    'en': "You have canceled the previous command",
    'ru': "Ты отменил последнюю команду"
}

TIME_FORMAT_ERROR = {
    'en': "Sorry, but that's wrong time format\. Please check your input _\(correct format: *hh:mm* or *hh*\)_",
    'ru': "Извини, но это неправильный часовой формат. Пожалуйста проверь свой ввод _\(формат: *чч:мм* или *чч*\)_"
}
