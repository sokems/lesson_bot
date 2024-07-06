from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import les_video
import les_doc
import time
import re
import sqlite3
import texts
import markups
import json

TOKEN = ''

bot = Bot(TOKEN, parse_mode='html')
disp = Dispatcher(bot)

db = sqlite3.connect('users.db')
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (id_user TEXT, name_user TEXT DEFAULT (''))""")
db.commit()


async def startup(_):
    print('Бот запущен ' + str(time.strftime("%H:%M | %d.%m.%Y", time.localtime())))

@disp.message_handler(content_types=['document'])
async def handle_docs_photo(message):
    with open('admins.json', 'r', encoding='utf-8') as file:
        admins = json.load(file)
    if str(message.chat.id) in admins.keys():
        try:
            await message.answer(text=message)
        except Exception as e:
            await message.answer(text=e)

@disp.message_handler(content_types=['video'])
async def handle_video(message):
    with open('admins.json', 'r', encoding='utf-8') as file:
        admins = json.load(file)
    if str(message.chat.id) in admins.keys():
        try:
            await message.answer(text=message)
        except Exception as e:
            await message.answer(text=e)

@disp.message_handler(content_types=['photo'])
async def handle_video(message):
    with open('admins.json', 'r', encoding='utf-8') as file:
        admins = json.load(file)
    if str(message.chat.id) in admins.keys():
        try:
            await message.answer(text=message)
        except Exception as e:
            await message.answer(text=e)

@disp.message_handler(content_types=['animation'])
async def handle_video(message):
    with open('admins.json', 'r', encoding='utf-8') as file:
        admins = json.load(file)
    if str(message.chat.id) in admins.keys():
        try:
            await message.answer(text=message)
        except Exception as e:
            await message.answer(text=e)

@disp.message_handler(commands='info')
async def info_command(message: types.Message):
    id_user_get = message.chat.id
    await message.answer(text=id_user_get)

@disp.message_handler(commands='start')
async def start_command(message: types.Message):
    cur.execute(f"SELECT id_user FROM users WHERE id_user = '{message.chat.id}'")
    if cur.fetchone() is None:
        cur.execute(f"INSERT INTO users(id_user) VALUES ('{message.chat.id}')")
        db.commit()
        await bot.send_photo(message.chat.id, texts.start_pic, caption=texts.start_text)
    with open('admins.json', 'r', encoding='utf-8') as file:
        admins = json.load(file)
    if str(message.chat.id) in admins.keys():
        await message.answer(text='Меню администатора:', reply_markup=markups.admin_menu)


@disp.callback_query_handler()
async def action_callback(callback: types.CallbackQuery):
    if callback.data == 'м':
        cur.execute(f"UPDATE users SET gender = 'Мужской' WHERE id_user = '{callback.message.chat.id}'")
        db.commit()
        await callback.message.answer(text=texts.pers_text, reply_markup=markups.inline_pers)
        await callback.answer()

    elif callback.data == 'ж':
        cur.execute(f"UPDATE users SET gender = 'Женский' WHERE id_user = '{callback.message.chat.id}'")
        db.commit()
        await callback.message.answer(text=texts.pers_text, reply_markup=markups.inline_pers)
        await callback.answer()

    elif callback.data == 'yes':
        cur.execute(f"UPDATE users SET flag_pers = 1 WHERE id_user = '{callback.message.chat.id}'")
        db.commit()
        await bot.send_animation(callback.message.chat.id, texts.done_pic, caption=texts.done_text)
        await callback.message.answer(text=texts.start_menu_text, reply_markup=markups.start_menu, parse_mode='Markdown')
        await callback.answer()

@disp.message_handler()
async def text_massage(message: types.Message):
    with open('admins.json', 'r', encoding='utf-8') as file:
        admins = json.load(file)
    if str(message.chat.id) in admins.keys():
        if message.text == markups.admin_menu_back_b:
            admins[str(message.chat.id)] = [0, 0, 0, 0, 0, 0]
            with open('admins.json', 'w', encoding='utf-8') as file:
                json.dump(admins, file, ensure_ascii=False)
            await message.answer(text='Действия отменены', reply_markup=markups.admin_menu)
        elif admins[str(message.chat.id)] == [1, 0, 0, 0, 0, 0]:
            if message.text.isdigit():
                cur.execute(f"UPDATE users SET pay_pack_1 = '{1}' WHERE id_user = '{int(message.text)}'")
                db.commit()
                date = time.strftime("%d.%m.%Y", time.localtime())
                cur.execute(f"UPDATE users SET pay_date = '{date}' WHERE id_user = '{int(message.text)}'")
                db.commit()
                admins[str(message.chat.id)] = [0, 0, 0, 0, 0, 0]
                with open('admins.json', 'w', encoding='utf-8') as file:
                    json.dump(admins, file, ensure_ascii=False)
                await message.answer(text='Ученик добавлен', reply_markup=markups.admin_menu)

        elif admins[str(message.chat.id)] == [0, 1, 0, 0, 0, 0]:
            if message.text.isdigit():
                cur.execute(f"UPDATE users SET pay_pack_1 = '{0}' WHERE id_user = '{int(message.text)}'")
                db.commit()
                admins[str(message.chat.id)] = [0, 0, 0, 0, 0, 0]
                with open('admins.json', 'w', encoding='utf-8') as file:
                    json.dump(admins, file, ensure_ascii=False)
                await message.answer(text='Ученик удален', reply_markup=markups.admin_menu)

        elif admins[str(message.chat.id)] == [0, 0, 1, 0, 0, 0]:
            if message.text.isdigit():
                admins[str(message.chat.id)] = [0, 0, 0, 0, 0, 0]
                admins[message.text] = [0, 0, 0, 0, 0, 0]
                with open('admins.json', 'w', encoding='utf-8') as file:
                    json.dump(admins, file, ensure_ascii=False)
                await message.answer(text='Администратор добавлен', reply_markup=markups.admin_menu)
                
        elif admins[str(message.chat.id)] == [0, 0, 0, 1, 0, 0]:
            admins[str(message.chat.id)] = [0, 0, 0, 0, 0, 0]
            with open('admins.json', 'w', encoding='utf-8') as file:
                json.dump(admins, file, ensure_ascii=False)
            cur.execute(f"SELECT id_user FROM users WHERE pay_pack_1 = 1")
            list_users = cur.fetchall()
            for user in list_users:
                await bot.send_message(chat_id=str(user[0]), text=message.text)
            await message.answer(text='Сообщение отправлено!', reply_markup=markups.admin_menu)                

        elif message.text == markups.admin_menu_b5:
            await message.answer('Введите сообщение:', reply_markup=markups.admin_menu_back)
            admins[str(message.chat.id)] = [0, 0, 0, 1, 0, 0]
            with open('admins.json', 'w', encoding='utf-8') as file:
                json.dump(admins, file, ensure_ascii=False)

        elif message.text == markups.admin_menu_b4:
            await message.answer('Введите ID пользователя:', reply_markup=markups.admin_menu_back)
            admins[str(message.chat.id)] = [0, 0, 1, 0, 0, 0]
            with open('admins.json', 'w', encoding='utf-8') as file:
                json.dump(admins, file, ensure_ascii=False)

        elif message.text == markups.admin_menu_b3:
            data = open('users.db', 'rb')
            await bot.send_document(message.chat.id, document=data)
            data.close()

        elif message.text == markups.admin_menu_b2:
            await message.answer('Введите ID ученика:', reply_markup=markups.admin_menu_back)
            admins[str(message.chat.id)] = [0, 1, 0, 0, 0, 0]
            with open('admins.json', 'w', encoding='utf-8') as file:
                json.dump(admins, file, ensure_ascii=False)

        elif message.text == markups.admin_menu_b1:
            await message.answer('Введите ID ученика:', reply_markup=markups.admin_menu_back)
            admins[str(message.chat.id)] = [1, 0, 0, 0, 0, 0]
            with open('admins.json', 'w', encoding='utf-8') as file:
                json.dump(admins, file, ensure_ascii=False)
        else:
            await message.answer(text=texts.main_menu_admin_text, reply_markup=markups.admin_menu)


    else:
        cur.execute(f"SELECT id_user FROM users WHERE id_user = '{message.chat.id}'")
        if cur.fetchone() is None:
            await bot.send_photo(message.chat.id, texts.reg_pic, caption=texts.reg_text)
        else:
            cur.execute(f"SELECT flag_birth FROM users WHERE id_user = '{message.chat.id}'")
            if cur.fetchone()[0] == 1:
                if re.fullmatch('\d\d\.\d\d\.\d\d\d\d', message.text):
                    cur.execute(f"UPDATE users SET flag_birth = '{0}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    cur.execute(f"UPDATE users SET birth = '{message.text}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    await bot.send_photo(message.chat.id, texts.gender_pic, caption=texts.gender_text, reply_markup=markups.inline_gender)
                else:
                    await bot.send_photo(message.chat.id, texts.start2_pic, caption=texts.birth2_text)

            cur.execute(f"SELECT flag_mail FROM users WHERE id_user = '{message.chat.id}'")
            if cur.fetchone()[0] == 1:
                cur.execute(f"UPDATE users SET flag_mail = '{0}' WHERE id_user = '{message.chat.id}'")
                db.commit()
                cur.execute(f"UPDATE users SET mail = '{message.text}' WHERE id_user = '{message.chat.id}'")
                db.commit()
                cur.execute(f"UPDATE users SET flag_birth = '{1}' WHERE id_user = '{message.chat.id}'")
                db.commit()
                await bot.send_photo(message.chat.id, texts.birth_pic, caption=texts.birth_text)
                # else:
                #    await bot.send_photo(message.chat.id, texts.start2_pic, caption=texts.mail2_text)

            cur.execute(f"SELECT flag_city FROM users WHERE id_user = '{message.chat.id}'")
            if cur.fetchone()[0] == 1:
                cur.execute(f"UPDATE users SET flag_city = '{0}' WHERE id_user = '{message.chat.id}'")
                db.commit()
                cur.execute(f"UPDATE users SET city = '{message.text}' WHERE id_user = '{message.chat.id}'")
                db.commit()
                cur.execute(f"UPDATE users SET flag_mail = '{1}' WHERE id_user = '{message.chat.id}'")
                db.commit()
                await bot.send_photo(message.chat.id, texts.mail_pic, caption=texts.mail_text)

            cur.execute(f"SELECT flag_phone FROM users WHERE id_user = '{message.chat.id}'")
            if cur.fetchone()[0] == 1:
                if re.fullmatch('\d\d\d\d\d\d\d\d\d\d\d', message.text):
                    cur.execute(f"UPDATE users SET flag_phone = '{0}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    cur.execute(f"UPDATE users SET phone = '{message.text}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    cur.execute(f"UPDATE users SET flag_city = '{1}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    await bot.send_photo(message.chat.id, texts.city_pic, caption=texts.city_text)
                else:
                    await bot.send_photo(message.chat.id, texts.start2_pic, caption=texts.phone2_text)

            cur.execute(f"SELECT flag_name FROM users WHERE id_user = '{message.chat.id}'")
            if cur.fetchone()[0] == 1:
                if re.fullmatch('\w+\s\w+', message.text):
                    cur.execute(f"UPDATE users SET flag_name = '{0}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    cur.execute(f"UPDATE users SET name_user = '{message.text}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    cur.execute(f"UPDATE users SET flag_phone = '{1}' WHERE id_user = '{message.chat.id}'")
                    db.commit()
                    await bot.send_photo(message.chat.id, texts.phone_pic, caption=texts.phone_text)
                else:
                    await bot.send_photo(message.chat.id, texts.start2_pic, caption=texts.start2_text)

            cur.execute(f"SELECT flag_pers FROM users WHERE id_user = '{message.chat.id}'")
            if cur.fetchone()[0] == 1:
                cur.execute(f"SELECT pay_pack_1 FROM users WHERE id_user = '{message.chat.id}'")
                if cur.fetchone()[0] == 0:
                    if message.text == markups.start_menu_b2:
                        id_user_get = message.chat.id
                        await message.answer(text=id_user_get)
                        await message.answer(text=texts.pay_text, parse_mode='Markdown')
                    elif message.text == markups.start_menu_b1:
                        await message.answer(text=texts.want_pay_text, parse_mode='Markdown')
                    else:
                        await message.answer(text=texts.start_menu_text, reply_markup=markups.start_menu, parse_mode='Markdown')
                elif message.text == markups.suport_b:
                    await message.answer(text=texts.support, parse_mode='Markdown')
                else:

                    # Модуль 1
                    cur.execute(f"SELECT flag_les_all FROM users WHERE id_user = '{message.chat.id}'")
                    if cur.fetchone()[0] == 1:

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 11:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod1_6_text, reply_markup=markups.mod1_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod1_7_text, reply_markup=markups.mod1_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod1_8_text, reply_markup=markups.mod1_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                                await message.answer(text=texts.mod1_9_text, reply_markup=markups.mod1_9_menu)
                            elif message.text == markups.pack1_menu_b10:
                                await message.answer(text=texts.mod1_10_text, reply_markup=markups.mod1_10_menu)
                            elif message.text == markups.pack1_menu_b:
                                await message.answer(text=texts.error_text)
                            #     await message.answer(text=texts.mod1_bonus_text, reply_markup=markups.mod1_bonus_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True) 
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_6_1,
                                                     caption=les_video.mod1_6_1_name, protect_content=True)
                            elif message.text == markups.mod1_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_6_2,
                                                     caption=les_video.mod1_6_2_name, protect_content=True)
                            elif message.text == markups.mod1_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_6_3,
                                                     caption=les_video.mod1_6_3_name, protect_content=True)
                            elif message.text == markups.mod1_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_6_4,
                                                     caption=les_video.mod1_6_4_name, protect_content=True)
                            elif message.text == markups.mod1_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_6_5,
                                                     caption=les_video.mod1_6_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_6_6,
                                                     caption=les_video.mod1_6_6_name, protect_content=True)
                            elif message.text == markups.mod1_6_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_6_7,
                                                     caption=les_video.mod1_6_7_name, protect_content=True)
                            elif message.text == markups.mod1_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_7_1,
                                                     caption=les_video.mod1_7_1_name, protect_content=True)
                            elif message.text == markups.mod1_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_7_2,
                                                     caption=les_video.mod1_7_2_name, protect_content=True)
                            elif message.text == markups.mod1_7_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_7_3,
                                                     caption=les_video.mod1_7_3_name, protect_content=True)
                            elif message.text == markups.mod1_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_8_1,
                                                     caption=les_video.mod1_8_1_name, protect_content=True)
                            elif message.text == markups.mod1_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_8_2,
                                                     caption=les_video.mod1_8_2_name, protect_content=True)
                            elif message.text == markups.mod1_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_9_1,
                                                     caption=les_video.mod1_9_1_name, protect_content=True)
                            elif message.text == markups.mod1_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_9_2,
                                                     caption=les_video.mod1_9_2_name, protect_content=True)
                            elif message.text == markups.mod1_9_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_9_3,
                                                     caption=les_video.mod1_9_3_name, protect_content=True)
                            elif message.text == markups.mod1_9_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_9_4,
                                                     caption=les_video.mod1_9_4_name, protect_content=True)
                            elif message.text == markups.mod1_10_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_10_1,
                                                     caption=les_video.mod1_10_1_name, protect_content=True)
                            elif message.text == markups.mod1_10_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_10_2,
                                                     caption=les_video.mod1_10_2_name, protect_content=True)
                            elif message.text == markups.mod1_bonus_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_bonus_1,
                                                     caption=les_video.mod1_bonus_1_name, protect_content=True)
                            elif message.text == markups.mod1_bonus_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_bonus_2,
                                                     caption=les_video.mod1_bonus_2_name, protect_content=True)
                            elif message.text == markups.mod1_bonus_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_bonus_3,
                                                     caption=les_video.mod1_bonus_3_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu11)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 10:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod1_6_text, reply_markup=markups.mod1_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod1_7_text, reply_markup=markups.mod1_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod1_8_text, reply_markup=markups.mod1_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                                await message.answer(text=texts.mod1_9_text, reply_markup=markups.mod1_9_menu)
                            elif message.text == markups.pack1_menu_b10:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_10_text, reply_markup=markups.mod1_10_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True)
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_6_1,
                                                     caption=les_video.mod1_6_1_name, protect_content=True)
                            elif message.text == markups.mod1_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_6_2,
                                                     caption=les_video.mod1_6_2_name, protect_content=True)
                            elif message.text == markups.mod1_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_6_3,
                                                     caption=les_video.mod1_6_3_name, protect_content=True)
                            elif message.text == markups.mod1_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_6_4,
                                                     caption=les_video.mod1_6_4_name, protect_content=True)
                            elif message.text == markups.mod1_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_6_5,
                                                     caption=les_video.mod1_6_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_6_6,
                                                     caption=les_video.mod1_6_6_name, protect_content=True)
                            elif message.text == markups.mod1_6_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_6_7,
                                                     caption=les_video.mod1_6_7_name, protect_content=True)
                            elif message.text == markups.mod1_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_7_1,
                                                     caption=les_video.mod1_7_1_name, protect_content=True)
                            elif message.text == markups.mod1_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_7_2,
                                                     caption=les_video.mod1_7_2_name, protect_content=True)
                            elif message.text == markups.mod1_7_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_7_3,
                                                     caption=les_video.mod1_7_3_name, protect_content=True)
                            elif message.text == markups.mod1_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_8_1,
                                                     caption=les_video.mod1_8_1_name, protect_content=True)
                            elif message.text == markups.mod1_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_8_2,
                                                     caption=les_video.mod1_8_2_name, protect_content=True)
                            elif message.text == markups.mod1_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_9_1,
                                                     caption=les_video.mod1_9_1_name, protect_content=True)
                            elif message.text == markups.mod1_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_9_2,
                                                     caption=les_video.mod1_9_2_name, protect_content=True)
                            elif message.text == markups.mod1_9_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_9_3,
                                                     caption=les_video.mod1_9_3_name, protect_content=True)
                            elif message.text == markups.mod1_9_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_9_4,
                                                     caption=les_video.mod1_9_4_name, protect_content=True)
                            elif message.text == markups.mod1_10_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_10_1,
                                                     caption=les_video.mod1_10_1_name, protect_content=True)
                            elif message.text == markups.mod1_10_b2:
                                cur.execute(f"UPDATE users SET module = '{11}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_10_2,
                                                     caption=les_video.mod1_10_2_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu10)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 9:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod1_6_text, reply_markup=markups.mod1_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod1_7_text, reply_markup=markups.mod1_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod1_8_text, reply_markup=markups.mod1_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_9_text, reply_markup=markups.mod1_9_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True)
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_6_1,
                                                     caption=les_video.mod1_6_1_name, protect_content=True)
                            elif message.text == markups.mod1_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_6_2,
                                                     caption=les_video.mod1_6_2_name, protect_content=True)
                            elif message.text == markups.mod1_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_6_3,
                                                     caption=les_video.mod1_6_3_name, protect_content=True)
                            elif message.text == markups.mod1_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_6_4,
                                                     caption=les_video.mod1_6_4_name, protect_content=True)
                            elif message.text == markups.mod1_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_6_5,
                                                     caption=les_video.mod1_6_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_6_6,
                                                     caption=les_video.mod1_6_6_name, protect_content=True)
                            elif message.text == markups.mod1_6_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_6_7,
                                                     caption=les_video.mod1_6_7_name, protect_content=True)
                            elif message.text == markups.mod1_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_7_1,
                                                     caption=les_video.mod1_7_1_name, protect_content=True)
                            elif message.text == markups.mod1_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_7_2,
                                                     caption=les_video.mod1_7_2_name, protect_content=True)
                            elif message.text == markups.mod1_7_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_7_3,
                                                     caption=les_video.mod1_7_3_name, protect_content=True)
                            elif message.text == markups.mod1_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_8_1,
                                                     caption=les_video.mod1_8_1_name, protect_content=True)
                            elif message.text == markups.mod1_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_8_2,
                                                     caption=les_video.mod1_8_2_name, protect_content=True)
                            elif message.text == markups.mod1_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_9_1,
                                                     caption=les_video.mod1_9_1_name, protect_content=True)
                            elif message.text == markups.mod1_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_9_2,
                                                     caption=les_video.mod1_9_2_name, protect_content=True)
                            elif message.text == markups.mod1_9_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_9_3,
                                                     caption=les_video.mod1_9_3_name, protect_content=True)
                            elif message.text == markups.mod1_9_b4:
                                cur.execute(f"UPDATE users SET module = '{10}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_9_4,
                                                     caption=les_video.mod1_9_4_name,protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu9)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 8:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod1_6_text, reply_markup=markups.mod1_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod1_7_text, reply_markup=markups.mod1_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_8_text, reply_markup=markups.mod1_8_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True)
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_6_1,
                                                     caption=les_video.mod1_6_1_name, protect_content=True)
                            elif message.text == markups.mod1_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_6_2,
                                                     caption=les_video.mod1_6_2_name, protect_content=True)
                            elif message.text == markups.mod1_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_6_3,
                                                     caption=les_video.mod1_6_3_name, protect_content=True)
                            elif message.text == markups.mod1_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_6_4,
                                                     caption=les_video.mod1_6_4_name, protect_content=True)
                            elif message.text == markups.mod1_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_6_5,
                                                     caption=les_video.mod1_6_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_6_6,
                                                     caption=les_video.mod1_6_6_name, protect_content=True)
                            elif message.text == markups.mod1_6_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_6_7,
                                                     caption=les_video.mod1_6_7_name, protect_content=True)
                            elif message.text == markups.mod1_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_7_1,
                                                     caption=les_video.mod1_7_1_name, protect_content=True)
                            elif message.text == markups.mod1_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_7_2,
                                                     caption=les_video.mod1_7_2_name, protect_content=True)
                            elif message.text == markups.mod1_7_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_7_3,
                                                     caption=les_video.mod1_7_3_name, protect_content=True)
                            elif message.text == markups.mod1_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_8_1,
                                                     caption=les_video.mod1_8_1_name, protect_content=True)
                            elif message.text == markups.mod1_8_b2:
                                cur.execute(f"UPDATE users SET module = '{9}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_8_2,
                                                     caption=les_video.mod1_8_2_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu8)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 7:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod1_6_text, reply_markup=markups.mod1_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_7_text, reply_markup=markups.mod1_7_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True)  
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_6_1,
                                                     caption=les_video.mod1_6_1_name, protect_content=True)
                            elif message.text == markups.mod1_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_6_2,
                                                     caption=les_video.mod1_6_2_name, protect_content=True)
                            elif message.text == markups.mod1_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_6_3,
                                                     caption=les_video.mod1_6_3_name, protect_content=True)
                            elif message.text == markups.mod1_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_6_4,
                                                     caption=les_video.mod1_6_4_name, protect_content=True)
                            elif message.text == markups.mod1_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_6_5,
                                                     caption=les_video.mod1_6_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_6_6,
                                                     caption=les_video.mod1_6_6_name, protect_content=True)
                            elif message.text == markups.mod1_6_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_6_7,
                                                     caption=les_video.mod1_6_7_name, protect_content=True)
                            elif message.text == markups.mod1_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_7_1,
                                                     caption=les_video.mod1_7_1_name, protect_content=True)
                            elif message.text == markups.mod1_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_7_2,
                                                     caption=les_video.mod1_7_2_name, protect_content=True)
                            elif message.text == markups.mod1_7_b3:
                                cur.execute(f"UPDATE users SET module = '{8}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_7_3,
                                                     caption=les_video.mod1_7_3_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu7)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 6:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_6_text, reply_markup=markups.mod1_6_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True) 
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_6_1,
                                                     caption=les_video.mod1_6_1_name, protect_content=True)
                            elif message.text == markups.mod1_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_6_2,
                                                     caption=les_video.mod1_6_2_name, protect_content=True)
                            elif message.text == markups.mod1_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_6_3,
                                                     caption=les_video.mod1_6_3_name, protect_content=True)
                            elif message.text == markups.mod1_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_6_4,
                                                     caption=les_video.mod1_6_4_name, protect_content=True)
                            elif message.text == markups.mod1_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_6_5,
                                                     caption=les_video.mod1_6_5_name, protect_content=True)
                            elif message.text == markups.mod1_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_6_6,
                                                     caption=les_video.mod1_6_6_name, protect_content=True)
                            elif message.text == markups.mod1_6_b7:
                                cur.execute(f"UPDATE users SET module = '{7}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_6_7,
                                                     caption=les_video.mod1_6_7_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu6)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 5:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_5_text, reply_markup=markups.mod1_5_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True) 
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            elif message.text == markups.mod1_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_5_1,
                                                     caption=les_video.mod1_5_1_name, protect_content=True)
                            elif message.text == markups.mod1_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_5_2,
                                                     caption=les_video.mod1_5_2_name, protect_content=True)
                            elif message.text == markups.mod1_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_5_3,
                                                     caption=les_video.mod1_5_3_name, protect_content=True)
                            elif message.text == markups.mod1_5_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_5_4,
                                                     caption=les_video.mod1_5_4_name, protect_content=True)
                            elif message.text == markups.mod1_5_b5:
                                cur.execute(f"UPDATE users SET module = '{6}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_5_5,
                                                     caption=les_video.mod1_5_5_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu5)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 4:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod1_4_text, reply_markup=markups.mod1_4_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True)
                            elif message.text == markups.mod1_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_4_1,
                                                     caption=les_video.mod1_4_1_name, protect_content=True)
                            elif message.text == markups.mod1_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_4_2,
                                                     caption=les_video.mod1_4_2_name, protect_content=True)
                            elif message.text == markups.mod1_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_4_3,
                                                     caption=les_video.mod1_4_3_name, protect_content=True)
                            elif message.text == markups.mod1_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_4_4,
                                                     caption=les_video.mod1_4_4_name, protect_content=True)
                            elif message.text == markups.mod1_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_4_5,
                                                     caption=les_video.mod1_4_5_name, protect_content=True)
                            elif message.text == markups.mod1_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_4_6,
                                                     caption=les_video.mod1_4_6_name, protect_content=True)
                            elif message.text == markups.mod1_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_4_7,
                                                     caption=les_video.mod1_4_7_name, protect_content=True)
                            elif message.text == markups.mod1_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_4_8,
                                                     caption=les_video.mod1_4_8_name, protect_content=True)
                            elif message.text == markups.mod1_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_4_9,
                                                     caption=les_video.mod1_4_9_name, protect_content=True)
                            elif message.text == markups.mod1_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_4_10,
                                                     caption=les_video.mod1_4_10_name, protect_content=True)
                            elif message.text == markups.mod1_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod1_4_11,
                                                     caption=les_video.mod1_4_11_name, protect_content=True)
                            elif message.text == markups.mod1_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod1_4_12,
                                                     caption=les_video.mod1_4_12_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_12_2, protect_content=True)
                            elif message.text == markups.mod1_4_b13:
                                await bot.send_video(message.chat.id, les_video.mod1_4_13,
                                                     caption=les_video.mod1_4_13_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_13_2, protect_content=True)
                            elif message.text == markups.mod1_4_b14:
                                await bot.send_video(message.chat.id, les_video.mod1_4_14,
                                                     caption=les_video.mod1_4_14_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod1_4_14_5, protect_content=True)
                            elif message.text == markups.mod1_4_b15:
                                await bot.send_video(message.chat.id, les_video.mod1_4_15,
                                                     caption=les_video.mod1_4_15_name, protect_content=True)
                            elif message.text == markups.mod1_4_b16:
                                await bot.send_video(message.chat.id, les_video.mod1_4_16,
                                                     caption=les_video.mod1_4_16_name, protect_content=True)
                            elif message.text == markups.mod1_4_b17:
                                cur.execute(f"UPDATE users SET module = '{5}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_4_17,
                                                     caption=les_video.mod1_4_17_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu4)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 3:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_3_text, reply_markup=markups.mod1_3_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            elif message.text == markups.mod1_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_3_1,
                                                     caption=les_video.mod1_3_1_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_1, protect_content=True)
                            elif message.text == markups.mod1_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_3_2,
                                                     caption=les_video.mod1_3_2_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_2, protect_content=True)
                            elif message.text == markups.mod1_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_3_3,
                                                     caption=les_video.mod1_3_3_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_3, protect_content=True)
                            elif message.text == markups.mod1_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_3_4,
                                                     caption=les_video.mod1_3_4_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_4, protect_content=True)
                            elif message.text == markups.mod1_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_3_5,
                                                     caption=les_video.mod1_3_5_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_5, protect_content=True)
                            elif message.text == markups.mod1_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_3_6,
                                                     caption=les_video.mod1_3_6_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_6, protect_content=True)
                            elif message.text == markups.mod1_3_b7:
                                cur.execute(f"UPDATE users SET module = '{4}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_3_7,
                                                     caption=les_video.mod1_3_7_name, protect_content=True)
                                await bot.send_video(message.chat.id, les_doc.mod1_3_7, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu3)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 2:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod1_2_text, reply_markup=markups.mod1_2_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_2_1,
                                                     caption=les_video.mod1_2_1_name, protect_content=True)
                            elif message.text == markups.mod1_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_2_2,
                                                     caption=les_video.mod1_2_2_name, protect_content=True)
                            elif message.text == markups.mod1_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_2_3,
                                                     caption=les_video.mod1_2_3_name, protect_content=True)
                            elif message.text == markups.mod1_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_2_4,
                                                     caption=les_video.mod1_2_4_name, protect_content=True)
                            elif message.text == markups.mod1_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod1_2_5,
                                                     caption=les_video.mod1_2_5_name, protect_content=True)
                            elif message.text == markups.mod1_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod1_2_6,
                                                     caption=les_video.mod1_2_6_name, protect_content=True)
                            elif message.text == markups.mod1_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod1_2_7,
                                                     caption=les_video.mod1_2_7_name, protect_content=True)
                            elif message.text == markups.mod1_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod1_2_8,
                                                     caption=les_video.mod1_2_8_name, protect_content=True)
                            elif message.text == markups.mod1_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod1_2_9,
                                                     caption=les_video.mod1_2_9_name, protect_content=True)
                            elif message.text == markups.mod1_2_b10:
                                cur.execute(f"UPDATE users SET module = '{3}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_2_10,
                                                     caption=les_video.mod1_2_10_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu2)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 1:
                            if message.text == markups.pack1_menu_b1:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod1_1_text, reply_markup=markups.mod1_1_menu)
                            elif message.text == markups.mod1_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod1_1_1,
                                                     caption=les_video.mod1_1_1_name, protect_content=True)
                            elif message.text == markups.mod1_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod1_1_2,
                                                     caption=les_video.mod1_1_2_name, protect_content=True)
                            elif message.text == markups.mod1_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod1_1_3,
                                                     caption=les_video.mod1_1_3_name, protect_content=True)
                            elif message.text == markups.mod1_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod1_1_4,
                                                     caption=les_video.mod1_1_4_name, protect_content=True)
                            elif message.text == markups.mod1_1_b5:
                                cur.execute(f"UPDATE users SET module = '{2}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod1_1_5,
                                                     caption=les_video.mod1_1_5_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu1)

                    # Модуль 2
                    cur.execute(f"SELECT flag_les_all FROM users WHERE id_user = '{message.chat.id}'")
                    if cur.fetchone()[0] == 2:

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 12:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod2_7_text, reply_markup=markups.mod2_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod2_8_text, reply_markup=markups.mod2_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                                await message.answer(text=texts.mod2_9_text, reply_markup=markups.mod2_9_menu)
                            elif message.text == markups.pack1_menu_b10:
                                await message.answer(text=texts.mod2_10_text, reply_markup=markups.mod2_10_menu)
                            elif message.text == markups.pack2_menu_b11:
                                await message.answer(text=texts.mod2_11_text, reply_markup=markups.mod2_11_menu)
                            elif message.text == markups.pack1_menu_b:
                                await message.answer(text=texts.error_text)
                            #    await message.answer(text=texts.mod2_bonus_text, reply_markup=markups.mod2_bonus_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            elif message.text == markups.mod2_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_7_1,
                                                     caption=les_video.mod2_7_1_name, protect_content=True)
                            elif message.text == markups.mod2_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_7_2,
                                                     caption=les_video.mod2_7_2_name, protect_content=True)
                            elif message.text == markups.mod2_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_8_1,
                                                     caption=les_video.mod2_8_1_name, protect_content=True)
                            elif message.text == markups.mod2_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_8_2,
                                                     caption=les_video.mod2_8_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_9_1,
                                                     caption=les_video.mod2_9_1_name, protect_content=True)
                            elif message.text == markups.mod2_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_9_2,
                                                     caption=les_video.mod2_9_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_9_3,
                                                     caption=les_video.mod2_9_3_name, protect_content=True)
                            elif message.text == markups.mod2_10_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_10_1,
                                                     caption=les_video.mod2_10_1_name, protect_content=True)
                            elif message.text == markups.mod2_10_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_10_2,
                                                     caption=les_video.mod2_10_2_name, protect_content=True)
                            elif message.text == markups.mod2_11_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_11_1,
                                                     caption=les_video.mod2_11_1_name, protect_content=True)
                            elif message.text == markups.mod2_11_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_11_2,
                                                     caption=les_video.mod2_11_2_name, protect_content=True)
                            elif message.text == markups.mod2_11_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_11_3,
                                                     caption=les_video.mod2_11_3_name, protect_content=True)
                            elif message.text == markups.mod2_11_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_11_4,
                                                     caption=les_video.mod2_11_4_name, protect_content=True)
                            elif message.text == markups.mod2_11_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_11_5,
                                                     caption=les_video.mod2_11_5_name, protect_content=True)
                            elif message.text == markups.mod2_11_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_11_6,
                                                     caption=les_video.mod2_11_6_name, protect_content=True)
                            elif message.text == markups.mod2_11_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_11_7,
                                                     caption=les_video.mod2_11_7_name, protect_content=True)
                            elif message.text == markups.mod2_11_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_11_8,
                                                     caption=les_video.mod2_11_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_8_2, protect_content=True)
                            elif message.text == markups.mod2_11_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_11_9,
                                                     caption=les_video.mod2_11_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_9_2, protect_content=True)
                            elif message.text == markups.mod2_11_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_11_10,
                                                     caption=les_video.mod2_11_10_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_5, protect_content=True)
                            elif message.text == markups.mod2_11_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_11_11,
                                                     caption=les_video.mod2_11_11_name, protect_content=True)
                            elif message.text == markups.mod2_11_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_11_12,
                                                     caption=les_video.mod2_11_12_name, protect_content=True)
                            elif message.text == markups.mod2_11_b13:
                                await bot.send_video(message.chat.id, les_video.mod2_11_13,
                                                     caption=les_video.mod2_11_13_name, protect_content=True)
                            elif message.text == markups.mod2_11_b14:
                                await bot.send_video(message.chat.id, les_video.mod2_11_14,
                                                     caption=les_video.mod2_11_14_name, protect_content=True)
                            elif message.text == markups.mod2_11_b15:
                                await bot.send_video(message.chat.id, les_video.mod2_11_15,
                                                     caption=les_video.mod2_11_15_name, protect_content=True)
                            elif message.text == markups.mod2_11_b16:
                                await bot.send_video(message.chat.id, les_video.mod2_11_16,
                                                     caption=les_video.mod2_11_16_name, protect_content=True)
                            elif message.text == markups.mod2_11_b17:
                                await bot.send_video(message.chat.id, les_video.mod2_11_17,
                                                     caption=les_video.mod2_11_17_name, protect_content=True)
                            elif message.text == markups.mod2_11_b18:
                                await bot.send_video(message.chat.id, les_video.mod2_11_18,
                                                     caption=les_video.mod2_11_18_name, protect_content=True)
                            elif message.text == markups.mod2_11_b19:
                                await bot.send_video(message.chat.id, les_video.mod2_11_19,
                                                     caption=les_video.mod2_11_19_name, protect_content=True)
                            elif message.text == markups.mod2_11_b20:
                                await bot.send_video(message.chat.id, les_video.mod2_11_20,
                                                     caption=les_video.mod2_11_20_name, protect_content=True)
                            elif message.text == markups.mod2_11_b21:
                                await bot.send_video(message.chat.id, les_video.mod2_11_21,
                                                     caption=les_video.mod2_11_21_name, protect_content=True)
                            elif message.text == markups.mod2_bonus_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_bonus_1,
                                                     caption=les_video.mod2_bonus_1_name, protect_content=True)
                            elif message.text == markups.mod2_bonus_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_bonus_2,
                                                     caption=les_video.mod2_bonus_2_name, protect_content=True)
                            elif message.text == markups.mod2_bonus_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_bonus_3,
                                                     caption=les_video.mod2_bonus_3_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu12)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 11:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod2_7_text, reply_markup=markups.mod2_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod2_8_text, reply_markup=markups.mod2_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                                await message.answer(text=texts.mod2_9_text, reply_markup=markups.mod2_9_menu)
                            elif message.text == markups.pack1_menu_b10:
                                await message.answer(text=texts.mod2_10_text, reply_markup=markups.mod2_10_menu)
                            elif message.text == markups.pack2_menu_b11:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_11_text, reply_markup=markups.mod2_11_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            elif message.text == markups.mod2_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_7_1,
                                                     caption=les_video.mod2_7_1_name, protect_content=True)
                            elif message.text == markups.mod2_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_7_2,
                                                     caption=les_video.mod2_7_2_name, protect_content=True)
                            elif message.text == markups.mod2_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_8_1,
                                                     caption=les_video.mod2_8_1_name, protect_content=True)
                            elif message.text == markups.mod2_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_8_2,
                                                     caption=les_video.mod2_8_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_9_1,
                                                     caption=les_video.mod2_9_1_name, protect_content=True)
                            elif message.text == markups.mod2_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_9_2,
                                                     caption=les_video.mod2_9_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_9_3,
                                                     caption=les_video.mod2_9_3_name, protect_content=True)
                            elif message.text == markups.mod2_10_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_10_1,
                                                     caption=les_video.mod2_10_1_name, protect_content=True)
                            elif message.text == markups.mod2_10_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_10_2,
                                                     caption=les_video.mod2_10_2_name, protect_content=True)
                            elif message.text == markups.mod2_11_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_11_1,
                                                     caption=les_video.mod2_11_1_name, protect_content=True)
                            elif message.text == markups.mod2_11_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_11_2,
                                                     caption=les_video.mod2_11_2_name, protect_content=True)
                            elif message.text == markups.mod2_11_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_11_3,
                                                     caption=les_video.mod2_11_3_name, protect_content=True)
                            elif message.text == markups.mod2_11_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_11_4,
                                                     caption=les_video.mod2_11_4_name, protect_content=True)
                            elif message.text == markups.mod2_11_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_11_5,
                                                     caption=les_video.mod2_11_5_name, protect_content=True)
                            elif message.text == markups.mod2_11_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_11_6,
                                                     caption=les_video.mod2_11_6_name, protect_content=True)
                            elif message.text == markups.mod2_11_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_11_7,
                                                     caption=les_video.mod2_11_7_name, protect_content=True)
                            elif message.text == markups.mod2_11_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_11_8,
                                                     caption=les_video.mod2_11_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_8_2, protect_content=True)
                            elif message.text == markups.mod2_11_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_11_9,
                                                     caption=les_video.mod2_11_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_9_2, protect_content=True)
                            elif message.text == markups.mod2_11_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_11_10,
                                                     caption=les_video.mod2_11_10_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_11_10_5, protect_content=True)
                            elif message.text == markups.mod2_11_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_11_11,
                                                     caption=les_video.mod2_11_11_name, protect_content=True)
                            elif message.text == markups.mod2_11_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_11_12,
                                                     caption=les_video.mod2_11_12_name, protect_content=True)
                            elif message.text == markups.mod2_11_b13:
                                await bot.send_video(message.chat.id, les_video.mod2_11_13,
                                                     caption=les_video.mod2_11_13_name, protect_content=True)
                            elif message.text == markups.mod2_11_b14:
                                await bot.send_video(message.chat.id, les_video.mod2_11_14,
                                                     caption=les_video.mod2_11_14_name, protect_content=True)
                            elif message.text == markups.mod2_11_b15:
                                await bot.send_video(message.chat.id, les_video.mod2_11_15,
                                                     caption=les_video.mod2_11_15_name, protect_content=True)
                            elif message.text == markups.mod2_11_b16:
                                await bot.send_video(message.chat.id, les_video.mod2_11_16,
                                                     caption=les_video.mod2_11_16_name, protect_content=True)
                            elif message.text == markups.mod2_11_b17:
                                await bot.send_video(message.chat.id, les_video.mod2_11_17,
                                                     caption=les_video.mod2_11_17_name, protect_content=True)
                            elif message.text == markups.mod2_11_b18:
                                await bot.send_video(message.chat.id, les_video.mod2_11_18,
                                                     caption=les_video.mod2_11_18_name, protect_content=True)
                            elif message.text == markups.mod2_11_b19:
                                await bot.send_video(message.chat.id, les_video.mod2_11_19,
                                                     caption=les_video.mod2_11_19_name, protect_content=True)
                            elif message.text == markups.mod2_11_b20:
                                await bot.send_video(message.chat.id, les_video.mod2_11_20,
                                                     caption=les_video.mod2_11_20_name, protect_content=True)
                            elif message.text == markups.mod2_11_b21:
                                cur.execute(f"UPDATE users SET module = '{12}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_11_21,
                                                     caption=les_video.mod2_11_21_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu11)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 10:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod2_7_text, reply_markup=markups.mod2_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod2_8_text, reply_markup=markups.mod2_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                                await message.answer(text=texts.mod2_9_text, reply_markup=markups.mod2_9_menu)
                            elif message.text == markups.pack1_menu_b10:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_10_text, reply_markup=markups.mod2_10_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            elif message.text == markups.mod2_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_7_1,
                                                     caption=les_video.mod2_7_1_name, protect_content=True)
                            elif message.text == markups.mod2_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_7_2,
                                                     caption=les_video.mod2_7_2_name, protect_content=True)
                            elif message.text == markups.mod2_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_8_1,
                                                     caption=les_video.mod2_8_1_name, protect_content=True)
                            elif message.text == markups.mod2_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_8_2,
                                                     caption=les_video.mod2_8_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_9_1,
                                                     caption=les_video.mod2_9_1_name, protect_content=True)
                            elif message.text == markups.mod2_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_9_2,
                                                     caption=les_video.mod2_9_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_9_3,
                                                     caption=les_video.mod2_9_3_name, protect_content=True)
                            elif message.text == markups.mod2_10_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_10_1,
                                                     caption=les_video.mod2_10_1_name, protect_content=True)
                            elif message.text == markups.mod2_10_b2:
                                cur.execute(f"UPDATE users SET module = '{11}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_10_2,
                                                     caption=les_video.mod2_10_2_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu10)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 9:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod2_7_text, reply_markup=markups.mod2_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                                await message.answer(text=texts.mod2_8_text, reply_markup=markups.mod2_8_menu)
                            elif message.text == markups.pack1_menu_b9:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_9_text, reply_markup=markups.mod2_9_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            elif message.text == markups.mod2_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_7_1,
                                                     caption=les_video.mod2_7_1_name, protect_content=True)
                            elif message.text == markups.mod2_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_7_2,
                                                     caption=les_video.mod2_7_2_name, protect_content=True)
                            elif message.text == markups.mod2_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_8_1,
                                                     caption=les_video.mod2_8_1_name, protect_content=True)
                            elif message.text == markups.mod2_8_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_8_2,
                                                     caption=les_video.mod2_8_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_9_1,
                                                     caption=les_video.mod2_9_1_name, protect_content=True)
                            elif message.text == markups.mod2_9_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_9_2,
                                                     caption=les_video.mod2_9_2_name, protect_content=True)
                            elif message.text == markups.mod2_9_b3:
                                cur.execute(f"UPDATE users SET module = '{10}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_9_3,
                                                     caption=les_video.mod2_9_3_name,protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu9)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 8:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                await message.answer(text=texts.mod2_7_text, reply_markup=markups.mod2_7_menu)
                            elif message.text == markups.pack1_menu_b8:
                            #    await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_8_text, reply_markup=markups.mod2_8_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            elif message.text == markups.mod2_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_7_1,
                                                     caption=les_video.mod2_7_1_name, protect_content=True)
                            elif message.text == markups.mod2_7_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_7_2,
                                                     caption=les_video.mod2_7_2_name, protect_content=True)
                            elif message.text == markups.mod2_8_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_8_1,
                                                     caption=les_video.mod2_8_1_name, protect_content=True)
                            elif message.text == markups.mod2_8_b2:
                                cur.execute(f"UPDATE users SET module = '{9}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_8_2,
                                                     caption=les_video.mod2_8_2_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu8)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 7:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.pack1_menu_b7:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_7_text, reply_markup=markups.mod2_7_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            elif message.text == markups.mod2_7_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_7_1,
                                                     caption=les_video.mod2_7_1_name, protect_content=True)
                            elif message.text == markups.mod2_7_b2:
                                cur.execute(f"UPDATE users SET module = '{8}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_7_2,
                                                     caption=les_video.mod2_7_2_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu7)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 6:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.pack1_menu_b6:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_6_text, reply_markup=markups.mod2_6_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_6_1,
                                                     caption=les_video.mod2_6_1_name, protect_content=True)
                            elif message.text == markups.mod2_6_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_6_2,
                                                     caption=les_video.mod2_6_2_name, protect_content=True)
                            elif message.text == markups.mod2_6_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_6_3,
                                                     caption=les_video.mod2_6_3_name, protect_content=True)
                            elif message.text == markups.mod2_6_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_6_4,
                                                     caption=les_video.mod2_6_4_name, protect_content=True)
                            elif message.text == markups.mod2_6_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_6_5,
                                                     caption=les_video.mod2_6_5_name, protect_content=True)
                            elif message.text == markups.mod2_6_b6:
                                cur.execute(f"UPDATE users SET module = '{7}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_6_6,
                                                     caption=les_video.mod2_6_6_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu6)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 5:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.pack1_menu_b5:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_5_text, reply_markup=markups.mod2_5_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            elif message.text == markups.mod2_5_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_5_1,
                                                     caption=les_video.mod2_5_1_name, protect_content=True)
                            elif message.text == markups.mod2_5_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_5_2,
                                                     caption=les_video.mod2_5_2_name, protect_content=True)
                            elif message.text == markups.mod2_5_b3:
                                cur.execute(f"UPDATE users SET module = '{6}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_5_3,
                                                     caption=les_video.mod2_5_3_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu5)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 4:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.pack1_menu_b4:
                                await message.answer(text=texts.mod2_4_text, reply_markup=markups.mod2_4_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            elif message.text == markups.mod2_4_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_4_1,
                                                     caption=les_video.mod2_4_1_name, protect_content=True)
                            elif message.text == markups.mod2_4_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_4_2,
                                                     caption=les_video.mod2_4_2_name, protect_content=True)
                            elif message.text == markups.mod2_4_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_4_3,
                                                     caption=les_video.mod2_4_3_name, protect_content=True)
                            elif message.text == markups.mod2_4_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_4_4,
                                                     caption=les_video.mod2_4_4_name, protect_content=True)
                            elif message.text == markups.mod2_4_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_4_5,
                                                     caption=les_video.mod2_4_5_name, protect_content=True)
                            elif message.text == markups.mod2_4_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_4_6,
                                                     caption=les_video.mod2_4_6_name, protect_content=True)
                            elif message.text == markups.mod2_4_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_4_7,
                                                     caption=les_video.mod2_4_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_7_2, protect_content=True)
                            elif message.text == markups.mod2_4_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_4_8,
                                                     caption=les_video.mod2_4_8_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_8_2, protect_content=True)
                            elif message.text == markups.mod2_4_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_4_9,
                                                     caption=les_video.mod2_4_9_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_2, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_3, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_4, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_4_9_5, protect_content=True)
                            elif message.text == markups.mod2_4_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_4_10,
                                                     caption=les_video.mod2_4_10_name, protect_content=True)
                            elif message.text == markups.mod2_4_b11:
                                await bot.send_video(message.chat.id, les_video.mod2_4_11,
                                                     caption=les_video.mod2_4_11_name, protect_content=True)
                            elif message.text == markups.mod2_4_b12:
                                cur.execute(f"UPDATE users SET module = '{5}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_4_12,
                                                     caption=les_video.mod2_4_12_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu4)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 3:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.pack1_menu_b3:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_3_text, reply_markup=markups.mod2_3_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            elif message.text == markups.mod2_3_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_3_1,
                                                     caption=les_video.mod2_3_1_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_1, protect_content=True)
                            elif message.text == markups.mod2_3_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_3_2,
                                                     caption=les_video.mod2_3_2_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_2, protect_content=True)
                            elif message.text == markups.mod2_3_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_3_3,
                                                     caption=les_video.mod2_3_3_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_3, protect_content=True)
                            elif message.text == markups.mod2_3_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_3_4,
                                                     caption=les_video.mod2_3_4_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_4, protect_content=True)
                            elif message.text == markups.mod2_3_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_3_5,
                                                     caption=les_video.mod2_3_5_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_5, protect_content=True)
                            elif message.text == markups.mod2_3_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_3_6,
                                                     caption=les_video.mod2_3_6_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_6, protect_content=True)
                            elif message.text == markups.mod2_3_b7:
                                cur.execute(f"UPDATE users SET module = '{4}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_3_7,
                                                     caption=les_video.mod2_3_7_name, protect_content=True)
                                await bot.send_document(message.chat.id, les_doc.mod2_3_7, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu3)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 2:
                            if message.text == markups.pack1_menu_b1:
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.pack1_menu_b2:
                                await message.answer(text=texts.mod2_2_text, reply_markup=markups.mod2_2_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_2_1,
                                                     caption=les_video.mod2_2_1_name, protect_content=True)
                            elif message.text == markups.mod2_2_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_2_2,
                                                     caption=les_video.mod2_2_2_name, protect_content=True)
                            elif message.text == markups.mod2_2_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_2_3,
                                                     caption=les_video.mod2_2_3_name, protect_content=True)
                            elif message.text == markups.mod2_2_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_2_4,
                                                     caption=les_video.mod2_2_4_name, protect_content=True)
                            elif message.text == markups.mod2_2_b5:
                                await bot.send_video(message.chat.id, les_video.mod2_2_5,
                                                     caption=les_video.mod2_2_5_name, protect_content=True)
                            elif message.text == markups.mod2_2_b6:
                                await bot.send_video(message.chat.id, les_video.mod2_2_6,
                                                     caption=les_video.mod2_2_6_name, protect_content=True)
                            elif message.text == markups.mod2_2_b7:
                                await bot.send_video(message.chat.id, les_video.mod2_2_7,
                                                     caption=les_video.mod2_2_7_name, protect_content=True)
                            elif message.text == markups.mod2_2_b8:
                                await bot.send_video(message.chat.id, les_video.mod2_2_8,
                                                     caption=les_video.mod2_2_8_name, protect_content=True)
                            elif message.text == markups.mod2_2_b9:
                                await bot.send_video(message.chat.id, les_video.mod2_2_9,
                                                     caption=les_video.mod2_2_9_name, protect_content=True)
                            elif message.text == markups.mod2_2_b10:
                                cur.execute(f"UPDATE users SET module = '{3}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_2_10,
                                                     caption=les_video.mod2_2_10_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu2)

                        cur.execute(f"SELECT module FROM users WHERE id_user = '{message.chat.id}'")
                        if cur.fetchone()[0] == 1:
                            if message.text == markups.pack1_menu_b1:
                                # await message.answer(text=texts.error_text)
                                await message.answer(text=texts.mod2_1_text, reply_markup=markups.mod2_1_menu)
                            elif message.text == markups.mod2_1_b1:
                                await bot.send_video(message.chat.id, les_video.mod2_1_1,
                                                     caption=les_video.mod2_1_1_name, protect_content=True)
                            elif message.text == markups.mod2_1_b2:
                                await bot.send_video(message.chat.id, les_video.mod2_1_2,
                                                     caption=les_video.mod2_1_2_name, protect_content=True)
                            elif message.text == markups.mod2_1_b3:
                                await bot.send_video(message.chat.id, les_video.mod2_1_3,
                                                     caption=les_video.mod2_1_3_name, protect_content=True)
                            elif message.text == markups.mod2_1_b4:
                                await bot.send_video(message.chat.id, les_video.mod2_1_4,
                                                     caption=les_video.mod2_1_4_name, protect_content=True)
                            elif message.text == markups.mod2_1_b5:
                                cur.execute(f"UPDATE users SET module = '{2}' WHERE id_user = '{message.chat.id}'")
                                db.commit()
                                await bot.send_video(message.chat.id, les_video.mod2_1_5,
                                                     caption=les_video.mod2_1_5_name, protect_content=True)
                            else:
                                await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu1)
                                

                    cur.execute(f"SELECT flag_les_all FROM users WHERE id_user = '{message.chat.id}'")
                    if cur.fetchone()[0] == 0:
                        if message.text == markups.pack_menu_b1:
                            cur.execute(f"UPDATE users SET flag_les_all = '{1}' WHERE id_user = '{message.chat.id}'")
                            db.commit()
                            cur.execute(f"UPDATE users SET module = '{1}' WHERE id_user = '{message.chat.id}'")
                            db.commit()
                            await message.answer(text=texts.pack1_start_text)
                            await message.answer(text=texts.pack1_text, reply_markup=markups.pack1_menu1)
                        elif message.text == markups.pack_menu_b2:
                            cur.execute(f"UPDATE users SET flag_les_all = '{2}' WHERE id_user = '{message.chat.id}'")
                            db.commit()
                            cur.execute(f"UPDATE users SET module = '{1}' WHERE id_user = '{message.chat.id}'")
                            db.commit()
                            await message.answer(text=texts.pack2_start_text)
                            await message.answer(text=texts.pack2_text, reply_markup=markups.pack2_menu1)
                        else:
                            await message.answer(text=texts.pack_text, reply_markup=markups.pack_menu)


if __name__ == '__main__':
    executor.start_polling(disp, on_startup=startup, skip_updates=True)