from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

app = Flask(__name__)

# Replace with your actual credential file path
cred = credentials.Certificate('C:\\Users\\franz\\OneDrive\\Documents\\VSCODE files\\PWA for hydro watch\\water-68ec3-firebase-adminsdk-pn9vj-2cde1b33f7.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://water-68ec3-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route('/')
def home():
    ref = db.reference('/')
    data = ref.get()

    pump_status = "On" if data.get('pump') == 1 else "Off"
    button_text = "Turn Off" if data.get('pump') == 1 else "Turn On"
    cleanliness = "Pure" if data.get('purity', 0) > 2500 else "Not Pure"

    return render_template('home.html',
                           pump_status=pump_status,
                           button_text=button_text,
                           cleanliness=cleanliness,
                           tsh=data.get('tsh', 'N/A'),
                           sh=data.get('sh', 'N/A'))

@app.route('/graph')
def graph():
    x = [1, 2, 3]
    y = [5, 7, 2]
    plt.plot(x, y)
    plt.xlabel('Time')
    plt.ylabel('Water Usage')
    plt.title('Water Usage Graph')
    
    graph_path = os.path.join('static', 'graph.png')
    plt.savefig(graph_path)
    plt.close()

    return render_template('graph.html', graph_image='static/graph.png')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    ref = db.reference('/')
    data = ref.get()

    if request.method == 'POST':
        new_sump_level = request.form.get('sump_level')
        new_tank_level = request.form.get('tank_level')

        if new_sump_level:
            ref.update({'sump': int(new_sump_level)})
        if new_tank_level:
            ref.update({'tank': int(new_tank_level)})

        return redirect(url_for('home'))

    return render_template('settings.html',
                           sump_level=data.get('sump', 0),
                           tank_level=data.get('tank', 0))

@app.route('/update_pump/<status>', methods=['PUT'])
def update_pump(status):
    ref = db.reference('/')
    ref.update({'pump': int(status)})
    return jsonify({'success': True})

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
