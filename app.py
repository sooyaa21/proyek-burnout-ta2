import os
import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Mengatur jalur direktori agar aman di server Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model_burnout.pkl')

# Load model pickle
with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    if request.method == 'POST':
        try:
            work_hours = float(request.form['work_hours'])
            # Prediksi menggunakan model asli kamu (.pkl)
            pred_val = model.predict([[work_hours]])[0]
            prediction_text = f"Prediksi Skor Burnout: {round(float(pred_val), 2)}"
        except Exception as e:
            prediction_text = f"Error: {str(e)}"
            
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
