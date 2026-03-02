from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import time
import random
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# モックデータ
mock_balance = {
    'BTC': 1.5,
    'ETH': 10.0,
    'JPY': 5000000  # 500万円
}

mock_deposit_history = [
    {'id': 1, 'date': '2026-02-25 10:30', 'currency': 'BTC', 'amount': 0.5, 'status': '完了'},
    {'id': 2, 'date': '2026-02-26 14:20', 'currency': 'ETH', 'amount': 5.0, 'status': '完了'},
    {'id': 3, 'date': '2026-02-27 09:15', 'currency': 'BTC', 'amount': 1.0, 'status': '処理中'},
]

mock_withdrawal_history = []

# 注文関連のモックデータ
mock_orders = []
order_id_counter = 1
CURRENT_BTC_PRICE = 15000000  # 1500万円（モック価格）

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

# API: 現在価格取得（モック）
@app.route('/api/current-price', methods=['GET'])
def get_current_price():
    # 実際にはBybit APIから取得すべきだが、モックで返す
    return jsonify({
        'symbol': 'BTC/JPY',
        'price': CURRENT_BTC_PRICE,
        'timestamp': int(time.time() * 1000)
    })

# API: 注文作成
@app.route('/api/orders', methods=['POST'])
def create_order():
    global order_id_counter
    data = request.json
    
    time.sleep(0.5)  # 処理遅延
    
    order_side = data.get('side')  # 'buy' or 'sell'
    order_type = data.get('type')  # 'market' or 'limit'
    amount = data.get('amount')
    price = data.get('price')  # 指値の場合のみ
    
    # バリデーション
    if order_side not in ['buy', 'sell']:
        return jsonify({'error': '注文種別を選択してください'}), 400
    
    if order_type not in ['market', 'limit']:
        return jsonify({'error': '注文タイプを選択してください'}), 400
    
    if not amount:
        return jsonify({'error': '数量を入力してください'}), 400
    
    try:
        amount_float = float(amount)
    except:
        return jsonify({'error': '数量は数値で入力してください'}), 400
    
    if amount_float <= 0:
        return jsonify({'error': '数量は0より大きい値を入力してください'}), 400
    
    # 最小数量チェック
    MIN_ORDER_AMOUNT = 0.0001
    if amount_float < MIN_ORDER_AMOUNT:
        return jsonify({'error': f'最小注文数量は {MIN_ORDER_AMOUNT} BTC です'}), 400
    
    # 指値注文の場合は価格チェック
    if order_type == 'limit':
        if not price:
            return jsonify({'error': '指値価格を入力してください'}), 400
        
        try:
            price_float = float(price)
        except:
            return jsonify({'error': '価格は数値で入力してください'}), 400
        
        if price_float <= 0:
            return jsonify({'error': '価格は0より大きい値を入力してください'}), 400
        
        # 価格範囲チェック（現在価格の±10%）
        min_price = CURRENT_BTC_PRICE * 0.9
        max_price = CURRENT_BTC_PRICE * 1.1
        if price_float < min_price or price_float > max_price:
            return jsonify({'error': f'価格は現在価格の±10%以内（{int(min_price):,}円〜{int(max_price):,}円）で指定してください'}), 400
        
        execution_price = price_float
    else:
        # 成行注文の場合は現在価格で約定
        execution_price = CURRENT_BTC_PRICE
    
    # 残高チェック
    if order_side == 'buy':
        # 買い注文：JPY残高が必要
        required_jpy = execution_price * amount_float
        fee = required_jpy * 0.001  # 0.1%手数料
        total_required = required_jpy + fee
        
        if total_required > mock_balance['JPY']:
            return jsonify({'error': f'JPY残高が不足しています（必要: {int(total_required):,}円、残高: {int(mock_balance["JPY"]):,}円）'}), 400
    else:
        # 売り注文：BTC残高が必要
        if amount_float > mock_balance['BTC']:
            return jsonify({'error': f'BTC残高が不足しています（必要: {amount_float}BTC、残高: {mock_balance["BTC"]}BTC）'}), 400
    
    # 注文作成
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_id = order_id_counter
    order_id_counter += 1
    
    new_order = {
        'id': order_id,
        'side': order_side,
        'type': order_type,
        'amount': amount_float,
        'price': execution_price,
        'total': execution_price * amount_float,
        'fee': execution_price * amount_float * 0.001,
        'status': 'filled' if order_type == 'market' else 'open',  # 成行は即約定
        'created_at': now,
        'filled_at': now if order_type == 'market' else None
    }
    
    mock_orders.append(new_order)
    
    # 成行注文の場合は即座に残高を更新
    if order_type == 'market':
        if order_side == 'buy':
            mock_balance['JPY'] -= (new_order['total'] + new_order['fee'])
            mock_balance['BTC'] += amount_float
        else:
            mock_balance['BTC'] -= amount_float
            mock_balance['JPY'] += (new_order['total'] - new_order['fee'])
    
    return jsonify({
        'success': True,
        'message': '注文を受け付けました' if order_type == 'limit' else '注文が約定しました',
        'order': new_order
    })

# API: 注文一覧取得
@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')  # 'open', 'filled', 'all'
    
    if status == 'open':
        filtered_orders = [o for o in mock_orders if o['status'] == 'open']
    elif status == 'filled':
        filtered_orders = [o for o in mock_orders if o['status'] == 'filled']
    else:
        filtered_orders = mock_orders
    
    return jsonify(filtered_orders)

# API: 注文キャンセル
@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    time.sleep(0.3)
    
    order = next((o for o in mock_orders if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'error': '注文が見つかりません'}), 404
    
    if order['status'] != 'open':
        return jsonify({'error': 'この注文はキャンセルできません'}), 400
    
    order['status'] = 'cancelled'
    order['cancelled_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        'success': True,
        'message': '注文をキャンセルしました',
        'order': order
    })

if __name__ == '__main__':
    print('=' * 50)
    print('デモサイトが起動しました！')
    print('ブラウザで http://localhost:5000 を開いてください')
    print('=' * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
