# 変更ログ

このプロジェクトの主要な変更履歴を記録します。

---

## [2.0.0] - 2026-03-02

### 🎉 メジャーアップデート：Bybit API統合とプロダクション級注文機能実装

このバージョンでは、テスト設計演習に適した本格的な暗号資産取引デモサイトを実現しました。

### ✨ 新機能

#### リアルタイムチャート機能

- **Bybit WebSocket API統合**
  - `wss://stream.bybit.com/v5/public/linear` を使用したリアルタイムKlineデータ取得
  - 自動再接続機能（5秒間隔でリトライ）
  - WebSocket接続状態の可視化（●マーク：緑=接続中、灰=切断、赤=エラー）
- **Bybit REST API統合**
  - `/v5/market/kline` エンドポイントで過去200件のKlineデータを取得
  - USD/JPY換算レート（150固定）での価格表示

- **時間足切替機能**
  - 対応時間足：1分、5分、15分、30分、1時間、4時間、1日
  - Bybit API対応インターバル：`1`, `5`, `15`, `30`, `60`, `240`, `D`
  - ボタンクリックで即座に切替可能

- **チャート表示切替**
  - ラインチャート（面グラフ）
  - キャンドルスティックチャート（ローソク足）
  - Chart.js の candlestick プラグイン使用

#### 注文機能（完全実装）

- **注文種別**
  - 買い注文（Buy）
  - 売り注文（Sell）

- **注文タイプ**
  - 成行注文（Market Order）：現在価格で即座に約定
  - 指値注文（Limit Order）：指定価格での注文（未約定状態で保持）

- **包括的なバリデーション機能**
  - 数量チェック：
    - 最小注文数量 0.0001 BTC
    - 正の数値のみ許可
    - 数値形式チェック
  - 価格チェック（指値注文）：
    - 現在価格の±10%以内に制限
    - 正の数値のみ許可
    - 価格範囲エラーメッセージ表示
  - 残高チェック：
    - 買い注文：JPY残高（手数料込み）
    - 売り注文：BTC残高
    - 残高不足時の詳細エラー表示

- **Quick Amountボタン**
  - 25%、50%、75%、100%の4段階
  - 買い注文：利用可能JPYから自動計算（手数料0.1%考慮）
  - 売り注文：保有BTCから自動計算

- **リアルタイム計算表示**
  - 概算金額（価格×数量）
  - 手数料（0.1%）
  - 合計金額（手数料込み/手数料引き）
  - 現在価格の常時表示

- **ユーザーフィードバック**
  - エラーメッセージ（赤色、8種類のバリデーションエラー）
  - 成功メッセージ（緑色）
  - ローディング状態表示（「処理中...」）

#### 注文管理機能

- **注文履歴タブ**
  - 全注文の一覧表示
  - 表示項目：注文日時、売買、種別、価格、数量、合計、ステータス、操作
  - ステータス別バッジ表示：
    - 約定（filled）：緑色バッジ
    - 未約定（open）：黄色バッジ
    - キャンセル済（cancelled）：灰色バッジ

- **注文キャンセル機能**
  - 未約定注文のみキャンセル可能
  - キャンセルボタン（赤枠）
  - 即座に注文一覧を更新

- **入出金履歴タブ**
  - 既存の入出金履歴表示機能を維持

### 🔧 バックエンド拡張

#### 新規APIエンドポイント

1. **`GET /api/current-price`**
   - 現在のBTC/JPY価格を取得
   - レスポンス：`{ symbol, price, timestamp }`

2. **`POST /api/orders`**
   - 新規注文作成
   - リクエスト：`{ side, type, amount, price? }`
   - バリデーション：
     - 注文種別（buy/sell）
     - 注文タイプ（market/limit）
     - 数量（最小0.0001 BTC）
     - 価格（指値の場合、現在価格±10%）
     - 残高チェック
   - レスポンス：`{ success, message, order }`

3. **`GET /api/orders?status={status}`**
   - 注文一覧取得
   - クエリパラメータ：`status` (open/filled/all)
   - レスポンス：注文オブジェクトの配列

4. **`DELETE /api/orders/{order_id}`**
   - 注文キャンセル
   - バリデーション：
     - 注文の存在確認
     - 未約定状態（open）のみキャンセル可能
   - レスポンス：`{ success, message, order }`

#### データモデル拡張

- **残高（balance）**
  - 追加：`JPY: 5000000`（500万円）
- **注文（order）**
  ```python
  {
    'id': int,
    'side': 'buy' | 'sell',
    'type': 'market' | 'limit',
    'amount': float,
    'price': float,
    'total': float,
    'fee': float,
    'status': 'open' | 'filled' | 'cancelled',
    'created_at': str,
    'filled_at': str | None,
    'cancelled_at': str | None
  }
  ```

### 🎨 フロントエンド強化

#### UIコンポーネント

- **TradingPanel（注文パネル）**
  - 完全リニューアル
  - 買い・売り切替ボタン
  - 成行・指値モード切替
  - 現在価格表示エリア
  - 数量・価格入力フォーム
  - Quick Amountボタン（4段階）
  - 概算金額サマリー
  - エラー・成功メッセージエリア
  - 注文ボタン（買い=緑、売り=赤）

- **HistoryView（履歴画面）**
  - タブ構成変更：注文履歴、入出金履歴
  - 注文履歴テーブル実装
  - キャンセルボタン追加
  - ステータスバッジ表示

- **PriceChart（チャート）**
  - Lightweight ChartsからChart.jsへ移行
  - Candlestickプラグイン使用
  - WebSocketデータのリアルタイム更新
  - 時間足に応じたX軸フォーマット変更

#### CSS追加

