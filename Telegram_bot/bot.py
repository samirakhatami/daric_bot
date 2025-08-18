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
import pytz

def TimeNow():
    iran_tz = pytz.timezone("Asia/Tehran")
    now = jdatetime.datetime.now(tz=iran_tz)
    formated = now.strftime("%Y/%m/%d %H:%M")
    year = now.strftime("%Y")
    mounth = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    hour = int(hour) - 1
    minute = now.strftime("%M")
    datetime_now = str(year) + "/" + str(mounth) + "/" + str(day) + " " + str(hour) + ":" + str(minute)
    return datetime_now


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
    try:
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
        if not len(tuple_currency) == 1:
            placeholders = ','.join(['%s'] * len(tuple_currency))
            query = f"SELECT title FROM currency WHERE id IN ({placeholders})"
            print("query:::", query)
        else:
            query = f"SELECT title FROM currency WHERE id = %s"
        cr.execute(query, tuple(tuple_currency))
        currency_name = cr.fetchall()
        print("currency namesss", currency_name)
        return time_zone, currency_name
    except Exception as e:
        print("printttt erroorrrr:", e)
    
    
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
        if currency == 'نقره 995 عیار':
            currency = 'نقره'
        currency_list.append(currency)
    url = "https://apie-stage.daricgold.com/public/general/GetGoldPrice"
    response = requests.get(url)
    data = response.json()
    result = []
    for item in data:
        fa_name = item.get("faName")
        if fa_name in currency_list:
            if fa_name == "سکه طرح جدید(امامی) خرید" or fa_name == "سکه طرح قدیم خرید":
                fa_name.replace(" خرید", "")
            if fa_name == 'نقره':
                fa_name = 'نقره 995 عیار'
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
    
    text = text + f"تاریخ: {TimeNow()}\n\n"
    text = text + "*داریک پیشرو در بازار آنلاین طلا*"
    await context.bot.sendMessage(chat_id=chat_id, text=text, parse_mode="Markdown")

