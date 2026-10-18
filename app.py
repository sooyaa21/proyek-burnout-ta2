from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

model_path = 'model_burnout.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('index.html', prediction_text=None, plot_url=None, analysis_text=None, status_badge=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_jam = float(request.form['work_hours'])
        
        features = np.array([[input_jam]])
        prediction = model.predict(features)[0]
        hasil_prediksi = round(prediction, 2)
        
        # Logika kategori dan warna badge status yang lebih rapi
        if hasil_prediksi > 70:
            status_badge = "bg-danger"
            status_teks = "Tinggi (Zona Bahaya Burnout!)"
            saran = "Segera kurangi jam kerja dan ambil waktu istirahat yang cukup."
        elif hasil_prediksi > 40:
            status_badge = "bg-warning text-dark"
            status_teks = "Sedang (Waspada Kelelahan)"
            saran = "Mulai jaga keseimbangan waktu kerja dan istirahat."
        else:
            status_badge = "bg-success"
            status_teks = "Rendah (Relatif Aman)"
            saran = "Kondisi jam kerja terpantau sehat dan seimbang."

        # Analisis ringkas dan mudah dipahami
        analysis_text = (
            f"Setiap penambahan 1 jam kerja per minggu, skor kelelahan mental cenderung naik sekitar 1.08 poin. "
            f"Dengan durasi kerja <b>{input_jam} jam/minggu</b>, estimasi skor burnout Anda adalah <b>{hasil_prediksi} dari 100</b>. "
            f"Saran: {saran}"
        )

        # Membuat Grafik
        os.makedirs('static', exist_ok=True)
        df = pd.read_csv('mental_health_burnout_prediction_dataset.csv')
        X_all = df['Work_Hours_Per_Week']
        y_all = df['Burnout_Score']
        
        plt.figure(figsize=(7, 4))
        plt.scatter(X_all, y_all, color='skyblue', alpha=0.3, label='Data Aktual')
        
        x_line = np.linspace(X_all.min(), X_all.max(), 100)
        y_line = model.intercept_ + model.coef_[0] * x_line
        plt.plot(x_line, y_line, color='crimson', linewidth=2, label='Garis Regresi')
        
        plt.scatter([input_jam], [prediction], color='green', s=150, zorder=5, label=f'Input Anda ({input_jam} jam)')
        
        plt.xlabel("Jam Kerja per Minggu")
        plt.ylabel("Skor Burnout")
        plt.title(f"Grafik Posisi Prediksi Jam Kerja: {input_jam} Jam")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        
        plot_path = 'static/plot.png'
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        
        plot_url = f"static/plot.png?t={os.path.getmtime(plot_path)}"
        
        return render_template('index.html', 
                               prediction_text=f"Estimasi Skor Burnout: {hasil_prediksi} / 100", 
                               plot_url=plot_url,
                               analysis_text=analysis_text,
                               status_badge=status_badge,
                               status_teks=status_teks)
                               
    except Exception as e:
        return render_template('index.html', prediction_text=f"Terjadi kesalahan: {str(e)}", plot_url=None, analysis_text=None, status_badge=None, status_teks=None)

if __name__ == '__main__':
    app.run(debug=True)