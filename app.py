from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = None
    status_badge = None
    analysis_text = None

    if request.method == 'POST':
        try:
            work_hours = float(request.form['work_hours'])
            # Rumus Regresi Linear Sederhana
            pred_val = (3.59 * work_hours) + 10.5
            score = round(float(pred_val), 2)
            
            prediction_text = f"Estimasi Skor Burnout: {score}"
            
            if score < 40:
                status_badge = "Rendah (Aman)"
                analysis_text = "Jam kerja masih dalam batas wajar."
            elif score < 70:
                status_badge = "Sedang (Waspada)"
                analysis_text = "Tingkat stres mulai terasa, perbanyak istirahat."
            else:
                status_badge = "Tinggi (Bahaya Burnout)"
                analysis_text = "Peringatan! Jam kerja terlalu tinggi, segera luangkan waktu relaksasi."
                
        except Exception as e:
            prediction_text = f"Error: {str(e)}"

    return render_template('index.html', 
                           prediction_text=prediction_text, 
                           status_badge=status_badge, 
                           analysis_text=analysis_text)

if __name__ == '__main__':
    app.run(debug=True)
