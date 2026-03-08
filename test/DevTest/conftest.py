"""
Pytest設定ファイル

Playwrightのフィクスチャを設定
"""
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """ブラウザコンテキストの設定"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "locale": "ja-JP",
        "timezone_id": "Asia/Tokyo",
    }


@pytest.fixture(scope="function")
def page(browser):
    """各テストに新しいページを提供"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
