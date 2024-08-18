from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate('C:\\Users\\franz\\OneDrive\\Documents\\VSCODE files\\PWA for hydro watch\\water-68ec3-firebase-adminsdk-pn9vj-2cde1b33f7.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://water-68ec3-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route('/')
def home():
    # Read data from Firebase
    ref = db.reference('/')
    data = ref.get()

    pump_status = "On" if data.get('pump') == 1 else "Off"
    button_text = "Turn Off" if pump_status == "On" else "Turn On"
    cleanliness = "Pure" if data.get('purity', 0) > 2500 else "Not Pure"

    return render_template('home.html',
                           pump_status=pump_status,
                           button_text=button_text,
                           cleanliness=cleanliness,
                           tsh=data.get('tsh', 'N/A'),
                           sh=data.get('sh', 'N/A'))

@app.route('/graph')
def graph():
    # Generate a sample graph
<searchRefSen indexList="1,2,3" order="0" >    x =</searchRefSen>
<searchRefSen indexList="5,7,2" order="1" >    y =</searchRefSen>
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
    # Handle settings updates
    ref = db.reference('/')
    data = ref.get()

    if request.method == 'POST':
        new_sump_level = request.form.get('sump_level')
        new_tank_level = request.form.get('tank_level')

        # Update sump and tank levels if provided
        updates = {}
        if new_sump_level:
            updates['sump'] = int(new_sump_level)
        if new_tank_level:
            updates['tank'] = int(new_tank_level)

        if updates:
            ref.update(updates)

        return redirect(url_for('home'))

    return render_template('settings.html',
                           sump_level=data.get('sump', 0),
                           tank_level=data.get('tank', 0))

@app.route('/update_pump/<int:status>', methods=['PUT'])
def update_pump(status):
    # Update pump status in Firebase
    ref = db.reference('/')
    ref.update({'pump': status})
    return jsonify({'success': True})

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
