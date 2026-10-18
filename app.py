from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    status_badge = None
    analysis_text = None
    selected_period = 'minggu'
    input_hours = ''

    if request.method == 'POST':
        try:
            input_hours = float(request.form['work_hours'])
            selected_period = request.form.get('period', 'minggu')
            
            # Konversi ke skala mingguan jika pengguna memilih opsi 'bulan' (1 bulan = 4 minggu)
            if selected_period == 'bulan':
                weekly_hours = input_hours / 4.0
            else:
                weekly_hours = input_hours
            
            # Perhitungan Regresi Linear berbasis jam mingguan (Patokan: 6 hari x 9 jam = 54 jam/minggu)
            pred_val = (1.25 * weekly_hours) + 5.0
            score = round(min(max(float(pred_val), 0.0), 100.0), 2)
            
            # Informasi Hasil Prediksi
            if selected_period == 'bulan':
                normal_text = f" (setara dengan {round(weekly_hours, 1)} jam/minggu, normal standar: 216 jam/bulan)"
            else:
                normal_text = f" (normal standar: 54 jam/minggu)"

            prediction_text = f"Estimasi Skor Burnout: {score}{normal_text}"
            
            # Pengkategorian Tingkat Stres / Burnout
            if score < 45:
                status_badge = "Rendah (Aman)"
                analysis_text = "Beban kerja Anda masih dalam batas normal dan wajar. Pertahankan keseimbangan kerja serta pola istirahat."
            elif score < 75:
                status_badge = "Sedang (Waspada)"
                analysis_text = "Beban kerja Anda mendekati atau berada di batas standar penuh (54 jam/minggu atau 216 jam/bulan). Jaga kondisi kesehatan fisik dan mental."
            else:
                status_badge = "Tinggi (Bahaya Burnout)"
                analysis_text = "Peringatan! Jam kerja Anda melebihi batas normal (overtime tinggi). Segera luangkan waktu untuk istirahat atau cuti."
                
        except Exception as e:
            prediction_text = f"Error: Input tidak valid ({str(e)})"

    return render_template('index.html', 
                           prediction_text=prediction_text, 
                           status_badge=status_badge, 
                           analysis_text=analysis_text,
                           selected_period=selected_period,
                           input_hours=input_hours)

if __name__ == '__main__':
    app.run(debug=True)
