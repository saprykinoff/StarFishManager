from aiogram import Bot, Dispatcher, executor, types, filters
import time, pickle, os
token = "?????"
bot = Bot(token=token, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


mas = []
accepted = []
balance = dict()
paid = dict()
admin = 472209097
def save():
    with open('saves/actual.dat', 'wb') as f:
        pickle.dump(mas, f)
    with open('saves/balance.dat', 'wb') as f:
        pickle.dump(balance, f)
    with open('saves/paid.dat', 'wb') as f:
        pickle.dump(paid, f)
    with open('saves/accepted.dat', 'wb') as f:
        pickle.dump(accepted, f)

def load():
    global mas, balance, paid, accepted
    if (os.path.exists('saves/actual.dat')):
        with open('saves/actual.dat', 'rb') as f:
            mas = pickle.load(f)
        with open('saves/balance.dat', 'rb') as f:
            balance = pickle.load(f)
        with open('saves/paid.dat', 'rb') as f:
            paid = pickle.load(f)
        with open('saves/accepted.dat', 'rb') as f:
            accepted = pickle.load(f)


@dp.message_handler(commands=['c'])
async def confirm(message: types.Message):
    if (message.from_user.id != admin):
        return
    theme = message.reply_to_message
    if (theme is None):
        await bot.send_message(chat_id=message.chat.id, text="Replay to confirmed message", reply_to_message_id=message.message_id)
        return
    name = message.get_args()
    if (name == ''):
        await bot.send_message(chat_id=message.chat.id, text="Send name after command", reply_to_message_id=message.message_id)
        return
    print(name)
    if (theme.message_id not in mas):
        await bot.send_message(chat_id=message.chat.id, text="Theme already closed", reply_to_message_id=message.message_id)
        return
    msg = theme.text.split('\n')
    cost = float(msg[3].split()[1]) / 2
    cnt = int(msg[4].split()[1])
    if (cnt == 0):
        await bot.send_message(chat_id=message.chat.id, text="Theme already done", reply_to_message_id=message.message_id)
        return
    cnt-=1
    msg[4] = msg[4][:-1] + (chr(ord('0') + cnt))
    d = dict()
    for i in range(5, len(msg)):
        nm, have = msg[i].split()
        nm = nm[:-1]
        d[nm] = float(have[:-1])
    d[name] =d.get(name, 0) + cost
    text = '\n'.join(msg[:5])
    text += '\n'
    for k, v in d.items():
        text+= k + ': ' + str(v) + 'Ⓝ\n'
    text = '```\n' + text + '\n```'
    save()
    await bot.edit_message_text(text, chat_id=message.chat.id, message_id=theme.message_id)
    d = await bot.send_message(chat_id=message.chat.id, text="Succses", reply_to_message_id=message.message_id)
    time.sleep(1)
    await bot.delete_message(d.chat.id, d.message_id)
@dp.message_handler(commands=['undo'])
async def confirm(message: types.Message):
    if (message.from_user.id != admin):
        return
    theme = message.reply_to_message
    if (theme is None):
        await bot.send_message(chat_id=message.chat.id, text="Replay to confirmed message", reply_to_message_id=message.message_id)
        return
    name = message.get_args()
    if (name == ''):
        await bot.send_message(chat_id=message.chat.id, text="Send name after command", reply_to_message_id=message.message_id)
        return
    print(name)
    if (theme.message_id not in mas):
        await bot.send_message(chat_id=message.chat.id, text="Theme already closed", reply_to_message_id=message.message_id)
        return
    msg = theme.text.split('\n')
    cost = float(msg[3].split()[1]) / 2

    d = dict()
    for i in range(5, len(msg)):
        nm, have = msg[i].split()
        nm = nm[:-1]
        d[nm] = float(have[:-1])
    if (name not in d.keys()):
        await bot.send_message(chat_id=message.chat.id, text="Cant undo",reply_to_message_id=message.message_id)
        return
    cnt = int(msg[4].split()[1]) + 1
    msg[4] = msg[4][:-1] + (chr(ord('0') + cnt))

    d[name] -= cost
    text = '\n'.join(msg[:5])
    text += '\n'
    for k, v in d.items():
        text+= k + ': ' + str(v) + 'Ⓝ\n'
    text = '```\n' + text + '\n```'
    save()
    await bot.edit_message_text(text, chat_id=message.chat.id, message_id=theme.message_id)
    d = await bot.send_message(chat_id=message.chat.id, text="Succses", reply_to_message_id=message.message_id)
    time.sleep(1)
    await bot.delete_message(d.chat.id, d.message_id)
@dp.message_handler(commands=['accept'])
async def confirm(message: types.Message):
    if (message.from_user.id != admin):
        return
    theme = message.reply_to_message
    if (theme is None):
        await bot.send_message(chat_id=message.chat.id, text="Replay to confirmed message", reply_to_message_id=message.message_id)
        return
    if (theme.message_id in accepted):
        await bot.send_message(chat_id=message.chat.id, text="Theme already accepted", reply_to_message_id=message.message_id)
        return
    if (theme.message_id in mas):
        await bot.send_message(chat_id=message.chat.id, text="Theme not submitted yet", reply_to_message_id=message.message_id)
        return
    msg = theme.text.split('\n')
    for i in range(5, len(msg)):
        nm, have = msg[i].split()
        nm = nm[:-1]
        balance[nm] = balance.get(nm, 0) + float(have[:-1])
    accepted.append(theme.message_id)
    save()
    d = await bot.send_message(chat_id=message.chat.id, text="Succses", reply_to_message_id=message.message_id)
    time.sleep(1)
    await bot.delete_message(d.chat.id, d.message_id)


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    if (message.from_user.id != admin):
        return
    text = message.get_args()
    text = text.strip()
    msg = '```\n'
    try:
        msg += text.split('.')[0] + '\n'
        msg += "Аккаунт: " + text.split('\n')[-1] + '\n'
        msg += "Тема:" + text.split('\n')[1].split(':')[1] + '\n'
        msg += "Цена: " + text.split('\n')[0].split('Ⓝ')[1][1:5] + '\n'
        msg += "Количество: " + text.split('\n')[0].split(':')[1][1:2] + '\n'
        msg += '```'
    except:
        await bot.send_message(chat_id=message.chat.id, text="Smth went wrong")
        return
    x = await bot.send_message(chat_id=message.chat.id, text=msg)
    mas.append(x.message_id)
    save()
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=x.message_id)



