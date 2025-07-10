
import os

SCREENSHOTS_FOLDER_PATH = "scripts/data/screenshots"
async def take_screenshot(page):
    os.makedirs(SCREENSHOTS_FOLDER_PATH, exist_ok=True)
    await page.screenshot(path=f"{SCREENSHOTS_FOLDER_PATH}/full_application.png", full_page=True)
    print(f"📸 Screenshot saved")