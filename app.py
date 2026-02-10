from flask import Flask, request, redirect, render_template, session, jsonify, url_for
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)

# ================= DATABASE =================
app.secret_key = os.getenv("SECRET_KEY", "nutriplan_secret_key")

# ================= KONEKSI DATABASE =================
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ================= HITUNG NUTRISI =================
def calculate_bmr(gender, weight, height, birth_date):
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    age = (datetime.now() - birth_date).days // 365

    if gender == 'L':
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    return round(10 * weight + 6.25 * height - 5 * age - 161)


def calculate_tdee(bmr, activity):
    multiplier = {
        'rendah': 1.375,
        'sedang': 1.55,
        'tinggi': 1.725
    }
    return round(bmr * multiplier.get(activity, 1.55))


def calculate_bmi(weight, height):
    return round(float(weight) / ((float(height) / 100) ** 2), 1)


# ================= REKOMENDASI =================
def get_food_recommendation(target_kalori):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    target_meal = target_kalori / 3

    cursor.execute("""
        SELECT *
        FROM tbl_foods
        ORDER BY ABS(kalori - %s)
        LIMIT 5
    """, (target_meal,))

    foods = cursor.fetchall()
    cursor.close()
    conn.close()
    return foods


def get_exercise_recommendation(tujuan):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if tujuan == 'diet':
        query = "SELECT * FROM tbl_olahraga ORDER BY kalori_per_menit DESC LIMIT 5"
    elif tujuan == 'naik':
        query = "SELECT * FROM tbl_olahraga ORDER BY kalori_per_menit ASC LIMIT 5"
    else:
        query = "SELECT * FROM tbl_olahraga LIMIT 5"

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data

def calculate_water_need(weight, aktivitas):

    # 35 ml per kg berat badan
    base = weight * 35

    # tambahan aktivitas
    if aktivitas == 'sedang':
        base += 300
    elif aktivitas == 'tinggi':
        base += 500

    return round(base)

