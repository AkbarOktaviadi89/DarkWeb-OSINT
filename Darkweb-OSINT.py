import requests
import re, random
import telebot

# Token to access the Telegram bot
BOT_TOKEN = "{{ YOUR TOKEN HERE }}"

# Initializing the bot object using the token
bot = telebot.TeleBot(BOT_TOKEN)

# Handler for the commands '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Sending a welcome message to the user when '/start' or '/hello' command is used
    bot.reply_to(message, """Welcome to Dark Web OSINT
    /darkweb (search)
    Example: /darkweb credit cards
                 """)

# Handler for the command '/darkweb'
@bot.message_handler(commands=['darkweb'])
def send_welcome(message):
    # Sending a message to the user that links are being retrieved
    bot.reply_to(message, "[+] Getting Links")
    
    # Extracting data from the user's message and performing scraping
    data = message.text
    newdata = data.replace('/darkweb', '')
    
    # Sending the scraped data back to the user
    bot.reply_to(message, scrape(newdata))
    
    # Sending a reminder that TOR is needed to access Onion Links
    bot.reply_to(message, "[!] You Need TOR to Access Onion Links")

# Function to perform web scraping based on the user's query
def scrape(newdata):
    yourquery = newdata
    
    # Replacing spaces with '+' in the query
    if " " in yourquery:
        yourquery = yourquery.replace(" ", "+")
    
    # Constructing the search URL
    url = "https://ahmia.fi/search/?q={}".format(yourquery)
    
    # Sending a request to the URL
    request = requests.get(url)
    content = request.text
    
    # Defining a regex pattern to extract Onion links
    regexquery = "\w+\.onion"
    
    # Extracting links using regex
    mineddata = re.findall(regexquery, content)

    # Generating a random filename for the text file
    n = random.randint(1, 9999)
    filename = "sites{}.txt".format(str(n))
    print("Saving to ...", filename)
    
    # Removing duplicate links
    mineddata = list(dict.fromkeys(mineddata))

    # Writing the links to a text file
    with open(filename, "w+") as _:
        print("")
    
    for k in mineddata:
        with open(filename, "a") as newfile:
            k__ = k + "\n"
            newfile.write(k + "\n")  # Add a newline character after each link
    print("All the File Written to a Text File : ", filename)
    
    # Reading the first 7 lines of the text file
    with open(filename) as input_file:
        head = [next(input_file, "") for _ in range(7)]
        content = '\n'.join(map(str, head))
        print(content)
    
    # Limiting the length of the content to fit within Telegram's message length limit
    max_length = 4096  # Telegram message length limit
    if len(content) > max_length:
        content = content[:max_length]
    
    return content

# Starting the bot and making it continuously poll for new messages
bot.infinity_polling()
