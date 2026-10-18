from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            work_hours = float(request.form['work_hours'])
            # Rumus Regresi Linear Sederhana langsung di app.py
            # Berdasarkan data pelatihan burnout (Y = koefisien * X + intercept)
            # Nilai estimasi koefisien standar untuk data burnout
            pred_val = (3.59 * work_hours) + 10.5
            prediction = round(float(pred_val), 2)
        except Exception as e:
            prediction = f"Error: {str(e)}"
            
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