# ================= ROUTES =================
@app.route('/')
def index():
    return redirect('/login')


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM tbl_users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))


        return render_template('login.html', error="Email / Password salah")

    return render_template('login.html')


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ================= REGISTRASI =================
@app.route('/registrasi', methods=['GET', 'POST'])
def registrasi():
    if request.method == 'POST':

        conn = get_db_connection()
        cursor = conn.cursor()

        # ==== INPUT USER ====
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        gender = request.form['gender']
        tanggal_lahir = request.form['tanggal_lahir']
        tinggi_cm = int(request.form['tinggi_cm'])
        berat_kg = float(request.form['berat_kg'])
        tingkat_aktivitas = request.form['tingkat_aktivitas']
        tujuan = request.form['tujuan']

        # ==== CEK EMAIL ====
        cursor.execute("SELECT id FROM tbl_users WHERE email=%s", (email,))
        if cursor.fetchone():
            return render_template('error.html', error="Email sudah terdaftar")

        # ==== HITUNG NUTRISI ====
        bmr = calculate_bmr(gender, berat_kg, tinggi_cm, tanggal_lahir)
        tdee = calculate_tdee(bmr, tingkat_aktivitas)

        target_kalori = tdee
        if tujuan == 'diet':
            target_kalori -= 500
        elif tujuan == 'naik':
            target_kalori += 500

        target_protein = round((target_kalori * 0.3) / 4)
        target_karbo = round((target_kalori * 0.4) / 4)
        target_lemak = round((target_kalori * 0.3) / 9)

        # ==== SIMPAN USER ====
        cursor.execute("""
            INSERT INTO tbl_users
            (name,email,password,gender,tanggal_lahir,tinggi_cm,berat_kg,tingkat_aktivitas,tujuan)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            name,email,password,gender,tanggal_lahir,
            tinggi_cm,berat_kg,tingkat_aktivitas,tujuan
        ))

        user_id = cursor.lastrowid

        # ==== SIMPAN TARGET ====
        cursor.execute("""
            INSERT INTO tbl_user_targets
            (user_id,target_kalori,target_protein,target_lemak,target_karbo)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            user_id,target_kalori,target_protein,target_lemak,target_karbo
        ))

        conn.commit()
        cursor.close()
        conn.close()

        # ==== AUTO LOGIN ====
        session['user_id'] = user_id

        # ==== REKOMENDASI ====
        foods = get_food_recommendation(target_kalori)
        exercises = get_exercise_recommendation(tujuan)

        return render_template(
            'registrasi_success.html',
            foods=foods,
            exercises=exercises
        )

    return render_template('registrasi.html')
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ==== DATA USER ====
    cursor.execute("SELECT * FROM tbl_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # ==== TARGET USER ====
    cursor.execute("""
        SELECT * FROM tbl_user_targets
        WHERE user_id=%s
        ORDER BY updated_at DESC LIMIT 1
    """, (user_id,))
    targets = cursor.fetchone()

    # ==== TOTAL MAKAN HARI INI ====
    cursor.execute("""
        SELECT 
            SUM(f.kalori * cm.jumlah_porsi) AS total_kalori,
            SUM(f.protein * cm.jumlah_porsi) AS total_protein,
            SUM(f.lemak * cm.jumlah_porsi) AS total_lemak,
            SUM(f.karbo * cm.jumlah_porsi) AS total_karbo
        FROM tbl_catatan_makan cm
        JOIN tbl_foods f ON cm.id_makanan = f.id_makanan
        WHERE cm.user_id=%s
        AND cm.tanggal = CURDATE()
    """, (user_id,))
    meals_today = cursor.fetchone() or {}

    # ==== TOTAL AIR ====
    cursor.execute("""
        SELECT SUM(jumlah_ml) AS total_air
        FROM tbl_catatan_air
        WHERE user_id=%s
        AND tanggal = CURDATE()
    """, (user_id,))
    water_today = cursor.fetchone() or {}

    # ==== TOTAL OLAHRAGA ====
    cursor.execute("""
        SELECT SUM(kalori_terbakar) AS total_kalori_terbakar
        FROM tbl_catatan_olahraga
        WHERE user_id=%s
        AND tanggal = CURDATE()
    """, (user_id,))
    exercise_today = cursor.fetchone() or {}

    # ================= BMI =================
    bmi = calculate_bmi(user['berat_kg'], user['tinggi_cm'])

    bmi_status = (
        "Underweight" if bmi < 18.5 else
        "Normal" if bmi < 25 else
        "Overweight" if bmi < 30 else
        "Obesitas"
    )

    # ================= PROGRESS MAKAN =================
    progress = {
        "kalori": 0,
        "protein": 0,
        "karbo": 0,
        "lemak": 0,
        "air": 0
    }

    if targets:
        progress["kalori"] = int((meals_today.get("total_kalori") or 0) / targets["target_kalori"] * 100)
        progress["protein"] = int((meals_today.get("total_protein") or 0) / targets["target_protein"] * 100)
        progress["karbo"] = int((meals_today.get("total_karbo") or 0) / targets["target_karbo"] * 100)
        progress["lemak"] = int((meals_today.get("total_lemak") or 0) / targets["target_lemak"] * 100)

        # rekomendasi air simple
        target_air = user["berat_kg"] * 35
        progress["air"] = int((water_today.get("total_air") or 0) / target_air * 100)

    # batasi max 100%
    for key in progress:
        progress[key] = min(progress[key], 100)

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        user=user,
        targets=targets,
        meals=meals_today,
        water=water_today,
        exercise=exercise_today,
        bmi=bmi,
        bmi_status=bmi_status,
        progress=progress
    )

