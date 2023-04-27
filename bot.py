import os
import pymongo
from pyrogram import Client, filters
from pyrogram.types import Message

DATABASE_URI = os.environ.get('DATABASE_URI')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
CHAT_ID = os.environ.get('CHAT_ID')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
POST_ID = int(os.environ.get('API_ID'))

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]


@app.on_message(filters.chat(CHAT_ID))
async def handle_new_files(client, message: Message):
    # Increment the total files count in the database
        mycol = mydb["file_counts"]
        myquery = {"_id": "total_files_sent"}
        newvalues = {"$inc": {"count": 1}}
        mycol.update_one(myquery, newvalues, upsert=True)
                        
        # Get the current total files count from the database
        count = mycol.find_one(myquery)["count"]
                                    
        # Edit the post in the chat with the new total files count
        await app.edit_message_text(
            chat_id=CHAT_ID,
            message_id=POST_ID,
            text = f"Total files sent: `{count}`"
        )

app.run()