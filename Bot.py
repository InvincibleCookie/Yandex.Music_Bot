from sorting import *
import telebot
from telebot import types
import time
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

bot = telebot.TeleBot('5102168831:AAHZAlDmEBOqUUEUBRP4hb3GQYFc36JR9gM')

Link = False
Sorting_playlist = False
Coping_playlist = False
Choosing_playlist = False
Clone = False


@bot.message_handler(commands=["start"])
def start(m, res=False):
    global loading
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    item1 = types.KeyboardButton("Вход")
    markup.add(item1)
    bot.send_message(m.chat.id, 'Вас приветсвует Яндекс.Музыка бот', reply_markup=markup)


def fiches():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сортировать плейлист")
    item2 = types.KeyboardButton("Обновить «Мне нравится»")
    item3 = types.KeyboardButton("Сделать копию плейлиста")
    markup.add(item1, item2)
    markup.add(item3)
    return markup


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global Link
    global client
    global Sorting_playlist
    global Coping_playlist
    global Choosing_playlist
    global Sorting_by
    global playlist_tracks
    global Playlist
    global Clone
    global Sort
    if Link:
        try:
            client = autorisation(str(message))
            Link = False
            bot.send_message(message.chat.id, 'Отлично, вы вошли. Что будем делать?', reply_markup=fiches())
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте отправить ссылку ещё раз')

    elif message.text.strip() == 'Вход':
        loading = bot.send_video(message.chat.id, 'https://i.gifer.com/L6MI.gif', None).message_id
        pc = types.InputMediaVideo(open('pc.mp4', 'rb'))
        phone = types.InputMediaVideo(open('phone.mp4', 'rb'))
        bot.send_media_group(message.chat.id, [pc, phone], None)
        answer = '''Перейди по ссылке \n https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d \n
И как на видео (Слева - для компьютера, справа - для телефона)\nво время перехода успей скопировать новую ссылку до того, как в адресной строке появится music.yandex.ru/home
                  \nПосле чего отправь скопированную целиком ссылку cообщением.\nВ этой ссылке находится токен, который необходим для авторизации'''
        bot.send_message(message.chat.id, answer, disable_web_page_preview=True,
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.delete_message(message.chat.id, loading)
        Link = True


    elif message.text.strip() == 'Сортировать плейлист':
        markup = types.ReplyKeyboardMarkup(row_width=4)
        markup.add(types.KeyboardButton("По исполнителю"), types.KeyboardButton("По альбому"))
        markup.add(types.KeyboardButton("По исполнителю и альбому"))
        markup.add(types.KeyboardButton('⬅ Назад'))
        bot.send_message(message.chat.id, 'Как отсортировать плейлист?',
                         reply_markup=markup)


    elif message.text.strip() == "По исполнителю и альбому":
        Sorting_by = 'По исполнителю и альбому'
        Choosing_playlist = True

    elif message.text.strip() == 'По исполнителю':
        Sorting_by = 'По исполнителю'
        Choosing_playlist = True
    elif message.text.strip() == 'По альбому':
        Sorting_by = 'По альбому'
        Choosing_playlist = True



    elif message.text.strip() == 'Обновить «Мне нравится»':
        bot.send_message(message.chat.id, 'Это займет некоторое время',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        loading = bot.send_video(message.chat.id, 'https://i.gifer.com/L6MI.gif', None).message_id
        try:
            liked_songs(client)
            bot.delete_message(message.chat.id, loading)
            bot.send_video(message.chat.id, 'https://i.gifer.com/Y0jp.gif', None)
            bot.send_message(message.chat.id, 'Готово!')
            bot.send_message(message.chat.id, 'Что-нибудь ещё?', reply_markup=fiches())
        except:
            bot.send_video(message.chat.id, 'https://i.gifer.com/2yOW.gif', None)
            bot.send_message(message.chat.id, 'Извини, что-то пошло не так. Можешь попробовать снова',
                             reply_markup=fiches())

    elif message.text.strip() == "Сделать копию плейлиста":
        markup = types.ReplyKeyboardMarkup(row_width=4)
        for e in client.users_playlists_list():
            markup.add(types.KeyboardButton(e['title']))
        markup.add(types.KeyboardButton('⬅ Назад'))
        Choosing_playlist = True
        Clone = True


    elif message.text.strip() == '⬅ Назад':
        Coping_playlist = False
        Sorting_playlist = False
        Choosing_playlist = False
        bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=fiches())

    if Choosing_playlist:
        markup = types.ReplyKeyboardMarkup(row_width=4)
        try:
            for e in client.users_playlists_list():
                markup.add(types.KeyboardButton(e['title']))
            markup.add(types.KeyboardButton('⬅ Назад'))
            if Clone:
                bot.send_message(message.chat.id, 'Выбери плейлист, который надо скопировать',
                                 reply_markup=markup)
                Choosing_playlist = False
                Coping_playlist = True
            else:
                bot.send_message(message.chat.id, 'Выбери плейлист, который надо отсортировать',
                                 reply_markup=markup)
                Choosing_playlist = False
                Sorting_playlist = True

        except:
            bot.send_message(message.chat.id, 'Извини, что-то пошло не так. Можешь попробовать снова',
                             reply_markup=fiches())

    elif Sorting_playlist:
        bot.send_message(message.chat.id, 'Это займет некоторое время',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        loading = bot.send_video(message.chat.id, 'https://i.gifer.com/L6MI.gif', None).message_id
        try:
            for e in client.users_playlists_list():
                if message.text.strip() == e['title']:
                    Playlist = get_playlist(e['title'], client)
                    playlist_tracks = sorting(Playlist, Sorting_by, client)
                    if len(playlist_tracks) > 200 and len(playlist_tracks) < 500:
                        time.sleep(10)
                        finish_sorting(playlist_tracks[0: (len(playlist_tracks) // 3)], Playlist)
                        time.sleep(10)
                        finish_sorting(playlist_tracks[(len(playlist_tracks) // 3): 2 * (len(playlist_tracks) // 3)],
                                       Playlist)
                        time.sleep(10)
                        finish_sorting(playlist_tracks[2 * (len(playlist_tracks) // 3): len(playlist_tracks)], Playlist)
                    elif len(playlist_tracks) > 500:
                        finish_sorting(playlist_tracks[0: (len(playlist_tracks) // 5)], Playlist)
                        time.sleep(20)
                        finish_sorting(playlist_tracks[(len(playlist_tracks) // 5): 2 * (len(playlist_tracks) // 5)],
                                       Playlist)
                        time.sleep(20)
                        finish_sorting(
                            playlist_tracks[2 * (len(playlist_tracks) // 5): 3 * (len(playlist_tracks) // 5)], Playlist)
                        time.sleep(20)
                        finish_sorting(
                            playlist_tracks[3 * (len(playlist_tracks) // 5): 4 * (len(playlist_tracks) // 5)], Playlist)
                        time.sleep(20)
                        finish_sorting(playlist_tracks[4 * (len(playlist_tracks) // 5): (len(playlist_tracks))],
                                       Playlist)
                    else:
                        time.sleep(10)
                        finish_sorting(playlist_tracks, Playlist)
                    break

            bot.delete_message(message.chat.id, loading)
            bot.send_video(message.chat.id, 'https://i.gifer.com/Y0jp.gif', None)
            bot.send_message(message.chat.id, 'Готово!', reply_markup=fiches())
            Sorting_playlist = False
        except:
            bot.delete_message(message.chat.id, loading)
            bot.send_video(message.chat.id, 'https://i.gifer.com/2yOW.gif', None)
            bot.send_message(message.chat.id, 'Извини, что-то пошло не так. Можешь попробовать снова',
                             reply_markup=fiches())
            Sorting_playlist = False

    elif Coping_playlist:
        Clone = False
        bot.send_message(message.chat.id, 'Это займет некоторое время',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        loading = bot.send_video(message.chat.id, 'https://i.gifer.com/L6MI.gif', None).message_id
        try:
            for e in client.users_playlists_list():
                if message.text.strip() == e['title']:

                    playlist, copy_playlist = playlist_copy(e['title'], client)
                    if len(playlist.tracks) >= 200 and len(playlist.tracks) < 500:
                        time.sleep(20)
                        finish_sorting(playlist.tracks[::-1][0: (len(playlist.tracks) // 3)], copy_playlist)
                        time.sleep(20)
                        finish_sorting(
                            playlist.tracks[::-1][(len(playlist.tracks) // 3):2 * (len(playlist.tracks) // 3)],
                            copy_playlist)
                        time.sleep(20)
                        finish_sorting(playlist.tracks[::-1][2 * (len(playlist.tracks) // 3):(len(playlist.tracks))],
                                       copy_playlist)

                    elif len(playlist.tracks) >= 500:
                        time.sleep(20)
                        finish_sorting(playlist.tracks[::-1][0: (len(playlist.tracks) // 5)], copy_playlist)
                        time.sleep(20)
                        finish_sorting(
                            playlist.tracks[::-1][(len(playlist.tracks) // 5):2 * (len(playlist.tracks) // 5)],
                            copy_playlist)
                        time.sleep(20)
                        finish_sorting(
                            playlist.tracks[::-1][2 * (len(playlist.tracks) // 5):(3 * len(playlist.tracks)) // 5],
                            copy_playlist)
                        time.sleep(20)
                        finish_sorting(
                            playlist.tracks[::-1][3 * (len(playlist.tracks) // 5):4 * (len(playlist.tracks) // 5)],
                            copy_playlist)
                        time.sleep(20)
                        finish_sorting(playlist.tracks[::-1][4 * (len(playlist.tracks) // 5):(len(playlist.tracks))],
                                       copy_playlist)
                    else:
                        finish_sorting(playlist.tracks[::-1], copy_playlist)
                    break
            bot.delete_message(message.chat.id, loading)
            bot.send_video(message.chat.id, 'https://i.gifer.com/Y0jp.gif', None)
            bot.send_message(message.chat.id, 'Готово!', reply_markup=fiches())

            Coping_playlist = False
        except:
            bot.delete_message(message.chat.id, loading)
            bot.send_video(message.chat.id, 'https://i.gifer.com/2yOW.gif', None)
            bot.send_message(message.chat.id, 'Извини, что-то пошло не так. Можешь попробовать снова',
                             reply_markup=fiches())
            Coping_playlist = False


bot.polling(none_stop=True, interval=0)
