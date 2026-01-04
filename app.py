from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    try:
        length = int(request.form.get('length', 12))
        if length < 6 or length > 32:
            return jsonify({"error": "Длина должна быть от 6 до 32 символов"}), 400
        
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))
        return jsonify({"password": password})
    except:
        return jsonify({"error": "Ошибка генерации"}), 500

@app.route('/validate', methods=['POST'])
def validate_password():
    password = request.form.get('password', '')
    if not password:
        return jsonify({"error": "Введите пароль"}), 400
    
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c in "!@#$%^&*" for c in password): score += 1
    
    strength = ["Очень слабый", "Слабый", "Средний", "Хороший", "Отличный"][min(score, 4)]
    
    return jsonify({
        "score": score,
        "strength": strength,
        "length": len(password)
    })

if __name__ == '__main__':
    app.run(debug=True)
