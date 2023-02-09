import telegram.ext
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, Application
from Tools import slice_lst, get_lst, base_key, send_mail
from stats import new_json_data, plot_total_data, plot_detail_data, plot_pie_data, refresh_data
import random
import logging
import os
import asyncio

Start, Books, Dictados, MeloHind, Sequences, Reconocimientos, Solfeos, Teoria = range(8)

#logging.basicConfig(filename="log.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)
#logger = logging.getLogger(__name__)

TOKEN = json.load(open("token.json"))["testtok"]
devid = json.load(open("token.json"))["chatid"]
reconocimientos = json.load(open("reconicimientos.json"))
teoria = json.load(open("teoria.json"))
#updater = telegram.ext.Updater(TOKEN, use_context=True)
application = Application.builder().token(TOKEN).build()
#disp = updater.dispatcher
datos = json.load(open("datos.json"))
tyc = json.load(open("typ.json"))

def main():
    #TOKEN = json.load(open("token.json"))["testtok"]
    #updater = telegram.ext.Updater(TOKEN, use_context=True)
    #disp = updater.dispatcher

    conv_handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler("start",start),
                      telegram.ext.CallbackQueryHandler(pattern="home", callback=start_over)],
        states={
            Start: [telegram.ext.CallbackQueryHandler(pattern="bib", callback=books),
                    telegram.ext.CallbackQueryHandler(pattern="dict", callback=mel_rit),
                    telegram.ext.CallbackQueryHandler(pattern="lect", callback=mel_rit),
                    telegram.ext.CallbackQueryHandler(pattern="hind", callback=chapters),
                    telegram.ext.CallbackQueryHandler(pattern="melo", callback=chapters),
                    telegram.ext.CallbackQueryHandler(pattern="secuencias", callback=sequence),
                    telegram.ext.CallbackQueryHandler(pattern="solf", callback=solf),
                    telegram.ext.CallbackQueryHandler(pattern="rec", callback=recon),
                    telegram.ext.CallbackQueryHandler(pattern="teo", callback=teo),
                    telegram.ext.CallbackQueryHandler(pattern="rep", callback=rep)],
            Dictados: [telegram.ext.CallbackQueryHandler(pattern="dict", callback=mel_rit),
                       telegram.ext.CallbackQueryHandler(pattern="lect", callback=mel_rit),
                       telegram.ext.CallbackQueryHandler(pattern="a", callback=años),
                       telegram.ext.CallbackQueryHandler(pattern="b", callback=dic_lec_lst),
                       telegram.ext.CallbackQueryHandler(pattern="c", callback=send_dic_lec),
                       telegram.ext.CallbackQueryHandler(pattern="d", callback=send_tyc),
                       telegram.ext.CallbackQueryHandler(pattern="e", callback=send_sol)],
            MeloHind: [telegram.ext.CallbackQueryHandler(pattern="melo", callback=chapters),
                       telegram.ext.CallbackQueryHandler(pattern="hind", callback=chapters),
                       telegram.ext.CallbackQueryHandler(pattern="f", callback=melo_hind_list),
                       telegram.ext.CallbackQueryHandler(pattern="g", callback=send_melo_hind)],
            Books: [telegram.ext.CallbackQueryHandler(pattern="bib", callback=books),
                telegram.ext.CallbackQueryHandler(pattern="h", callback=send_pdf)],
            Sequences: [telegram.ext.CallbackQueryHandler(pattern="secuencias", callback=sequence),
                        telegram.ext.CallbackQueryHandler(pattern="i", callback=seq2),
                        telegram.ext.CallbackQueryHandler(pattern="j", callback=seq3),
                        telegram.ext.CallbackQueryHandler(pattern="k", callback=seq4),
                        telegram.ext.CallbackQueryHandler(pattern="l", callback=snd_scale_or_pulse),
                        telegram.ext.CallbackQueryHandler(pattern="m", callback=seq_sol),
                        telegram.ext.CallbackQueryHandler(pattern="n", callback=snd_seq)],
            Solfeos: [telegram.ext.CallbackQueryHandler(pattern="solf", callback=solf),
                      telegram.ext.CallbackQueryHandler(pattern="ñ", callback=solf_lst),
                      telegram.ext.CallbackQueryHandler(pattern="o", callback=snd_solf)],
            Reconocimientos: [telegram.ext.CallbackQueryHandler(pattern="rec", callback=recon),
                              telegram.ext.CallbackQueryHandler(pattern="p", callback=recon2),
                              telegram.ext.CallbackQueryHandler(pattern="q", callback=snd_recon),
                              telegram.ext.CallbackQueryHandler(pattern="r", callback=recon_sol)],
            Teoria: [telegram.ext.CallbackQueryHandler(pattern="teo", callback=teo),
                     telegram.ext.CallbackQueryHandler(pattern="s", callback=teo2),
                     telegram.ext.CallbackQueryHandler(pattern="t", callback=teo3),
                     telegram.ext.CallbackQueryHandler(pattern="u", callback=teo4),
                     telegram.ext.CallbackQueryHandler(pattern="v", callback=teo5),
                     telegram.ext.CallbackQueryHandler(pattern="w", callback=teosol)]
        },
        fallbacks=[telegram.ext.CallbackQueryHandler(pattern="end", callback=end)],
        allow_reentry=True
    )

    ##disp.add_handler(conv_handler)
    application.add_handler(conv_handler)
    #disp.add_handler(telegram.ext.CommandHandler("stats", stats))
    application.add_handler(telegram.ext.CommandHandler("stats", stats))
    ##disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    application.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT, handle_message))
    ##disp.add_error_handler(error)
    application.add_error_handler(error)

    ##updater.start_polling(drop_pending_updates=True, timeout=15)
    application.run_polling()
    ##updater.idle()

