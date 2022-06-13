from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import speech_recognition as sr


app = Flask(__name__)

bot = ChatBot(
    'Example Bot',

    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        }
    ]
)

trainer = ListTrainer(bot)
trainer.train([
    'may i know services offered',
    'gynecologist,cardiology',
    'doctor available timings',
    '12 to 4,5 to 7',
    'may i know your name',
    'i am techbot',
])

#created chatbot with name john 
#SQLStorageAdapter which allows the chat bot to connect to SQL databases. By default, this adapter will create a SQLite database.
english_bot = ChatBot("John", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)#allows the chat bot to be trained using data from the ChatterBot dialog corpus.
trainer.train("chatterbot.corpus.english")# trainning based on  english greetings and conversations corpora 

@app.route('/speechreg')
def speechreg():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        mydata=r.recognize_google(audio)
    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        print(type(r.recognize_google(audio)))
    except:
        print('error')
    return str(english_bot.get_response(mydata))
    # return render_template('index.html',data=str(english_bot.get_response(mydata)))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


if __name__ == "__main__":
    app.run(debug=True)