# ================= ADD MEAL =================
@app.route('/add_meal', methods=['POST'])
def add_meal():

    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_catatan_makan
        (user_id,id_makanan,waktu_makan,jumlah_porsi,tanggal)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        session['user_id'],
        data['id_makanan'],
        data['waktu_makan'],
        data['jumlah_porsi'],
        datetime.now().date()
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

@app.route('/foods')
def foods():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ==== DATA USER ====
    cursor.execute("SELECT * FROM tbl_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # ==== TARGET USER ====
    cursor.execute("""
        SELECT * FROM tbl_user_targets
        WHERE user_id=%s
        ORDER BY updated_at DESC LIMIT 1
    """, (user_id,))
    targets = cursor.fetchone()

    # ==== TOTAL MAKAN HARI INI ====
    cursor.execute("""
        SELECT 
            SUM(f.kalori * cm.jumlah_porsi) AS total_kalori
        FROM tbl_catatan_makan cm
        JOIN tbl_foods f ON cm.id_makanan = f.id_makanan
        WHERE cm.user_id=%s
        AND cm.tanggal = CURDATE()
    """, (user_id,))
    meals_today = cursor.fetchone()

    total_kalori = meals_today['total_kalori'] or 0
    sisa_kalori = targets['target_kalori'] - total_kalori

    # ==== REKOMENDASI ====
    foods_recommend = get_food_recommendation(sisa_kalori)

    # ==== LIST MAKANAN ====
    cursor.execute("SELECT * FROM tbl_foods")
    foods_all = cursor.fetchall()

    # ==== HISTORY MAKAN HARI INI ====
    cursor.execute("""
        SELECT f.nama_makanan, cm.jumlah_porsi, cm.waktu_makan
        FROM tbl_catatan_makan cm
        JOIN tbl_foods f ON cm.id_makanan = f.id_makanan
        WHERE cm.user_id=%s
        AND cm.tanggal = CURDATE()
    """, (user_id,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'foods.html',
        user=user,
        foods_all=foods_all,
        foods_recommend=foods_recommend,
        history=history,
        sisa_kalori=sisa_kalori
    )
# ================= HALAMAN OLAHRAGA =================
@app.route('/exercises')
def exercises():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ==== DATA USER ====
    cursor.execute("SELECT * FROM tbl_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # ==== REKOMENDASI OLAHRAGA ====
    exercises = get_exercise_recommendation(user['tujuan'])

    # ==== CATATAN OLAHRAGA HARI INI ====
    cursor.execute("""
        SELECT co.*, o.nama_olahraga
        FROM tbl_catatan_olahraga co
        JOIN tbl_olahraga o ON co.id_olahraga = o.id_olahraga
        WHERE co.user_id=%s
        AND co.tanggal = CURDATE()
    """, (user_id,))
    today_exercises = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'exercises.html',
        user=user,
        exercises=exercises,
        today_exercises=today_exercises
    )
# ================= ADD EXERCISE =================
@app.route('/add_exercise', methods=['POST'])
def add_exercise():

    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ambil kalori per menit
    cursor.execute("""
        SELECT kalori_per_menit 
        FROM tbl_olahraga 
        WHERE id_olahraga=%s
    """, (data['id_olahraga'],))

    olahraga = cursor.fetchone()

    kalori_terbakar = olahraga['kalori_per_menit'] * int(data['durasi'])

    cursor.execute("""
        INSERT INTO tbl_catatan_olahraga
        (user_id,id_olahraga,durasi_menit,kalori_terbakar,tanggal)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        session['user_id'],
        data['id_olahraga'],
        data['durasi'],
        kalori_terbakar,
        datetime.now().date()
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

# ================= HALAMAN AIR =================
@app.route('/water')
def water():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ==== DATA USER ====
    cursor.execute("SELECT * FROM tbl_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # ==== TARGET AIR ====
    target_air = calculate_water_need(user['berat_kg'], user['tingkat_aktivitas'])

    # ==== TOTAL AIR HARI INI ====
    cursor.execute("""
        SELECT SUM(jumlah_ml) AS total_air
        FROM tbl_catatan_air
        WHERE user_id=%s
        AND tanggal = CURDATE()
    """, (user_id,))

    water_today = cursor.fetchone()
    total_air = water_today['total_air'] or 0

    sisa_air = target_air - total_air

    # ==== HISTORY AIR ====
    cursor.execute("""
        SELECT jumlah_ml, waktu_minum
        FROM tbl_catatan_air
        WHERE user_id=%s
        AND tanggal = CURDATE()
        ORDER BY waktu_minum DESC
    """, (user_id,))

    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'water.html',
        user=user,
        target_air=target_air,
        total_air=total_air,
        sisa_air=sisa_air,
        history=history
    )

@app.route('/add_water', methods=['POST'])
def add_water():

    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tbl_catatan_air
        (user_id,jumlah_ml,waktu_minum,tanggal)
        VALUES (%s,%s,%s,%s)
    """, (
        session['user_id'],
        data['jumlah_ml'],
        datetime.now().time(),
        datetime.now().date()
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

@app.route('/update_activity', methods=['POST'])
def update_activity():

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    aktivitas_baru = request.form['tingkat_aktivitas']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ===== ambil data user =====
    cursor.execute("SELECT * FROM tbl_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # ===== update aktivitas user =====
    cursor.execute("""
        UPDATE tbl_users 
        SET tingkat_aktivitas=%s 
        WHERE id=%s
    """, (aktivitas_baru, user_id))

    # ===== hitung ulang nutrisi =====
    bmr = calculate_bmr(
        user['gender'],
        float(user['berat_kg']),
        user['tinggi_cm'],
        user['tanggal_lahir'].strftime('%Y-%m-%d')
    )

    tdee = calculate_tdee(bmr, aktivitas_baru)

    target_kalori = tdee

    if user['tujuan'] == 'diet':
        target_kalori -= 500
    elif user['tujuan'] == 'naik':
        target_kalori += 500

    target_protein = round((target_kalori * 0.3) / 4)
    target_karbo = round((target_kalori * 0.4) / 4)
    target_lemak = round((target_kalori * 0.3) / 9)

    # ===== update target nutrisi =====
    cursor.execute("""
        INSERT INTO tbl_user_targets
        (user_id,target_kalori,target_protein,target_lemak,target_karbo)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        user_id,
        target_kalori,
        target_protein,
        target_lemak,
        target_karbo
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/dashboard')
@app.route("/update_profile", methods=["POST"])
def update_profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    berat = float(request.form["berat_badan"])
    tujuan = request.form["tujuan"]
    aktivitas = request.form["tingkat_aktivitas"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ===== ambil data user lama =====
    cursor.execute("SELECT * FROM tbl_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # ===== update profil user =====
    cursor.execute("""
        UPDATE tbl_users
        SET berat_kg=%s, tujuan=%s, tingkat_aktivitas=%s
        WHERE id=%s
    """, (berat, tujuan, aktivitas, user_id))

    # ===== hitung ulang nutrisi =====
    bmr = calculate_bmr(
        user['gender'],
        berat,
        user['tinggi_cm'],
        user['tanggal_lahir'].strftime('%Y-%m-%d')
    )

    tdee = calculate_tdee(bmr, aktivitas)

    target_kalori = tdee

    if tujuan == 'diet':
        target_kalori -= 500
    elif tujuan == 'naik':
        target_kalori += 500

    target_protein = round((target_kalori * 0.3) / 4)
    target_karbo = round((target_kalori * 0.4) / 4)
    target_lemak = round((target_kalori * 0.3) / 9)

    # ===== simpan target baru =====
    cursor.execute("""
        INSERT INTO tbl_user_targets
        (user_id,target_kalori,target_protein,target_lemak,target_karbo)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        user_id,
        target_kalori,
        target_protein,
        target_lemak,
        target_karbo
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("dashboard"))

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
