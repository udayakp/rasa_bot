from flask import Flask, render_template, request, jsonify
import bot
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template('chat.html')
    
@application.route("/ask", methods=['POST'])
def ask():
    message = str(request.form['messageText'])
    if (message == "train"):
        a = bot.train()
    else:
        a = bot.pretrained()    
    while True:
        message = str(request.form['messageText'])
        bot_response = bot.respond(a,message)
        # print bot_response
        return jsonify({'status':'OK','answer':bot_response})


if __name__ == "__main__":
    application.run()