- `.order-mode-toggle` - 成行・指値切替ボタン
- `.current-price-display` - 現在価格表示エリア
- `.input-hint` - 入力フィールドヒント
- `.error-message` - エラーメッセージ（赤背景）
- `.success-message` - 成功メッセージ（緑背景）
- `.cancel-order-btn` - 注文キャンセルボタン
- `.order-type-badge` - 注文種別バッジ
- `.summary-row.total` - 合計金額行
- `.ws-status` - WebSocket接続状態インジケーター

### 🔄 変更内容

#### データソース変更

- **変更前**：CoinGecko API（`api.coingecko.com`）
  - 制限：時間足なし、1時間/1日/1週間/1ヶ月の粒度のみ
  - データ：BTC/JPY直接取得

- **変更後**：Bybit API（`api.bybit.com`, `stream.bybit.com`）
  - 利点：実取引所データ、1分〜1日の7段階時間足対応
  - データ：BTC/USDT取得後、JPY換算（レート150）

#### 関数の変更

- `fetchBTCPriceData()` → 削除
- `fetchBTCOhlcData()` → 削除
- `fetchBybitKlineData(interval, limit)` → 新規追加
- `getBybitInterval(interval)` → 新規追加

#### コンポーネントの変更

- `PriceChart`
  - Lightweight Charts API → Chart.js API
  - useEffect依存関係：`[interval, chartType]` → `[klineData, chartType, interval]`
  - WebSocket接続管理追加

- `TradingPanel`
  - Props：`onTrade` → `onOrderCreated`
  - State大幅拡張（orderSide, orderType, currentPrice, error, success, loading）
  - ロジック追加：残高計算、API通信、バリデーション

- `App`
  - State追加：`orders`
  - 関数追加：`fetchOrders()`, `handleOrderCreated()`, `handleCancelOrder()`
  - 初期値変更：`chartInterval: "60"`, `chartType: "candle"`

### 🐛 バグ修正

- チャートコンテナの参照エラー修正（`chartRootRef` → `chartRef`）
- HistoryViewの重複コード削除
- JSX構文エラー修正

### 📚 テスト設計観点の拡充

| テスト観点             | 実装内容                     | 期待されるテストケース数 |
| ---------------------- | ---------------------------- | ------------------------ |
| **境界値分析**         | 最小数量0.0001、価格±10%     | 10+                      |
| **同値分割**           | 有効/無効数量、有効/無効価格 | 8+                       |
| **エラーケース**       | 8種類のバリデーションエラー  | 8                        |
| **状態遷移**           | open→filled/cancelled        | 6+                       |
| **組み合わせテスト**   | 買売×成行指値×数量×価格      | 20+                      |
| **入力バリデーション** | 文字列、負数、ゼロ、NULL     | 12+                      |
| **データ整合性**       | 残高更新、注文履歴、チャート | 8+                       |

### 📦 依存関係

#### 追加なし

- すべて既存のCDN経由で提供されるライブラリを使用
- Chart.js candlestickプラグインは既にindex.htmlに含まれていた

#### Python（変更なし）

- Flask
- flask-cors

### 🔐 セキュリティ

- WebSocket接続エラーハンドリング追加
- API呼び出し時のtry-catchブロック実装
- ユーザー入力の厳格なバリデーション（数値チェック、範囲チェック、型チェック）

### ⚡ パフォーマンス

- WebSocket自動再接続により接続安定性向上
- REST APIは初回ロード時のみ、以降はWebSocketで更新
- 注文作成後は必要なデータのみ再取得（残高、注文一覧）

### 📖 ドキュメント

- コード内コメント追加
- API仕様の明確化（バリデーションルール記載）

### 🎯 テスト設計演習としての価値

このバージョンにより、以下のテスト設計スキルを実践的に学習可能：

1. ✅ **入力バリデーション設計**
   - 必須チェック、形式チェック、範囲チェック、桁数チェック
2. ✅ **エラーメッセージ設計**
   - 8種類の具体的エラーメッセージ、表示位置、優先順位

3. ✅ **状態管理テスト**
   - 注文ステータス遷移（未約定→約定/キャンセル）
   - 残高の増減パターン

4. ✅ **組み合わせテスト**
   - 買売×成行指値×価格帯×数量の組み合わせ
   - ペアワイズ法やオールペア法の適用

5. ✅ **非機能テスト観点**
   - WebSocket接続断時の挙動
   - API遅延時のローディング表示
   - エラーリカバリー

---

## [1.0.0] - 2026-02-27

### 初回リリース

#### 主要機能

- テスト設計トレーニング文書（index.md）
- 暗号資産取引デモサイト（Flask + React）
- 基本的なチャート表示（CoinGecko API）
- 入出金機能
- 資産状況表示
- ダークテーマUI
- Playwright E2Eテストスイート

#### 技術スタック

- バックエンド：Flask（Python 3.13）
- フロントエンド：React 18（CDN）
- チャート：Lightweight Charts（当時）
- テスト：Pytest + Playwright
- 価格データ：CoinGecko API

---

## フォーマット

このCHANGELOGは [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) のフォーマットに従っており、
[セマンティック バージョニング](https://semver.org/lang/ja/) を採用しています。

### カテゴリー

- **✨ 新機能**: 新しい機能の追加
- **🔧 変更**: 既存機能の変更
- **🐛 バグ修正**: バグ修正
- **🔐 セキュリティ**: セキュリティに関する変更
- **⚡ パフォーマンス**: パフォーマンス改善
- **📚 ドキュメント**: ドキュメントの変更
- **🎨 スタイル**: UI/UXの改善
- **♻️ リファクタリング**: コードの内部構造改善
- **🧪 テスト**: テストの追加・修正
