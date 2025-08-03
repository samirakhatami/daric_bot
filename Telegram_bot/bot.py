from pyrogram import Client
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, CallbackQueryHandler, filters, ConversationHandler
import config
import db as database
import psutil
import os
import time
import requests
import jdatetime

jdatetime.set_locale('fa_IR')

def get_pids_by_full_script_name(script_name):
    pids = []
    for proc in psutil.process_iter():
        try:
            cmdline = proc.cmdline()
            pid = proc.pid
        except psutil.NoSuchProcess:
            continue
        except Exception as e:
            # print(e)
            pass

        if (len(cmdline) >= 2 and 'python' in cmdline[0] and cmdline[1] == script_name):
            pids.append(int(pid))
    return pids


directory = os.path.dirname(os.path.abspath(__file__))
filename = str(os.path.basename(__file__))
pid_this_thread = int(os.getpid())
result = get_pids_by_full_script_name(f"{directory}/{filename}")
for pid in result:
    if pid_this_thread != pid:
        try:
            pid = psutil.Process(pid)
            pid.terminate()
            time.sleep(2)
        except:
            pass
print(f"ok: {filename}")


def get_timed_message_info(user_id):
    cr, db = database.conect_database()
    cr.execute(f"SELECT time_frame_id FROM frame_member WHERE chat_id = {user_id}")
    time_id = cr.fetchone()
    time_id = time_id[0]
    cr.execute(f"SELECT title FROM time_frame WHERE id = {time_id}")
    time_zone = cr.fetchone()
    time_zone = time_zone[0]
    time_zone = int(time_zone.split()[0])
    print(time_zone)
    cr.execute(f"SELECT currency_id FROM frame_member WHERE chat_id = {user_id}")
    currency_id = cr.fetchone()
    currency_id = currency_id[0]
    tuple_currency = []
    currency_id = currency_id.split(",")
    for i in currency_id:
        tuple_currency.append(int(i))
    cr.execute(f"SELECT title FROM currency WHERE id IN {tuple(tuple_currency)}")
    currency_name = cr.fetchall()
    return time_zone, currency_name
    
    
