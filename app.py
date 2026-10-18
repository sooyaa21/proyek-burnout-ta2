from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = None
    if request.method == 'POST':
        try:
            work_hours = float(request.form['work_hours'])
            # Rumus Regresi Linear Sederhana untuk prediksi burnout
            pred_val = (3.59 * work_hours) + 10.5
            prediction_text = f"Prediksi Skor Burnout: {round(float(pred_val), 2)}"
        except Exception as e:
            prediction_text = f"Error: {str(e)}"
            
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
