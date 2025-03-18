import os
import time

from playwright_recaptcha import recaptchav2

from browser_use.agent.service import Agent


class ReCaptchaSolver:
    async def solve_captcha(self, context: Agent, image_challenge: bool) -> None:
        captcha_key = os.getenv("CAPSOLVER_API_KEY")
        if not captcha_key and image_challenge:
            print("[WARNING] CAPSOLVER_API_KEY is not set in environment variables.")
        try:
            page = await context.browser_context.get_current_page()

            recaptcha_frame_locator = page.frame_locator("iframe[title='reCAPTCHA']")
            recaptcha_iframes = await page.locator("iframe[title='reCAPTCHA']").count()

            if recaptcha_iframes:
                # Check is reCAPTCHA already solved
                checkbox_locator = recaptcha_frame_locator.locator("span[aria-checked='true']")
                if await checkbox_locator.count() > 0:
                    print("[INFO] reCAPTCHA already solved.")
                    return

                print("[INFO] reCAPTCHA found, solving using audio...")
                solver = recaptchav2.AsyncSolver(page, capsolver_api_key=captcha_key)
                await solver.solve_recaptcha(wait=True, image_challenge=image_challenge)
            else:
                print("[INFO] reCAPTCHA not found.")
        except Exception as e:
            if not image_challenge:
                time.sleep(1)
                await context.browser_context.refresh_page()
                print(f"[INFO] Retry reCAPTCHA solving using Capsolver...")
                await self.solve_captcha(context, True)
            else:
                print(f"[ERROR] Error during solving reCAPTCHA: {e}")
