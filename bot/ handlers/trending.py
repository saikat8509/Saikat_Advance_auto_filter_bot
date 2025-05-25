from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta
import asyncio

# Placeholder for your database instance (MongoDB or similar)
# Replace this with your actual DB import and usage
db = None  # TODO: replace with your actual database client


# Helper function: format file size (bytes to human readable)
def human_readable_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    p = 1024
    while size_bytes >= p and i < len(size_name) - 1:
        size_bytes /= p
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"


# Helper: build inline keyboard with download buttons and pagination
def build_trending_keyboard(files, page, total_pages):
    buttons = []
    for file in files:
        btn_text = file.get("filename", "Unknown")
        btn_data = f"download_{file.get('file_id')}"
        buttons.append([InlineKeyboardButton(btn_text[:40], callback_data=btn_data)])

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton("⬅️ Previous", callback_data=f"trending_page_{page - 1}")
        )
    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton("Next ➡️", callback_data=f"trending_page_{page + 1}")
        )

    if navigation_buttons:
        buttons.append(navigation_buttons)

    buttons.append(
        [InlineKeyboardButton("🏠 Home", callback_data="start_back_cb")]
    )
    return InlineKeyboardMarkup(buttons)


@Client.on_message(filters.command("trending"))
async def trending_command(client: Client, message: Message):
    """
    /trending command: Show top trending files based on search frequency.
    Pagination supported (10 items per page).
    """

    # Number of items per page
    PER_PAGE = 10
    page = 1

    # Parse page number if provided, e.g. "/trending 2"
    if len(message.command) > 1:
        try:
            page = int(message.command[1])
            if page < 1:
                page = 1
        except ValueError:
            page = 1

    # Fetch trending files sorted by search frequency descending
    # Assume 'search_logs' collection logs search queries and file_ids
    # We aggregate counts per file and sort by count
    if db:
        pipeline = [
            {
                "$group": {
                    "_id": "$file_id",
                    "search_count": {"$sum": 1},
                }
            },
            {"$sort": {"search_count": -1}},
            {"$skip": (page - 1) * PER_PAGE},
            {"$limit": PER_PAGE},
        ]
        trending_cursor = db.search_logs.aggregate(pipeline)

        trending_files = []
        async for item in trending_cursor:
            file_id = item["_id"]
            search_count = item["search_count"]

            # Fetch file metadata from 'files' collection (e.g., filename, size)
            file_doc = await db.files.find_one({"file_id": file_id})
            if not file_doc:
                continue

            trending_files.append({
                "file_id": file_id,
                "filename": file_doc.get("filename", "Unknown"),
                "size": human_readable_size(file_doc.get("size", 0)),
                "search_count": search_count,
            })

        # Fetch total count for pagination
        total_count_doc = await db.search_logs.aggregate([
            {"$group": {"_id": "$file_id"}},
            {"$count": "total_unique_files"}
        ]).to_list(length=None)

        total_unique_files = total_count_doc[0]["total_unique_files"] if total_count_doc else 0
        total_pages = (total_unique_files + PER_PAGE - 1) // PER_PAGE

    else:
        # DB not connected fallback
        trending_files = []
        total_pages = 1

    if not trending_files:
        await message.reply_text(
            "No trending files found yet. Try again later!",
            quote=True
        )
        return

    # Compose message text
    text_lines = [f"🔥 **Trending Files (Page {page}/{total_pages})** 🔥\n"]
    for idx, file in enumerate(trending_files, start=1 + (page - 1) * PER_PAGE):
        text_lines.append(
            f"{idx}. [{file['filename']}] - {file['size']} - 🔍 {file['search_count']} searches"
        )
    text = "\n".join(text_lines)

    # Build inline keyboard for files + navigation
    keyboard = build_trending_keyboard(trending_files, page, total_pages)

    await message.reply_text(text, reply_markup=keyboard, parse_mode="md")


@Client.on_callback_query(filters.regex(r"^trending_page_(\d+)$"))
async def trending_pagination_callback(client: Client, callback_query: CallbackQuery):
    """
    Handle pagination buttons in trending list.
    """

    page = int(callback_query.data.split("_")[-1])
    PER_PAGE = 10

    # Fetch trending files for requested page
    if db:
        pipeline = [
            {
                "$group": {
                    "_id": "$file_id",
                    "search_count": {"$sum": 1},
                }
            },
            {"$sort": {"search_count": -1}},
            {"$skip": (page - 1) * PER_PAGE},
            {"$limit": PER_PAGE},
        ]
        trending_cursor = db.search_logs.aggregate(pipeline)

        trending_files = []
        async for item in trending_cursor:
            file_id = item["_id"]
            search_count = item["search_count"]

            file_doc = await db.files.find_one({"file_id": file_id})
            if not file_doc:
                continue

            trending_files.append({
                "file_id": file_id,
                "filename": file_doc.get("filename", "Unknown"),
                "size": human_readable_size(file_doc.get("size", 0)),
                "search_count": search_count,
            })

        total_count_doc = await db.search_logs.aggregate([
            {"$group": {"_id": "$file_id"}},
            {"$count": "total_unique_files"}
        ]).to_list(length=None)

        total_unique_files = total_count_doc[0]["total_unique_files"] if total_count_doc else 0
        total_pages = (total_unique_files + PER_PAGE - 1) // PER_PAGE

    else:
        trending_files = []
        total_pages = 1

    if not trending_files:
        await callback_query.answer("No trending files found.", show_alert=True)
        return

    text_lines = [f"🔥 **Trending Files (Page {page}/{total_pages})** 🔥\n"]
    for idx, file in enumerate(trending_files, start=1 + (page - 1) * PER_PAGE):
        text_lines.append(
            f"{idx}. [{file['filename']}] - {file['size']} - 🔍 {file['search_count']} searches"
        )
    text = "\n".join(text_lines)

    keyboard = build_trending_keyboard(trending_files, page, total_pages)

    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="md")
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^download_(.+)$"))
async def download_file_callback(client: Client, callback_query: CallbackQuery):
    """
    Handle download button clicks from trending or other listings.
    Sends the file to user or provides download link depending on user premium status.
    """

    user_id = callback_query.from_user.id
    file_id = callback_query.data.split("_", 1)[1]

    # Fetch file metadata
    if db:
        file_doc = await db.files.find_one({"file_id": file_id})
    else:
        file_doc = None

    if not file_doc:
        await callback_query.answer("File not found or removed.", show_alert=True)
        return

    filename = file_doc.get("filename", "Unknown")
    file_link = file_doc.get("direct_link")  # direct download link if available

    # Here you should implement your premium check logic
    # Example placeholder: is_premium = await check_user_premium(user_id)
    is_premium = False  # TODO: Replace with actual premium status check

    if is_premium:
        # Send file directly or direct link
        # For example, sending direct link as a message
        await callback_query.message.reply_text(
            f"Here is your direct download link for **{filename}**:\n\n{file_link}",
            parse_mode="md"
        )
        await callback_query.answer("Download link sent!")
    else:
        # Send shortener link or token verification prompt for non-premium users
        short_link = file_doc.get("short_link") or file_link or "No link available"
        await callback_query.message.reply_text(
            f"**Buy Premium Membership** to get direct downloads!\n\n"
            f"File: **{filename}**\n"
            f"Download link (shortened): {short_link}",
            parse_mode="md"
        )
        await callback_query.answer("Buy premium to get direct download.")


# Optional: register commands in help text or command list (depends on your bot setup)
# e.g. add "/trending" command in help.py

