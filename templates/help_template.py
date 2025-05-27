# templates/help_template.py

HELP_TEXT = """
<b>⚒️ ADMIN COMMANDS MENU ⚒️</b>

<b>👤 User Commands:</b>
/start - Start the bot and view the main menu  
/myplan - Check your current premium plan  
/invite - View your referral link and rewards  
/id - Get your Telegram ID  

<b>🎬 Movie & IMDb Commands:</b>
/search <query> - Search for movies in group  
/imdb <movie name> - Get IMDb details  
/trending - Show trending movies  
/popular - Show popular movies  
/request <movie name> - Request a movie  

<b>💎 Premium Commands:</b>
/take_trial - Activate trial (once)  
/redeem <referral_code> - Redeem referral  
/payment_done - Trigger screenshot check (AI OCR)  

<b>👑 Admin-Only Commands:</b>
/addpremium <user_id> <days> - Grant premium  
/removepremium <user_id> - Remove premium  
/activeplans - List active premium users  
/broadcast <message> - Send message to users  
/setchannel - Set Force Subscribe channels  
/setwelcome - Set custom welcome image/text  
/setgoodbye - Set goodbye message  

<b>⚙️ Utilities:</b>
/shorten <url> - Shorten a URL with token  
/verifytoken <token> - Verify shortened token  
/checkshorteners - Show all shortener APIs configured  
/setpopular - Pin a movie as popular  
/settrending - Pin a movie as trending  

<b>🧠 AI Tools (if enabled):</b>
OCR-based payment screenshot verification  
Auto-premium based on screenshot match  
Tesseract / Google Vision supported  

<b>🔧 Deployment Settings:</b>
Environment variables used for MongoDB, Premium Plans, Wish Messages, Force Subscribe, etc.

<b>📌 Useful Links:</b>
- <a href='https://t.me/creazy_announcement_hub'>Update Channel</a>  
- <a href='https://t.me/Creazy_Movie_Surch_Group'>Movie Group</a>  
- <a href='https://t.me/Leazy_support_group'>Support Group</a>  
- <a href='https://t.me/How_to_open_file_to_link'>How To Download</a>  
- <a href='https://t.me/creazy_payments_proof'>Payment Proofs</a>  
"""

HELP_FOOTER_BUTTONS = [
    [
        {"text": "🏠 HOME", "callback_data": "start"},
        {"text": "💎 PREMIUM MENU", "callback_data": "premium_menu"}
    ]
]
