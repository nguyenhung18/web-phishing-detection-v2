import pickle
from flask import Flask, request, render_template, jsonify
from urllib.parse import urlparse
from features import extract_features

app = Flask(__name__)

with open('rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

with open('xgb_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)


@app.route('/')
def home():
    return render_template('index.html')


# Kiểm tra URL hợp lệ
def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and parsed.netloc != ''


# Endpoint dự đoán
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy URL từ người dùng gửi lên
        url = request.form['url']

        # Kiểm tra URL hợp lệ
        if not is_valid_url(url):
            return render_template('index.html', error="URL không hợp lệ. Vui lòng nhập lại URL đúng.")

        # Trích xuất các đặc trưng từ URL
        features = extract_features(url)

        # Chuyển các giá trị đặc trưng thành dạng mảng 2D
        feature_values = list(features.values())
        feature_values = [feature_values]  # Để tạo thành mảng 2D (1 mẫu)

        # Dự đoán với Random Forest
        rf_prediction = rf_model.predict(feature_values)
        rf_result = 'Phishing' if rf_prediction == 1 else 'Legit'

        # Dự đoán với XGBoost
        xgb_prediction = xgb_model.predict(feature_values)
        xgb_result = 'Phishing' if xgb_prediction == 1 else 'Legit'

        # Trả về kết quả dự đoán
        return render_template('index.html', url=url, rf_result=rf_result, xgb_result=xgb_result)

    except Exception as e:
        return render_template('index.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
