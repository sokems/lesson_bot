from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_gender = InlineKeyboardMarkup(row_width=2)
inline_gender_b1 = InlineKeyboardButton(text='Мужской', callback_data='м')
inline_gender_b2 = InlineKeyboardButton(text='Женский', callback_data='ж')
inline_gender.add(inline_gender_b1, inline_gender_b2)

inline_pers = InlineKeyboardMarkup(row_width=2)
inline_pers_b1 = InlineKeyboardButton(text='✅ Я согласен(-на)', callback_data='yes')
inline_pers.add(inline_pers_b1)

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
start_menu_b1 = '💸 Оплатить курс'
start_menu_b2 = '✅ Я оплатил'
start_menu.add(start_menu_b1, start_menu_b2)

admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu_b1 = 'Добавить ученика'
admin_menu_b2 = 'Удалить ученика'
admin_menu_b3 = 'Выгрузить базу данных'
admin_menu_b4 = 'Добавить администратора'
admin_menu_b5 = 'Написать сообщение всем ученикам'
admin_menu.add(admin_menu_b1, admin_menu_b2).add(admin_menu_b3, admin_menu_b4).add(admin_menu_b5)

admin_menu_back = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu_back_b = 'Отмена'
admin_menu_back.add(admin_menu_back_b)

pack_menu = ReplyKeyboardMarkup(resize_keyboard=True)
pack_menu_b1 = '1️⃣ Ozon и WB одновременно'
pack_menu_b2 = '2️⃣ Начнем с Ozon'
pack_menu.add(pack_menu_b1).add(pack_menu_b2)

pack1_menu1 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu2 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu3 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu4 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu5 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu6 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu7 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu8 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu9 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu10 = ReplyKeyboardMarkup(resize_keyboard=True)
pack1_menu11 = ReplyKeyboardMarkup(resize_keyboard=True)

pack2_menu1 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu2 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu3 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu4 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu5 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu6 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu7 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu8 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu9 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu10 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu11 = ReplyKeyboardMarkup(resize_keyboard=True)
pack2_menu12 = ReplyKeyboardMarkup(resize_keyboard=True)

pack1_menu_b1 = '🐥 Модуль 1'
pack1_menu_b2 = '🎾 Модуль 2'
pack1_menu_b3 = '📝 Модуль 3'
pack1_menu_b4 = '💻 Модуль 4'
pack1_menu_b5 = '💣 Модуль 5'
pack1_menu_b6 = '📦 Модуль 6'
pack1_menu_b7 = '🚚 Модуль 7'
pack1_menu_b8 = '⚜️ Модуль 8'
pack1_menu_b9 = '💼 Модуль 9'
pack1_menu_b10 = '🌎 Модуль 10'
pack1_menu_b = '🔥 Бонус'
pack2_menu_b11 = '🟣 Модуль 11'
suport_b = '☎️ Поддержка'
pack1_menu1.add(pack1_menu_b1).add(suport_b)
pack1_menu2.add(pack1_menu_b1, pack1_menu_b2).add(suport_b)
pack1_menu3.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3).add(suport_b)
pack1_menu4.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(suport_b)
pack1_menu5.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5).add(suport_b)
pack1_menu6.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6).add(suport_b)
pack1_menu7.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7).add(suport_b)
pack1_menu8.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(suport_b)
pack1_menu9.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9).add(suport_b)
pack1_menu10.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9, pack1_menu_b10).add(suport_b)
pack1_menu11.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9, pack1_menu_b10).add(pack1_menu_b).add(suport_b)

pack2_menu1.add(pack1_menu_b1).add(suport_b)
pack2_menu2.add(pack1_menu_b1, pack1_menu_b2).add(suport_b)
pack2_menu3.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3).add(suport_b)
pack2_menu4.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(suport_b)
pack2_menu5.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5).add(suport_b)
pack2_menu6.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6).add(suport_b)
pack2_menu7.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7).add(suport_b)
pack2_menu8.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(suport_b)
pack2_menu9.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9).add(suport_b)
pack2_menu10.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9, pack1_menu_b10).add(suport_b)
pack2_menu11.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9, pack1_menu_b10).add(pack2_menu_b11).add(suport_b)
pack2_menu12.add(pack1_menu_b1, pack1_menu_b2).add(pack1_menu_b3, pack1_menu_b4).add(pack1_menu_b5, pack1_menu_b6)\
    .add(pack1_menu_b7, pack1_menu_b8).add(pack1_menu_b9, pack1_menu_b10).add(pack2_menu_b11, pack1_menu_b).add(suport_b)


