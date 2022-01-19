import discord
import os
import requests
import json #module that make it easier to work with data that is returned
import random #the bot will give the messages randomly 
from replit import db
client = discord.Client()

#whenever a bot sees one of these depressing words then it's going to respond 
sad_word=["sad", "depressed", "want better", "crying", "lifesucks"]
#the bot starts with these phrases but the users will be able to add more
starter_encouragements = ["Cheer UP!", "Hang in there!","you are a great person"]

#this allows you to turn on and off whenever you say sad_words
if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  #storing the response from the api
  response = requests.get("https://zenquotes.io/api/random") 
  #convert the response into json
  json_data = json.loads(response.text)
  #q is the quote
  #a is the author
  quote = json_data[0]['q'] + " -"+ json_data[0]['a']
  return(quote)


def update_encouragements(enc_message):
  #check if encouragements is a key in the database
  if "encouragements" in db.keys(): 
    #getting the value that's stored under a key
    encouragements = db["encouragements"]
    #adding the new encouragements 
    encouragements.append(enc_message)
    #saving the value after appending
    db["encouragements"]= encouragements
  else:
    #if there is not a list created, then we create the list and make the first one the inputted one 
    db["encouragements"]= [enc_message]
 
#index of the message that is to be deleted
def delete_encouragement(index):
  #getting a key's value
  encouragements = db["encouragements"]
  #the person could pass an index that isn't there on the list
  if len(encouragements) > index:
    del encouragements[index] 
    #we save it again
    db["encouragements"] = encouragements

@client.event #registering an event
#this is an asynchronous library 
#callbacks

#this function is called from the library discord.py
async def on_ready():
  #This is when the bot is ready to be start being used
  print("We have logged in as {0.user}".format(client))
  # the 0 here is being replaced by client
  #this is going to be printed in to the consel

#if the bots senses a message in the discord server 

@client.event 

async def on_message(message):
  if message.author== client.user:
    return 
  #if the message id $hello then the bot knows that it has a command and messages hello back
  if message.content.startswith("$inspire"):
    quote = get_quote();
    await message.channel.send(quote)

  #this is giving a turn on and off to updating the value
  if db["responding"]:
    options = starter_encouragements
    #adding the user input in the start_encouragement list
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"]) 

    if any(word in message.content for word in sad_word):
        await message.channel.send(random.choice(options))
    
  

  if message.content.startswith("$new"):
    #we don't want "$new" to be added in the list
    enc_message = message.content.split("$new ",1)[1]
    update_encouragements(enc_message)
    await message.channel.send("Added:)")

  if message.content.startswith("$del"):

    encouragements = []
    #checking if there are any encouragements in the database
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
#this prints everything in the database
  if message.content.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if message.content.startswith("$responding"):
    value= message.content.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"]= True
      await message.channel.send("Responding is on")
    else:
      db["responding"]= False
      await message.channel.send("Responding is false")

#line to run the bot
#in the run() we are supposed to put in the key for the bot but since that is private let's add an enviornment variable which allows not everyone to see the key

client.run(os.environ["TOKEN"])
