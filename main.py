from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Set up logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN"

# User data storage
user_data = {}

# Start command
def start(update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0, "referrals": 0, "task_completed": 0}

    keyboard = [
        [InlineKeyboardButton("💰 Check Balance", callback_data="balance")],
        [InlineKeyboardButton("🎁 Referral Link", callback_data="referral")],
        [InlineKeyboardButton("📝 Earn from Tasks", callback_data="tasks")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🔥 Welcome! 🔥\n\nEarn money by completing tasks and referring friends.\n\n👇 Choose an option below:", reply_markup=reply_markup)

# Show balance
def show_balance(update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id
    balance = user_data.get(user_id, {"balance": 0})["balance"]

    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text(f"💰 Your Balance: ₹{balance}", reply_markup=reply_markup)

# Show referral link
def referral_link(update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id
    ref_link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"  

    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text(f"🎁 Your Referral Link:\n{ref_link}\n\nRefer friends & earn rewards!", reply_markup=reply_markup)

# Task Menu
def task_menu(update, context: CallbackContext):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton("✅ Task 1: Sign Up & Earn", url="https://example.com")],
        [InlineKeyboardButton("✅ Task 2: Invite Friends", callback_data="task2")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text("📝 Complete Tasks & Earn!\n\nClick below to complete a task:", reply_markup=reply_markup)

# Task 2: Invite Friends
def task2(update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0, "referrals": 0, "task_completed": 0}
    
    user_data[user_id]["task_completed"] += 1
    user_data[user_id]["balance"] += 10  

    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="tasks")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text("✅ Task 2 Completed! You have earned ₹10.", reply_markup=reply_markup)

# Withdraw Money
def withdraw(update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0, "referrals": 0, "task_completed": 0}
    
    balance = user_data[user_id]["balance"]

    if balance < 50:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.answer()
        query.edit_message_text("❌ Minimum ₹50 required to withdraw.", reply_markup=reply_markup)
    else:
        user_data[user_id]["balance"] -= 50  
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.answer()
        query.edit_message_text("✅ Withdrawal request submitted!", reply_markup=reply_markup)