async def mel_rit(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i, j in zip(datos[c[0]][0], datos[c[0]][1]):
        k2.append(InlineKeyboardButton(i, callback_data="a" + j))

    keyboard.append(k2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        text="\U0001f916 <strong>" + datos[c[0]][0][0] + " o " + datos[c[0]][0][1] + "?</strong>",
        reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

    return Dictados


async def años(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    for i in datos["years"]:
        k2.append(InlineKeyboardButton(i, callback_data="b" + i))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>De que año?</strong>", reply_markup=reply_markup,
                                            parse_mode=telegram.constants.ParseMode.HTML)


async def dic_lec_lst(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "a" + c[1], two=False)
    k2 = []
    d = {"m": True, "r": False}
    try:
        for i in get_lst(c[0] + "/" + c[1] + "/" + c[2], clear=True, nr=d[c[1]]):
            k2.append(InlineKeyboardButton(str(i), callback_data="c" + str(i)))
        keyboard = slice_lst(k2, keyboard, 4)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(text="\U0001f916<strong>" + datos[c[0]][2] + "</strong>",
                                                reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    except: # FileNotFoundError
        await error_no_file(update, context)



async def send_dic_lec(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    logging.info("Sending Dict/Lect -- " + c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3])
    path = c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3]

    if c[0] == "dict":
        await update.callback_query.edit_message_text(text="\U0001f916 <strong>Esperá.. te voy a mandar 5 audios\n"
                                                     "Ahí van..!! </strong>",
                                                      parse_mode=telegram.constants.ParseMode.HTML)
        if c[1] == "m":
            new_json_data("dm")
            nro = u"\U0001F3BC " + c[2] + " / " + c[3] + u" \U0001F449"
            cp = "captionm"
        elif c[1] == "r":
            new_json_data("dr")
            nro = u"\U0001F941 " + c[2] + " / " + c[3] + u" \U0001F449"
            cp = "captionr"

        for i, j in zip(get_lst(path, clear=False, nr=False), datos[cp]):
            await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            with open(path + "/" + i, "rb") as audio_file:
                await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                       caption=nro + j)

        keyboard = [[InlineKeyboardButton("Volver a dictados", callback_data="dict")],
                    [InlineKeyboardButton("Tonalidad y/o compás", callback_data="d")],
                    [InlineKeyboardButton("Solución", callback_data="e")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Elegí una opción</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    elif c[0] == "lect":
        await update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 working.... </strong>",
                                                parse_mode=telegram.constants.ParseMode.HTML)
        if c[1] == "m":
            new_json_data("lm")
            msg = u'\U0001F440 \U0001F3BC' + " Nro: " + c[3]
        elif c[1] == "r":
            new_json_data("lr")
            msg = u'\U0001F440 \U0001F941' + " Letra: " + c[3]

        with open(path + ".png", "rb") as photo_file:
            await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            await context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                                         caption=msg)
        keyboard = base_key("Volver a lecturas", "lect", two=False)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Elegí una opción</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    else:
        return error_no_file(update, context)


async def send_sol(update, context):
    await update.callback_query.answer()
    c = context.user_data
    path = c[1] + "/" + c[2] + "/" + c[3]
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>A ver.........</strong>",
                                            parse_mode=telegram.constants.ParseMode.HTML)
    with open("dictimag/" + path + ".png", "rb") as photo_file:
        await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_photo")
        await context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                               caption=u'\U0001F648 \U0001F91E \U0001F91E \U0001F91E')
    keyboard = base_key("Volver a dictados", "dict", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí una opción</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def send_tyc(update, context):
    await update.callback_query.answer()
    c = context.user_data
    keyboard = [[InlineKeyboardButton("volver a dictados", callback_data="dict")],
                [InlineKeyboardButton("Solución", callback_data="e")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=" \U0001f916 <strong>Está en: " + tyc[c[1]][c[2]][c[3]] +
                                                 "</strong>", reply_markup=reply_markup,
                                            parse_mode=telegram.constants.ParseMode.HTML)


async def chapters(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in datos[c[0]]:
        k2.append(InlineKeyboardButton("Cap" + i, callback_data="f" + i))
    keyboard = slice_lst(k2, keyboard, 4)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Elegí un capítulo</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return MeloHind

async def melo_hind_list(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    try:
        for i in get_lst(c[0] + "/" + c[1], clear=True, nr=False):
            k2.append(InlineKeyboardButton(i, callback_data="g" + i))
        keyboard = slice_lst(k2, keyboard, 3)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(text="\U0001f916 <strong>Puedo ofrecerte estos ejercicios:</strong>",
                                                      reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    except:
        await error_no_file(update, context)


async def send_melo_hind(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    logging.info("Sending Melo/Hind -- " + c[0] + "/" + c[1] + "/" + c[2])
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 procesando...</strong>",
                                            parse_mode=telegram.constants.ParseMode.HTML)
    if c[0] == "melo":
        new_json_data("melo")
        cap = u'\U0001F941' + " Melo Castillo " + c[2]
    elif c[0] == "hind":
        new_json_data("hind")
        cap = u'\U0001F941' + " Hindemith " + c[2]

    with open(c[0] + "/" + c[1] + "/" + c[2] + ".mp3", "rb") as audio_file:
        await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
        await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption=cap)

    keyboard = base_key("Atras", "f" + c[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Hecho!!, Como seguimos...?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def books(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0], clear=True, nr=False):
        k2.append(InlineKeyboardButton(i, callback_data="h" + i))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Tengo estos libros:</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return Books


async def send_pdf(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    logging.info("Sending .pdf file -- " + c[1])
    new_json_data("bib")
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Esperame que lo tengo que buscar...\n"
                                                 "Mi casa es un lio de papeles</strong>",
                                            parse_mode=telegram.constants.ParseMode.HTML)
    with open(c[0] + "/" + c[1] + ".pdf", "rb") as pdf_file:
        await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_document")
        await context.bot.send_document(chat_id=update.callback_query["message"]["chat"]["id"], document=pdf_file,
                                  caption=u'📖 🤓 ' + c[1])
    keyboard = base_key("Atras", c[0], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Ahí está!! Que mas....?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def sequence(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="i" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Melódicas o Rítmicas?....</strong>",
                                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return Sequences


async def seq2(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", c[0], two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="j" + str(i)))
    keyboard = slice_lst(k2, keyboard, 7)
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = {'M': "\U0001f916 <strong> Elegí una fundamental....... </strong>",
           'R': "\U0001f916 <strong> Pie binario o ternario?....... </strong>"}
    await update.callback_query.edit_message_text(
        text=msg[c[1][0]], reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def seq3(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "i" + c[1], two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1] + "/" + c[2], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="k" + str(i)))
    keyboard = slice_lst(k2, keyboard, 2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = {'M': "\U0001f916 <strong>Eligí un modo.....</strong>",
           'R': "\U0001f916 <strong> De que año?....... </strong>"}
    await update.callback_query.edit_message_text(
        text=msg[c[1][0]], reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def seq4(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "j" + c[2], two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1] + "/" + c[2] + "/" + c[3], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="l" + i))
    keyboard = slice_lst(k2, keyboard, 7)
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = {'M': ["\U0001f916 <strong>Cuantas notas te mando?\n3, 4 y 5 son secuencias que comienzan siempre "
                 "en la tónica.\n"
                 "Hard son seis notas y puede empezar por cualquier sonido!!!</strong>", "snd_scl", "x"],
           'R': ["\U0001f916 <strong> Cuantos pulsos?....... </strong>", "snd_pulse", "y"]}
    await update.callback_query.edit_message_text(text=msg[c[1][0]][0], reply_markup=reply_markup,
                                                  parse_mode=telegram.constants.ParseMode.HTML)


async def snd_scale_or_pulse(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[4] = update.callback_query["data"][1:]
    if c[1][0] == "M":
        await update.callback_query.edit_message_text(text="\U0001f916 <strong>Primero te mando la escala!! </strong>",
                                                parse_mode=telegram.constants.ParseMode.HTML)
        with open("escalas/" + c[3] + "/" + c[2] + ".mp3", "rb") as audio_file:
            await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption="<strong>" + c[2] + " " + c[3] + ":</strong>" + " " +
                                   str(json.load(open("scale_note_names.json"))[c[3]][c[2]])[2:-2],
                                   parse_mode=telegram.constants.ParseMode.HTML)
        await snd_seq(update, context)
    else:
        await update.callback_query.edit_message_text(text="\U0001f916 <strong>Primero te mando el pulso!! </strong>",
                                                      parse_mode=telegram.constants.ParseMode.HTML)

        with open("escalas/pulsos/" + c[2] + "/" + c[4] + ".flac", "rb") as audio_file:
            await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption=c[4] + " pulsos", parse_mode=telegram.constants.ParseMode.HTML)
        await snd_seq(update, context)


async def snd_seq(update, context):
    await update.callback_query.answer()
    c = context.user_data
    logging.info("Enviando secuencia -- " + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4])
    if c[1] == 'Melódicas':
        new_json_data("sm")
    else:
        new_json_data("sr")
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Elegí estos sonidos para vos....\n"
                                 "Cuando lo tengas pedime la solución </strong>",
                            parse_mode=telegram.constants.ParseMode.HTML)
    file = random.choice(get_lst("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4], True, False))
    c[5] = file.split(".")[0]
    with open("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4] + "/" + file + ".flac", "rb") as audio_file:
        await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
        await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                               caption="Secuencia, " + c[1] + ", " + c[2] + ", " + c[3])
    keyboard = base_key("Solución", "m", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Waiting orders .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def seq_sol(update, context):
    await update.callback_query.answer()
    c = context.user_data
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>A ver ????....</strong>",
                                                  parse_mode=telegram.constants.ParseMode.HTML)

    with open("secuencias/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + c[4] + "/" + c[5] + ".png", "rb") as png_file:
        await context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=png_file,
                                     caption="Secuencia de " + c[4] + " pulsos en " + c[2])

    keyboard = base_key("Otro!!", "n", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                  text="\U0001f916 <strong>Como seguimos? .......</strong>",
                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def solf(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="ñ" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>De que libro?....</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return Solfeos


async def solf_lst(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "solf", two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1] + "/", True, True):
        k2.append(InlineKeyboardButton(i, callback_data="o" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Tengo estas lecciones para ofrecerte:...</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def snd_solf(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    logging.info("Enviando solfeo -- " + c[0] + "/" + c[1] + "/" + c[2])
    new_json_data("sol")
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>As2d2 procesando...</strong>",
                                            parse_mode=telegram.constants.ParseMode.HTML)
    cap = u"\U0001F3B6 Solfeo " + c[1] + " " + c[2]
    for i, j in zip(get_lst(c[0] + "/" + c[1] + "/" + c[2] + "/", False, False), datos["solf"]):
        await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_document")
        with open(c[0] + "/" + c[1] + "/" + c[2] + "/" + i, "rb") as audio_file:
            await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption=cap + j)

    keyboard = base_key("Atras", "ñ" + c[1], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Hecho!!, Como seguimos...?</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def recon(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="p" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Que tipo de reconocimiento?....</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return Reconocimientos

async def recon2(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "rec", two=False)
    k2 = []
    for i in reconocimientos[c[1]]:
        k2.append(InlineKeyboardButton(i, callback_data="q" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>De que año?....</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

async def snd_recon(update, context):
    await update.callback_query.answer()
    c = context.user_data
    if update.callback_query["data"] != "q":
        c[2] = update.callback_query["data"][1:]
    logging.info("Enviando Reconocimiento -- " + c[1] + "/" + c[2])
    new_json_data("rec")

    try:
        file = random.choice(reconocimientos[c[1]][c[2]])
        with open("rec/" + c[1] + "/" + file + ".mp3", "rb") as audio_file:
            await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                    text="\U0001f916 <strong>Elegí este ejemplo para vos....\n"
                                         "Cuando lo tengas pedime la solución </strong>",
                                    parse_mode=telegram.constants.ParseMode.HTML)
            await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_audio")
            await context.bot.send_voice(chat_id=update.callback_query["message"]["chat"]["id"], voice=audio_file,
                                   caption="Reconocimiento de " + c[1] + " " + c[2])
        keyboard = base_key("Solución", "r" + file, two=False)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Waiting orders .......</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    except:
        return error_no_file(update, context)

async def recon_sol(update, context):
    await  update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:].split(".")[0]
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>La respuesta es:\n" +
                                            reconocimientos["sol"][c[3].split("-")[1]] +
                                                 "</strong>", parse_mode=telegram.constants.ParseMode.HTML)

    keyboard = base_key("Otro!!", "q", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="\U0001f916 <strong>Como seguimos? .......</strong>",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

async def teo(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    k2 = []
    for i in get_lst(c[0] + "/", True, False):
        k2.append(InlineKeyboardButton(i, callback_data="s" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Elegí una categoria....</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return Teoria

async def teo2(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[1] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "teo", two=False)
    k2 = []
    for i in get_lst(c[0] + "/" + c[1], True, False):
        k2.append(InlineKeyboardButton(i, callback_data="t" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>A tus órdenes....</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

async def teo3(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[2] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "teo", two=False)
    k2 = []
    if c[1] == "Apuntes":
        with open(c[0] + "/" + c[1] + "/" +  c[2] + ".pdf", "rb") as pdf_file:
            await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"],
                                               action="upload_document")
            await context.bot.send_document(chat_id=update.callback_query["message"]["chat"]["id"], document=pdf_file,
                                            caption=u'📖 🤓 ' + c[2])
            keyboard = base_key("Atras", c[0], two=False)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                          text="\U0001f916 <strong>Ahí está!! Que mas....?</strong>",
                                          reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    else:
        for i in get_lst(c[0] + "/" + c[1] + "/" + c[2], True, False):
            k2.append(InlineKeyboardButton(i, callback_data="u" + str(i)))
        keyboard = slice_lst(k2, keyboard, 1)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text(text="\U0001f916 <strong>Soy todo oídos....</strong>",
                                                      reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

async def teo4(update, context):
    await update.callback_query.answer()
    c = context.user_data
    c[3] = update.callback_query["data"][1:]
    keyboard = base_key("Atras", "teo", two=False)
    k2 = []
    for i in datos["years"][:-1]:
        k2.append(InlineKeyboardButton(i, callback_data="v" + str(i)))
    keyboard = slice_lst(k2, keyboard, 1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>De que año....</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

async def teo5(update, context):
    await update.callback_query.answer()
    c = context.user_data
    if update.callback_query["data"] != "v":
        c[4] = update.callback_query["data"][1:]
        if c[3] == "Acordes sobre un bajo":
            msg = "Tenés que escribir el tipo de acorde pedido entre paréntesis, \n" \
                "en el estado indicado, y sobre la nota que te doy...\n" \
                "Resolvelo y cifrá la resolución \n" \
                "Algunos acordes sabes que pueden resolver en modo mayor o en menor...\n" \
                "Elegí tu propia aventura"
        else:
            msg = "Escribi el siguiente acorde, \n" \
                  "invertilo, cifralo y si corresponde resolvelo\n"

    else:
        msg = "Ahí va otro!!"

    logging.info("Enviando Teoria -- " + c[1] + "/" + c[2])
    new_json_data("teo")

    try:
        file = random.choice(teoria[c[3]][c[4]])
        with open("teo/" + c[1] + "/" + c[2] + "/" + c[3] + "/" + file + ".png", "rb") as exercise:
            await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                    text="\U0001f916 <strong>" + msg + "</strong>",
                                    parse_mode=telegram.constants.ParseMode.HTML)
            await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_photo")
            await context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=exercise,
                                   caption="Ejercicio de " + c[3] + " " + c[4] + " año " + "📖 ✏ 🤓")

        keyboard = base_key("Solución", "w" + file, two=False)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                text="\U0001f916 <strong>Te espero .......</strong>",
                                reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    except:
        await error_no_file(update, context)

async def teosol(update,context):
    await update.callback_query.answer()
    c = context.user_data
    c[5] = update.callback_query["data"][1:]
    path = c[0] +  "/" + c[1] + "/" + c[2] + "/" + c[3]
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Ya te lo mando.........</strong>",
                                                  parse_mode=telegram.constants.ParseMode.HTML)
    with open(path + "/" + c[5] + "r" + ".png", "rb") as photo_file:
        await context.bot.send_chat_action(chat_id=update.callback_query["message"]["chat"]["id"], action="upload_photo")
        await context.bot.send_photo(chat_id=update.callback_query["message"]["chat"]["id"], photo=photo_file,
                                     caption=u'\U0001F648 \U0001F91E \U0001F91E \U0001F91E')
    keyboard = base_key("Otro!!", "v", two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                                  text="\U0001f916 <strong>Como seguimos? .......</strong>",
                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)

async def rep(update, context):
    logging.info("Reporting")
    await update.callback_query.answer()
    c = context.user_data
    c[0] = update.callback_query["data"]
    keyboard = base_key(two=True)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Escribime un mensaje con tu reporte.</strong>\n"
                                                 "Podes reportar si no estoy funcionando bien, o si encontraste "
                                                 "algun error en los materiales que envío.\nTambién podes escribirme a:"
                                                 "\n astorito.bot@gmail.com",
                                                 reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


async def start(update, context):
    await update.message.reply_text('🤖')
    first_name = update.message.from_user.first_name
    context.user_data[0] = "start"
    msg = u" <strong>Hola {}!! soy Astorito, el droide de Astor.</strong>\U0001FA97\n" \
          "Puedo ofrecerte las siguientes opciones, mucha suerte!!\U0001F3B6".format(first_name)
    k = [InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/")]
    k2 = []
    for i in json.load(open("datos.json"))["start"]:
        k.append(InlineKeyboardButton(i[0], callback_data=i[1]))
        #disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=i[1], callback=eval(i[2])))
    for i in range(0, len(k), 2):
        k2.append(k[i:i + 2])
    reply_markup = InlineKeyboardMarkup(k2)
    await context.bot.sendMessage(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup,
                            parse_mode=telegram.constants.ParseMode.HTML)
    return Start


async def start_over(update, context):
    await update.callback_query.answer()
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"], text="🤖",
                            parse_mode=telegram.constants.ParseMode.HTML)
    context.user_data[0] = "start"
    k = [InlineKeyboardButton(text="Programa", url="https://cmbsas-caba.infd.edu.ar/sitio/nivel-medio/")]
    k2 = []
    for i in json.load(open("datos.json"))["start"]:
        k.append(InlineKeyboardButton(i[0], callback_data=i[1]))
        #disp.add_handler(telegram.ext.CallbackQueryHandler(pattern=i[1], callback=eval(i[2])))
    for i in range(0, len(k), 2):
        k2.append(k[i:i + 2])
    reply_markup = InlineKeyboardMarkup(k2)
    await context.bot.sendMessage(chat_id=update.callback_query["message"]["chat"]["id"],
                            text="<strong>Empecemos otra vez!!</strong>\n"
                                 "Contame que queres hacer.",
                            reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)
    return Start


async def end(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>Nos vemos la próxima!!</strong> \U0001FA97",
                                                  parse_mode=telegram.constants.ParseMode.HTML)
    return ConversationHandler.END


async def handle_message(update, context):
    if context.user_data[0] == "rep":
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        send_mail(update.message["text"])
        await update.message.reply_text("\U0001f916 <strong>Listo!!\nTu reporte fue enviado.\nGracias!!\n"
                                        f"Algo mas? 👉 /start"
                                        f"</strong>", parse_mode=telegram.constants.ParseMode.HTML)
        context.user_data[0] = "-"
    else:
        await update.message.reply_text(f"\U0001f916 <strong>Dijiste {update.message.text} y no te entiendo.....</strong>\n"
                                        "Todavia no se conversar pero tengo muchos botones!!\n"
                                        "para inciar apretá 👉 /start", parse_mode=telegram.constants.ParseMode.HTML)


async def error_no_file(update, context):
    await update.callback_query.answer()
    c = context.user_data
    logging.error("No habia materiales en " + str(c))
    if c[0] == "start":
        keyboard = base_key("Volver", c[0], two=True)
    else:
        keyboard = base_key("Volver", c[0], two=False)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text="\U0001f916 <strong>No tengo materiales en esa categoría....\n"
                                                 "Que hacemos?</strong>",
                                                  reply_markup=reply_markup, parse_mode=telegram.constants.ParseMode.HTML)


# No deberia hacer mas falta, revisar y sacar este error y su handler
async def error(update, context): # Para cuando usan botoneras viejas y se marea el dicc user_data
    logging.error(str(context.error))
    if str(context.error) != "Message is not modified: specified new message content and reply markup are exactly" \
                             " the same as a current content and reply markup of the message":
        await context.bot.sendMessage(chat_id=devid, text="Hubo un error " + str(context.error))
        await context.bot.sendMessage(chat_id=update.effective_chat.id,
                                      text="<strong>🤖 Que papelón!!,\nalgo salió mal..... \n"
                                      f"Seguí por acá 👉 /start </strong>", parse_mode=telegram.constants.ParseMode.HTML)
    return telegram.ext.ConversationHandler.END

async def stats(update, context):
    await update.message.reply_text('🤖')
    first_name = update.message.from_user.first_name
    context.user_data[0] = "start"
    msg = u" <strong>Hola {}!! Aqui están algunos datos del uso del bot.</strong>".format(first_name)
    await context.bot.sendMessage(chat_id=devid, text=msg, parse_mode=telegram.constants.ParseMode.HTML)
    uso = json.load(open("usage.json"))
    refresh_data()
    plot_total_data(uso)
    plot_detail_data(uso)
    plot_pie_data(uso)
    for i in range(3):
        with open("grafico_uso" + str(i) + ".png", "rb") as photo_file:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file)
        os.remove("grafico_uso" + str(i) + ".png")
    await context.bot.sendMessage(chat_id=update.effective_chat.id,
                            text="<strong>🤖 No vayas a tipear esto..... \n"
                                f"Seguí por acá 👉 /start </strong>", parse_mode=telegram.constants.ParseMode.HTML)


if __name__ == "__main__":
    main()

#conv_handler = telegram.ext.ConversationHandler(
#        entry_points=[telegram.ext.CommandHandler("start", start)],
#        states={
#            #Start: [telegram.ext.CallbackQueryHandler(pattern="dict", callback=mel_rit)],
#            Dictados: [telegram.ext.CallbackQueryHandler(pattern="o", callback=años)],
#            Reconocimientos: []
#        },
#        fallbacks=[telegram.ext.CommandHandler("end", end)]
#    )

#disp.add_handler(conv_handler)
#disp.add_handler(telegram.ext.CommandHandler("stats", stats))
#disp.add_handler(telegram.ext.CommandHandler("start", start))
#disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
#disp.add_handler(telegram.ext.CallbackQueryHandler(pattern="home", callback=start_over))
#disp.add_error_handler(error)


#updater.start_polling(drop_pending_updates=True, timeout=15)
#updater.idle()
