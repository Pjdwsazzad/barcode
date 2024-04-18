from flask import Flask, render_template, request, send_file
import pdf417gen
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Retrieve form data
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    license_number = request.form['license_number']
    issue_date = request.form['issue_date']
    expiration_date = request.form['expiration_date']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    postal_code = request.form['postal_code']
    height = request.form['height']
    eye_color = request.form['eye_color']
    sex = request.form['sex']

    # Generate PDF417 barcode
    data = f"""\
ANSI 636002080001DL00410288ZA03290001DLDCAN
DCBNONE
DCDNONE
DACK06070000
DAH06{issue_date}07{expiration_date}
DBA{dob}
DBB{sex}
DBC1
DBD{height}
DAZ{eye_color}
DAG{address}
DAI{city}
DAJ{state}
DAK{postal_code}
DAQ{license_number}
DCT{last_name}
DCU{first_name}
DCV{middle_name}
DCSAL
DAW180
DAU180
DCF{issue_date}
"""

    # Generate barcode image
    barcode = pdf417gen.encode(data)
    image = barcode.render(scale=3, padding=10)
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Prepare response to download the image
    return send_file(img_io, mimetype='image/png', as_attachment=True,
                     attachment_filename='alabama_driver_license.png')

if __name__ == '__main__':
    app.run(debug=True)
