from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import time
import random

app = Flask(__name__, static_folder='static')
CORS(app)

# モックデータ
mock_balance = {
    'BTC': 1.5,
    'ETH': 10.0
}

mock_deposit_history = [
    {'id': 1, 'date': '2026-02-25 10:30', 'currency': 'BTC', 'amount': 0.5, 'status': '完了'},
    {'id': 2, 'date': '2026-02-26 14:20', 'currency': 'ETH', 'amount': 5.0, 'status': '完了'},
    {'id': 3, 'date': '2026-02-27 09:15', 'currency': 'BTC', 'amount': 1.0, 'status': '処理中'},
]

mock_withdrawal_history = []

# 静的ファイルの配信
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# API: 残高取得
@app.route('/api/balance', methods=['GET'])
def get_balance():
    time.sleep(0.3)  # レスポンス遅延を模擬
    return jsonify(mock_balance)

# API: 入金履歴取得
@app.route('/api/deposits', methods=['GET'])
def get_deposits():
    time.sleep(0.3)
    return jsonify(mock_deposit_history)

# API: 出金履歴取得
@app.route('/api/withdrawals', methods=['GET'])
def get_withdrawals():
    time.sleep(0.3)
    return jsonify(mock_withdrawal_history)

# API: 出金申請
@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    
    # バリデーションのシミュレーション
    time.sleep(1)  # 処理中の表現
    
    currency = data.get('currency')
    address = data.get('address')
    amount = data.get('amount')
    
    # エラーケースのシミュレーション
    if not currency:
        return jsonify({'error': '通貨を選択してください'}), 400
    
    if not address:
        return jsonify({'error': '出金先アドレスを入力してください'}), 400
    
    if not amount:
        return jsonify({'error': '出金額を入力してください'}), 400
    
    try:
        amount_float = float(amount)
    except:
        return jsonify({'error': '出金額は数値で入力してください'}), 400
    
    if amount_float <= 0:
        return jsonify({'error': '出金額は0より大きい値を入力してください'}), 400
    
    # 最小額チェック
    min_amount = 0.001 if currency == 'BTC' else 0.01
    if amount_float < min_amount:
        return jsonify({'error': f'最小出金額は {min_amount} {currency} です'}), 400
    
    # 残高チェック
    fee = 0.0005 if currency == 'BTC' else 0.005
    if amount_float + fee > mock_balance.get(currency, 0):
        return jsonify({'error': '残高が不足しています'}), 400
    
    # アドレス形式チェック（簡易版）
    if currency == 'BTC' and not (address.startswith('1') or address.startswith('3') or address.startswith('bc1')):
        return jsonify({'error': 'BTCアドレスの形式が正しくありません'}), 400
    
    if currency == 'ETH' and not address.startswith('0x'):
        return jsonify({'error': 'ETHアドレスの形式が正しくありません'}), 400
    
    # 成功
    withdrawal_id = len(mock_withdrawal_history) + 1
    new_withdrawal = {
        'id': withdrawal_id,
        'date': '2026-02-27 12:00',
        'currency': currency,
        'amount': amount_float,
        'address': address,
        'fee': fee,
        'status': '処理中'
    }
    mock_withdrawal_history.append(new_withdrawal)
    
    # 残高を減らす
    mock_balance[currency] -= (amount_float + fee)
    
    return jsonify({
        'success': True,
        'message': '出金申請を受け付けました',
        'withdrawal_id': withdrawal_id
    })

if __name__ == '__main__':
    print('=' * 50)
    print('デモサイトが起動しました！')
    print('ブラウザで http://localhost:5000 を開いてください')
    print('=' * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
