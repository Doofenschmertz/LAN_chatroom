from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import time

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

current_users = {}  # {user_id: (username, color)}

active_users_count = 0  # Global counter for active users

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global active_users_count

    user_id = request.remote_addr  # Get the user's IP address
    if user_id not in current_users:
        counter = len(current_users)
        user_name = usernames[counter % len(usernames)]  # Assign a username
        current_users[user_id] = (user_name, "#007BFF")  # Default color

        # Increment active user count
        active_users_count += 1
        emit_active_user_count()  # Emit the updated count

        # Broadcast welcome message
        welcome_message = f"{user_name} has joined the chat!"
        emit('message', {'username': 'System', 'message': welcome_message, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)
        
    else:
        user_name, _= current_users[user_id]
        active_users_count += 1
        welcome_message = f"{user_name} has joined the chat!"
        emit('message', {'username': 'System', 'message': welcome_message, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)
        
    t = int(active_users_count/2)
    curr_count = f"Active user count : {t}"
    emit('message', {'username': 'System', 'message': curr_count, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global active_users_count

    user_id = request.remote_addr

    if user_id in current_users:
        user_name, _ = current_users[user_id]
        active_users_count -= 1

        # Broadcast disconnect message
        disconnect_message = f"{user_name} has disconnected."
        emit('message', {'username': 'System', 'message': disconnect_message, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    user_id = request.remote_addr  # Get the user's IP address

    if user_id not in current_users:
        counter = len(current_users)
        user_name = usernames[counter % len(usernames)]  # Assign a username
        current_users[user_id] = (user_name, "#007BFF")  # Default color

    user_name, user_color = current_users[user_id]  # Get username and color

    # Handle special commands like /username and /color
    if msg.startswith("/username"):
        new_username = msg.split(' ')[1]
        previous_username = user_name
        current_users[user_id] = (new_username, user_color)  # Update username

        # Broadcast username change message
        change_message = f"{previous_username} changed their username to {new_username}."
        emit('message', {'username': 'System', 'message': change_message, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)
        return
    elif msg.startswith("/color"):
        new_color = msg.split(' ')[1]
        current_users[user_id] = (user_name, new_color)  # Update color

        # Broadcast color change message
        change_message = f"{user_name} changed their color to {new_color}."
        emit('message', {'username': 'System', 'message': change_message, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)
        return
    
    elif msg.startswith("/count"):
        t = int(active_users_count/2)
        curr_count = f"Active user count : {t}"
        time.sleep(0.2)
        emit('message', {'username': 'System', 'message': curr_count, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)
        return
    
        
    elif msg.startswith("/help"):
        commands = f" Type /color followed by a color to change usercolor.\nType /username followed by a username to change it."
        emit('message', {'username': 'System', 'message': commands, 'time': datetime.now().strftime('%H:%M:%S'), 'color': 'darkbrown'}, broadcast=True)
        return
    # Get current time
    current_time = datetime.now().strftime('%H:%M:%S')

    # Emit the message to all clients
    emit('message', {'username': user_name, 'message': msg, 'time': current_time, 'color': user_color}, broadcast=True)

def emit_active_user_count():
    """Emit the current active user count to all clients."""
    print(f"Active users: {active_users_count}")
    socketio.emit('active_user_count', {'count': active_users_count}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