mod_back_b = 'Назад'
mod1_1_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_1_b1 = 'Урок 1.1'
mod1_1_b2 = 'Урок 1.2'
mod1_1_b3 = 'Урок 1.3'
mod1_1_b4 = 'Урок 1.4'
mod1_1_b5 = 'Урок 1.5'
mod1_1_menu.add(mod1_1_b1, mod1_1_b2).add(mod1_1_b3, mod1_1_b4).add(mod1_1_b5, mod_back_b)
mod1_2_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_2_b1 = 'Урок 2.1'
mod1_2_b2 = 'Урок 2.2'
mod1_2_b3 = 'Урок 2.3'
mod1_2_b4 = 'Урок 2.4'
mod1_2_b5 = 'Урок 2.5'
mod1_2_b6 = 'Урок 2.6'
mod1_2_b7 = 'Урок 2.7'
mod1_2_b8 = 'Урок 2.8'
mod1_2_b9 = 'Урок 2.9'
mod1_2_b10 = 'Урок 2.10'
mod1_2_menu.add(mod1_2_b1, mod1_2_b2).add(mod1_2_b3, mod1_2_b4).add(mod1_2_b5, mod1_2_b6).add(mod1_2_b7, mod1_2_b8).add(mod1_2_b9, mod1_2_b10).add(mod_back_b)
mod1_3_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_3_b1 = 'Урок 3.1'
mod1_3_b2 = 'Урок 3.2'
mod1_3_b3 = 'Урок 3.3'
mod1_3_b4 = 'Урок 3.4'
mod1_3_b5 = 'Урок 3.5'
mod1_3_b6 = 'Урок 3.6'
mod1_3_b7 = 'Урок 3.7'
mod1_3_menu.add(mod1_3_b1, mod1_3_b2).add(mod1_3_b3, mod1_3_b4).add(mod1_3_b5, mod1_3_b6).add(mod1_3_b7, mod_back_b)
mod1_4_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_4_b1 = 'Урок 4.1'
mod1_4_b2 = 'Урок 4.2'
mod1_4_b3 = 'Урок 4.3'
mod1_4_b4 = 'Урок 4.4'
mod1_4_b5 = 'Урок 4.5'
mod1_4_b6 = 'Урок 4.6'
mod1_4_b7 = 'Урок 4.7'
mod1_4_b8 = 'Урок 4.8'
mod1_4_b9 = 'Урок 4.9'
mod1_4_b10 = 'Урок 4.10'
mod1_4_b11 = 'Урок 4.11'
mod1_4_b12 = 'Урок 4.12'
mod1_4_b13 = 'Урок 4.13'
mod1_4_b14 = 'Урок 4.14'
mod1_4_b15 = 'Урок 4.15'
mod1_4_b16 = 'Урок 4.16'
mod1_4_b17 = 'Урок 4.17'
mod1_4_menu.add(mod1_4_b1, mod1_4_b2).add(mod1_4_b3, mod1_4_b4).add(mod1_4_b5, mod1_4_b6).add(mod1_4_b7, mod1_4_b8)\
    .add(mod1_4_b9, mod1_4_b10).add(mod1_4_b11, mod1_4_b12).add(mod1_4_b13, mod1_4_b14).add(mod1_4_b15, mod1_4_b16)\
    .add(mod1_4_b17, mod_back_b)
