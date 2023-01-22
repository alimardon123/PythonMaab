from flask import Flask, render_template, request
import pyqrcode

app = Flask(__name__)

@app.route('/')
def generate_qr_code():
  data = request.args.get('data')
  if data:
    # Generate a QR code image
    qr = pyqrcode.create(data)
    qr_code = qr.png_as_base64_str(scale=6)
  else:
    qr_code = None
  return render_template('index.html', qr_code=qr_code)

if __name__ == '__main__':
  app.run()