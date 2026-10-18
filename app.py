from flask import Flask, render_template, request

# Mengatur template_folder ke direktori saat ini agar Vercel langsung menemukannya
app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    status_badge = None
    analysis_text = None

    if request.method == 'POST':
        try:
            # Mengambil input jam kerja dari form HTML
            work_hours = float(request.form['work_hours'])
            
            # Perhitungan Regresi Linear Sederhana langsung di server
            pred_val = (3.59 * work_hours) + 10.5
            score = round(float(pred_val), 2)
            
            prediction_text = f"Estimasi Skor Burnout: {score}"
            
            # Kategori status kesehatan mental
            if score < 40:
                status_badge = "Rendah (Aman)"
                analysis_text = "Jam kerja Anda masih dalam batas wajar. Pertahankan keseimbangan hidup dan kerja yang baik."
            elif score < 70:
                status_badge = "Sedang (Waspada)"
                analysis_text = "Tingkat stres mulai terasa. Pastikan Anda memiliki waktu istirahat dan relaksasi yang cukup."
            else:
                status_badge = "Tinggi (Bahaya Burnout)"
                analysis_text = "Peringatan! Jam kerja terlalu tinggi. Segera ambil waktu cuti atau istirahat untuk memulihkan kondisi."
                
        except Exception as e:
            prediction_text = f"Error: Input tidak valid atau kosong ({str(e)})"

    return render_template('index.html', 
                           prediction_text=prediction_text, 
                           status_badge=status_badge, 
                           analysis_text=analysis_text)

if __name__ == '__main__':
    app.run(debug=True)