mod1_5_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_5_b1 = 'Урок 5.1'
mod1_5_b2 = 'Урок 5.2'
mod1_5_b3 = 'Урок 5.3'
mod1_5_b4 = 'Урок 5.4'
mod1_5_b5 = 'Урок 5.5'
mod1_5_menu.add(mod1_5_b1, mod1_5_b2).add(mod1_5_b3, mod1_5_b4).add(mod1_5_b5, mod_back_b)
mod1_6_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_6_b1 = 'Урок 6.1'
mod1_6_b2 = 'Урок 6.2'
mod1_6_b3 = 'Урок 6.3'
mod1_6_b4 = 'Урок 6.4'
mod1_6_b5 = 'Урок 6.5'
mod1_6_b6 = 'Урок 6.6'
mod1_6_b7 = 'Урок 6.7'
mod1_6_menu.add(mod1_6_b1, mod1_6_b2).add(mod1_6_b3, mod1_6_b4).add(mod1_6_b5, mod1_6_b6).add(mod1_6_b7, mod_back_b)
mod1_7_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_7_b1 = 'Урок 7.1'
mod1_7_b2 = 'Урок 7.2'
mod1_7_b3 = 'Урок 7.3'
mod1_7_menu.add(mod1_7_b1, mod1_7_b2).add(mod1_7_b3, mod_back_b)
mod1_8_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_8_b1 = 'Урок 8.1'
mod1_8_b2 = 'Урок 8.2'
mod1_8_menu.add(mod1_8_b1, mod1_8_b2).add(mod_back_b)
mod1_9_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_9_b1 = 'Урок 9.1'
mod1_9_b2 = 'Урок 9.2'
mod1_9_b3 = 'Урок 9.3'
mod1_9_b4 = 'Урок 9.4'
mod1_9_menu.add(mod1_9_b1, mod1_9_b2).add(mod1_9_b3, mod1_9_b4).add(mod_back_b)
mod1_10_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_10_b1 = 'Урок 10.1'
mod1_10_b2 = 'Урок 10.2'
mod1_10_menu.add(mod1_10_b1, mod1_10_b2).add(mod_back_b)
mod1_bonus_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod1_bonus_b1 = 'Урок 1'
mod1_bonus_b2 = 'Урок 2'
mod1_bonus_b3 = 'Урок 3'
mod1_bonus_menu.add(mod1_bonus_b1, mod1_bonus_b2).add(mod1_bonus_b3, mod_back_b)


mod2_1_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_1_b1 = 'Урок 1.1'
mod2_1_b2 = 'Урок 1.2'
mod2_1_b3 = 'Урок 1.3'
mod2_1_b4 = 'Урок 1.4'
mod2_1_b5 = 'Урок 1.5'
mod2_1_menu.add(mod2_1_b1, mod2_1_b2).add(mod2_1_b3, mod2_1_b4).add(mod2_1_b5, mod_back_b)
mod2_2_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_2_b1 = 'Урок 2.1'
mod2_2_b2 = 'Урок 2.2'
mod2_2_b3 = 'Урок 2.3'
mod2_2_b4 = 'Урок 2.4'
mod2_2_b5 = 'Урок 2.5'
mod2_2_b6 = 'Урок 2.6'
mod2_2_b7 = 'Урок 2.7'
mod2_2_b8 = 'Урок 2.8'
mod2_2_b9 = 'Урок 2.9'
mod2_2_b10 = 'Урок 2.10'
mod2_2_menu.add(mod2_2_b1, mod2_2_b2).add(mod2_2_b3, mod2_2_b4).add(mod2_2_b5, mod2_2_b6).add(mod2_2_b7, mod2_2_b8).add(mod2_2_b9, mod2_2_b10).add(mod_back_b)
mod2_3_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_3_b1 = 'Урок 3.1'
mod2_3_b2 = 'Урок 3.2'
mod2_3_b3 = 'Урок 3.3'
mod2_3_b4 = 'Урок 3.4'
mod2_3_b5 = 'Урок 3.5'
mod2_3_b6 = 'Урок 3.6'
mod2_3_b7 = 'Урок 3.7'
mod2_3_menu.add(mod2_3_b1, mod2_3_b2).add(mod2_3_b3, mod2_3_b4).add(mod2_3_b5, mod2_3_b6).add(mod2_3_b7, mod_back_b)
mod2_4_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_4_b1 = 'Урок 4.1'
mod2_4_b2 = 'Урок 4.2'
mod2_4_b3 = 'Урок 4.3'
mod2_4_b4 = 'Урок 4.4'
mod2_4_b5 = 'Урок 4.5'
mod2_4_b6 = 'Урок 4.6'
mod2_4_b7 = 'Урок 4.7'
mod2_4_b8 = 'Урок 4.8'
mod2_4_b9 = 'Урок 4.9'
mod2_4_b10 = 'Урок 4.10'
mod2_4_b11 = 'Урок 4.11'
mod2_4_b12 = 'Урок 4.12'
mod2_4_menu.add(mod2_4_b1, mod2_4_b2).add(mod2_4_b3, mod2_4_b4).add(mod2_4_b5, mod2_4_b6).add(mod2_4_b7, mod2_4_b8)\
    .add(mod2_4_b9, mod2_4_b10).add(mod2_4_b11, mod2_4_b12).add(mod_back_b)
