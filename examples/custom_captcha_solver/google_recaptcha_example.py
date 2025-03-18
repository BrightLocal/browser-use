from datetime import datetime

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from examples.custom_captcha_solver.captcha_solver import ReCaptchaSolver

load_dotenv()

import asyncio

browser = Browser(
    config=BrowserConfig(
        disable_security=True,
        headless=False,
    )
)
llm = ChatOpenAI(model="gpt-4o")


async def main():
    task = (
        "Open this site https://www.google.com/recaptcha/api2/demo"
        " check is captcha solved by me each second"
        " click 'Submit' button if solved"
        " finish the task"
    )

    solver_instance = ReCaptchaSolver()

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        captcha_solver=solver_instance,
    )

    result = await agent.run()
    print(result)

asyncio.run(main())