def create_job_queue(context, id, currency_name, time_zone):
    if time_zone == 4 or time_zone == 12:
        context.job_queue.run_repeating(
                send_costs,
                interval= time_zone * 3600,
                first=0,
                chat_id=id, 
                data= currency_name
            )
    else:
        context.job_queue.run_repeating(
                send_costs,
                interval= time_zone * 60,
                first=0,
                chat_id=id, 
                data= currency_name)

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
            cr.execute("SELECT state FROM frame_member WHERE chat_id = %s", (user.id,))
            state = cr.fetchone()
            if state[0] == "1":
                id = user.id
                time_zone, currency_name = get_timed_message_info(id)
                create_job_queue(context, update.effective_chat.id, currency_name, time_zone)
            
            
        
    except Exception as e:
        print("error: ", e)
    keyboard = [["مدیریت قیمت", "قیمت لحظه ای"],
                ["مدیریت تحلیل", "تحلیل روز"],
                ["راهنما❗", "تنظیمات⚙"]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("به داریک بات خوش‌آمدید.",reply_markup= reply_markup)


async def button_outline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    if text=="مدیریت قیمت": 
        cr, db = database.conect_database()
        cr.execute("SELECT currency_id FROM frame_member WHERE chat_id = %s", (user.id,))
        cvl = cr.fetchall()
        currency_list = []
        
        for currency_want in cvl:
            currency_list.append(currency_want[0])
        cvl_id_list = str(currency_list[0]).split(",")
        cvl_name = []
        for cvl_id in cvl_id_list:
            cr.execute("SELECT title FROM currency WHERE id = %s", (cvl_id,))
            n = cr.fetchone()
            if n:
                n = n[0]
                cvl_name.append(n)
        
        cr.execute("SELECT title FROM currency WHERE state = 1")
        currencies = cr.fetchall()
        keyboard = []
        i = 0
        for currency in currencies:
            currency = currency[0]
            # currency_wanted_list = context.user_data.get("currency_wanted_list", [])
            if i == 0:
                
                if currency in cvl_name:
                    list1 = [InlineKeyboardButton(f"✔{currency}", callback_data=str(currency))]
                else:
                    list1 = [InlineKeyboardButton(str(currency), callback_data=str(currency))]
                i += 1 
            elif i == 1:
                if currency in cvl_name:
                    list1.append(InlineKeyboardButton(f"✔{currency}", callback_data=str(currency)))
                else:
                    list1.append(InlineKeyboardButton(str(currency), callback_data=str(currency)))
                keyboard.append(list1)
                list1 = []
                i = 0 

        context.user_data["currency_wanted_list"] = cvl_name
        keyboard.append([InlineKeyboardButton("✅تایید نهایی", callback_data="final_accept")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        
        await update.message.reply_text("لطفا گزینه‌های مورد نظر خود را انتخاب کنید (چند انتخابی): ", reply_markup= reply_markup)
    elif text == "قیمت لحظه ای":
        try: 
            url =  "https://apie-stage.daricgold.com/api/Dashboard/PairList?src=TMN"
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
            url = "https://apie-stage.daricgold.com/public/general/GetGoldPrice"    
            response = requests.get(url)
            data = response.json()
            for item in data:
                if item["faName"] == "انس جهانی":
                    bestBuy = f"{int(item["bestBuy"]):,}"
                    
                    text = text + f"""📊*{item["faName"]}*
    🟢قیمت: {bestBuy} دلار\n\n"""
            text = text + "------------------------------------\n\n"
            text = text + f"تاریخ: {TimeNow()}\n\n"
            text = text + "*داریک پیشرو در بازار آنلاین طلا*"
            keyboard = [[InlineKeyboardButton("خرید طلا از داریک", url= "https://pwa.daric.gold/trade"), InlineKeyboardButton("وبسایت داریک", url="https://daric.gold/")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup= reply_markup)
        except Exception as e :
            print("Errore: ", e)
    elif text== "تحلیل روز":
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
    elif text == "مدیریت تحلیل":
        keyboard = [[InlineKeyboardButton("✨بلی", callback_data="yes"), InlineKeyboardButton("❌خیر", callback_data="no")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("مایل به دریافت روزانه ی تحلیل ها هستید؟", reply_markup=reply_markup)
    elif text == "تنظیمات⚙":
        keyboard = [[InlineKeyboardButton("لغو ارسال تحلیل", callback_data="tahlil_setting",), InlineKeyboardButton("لغو ارسال قیمت", callback_data="send_price_setting")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("بخش تنظیمات⚙: \n لطفا یکی از گزینه های زیر را انتخاب کنید", reply_markup=reply_markup)
    elif text == "راهنما❗":
        await update.message.reply_text("📌بخش راهنما: \n کاربرگرامی، برای استفاده از این ربات میتوانید از پنج گزینه‌ی زیر بهره‌مند شوید: \n\n 🔹گزینه‌ی اول: قیمت لحظه ای \n با انتخاب این گزینه، قیمت لحظه‌ای طلا، نقره و انس جهانی برای شما نمایش داده میشود \n\n 🔹گزینه‌ی دوم: مدیریت قیمت \n در این بخش می‌توانید ارز مورد نظر خود را از لیست انتخاب کرده و با تعیین بازه زمانی دلخواه، ربات به صورت خودکار قیمت ارز انتخابی شما را ارسال خواهد کرد \n\n 🔹گزینه‌ی سوم: تحلیل روز \n با انتخاب این گزینه، می‌توانید تحلیل های منتشر شده امروز را دریافت کنید. \n\n 🔹گزینه‌ی چهارم: مدیریت تحلیل \n در این بخش می‌توانید تعیین کنید که هر زمان تحلیل جدیدی توسط کارشناسان ما ثبت شد، به طور خودکار برای شما ارسال شود \n\n 🔹گزینه‌ی پنجم: تنظیمات \n در این بخش می‌توانید ارسال خودکار تحلیل ها و قیمت ارزها را فعال و غیرفعال نمایید")



async def button_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    
    # query.answer()
    cr, db = database.conect_database()
    


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
        await context.bot.sendMessage(chat_id=user.id, text="درخواست شما لغو شد. ❌")
        # try:

        #     cr.execute("SELECT chat_id FROM analysis_member")
        #     chat_ids = cr.fetchall()
        #     ids = []
        #     for chat_id in chat_ids:
        #         chat_id = chat_id[0]
        #         ids.append(chat_id)
        #     if str(user.id) in ids:
        #         sql = "UPDATE analysis_member SET send_analysis = %s WHERE chat_id = %s"
        #         value = ("0", user.id)
        #         cr.execute(sql, value)
                
        #         db.commit()
        #         await context.bot.sendMessage(chat_id=user.id, text="درخواست شما لغو شد. ❌")
        #     else:
        #         await context.bot.sendMessage(chat_id=user.id, text="درخواست شما لغو شد. ❌")
        # except Exception as e:
        #     print("errore:", e)
    if query.data == "disable":
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
            await context.bot.sendMessage(chat_id=user.id, text="درخواست شما با موفقیت انجام شد ✅")
    if query.data == "disable_send_price":
        cr.execute("UPDATE frame_member SET state = %s WHERE chat_id = %s", ("0", user.id))
        db.commit()
        await context.bot.sendMessage(chat_id=user.id, text="درخواست شما با موفقیت انجام شد ✅")
    if query.data == "Activate_send_prica":
        cr.execute("UPDATE frame_member SET state = %s WHERE chat_id = %s", ("1", user.id))
        db.commit()
        await context.bot.sendMessage(chat_id=user.id, text="درخواست شما با موفقیت انجام شد ✅")
    if query.data == "send_price_setting":
        cr.execute("SELECT chat_id FROM frame_member")
        chat_ids = cr.fetchall()        
        id_list = []
        for chat_id in chat_ids:
                id_list.append(chat_id[0])
            
        id_list = [str(i).strip() for i in id_list]
        if str(user.id) in id_list:
            cr.execute("SELECT state FROM frame_member WHERE chat_id = %s", (user.id,))
            state = cr.fetchone()
            print(state)
            if state[0] == "1":
                keyboard = [[InlineKeyboardButton("خیر❌", callback_data="no"), InlineKeyboardButton("بله✅", callback_data="disable_send_price")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.sendMessage(chat_id=user.id, text="برای لغو ارسال خودکار قیمت ها گزینه‌ی (بله) و برای انصراف از این فرایند گزینه‌ی (خیر) را انتخاب کنید", reply_markup=reply_markup)
            else:
                keyboard = [[InlineKeyboardButton("فعال کردن", callback_data="Activate_send_prica")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.sendMessage(chat_id=user.id, text="شما قبلا این قابلیت را غیر فعال کردید \n برای فعال کردن دوباره گزینه‌ی زیر را انتخاب کنید", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton("فعال کردن", callback_data="")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.sendMessage(chat_id=user.id, text="این قابلیت برای شما هنوز فعال نیست❗ \n برای فعال کردن این قابلیت از طریق گزینه‌ی مدیریت قیمت در منوی اصلی اقدام بفرمایید")
    
    
    if query.data == "tahlil_setting":
        cr.execute("SELECT send_analysis FROM analysis_member WHERE chat_id = %s", (user.id,))
        state = cr.fetchone()
        print(state[0])
        if state[0] == 1:
            keyboard = [[ InlineKeyboardButton("❌خیر", callback_data="no"), InlineKeyboardButton("بله✅", callback_data="disable")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.sendMessage(chat_id=user.id, text="برای لغو ارسال خودکار تحلیل ها روی (بله) و برای انصراف از این فرایند گزینه‌ی (خیر) را انتخاب کنید", reply_markup=reply_markup)
        elif state[0] == 0:
            keyboard = [[InlineKeyboardButton("فعال کردن", callback_data="yes")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.sendMessage(chat_id=user.id, text="شما هنوزارسال خودکار تحلیل ها را فعال نکردید \n درصورت تمایل برای فعال کردن این قابلیت گزینه‌ی زیر را انتخاب کنید", reply_markup=reply_markup)
    cr.execute("SELECT title FROM currency WHERE state = 1")
    currencies = cr.fetchall()
    for currency in currencies:
        currency = currency[0]
        if query.data == currency:            
            currency_list =  context.user_data.get("currency_wanted_list", [])
            print("currency wanted list:",currency_list, "\n currency:", currency)

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
            cr.execute("SELECT time_frame_id FROM frame_member WHERE chat_id = %s", (user.id,))
            time_wnated_id = cr.fetchone()
            if time_wnated_id:
                time_wnated_id = time_wnated_id[0]
                cr.execute("SELECT title FROM time_frame WHERE id = %s", (time_wnated_id,))
                time_wnated_name = cr.fetchone()
                time_wnated_name = time_wnated_name[0]

            cr.execute("SELECT title FROM time_frame")
            times = cr.fetchall()
            keyboard = []
            i = 0
            for time in times:
                time = time[0]
                
                if i == 0:
                    if time_wnated_name:
                        if time == time_wnated_name:
                            list1 = [InlineKeyboardButton(f"✔{time}", callback_data=str(time))]
                        else:
                            list1 = [InlineKeyboardButton(str(time), callback_data=str(time))]  
                    else:
                        list1 = [InlineKeyboardButton(str(time), callback_data=str(time))]
                    i += 1 
                elif i == 1:
                    if time_wnated_name:
                        if time == time_wnated_name:
                            list1.append(InlineKeyboardButton(f"✔{time}", callback_data=str(time)))
                            context.user_data["last_selected_time"] = time_wnated_name
                        else:
                            list1.append(InlineKeyboardButton(str(time), callback_data=str(time)))
                    else:
                        list1.append(InlineKeyboardButton(str(time), callback_data=str(time)))
                    keyboard.append(list1)
                    list1 = []
                    i = 0 
            context.user_data["Time_Frame_wanted"] = time_wnated_name
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.sendMessage(chat_id=user.id, text="بازه زمانی مدنظر را انتخاب کنید:", reply_markup=reply_markup)
    cr.execute("SELECT title FROM time_frame")
    times_zone = cr.fetchall()
    
    for time_zone in times_zone:
        time_zone = time_zone[0]       
        if query.data == time_zone:
            cr.execute("SELECT time_frame_id FROM frame_member WHERE chat_id = %s", (user.id,))
            time_wnated_id = cr.fetchone()
            if time_wnated_id:
                time_wnated_id = time_wnated_id[0]
                cr.execute("SELECT title FROM time_frame WHERE id = %s", (time_wnated_id,))
                time_wnated_name = cr.fetchone()
                time_wnated_name = time_wnated_name[0]

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
                sql_query = "UPDATE frame_member SET time_frame_id = %s , state = %s WHERE chat_id = %s"
                value = (time_id, "1", user.id)  
                cr.execute(sql_query, value)
                db.commit()
                
            else:    
                sql_query = "INSERT INTO frame_member (chat_id, time_frame_id, state) VALUES (%s, %s, %s)"
                value = (user.id, time_id, "1")
                cr.execute(sql_query, value)
                db.commit()
            cr.execute("SELECT time_frame_id FROM frame_member WHERE chat_id = %s", (user.id,))
            new_time_id = cr.fetchone()[0]

            cr.execute("SELECT title FROM time_frame WHERE id = %s", (new_time_id,))
            new_time_name = cr.fetchone()[0]

        # ساخت دوباره‌ی کیبورد با ✔ روی گزینه‌ی جدید
            
            print("asifhsdvl", time_wnated_name)
            if new_time_name != time_wnated_name:
                cr.execute("SELECT title FROM time_frame")
                times = cr.fetchall()
                keyboard = []
                row = []

                for i, time in enumerate(times, start=1):
                    time = time[0]
                    if time == new_time_name:
                        btn = InlineKeyboardButton(f"✔{time}", callback_data=str(time))
                    else:
                        btn = InlineKeyboardButton(str(time), callback_data=str(time))
                    row.append(btn)

                    if i % 2 == 0:  # دو تا دکمه در هر ردیف
                        keyboard.append(row)
                        row = []
                if row:
                    keyboard.append(row)

                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                text="بازه زمانی مدنظر را انتخاب کنید:",
                reply_markup=reply_markup
                )  
            else:
                await context.bot.sendMessage(chat_id= user.id, text="✅اطلاعات با موفقیت ثبت شد") 
            try:
                cr.execute("SELECT state FROM frame_member WHERE chat_id = %s", (user.id,))
                state = cr.fetchone()
                if state[0] == "1":
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
        app.initialize()
        app.start()
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
