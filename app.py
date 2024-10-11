from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Usernames list
usernames = [
    "Extrorse", "Ailuromancy", "ChivyanPlenum", "Plenumtokz", "Sequestrate",
    "Incivism", "Scepter", "Logomancy", "Demigration", "Morling", "Sederunt",
    "Fluorimeter", "Enjambment", "Chenille", "Myophobia", "Deponent",
    "Elytriferous", "Hornwork", "Phallephoric", "Jade3Virage", "Virageheon",
    "Paremptosis", "Dch93Abba", "Abbajoe6677", "Serigraphy", "KejtieMorgen",
    "Morgenke813", "Riffler", "Exungulation", "Nabalism", "Gemmeous",
    "Proboscidate", "Halieutic", "ScannanStirps", "Stirps_man325", "Td998Yapp",
    "Yappleon250", "Decession", "Ligulate", "Estiferous", "Scientaster",
    "GominWurst", "Wurstke57", "DizigRivel", "Rivelrazz199", "StriimRheme",
    "Rhemewan234", "Predacious", "Pulicoid", "Kraurosis", "Proethnic",
    "Patriolatry", "Turnverein", "Oestrogenic", "Sugillate", "Pullulate",
    "Piscivorous"
]
  # Initialize counter for usernames

current_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):

    counter = len(current_users)
    # Declare counter as global to modify it
    user_id = request.remote_addr  # Get the user's IP address
    
    if user_id in current_users:
        if msg.startswith("/username"):
            new_username = msg.split(' ')[1]
            current_users[user_id] = new_username
        user_name = current_users[user_id]
        
    else:
        user_name = usernames[counter % len(usernames)]  # Wrap around if necessary
        counter += 1
        current_users[user_id] = user_name

      # Increment counter
      
    current_time = datetime.now().strftime('%H:%M:%S')
    formatted_message = f"{current_time} -> {user_name}: {msg}"  # Format the message
    emit('message', formatted_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=6969)