mod2_5_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_5_b1 = 'Урок 5.1'
mod2_5_b2 = 'Урок 5.2'
mod2_5_b3 = 'Урок 5.3'
mod2_5_menu.add(mod2_5_b1, mod2_5_b2).add(mod2_5_b3, mod_back_b)
mod2_6_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_6_b1 = 'Урок 6.1'
mod2_6_b2 = 'Урок 6.2'
mod2_6_b3 = 'Урок 6.3'
mod2_6_b4 = 'Урок 6.4'
mod2_6_b5 = 'Урок 6.5'
mod2_6_b6 = 'Урок 6.6'
mod2_6_menu.add(mod2_6_b1, mod2_6_b2).add(mod2_6_b3, mod2_6_b4).add(mod2_6_b5, mod2_6_b6).add(mod_back_b)
mod2_7_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_7_b1 = 'Урок 7.1'
mod2_7_b2 = 'Урок 7.2'
mod2_7_menu.add(mod2_7_b1, mod2_7_b2).add(mod_back_b)
mod2_8_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_8_b1 = 'Урок 8.1'
mod2_8_b2 = 'Урок 8.2'
mod2_8_menu.add(mod2_8_b1, mod2_8_b2).add(mod_back_b)
mod2_9_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_9_b1 = 'Урок 9.1'
mod2_9_b2 = 'Урок 9.2'
mod2_9_b3 = 'Урок 9.3'
mod2_9_menu.add(mod2_9_b1, mod2_9_b2).add(mod2_9_b3, mod_back_b)
mod2_10_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_10_b1 = 'Урок 10.1'
mod2_10_b2 = 'Урок 10.2'
mod2_10_menu.add(mod2_10_b1, mod2_10_b2).add(mod_back_b)
mod2_11_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_11_b1 = 'Урок 11.1'
mod2_11_b2 = 'Урок 11.2'
mod2_11_b3 = 'Урок 11.3'
mod2_11_b4 = 'Урок 11.4'
mod2_11_b5 = 'Урок 11.5'
mod2_11_b6 = 'Урок 11.6'
mod2_11_b7 = 'Урок 11.7'
mod2_11_b8 = 'Урок 11.8'
mod2_11_b9 = 'Урок 11.9'
mod2_11_b10 = 'Урок 11.10'
mod2_11_b11 = 'Урок 11.11'
mod2_11_b12 = 'Урок 11.12'
mod2_11_b13 = 'Урок 11.13'
mod2_11_b14 = 'Урок 11.14'
mod2_11_b15 = 'Урок 11.15'
mod2_11_b16 = 'Урок 11.16'
mod2_11_b17 = 'Урок 11.17'
mod2_11_b18 = 'Урок 11.18'
mod2_11_b19 = 'Урок 11.19'
mod2_11_b20 = 'Урок 11.20'
mod2_11_b21 = 'Урок 11.22'
mod2_11_menu.add(mod2_11_b1, mod2_11_b2).add(mod2_11_b3, mod2_11_b4).add(mod2_11_b5, mod2_11_b6).add(mod2_11_b7, mod2_11_b8)\
    .add(mod2_11_b9, mod2_11_b10).add(mod2_11_b11, mod2_11_b12).add(mod2_11_b13, mod2_11_b14).add(mod2_11_b15, mod2_11_b16).add(mod2_11_b17, mod2_11_b18).add(mod2_11_b19, mod2_11_b20).add(mod2_11_b21, mod_back_b)
mod2_bonus_menu = ReplyKeyboardMarkup(resize_keyboard=True)
mod2_bonus_b1 = 'Урок 1'
mod2_bonus_b2 = 'Урок 2'
mod2_bonus_b3 = 'Урок 3'
mod2_bonus_menu.add(mod2_bonus_b1, mod2_bonus_b2).add(mod2_bonus_b3, mod_back_b)
