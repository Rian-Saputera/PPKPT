from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

EMAIL = "akuntugas3916@gmail.com"
PASSWORD = "rybw zfpr cfmp fzkh"  # App Password Gmail

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/kontak")
def kontak():
    return render_template("index.html")  # kalau ada kontak.html, ganti di sini

@app.route("/terimakasih")
def terimakasih():
    return render_template("terimakasih.html")

@app.route("/pelaporan", methods=["GET", "POST"])
def pelaporan():
    if request.method == "GET":
        return render_template("pelaporan.html")

    # Ambil data dari form
    jenis = request.form.get("jenis")
    tanggal = request.form.get("tanggal")
    lokasi = request.form.get("lokasi")
    kronologi = request.form.get("kronologi")
    kontak = request.form.get("kontak")
    bukti_file = request.files.get("bukti")

    # Buat email
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = "Laporan Pelanggaran Kampus"

    body = f"""
    Jenis: {jenis}
    Tanggal: {tanggal}
    Lokasi: {lokasi}
    Kronologi: {kronologi}
    Kontak: {kontak}
    """
    msg.attach(MIMEText(body, "plain"))

    # Lampirkan file bukti jika ada
    if bukti_file and bukti_file.filename:
        bukti_file.stream.seek(0)
        part = MIMEBase("application", "octet-stream")
        part.set_payload(bukti_file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{bukti_file.filename}"'
        )
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        # setelah sukses kirim email, redirect ke halaman terimakasih
        return redirect(url_for("terimakasih"))
    except Exception as e:
        return f"Gagal mengirim laporan. Periksa koneksi internet Anda: {e}"

if __name__ == "__main__":
    app.run(debug=True)