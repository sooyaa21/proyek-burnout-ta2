import os
import pickle
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

# Memastikan jalur file model dibaca dengan benar di server Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model_burnout.pkl')

# Load model pickle
with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            work_hours = float(request.form['work_hours'])
            # Prediksi menggunakan model regresi linear
            pred_val = model.predict([[work_hours]])[0]
            prediction = round(float(pred_val), 2)
        except Exception as e:
            prediction = f"Error: {str(e)}"
            
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