@dp.message_handler(commands=['close'])
async def add(message: types.Message):
    if (message.from_user.id != admin):
        return
    theme = message.reply_to_message

    if (theme is None):
        await bot.send_message(chat_id=message.chat.id, text="Replay to confirmed message", reply_to_message_id=message.message_id)
        return
    did = theme.message_id
    if (did not in mas) :
        await bot.send_message(chat_id=message.chat.id, text="Already closed", reply_to_message_id=message.message_id)
        return
    msg = theme.text.split('\n')
    cnt = int(msg[4].split()[1])
    if (cnt):
        await bot.send_message(chat_id=message.chat.id, text=f"Remain {cnt} puzzles", reply_to_message_id=message.message_id)
        return
    mas.remove(did)
    save()
    msg[0] += ' #submit'
    text = '\n'.join(msg)
    text = '```\n' + text + '\n```'
    await bot.edit_message_text(text, theme.chat.id, theme.message_id)
    await bot.unpin_chat_message(chat_id=message.chat.id, message_id=theme.message_id)
    await bot.send_message(chat_id=message.chat.id, text=f"Succesfuly submitted", reply_to_message_id=message.message_id)


@dp.message_handler(commands=['balance'])
async def add(message: types.Message):
    s = set()
    for k in balance.keys():
        s.add(k)
    for k in paid.keys():
        s.add(k)
    msg = ""
    for x in s:
        a = int((balance.get(x, 0) + 0.0001) * 1000) / 1000
        b = int((paid.get(x, 0) + 0.0001) * 1000) / 1000
        if (a > 0.001 or b > 0.001):
            text = f"{x}: {a}Ⓝ, paid:{b}Ⓝ\n"
            msg += text
    if (msg == ""):
        msg = "Empty"
    msg = "```\n" + msg + "\n```"
    await bot.send_message(chat_id=message.chat.id, text=msg, reply_to_message_id=message.message_id)

@dp.message_handler(commands=['abacabadel'])
async def add(message: types.Message):
    if (message.from_user.id != admin):
        return
    name = message.get_args()
    if (name == ''):
        await bot.send_message(chat_id=message.chat.id, text="Send name after command",
                               reply_to_message_id=message.message_id)
    print(name)
    balance[name] = 0
    save()
    await bot.send_message(chat_id=message.chat.id, text="Succesful clear", reply_to_message_id=message.message_id)

@dp.message_handler(commands=['abobaclear'])
async def add(message: types.Message):
    if (message.from_user.id != admin):
        return
    global balance, mas, paid, accepted
    balance = dict()
    paid = dict()
    for x in mas:
        try:
            await bot.unpin_chat_message(chat_id=message.chat.id, message_id=x)
        except:
            print("Unsucces unpin for:", x)
            pass
    mas = []
    accepted = []
    save()
    await bot.send_message(chat_id=message.chat.id, text="Succesful clear", reply_to_message_id=message.message_id)

@dp.message_handler(commands=['pay'])
async def add(message: types.Message):
    if (message.from_user.id != admin):
        return
    name = message.get_args()
    if (name == ''):
        await bot.send_message(chat_id=message.chat.id, text="Send name after command",
                               reply_to_message_id=message.message_id)
    print(name)
    if (balance.get(name, 0) == 0):
        await bot.send_message(chat_id=message.chat.id, text=f"{name} haven't money(",
                               reply_to_message_id=message.message_id)
        return
    x = balance[name]
    paid[name] = paid.get(name, 0) + x
    balance[name] = 0
    save()
    await bot.send_message(chat_id=message.chat.id, text=f"Succesfuly paid {x}Ⓝ for {name} ",
                           reply_to_message_id=message.message_id)

if __name__ == '__main__':
    print("Bot starts")
    load()
    executor.start_polling(dp, skip_updates=True)