async def send_costs(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id   
    currency_name = context.job.data 
    currency_list = []
    for currency in currency_name:
        currency = currency[0]
        if currency == "سکه طرح جدید(امامی)":
            currency = currency + " خرید"
        if currency == "سکه طرح قدیم":
            currency = currency + " خرید"
        currency_list.append(currency)
    url = "https://apie.daric.gold/public/general/GetGoldPrice"
    response = requests.get(url)
    data = response.json()
    result = []
    for item in data:
        fa_name = item.get("faName")
        if fa_name in currency_list:
            if fa_name == "سکه طرح جدید(امامی) خرید" or fa_name == "سکه طرح قدیم خرید":
                fa_name.replace(" خرید", "")
            
            result.append([{
                           "name": fa_name,
                           "bestBuy": item["bestBuy"],
                           "bestSell": item["bestSell"] 
            }])
    text = """"""
    for currency in result:
        for items in currency:
            bestBuy= f"{int(items["bestBuy"]):,}"
            bestSell = f"{int(items["bestSell"]):,}"
            print(items)
            text = text + f"""📊*{items["name"]}*
🟢خرید: {bestBuy} تومان
🔴فروش: {bestSell} تومان \n\n"""
    text = text + "------------------------------------\n\n"
    now = jdatetime.datetime.now()
    formated = now.strftime("%Y/%m/%d %H:%M")
    text = text + f"تاریخ: {formated}\n\n"
    text = text + "*داریک پیشرو در بازار آنلاین طلا*"
    await context.bot.sendMessage(chat_id=chat_id, text=text, parse_mode="Markdown")

def create_job_queue(context, id, currency_name, time_zone):
    context.job_queue.run_repeating(
                send_costs,
                interval= time_zone * 60,
                first=0,
                chat_id=id, 
                data= currency_name
            )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cr, db = database.conect_database()
        chat_id = update.effective_chat.id
        user = update.effective_user
        if user.username:
            username = user.first_name
        else: 
            username = None
        sql_query = "SELECT chat_id FROM bot_member"
        cr.execute(sql_query)
        chat_ids = cr.fetchall()
        for id in chat_ids:
            id = id[0]
            if id == str(chat_id):
                is_first = False
            else:
                is_first = True
        if is_first == True:
            value = ("17",chat_id, username)
            sql_query = "INSERT INTO bot_member (bot_id, chat_id, name) VALUES (%s,%s, %s)"
            cr.execute(sql_query, value)
            db.commit()
            db.close
        
        cr.execute("SELECT chat_id FROM frame_member")
        chat_ids = cr.fetchall()        
        id_list = []
        for chat_id in chat_ids:
                id_list.append(chat_id[0])
            
        id_list = [str(i).strip() for i in id_list]
        if str(user.id) in id_list:
            id = user.id
            time_zone, currency_name = get_timed_message_info(id)
            create_job_queue(context, update.effective_chat.id, currency_name, time_zone)
            
            
        
    except Exception as e:
        print("error: ", e)
    keyboard = [["ارسال قیمت", "قیمت لحظه ای"],
                ["ارسال تحلیل", "تحلیل"]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("به ربات خوش‌آمدید.",reply_markup= reply_markup)


async def button_outline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    if text=="ارسال قیمت": 
        cr, db = database.conect_database()
        cr.execute("SELECT title FROM currency WHERE state = 1")
        currencies = cr.fetchall()
        keyboard = []
        i = 0
        for currency in currencies:
            currency = currency[0]
            if i == 0:
                
                list1 = [InlineKeyboardButton(str(currency), callback_data=str(currency))]
                i += 1 
            elif i == 1:
                list1.append(InlineKeyboardButton(str(currency), callback_data=str(currency)))
                keyboard.append(list1)
                list1 = []
                i = 0 
        keyboard.append([InlineKeyboardButton("✅تایید نهایی", callback_data="final_accept")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.user_data["currency_wanted_list"] = []
        await update.message.reply_text("لطفا ارز مورد نظر خود را انتخاب کنید (چند انتخابی): ", reply_markup= reply_markup)
    elif text == "قیمت لحظه ای":
        try: 
            url =  "https://apie.daric.gold/api/Dashboard/PairList?src=TMN"
            response = requests.get(url)
            print(response.status_code)
            data = response.json()
            text = ""
            for item in data:
                bestBuy = f"{int(item["bestBuy"]):,}"
                bestSell = f"{int(item["bestSell"]):,}"
                text = text + f"""📊*{item["destinationCoinNameFa"]}*
    🟢خرید: {bestBuy} تومان
    🔴فروش: {bestSell} تومان\n\n"""
            url = "https://apie.daric.gold/public/general/GetGoldPrice"    
            response = requests.get(url)
            data = response.json()
            for item in data:
                if item["faName"] == "انس جهانی":
                    bestBuy = f"{int(item["bestBuy"]):,}"
                    
                    text = text + f"""📊*{item["faName"]}*
    🟢قیمت: {bestBuy} دلار\n\n"""
            text = text + "------------------------------------\n\n"
            now = jdatetime.datetime.now()
            formated = now.strftime("%Y/%m/%d %H:%M")
            text = text + f"تاریخ: {formated}\n\n"
            text = text + "*داریک پیشرو در بازار آنلاین طلا*"
            await update.message.reply_text(text, parse_mode="Markdown")
        except Exception as e :
            print("Errore: ", e)
    elif text=="تحلیل":
        now = jdatetime.datetime.now()
        formated = now.strftime("%Y-%m-%d")
        cr, db = database.conect_database()
        
        sql = f"SELECT * FROM analysis WHERE date = '{formated}'"
        cr.execute(sql)
        analysis = cr.fetchall()
        if analysis == []:
            await update.message.reply_text("⏳ تحلیلی برای امروز ثبت نشده است. \n\n لطفا ساعات دیگر مجددا بررسی نمایید")
        else:
            try:
                soerted_analysis_data = sorted(analysis, key=lambda x:x[5])
                for im in soerted_analysis_data:
                    text = f"""⚪{im[1]}

        {im[2]}

    تاریخ: {im[4]}"""
                    if im[3] == '':                
                        await context.bot.sendMessage(chat_id=user.id, text=text)
                    if str(im[3]).endswith(".jpg") or str(im[3]).endswith(".png"):                    
                        await context.bot.send_photo(chat_id=user.id, photo=f"https://bot.daricgold.com/{im[3]}", caption=text)
                    if str(im[3]).endswith(".pdf"):
                        await context.bot.send_document(chat_id=user.id, document=f"https://bot.daricgold.com/{im[3]}", caption=text)                
            except Exception as e:
                    print("erroreee:", e)
    elif text == "ارسال تحلیل":
        keyboard = [[InlineKeyboardButton("✨بلی", callback_data="yes"), InlineKeyboardButton("❌خیر", callback_data="no")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("مایل به دریافت روزانه ی تحلیل ها هستید؟", reply_markup=reply_markup)

async def button_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    
    # query.answer()
    cr, db = database.conect_database()
    cr.execute("SELECT title FROM currency WHERE state = 1")
    currencies = cr.fetchall()


    if query.data == "yes":
        try:
            cr.execute("SELECT chat_id FROM analysis_member")
            chat_ids = cr.fetchall()
            ids = []
            for chat_id in chat_ids:
                chat_id = chat_id[0]
                ids.append(chat_id)
            if str(user.id) in ids:
                sql = "UPDATE analysis_member SET send_analysis = %s WHERE chat_id = %s"
                
                value = ("1", user.id)
                cr.execute(sql, value)
                db.commit()
                await context.bot.sendMessage(chat_id=user.id, text="درخواست تحلیل‌ها ثبت شد! ✅")
            else:
                sql = "INSERT INTO analysis_member(chat_id, send_analysis) VALUES (%s, %s)"                
                value = (user.id, "1")
                cr.execute(sql, value)
                db.commit()
                await context.bot.sendMessage(chat_id=user.id, text="درخواست تحلیل‌ها ثبت شد! ✅")
        except Exception as e:
            print("errore:", e)

    if query.data == "no":
        try:

            cr.execute("SELECT chat_id FROM analysis_member")
            chat_ids = cr.fetchall()
            ids = []
            for chat_id in chat_ids:
                chat_id = chat_id[0]
                ids.append(chat_id)
            if str(user.id) in ids:
                sql = "UPDATE analysis_member SET send_analysis = %s WHERE chat_id = %s"
                value = ("0", user.id)
                cr.execute(sql, value)
                
                db.commit()
                await context.bot.sendMessage(chat_id=user.id, text="درخواست شما لغو شد. ❌")
            else:
                await context.bot.sendMessage(chat_id=user.id, text="درخواست شما لغو شد. ❌")
        except Exception as e:
            print("errore:", e)
        

    for currency in currencies:
        currency = currency[0]
        if query.data == currency:            
            currency_list =  context.user_data.get("currency_wanted_list", [])
            

            if currency in currency_list:
                currency_list.remove(currency)
            else:
                currency_list.append(currency)
            context.user_data["currency_wanted_list"] = currency_list
            print(currency_list)
            keyboard = []
            row = []
            for i, currency in enumerate(currencies):
                currency = currency[0]
                label = f"✔ {currency}" if currency in currency_list else str(currency)
                btn = InlineKeyboardButton(text=label, callback_data=str(currency))
                row.append(btn)
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)
            keyboard.append([InlineKeyboardButton("✅ تایید نهایی", callback_data="final_accept")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
    if query.data == "final_accept":
            currency_list = context.user_data.get("currency_wanted_list", [])
            ids = ""
            for currency in currency_list:
                sql = f"SELECT id FROM currency WHERE title= %s"
                
                cr.execute(sql, (currency,))
                id = cr.fetchone()
                id = id[0]
                if ids == "":
                    ids = str(id)
                else:
                    ids = ids + "," + str(id)
            sql = "SELECT chat_id FROM frame_member"
            cr.execute(sql)
            chat_ids = cr.fetchall()
            id_list = []
            for chat_id in chat_ids:
                id_list.append(chat_id[0])
            print("id_list: ", id_list, "\n", "userId", user.id)
            id_list = [str(i).strip() for i in id_list]
            

            if str(user.id) in id_list:
                sql_query = "UPDATE frame_member SET currency_id = %s WHERE chat_id = %s"
                value = (ids, user.id)  
                cr.execute(sql_query, value)
                db.commit()
            else:    
                sql_query = "INSERT INTO frame_member (chat_id, currency_id) VALUES (%s, %s)"
                value = (user.id, ids)
                cr.execute(sql_query, value)
                db.commit() 

            cr.execute("SELECT title FROM time_frame")
            times = cr.fetchall()
            keyboard = []
            i = 0
            for time in times:
                time = time[0]
                
                if i == 0:
                
                    list1 = [InlineKeyboardButton(str(time), callback_data=str(time))]
                    i += 1 
                elif i == 1:
                    list1.append(InlineKeyboardButton(str(time), callback_data=str(time)))
                    keyboard.append(list1)
                    list1 = []
                    i = 0 
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.sendMessage(chat_id=user.id, text="بازه زمانی مدنظر را انتخاب کنید:", reply_markup=reply_markup)
    cr.execute("SELECT title FROM time_frame")
    times_zone = cr.fetchall()
    
    for time_zone in times_zone:
        time_zone = time_zone[0]       
        if query.data == time_zone:
            
            sql = "SELECT id FROM time_frame WHERE title = %s"
            cr.execute(sql, (time_zone,))
            id = cr.fetchone()
            time_id = id[0]
            sql = "SELECT chat_id FROM frame_member"
            cr.execute(sql)
            chat_ids = cr.fetchall()
            id_list = []
            for chat_id in chat_ids:
                id_list.append(chat_id[0])
                   
            id_list = [str(i).strip() for i in id_list]
            if str(user.id) in id_list :              
                sql_query = "UPDATE frame_member SET time_frame_id = %s WHERE chat_id = %s"
                value = (time_id, user.id)  
                cr.execute(sql_query, value)
                db.commit()
            else:    
                sql_query = "INSERT INTO frame_member (chat_id, time_frame_id) VALUES (%s, %s)"
                value = (user.id, time_id)
                cr.execute(sql_query, value)
                db.commit()
            try:

                time_zone, currency_name = get_timed_message_info(user.id) 
                create_job_queue(context, update.effective_chat.id, currency_name, time_zone)
            except Exception as e :
                print("erorrr : ", e)
            await context.bot.sendMessage(chat_id=user.id, text="✅اطلاعات با موفقیت ثبت شد")





            
def main():
    try:
        cr, db = database.conect_database()
        cr.execute("SELECT token FROM bot WHERE id = 17")
        token = cr.fetchone()
        
        app = ApplicationBuilder().token(token[0]).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_outline))
        app.add_handler(CallbackQueryHandler(button_inline))
        print("✅ ربات فعال شد ...")
        app.run_polling()
    except Exception as e:
        print("error:", e)

# اجرای برنامه
if __name__ == "__main__":

    # import nest_asyncio
    # nest_asyncio.apply()
    # asyncio.get_event_loop().run_until_complete(main())
    main()
