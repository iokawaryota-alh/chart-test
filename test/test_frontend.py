"""
フロントエンド表示とコンソールエラーのテスト

実行方法:
    pytest test/test_frontend.py -v
    
または
    python -m pytest test/test_frontend.py -v
"""
import pytest
from playwright.sync_api import Page, expect


class TestFrontendDisplay:
    """フロント表示のテスト"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """テスト実行前の注意事項を表示"""
        print("\n" + "="*60)
        print("⚠️  サーバーが起動していることを確認してください")
        print("   実行: .\\start.bat")
        print("="*60 + "\n")
        yield
    
    def test_page_loads_successfully(self, page: Page):
        """ページが正常に読み込まれるかテスト"""
        # ページにアクセス
        response = page.goto("http://localhost:5000")
        
        # ステータスコードが200であることを確認
        assert response is not None, "レスポンスがNoneです"
        assert response.ok, f"ページ読み込み失敗: ステータス {response.status}"
        
        # タイトルが正しいことを確認
        expect(page).to_have_title("SBI VC Trade デモサイト - テスト設計演習用")
    
    def test_main_elements_visible(self, page: Page):
        """主要な要素が表示されているかテスト"""
        page.goto("http://localhost:5000")
        
        # ヘッダーが表示されているか
        header = page.locator(".top-header")
        expect(header).to_be_visible()
        
        # タイトルが表示されているか
        title = page.locator(".header-title")
        expect(title).to_be_visible()
        expect(title).to_contain_text("SBI VC Trade")
        
        # タブが表示されているか
        tabs = page.locator(".tabs")
        expect(tabs).to_be_visible()
        
        # 3つのタブボタンが存在するか
        tab_buttons = page.locator(".tab")
        expect(tab_buttons).to_have_count(3)
        
        # サイドバーが表示されているか
        sidebar = page.locator(".sidebar")
        expect(sidebar).to_be_visible()
    
    def test_balance_display(self, page: Page):
        """残高が表示されているかテスト"""
        page.goto("http://localhost:5000")
        
        # 残高カードが表示されているか
        balance_cards = page.locator(".balance-card")
        expect(balance_cards).to_have_count(2)
        
        # BTC残高が表示されているか
        btc_balance = balance_cards.nth(0)
        expect(btc_balance).to_contain_text("BTC 残高")
        
        # ETH残高が表示されているか
        eth_balance = balance_cards.nth(1)
        expect(eth_balance).to_contain_text("ETH 残高")
    
    def test_tab_switching(self, page: Page):
        """タブ切り替えが動作するかテスト"""
        page.goto("http://localhost:5000")
        
        # 各タブをクリックして切り替え
        chart_tab = page.locator(".tab", has_text="チャート")
        deposit_tab = page.locator(".tab", has_text="入金")
        withdraw_tab = page.locator(".tab", has_text="出金")
        
        # チャートタブをクリック
        chart_tab.click()
        expect(chart_tab).to_have_class("tab active")
        
        # 入金タブをクリック
        deposit_tab.click()
        expect(deposit_tab).to_have_class("tab active")
        
        # 出金タブをクリック
        withdraw_tab.click()
        expect(withdraw_tab).to_have_class("tab active")


class TestConsoleErrors:
    """コンソールエラーのテスト"""
    
    def test_no_console_errors(self, page: Page):
        """コンソールにエラーが出ないかテスト"""
        console_messages = []
        errors = []
        
        # コンソールメッセージをキャプチャ
        def handle_console(msg):
            console_messages.append({
                'type': msg.type,
                'text': msg.text
            })
            if msg.type == 'error':
                errors.append(msg.text)
        
        page.on("console", handle_console)
        
        # ページを読み込み
        page.goto("http://localhost:5000")
        
        # Reactアプリがレンダリングされるまで少し待つ
        page.wait_for_selector(".app-container", timeout=5000)
        
        # エラーログを確認
        if errors:
            print("\n⚠️  コンソールエラーが検出されました:")
            for error in errors:
                print(f"  - {error}")
        
        # エラーがないことを確認
        assert len(errors) == 0, f"コンソールエラーが {len(errors)} 件検出されました: {errors}"
    
    def test_no_failed_requests(self, page: Page):
        """APIリクエストが失敗しないかテスト"""
        failed_requests = []
        
        # リクエストの失敗をキャプチャ
        def handle_response(response):
            if not response.ok and response.url.startswith("http://localhost:5000/api"):
                failed_requests.append({
                    'url': response.url,
                    'status': response.status
                })
        
        page.on("response", handle_response)
        
        # ページを読み込み
        page.goto("http://localhost:5000")
        
        # APIリクエストが完了するまで待つ
        page.wait_for_timeout(2000)
        
        # 失敗したリクエストを確認
        if failed_requests:
            print("\n⚠️  失敗したAPIリクエスト:")
            for req in failed_requests:
                print(f"  - {req['url']} (ステータス: {req['status']})")
        
        # 失敗したリクエストがないことを確認
        assert len(failed_requests) == 0, f"APIリクエストが {len(failed_requests)} 件失敗しました"
    
    def test_chart_tab_no_errors(self, page: Page):
        """チャートタブでコンソールエラーが出ないかテスト"""
        errors = []
        
        def handle_console(msg):
            if msg.type == 'error':
                errors.append(msg.text)
        
        page.on("console", handle_console)
        
        # ページを読み込み
        page.goto("http://localhost:5000")
        
        # チャートタブをクリック
        chart_tab = page.locator(".tab", has_text="チャート")
        chart_tab.click()
        
        # チャートがレンダリングされるまで待つ
        page.wait_for_timeout(3000)
        
        # エラーがないことを確認（CoinGecko APIのレート制限エラーは除外）
        critical_errors = [e for e in errors if 'chart data fetch error' not in e.lower()]
        
        if critical_errors:
            print("\n⚠️  チャートタブでコンソールエラーが検出されました:")
            for error in critical_errors:
                print(f"  - {error}")
        
        assert len(critical_errors) == 0, f"クリティカルエラーが {len(critical_errors)} 件検出されました"
