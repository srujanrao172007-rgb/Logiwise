"""
LogiWise Demo — exercises all features via ADK API with resilience.
Run: uv run python demo.py
"""
import asyncio
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["MODEL_BACKEND"] = "nvidia"
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["NVIDIA_MODEL"] = "nvidia/nemotron-4-340b-instruct"

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from app.agent import root_agent

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="logiwise", session_service=session_service)


def clean(text: str) -> str:
    import re
    text = re.sub(r'\s+', ' ', text)
    for c in ['\u2019', '\u2013', '\u2014', '\u00d7', '\u202f', '\u2011']:
        text = text.replace(c, {'\u2019': "'", '\u2013': '--', '\u2014': '---',
                                '\u00d7': 'x', '\u202f': ' ', '\u2011': '-'}[c])
    return text.strip()


async def run(prompt: str) -> str:
    session = await session_service.create_session(app_name="logiwise", user_id="demo")
    content = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    last = ""
    async for event in runner.run_async(
        user_id="demo",
        session_id=session.id,
        new_message=content,
    ):
        if event.author == "user":
            continue
        if event.content and event.content.parts:
            text = "".join(p.text for p in event.content.parts if p.text)
            if text.strip():
                last = clean(text.strip())
    return last


async def main():
    scenarios = [
        ("List all orders", "List all orders"),
        ("List all products in inventory", "List all products"),
        ("Check inventory for Bluetooth Speaker", "Check inventory for SKU-ELEC-004"),
        ("Restock a product", "Restock Bluetooth Speakers with 20 units"),
        ("Verify restock worked", "Check inventory for SKU-ELEC-004"),
        ("Add a new product", "Add a new product Titanium Widget with quantity 100"),
        ("Verify new product in inventory", "List all products"),
        ("Create a new order", "Create an order for Walkarounds Inc with USB-C Hub:50, Packing Tape Roll:100"),
        ("Show orders for a customer", "Show me orders for FabIndia Textiles"),
        ("Track a shipment", "What is the status of shipment TRK20004?"),
        ("Predict delay", "Predict delay for TRK20004 at Shanghai Port"),
        ("Prioritize all orders", "Prioritize all orders by urgency"),
        ("Show urgent orders", "Show urgent orders that need priority pushing"),
        ("Calculate order margins", "Calculate margins for ORD-2004"),
        ("Minimize losses", "Minimize losses for ORD-1004"),
        ("Forecast demand", "Forecast demand for SKU-ELEC-004"),
        ("Analyze customer demand", "Analyze customer demand for all customers"),
        ("Get reorder recommendations", "Get reorder recommendations for all products"),
        ("Customer 360 view", "Show customer 360 for CUST003"),
        ("Search company trends", "Search company trends for textile"),
        ("Suggest partnerships", "Suggest partnership opportunities"),
        ("Notify customer", "Notify CUST003 about shipment delay via email"),
    ]

    results = []
    for label, prompt in scenarios:
        print(f"\n{'='*60}")
        print(f">> {label}")
        print(f">> Prompt: {prompt}")
        try:
            response = await run(prompt)
            results.append((label, prompt, response, ""))
            preview = response[:200].replace("\n", " | ")
            print(f">> OK: {preview}...")
        except Exception as e:
            err = str(e)[:300]
            results.append((label, prompt, "", err))
            print(f">> ERROR: {err}")
        await asyncio.sleep(2)

    lines = ["# LogiWise Demo Script", "", "End-to-end demonstration of all features.", ""]
    successes = 0
    failures = 0
    for label, prompt, response, err in results:
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"> **User:** _{prompt}_")
        lines.append("")
        if response:
            successes += 1
            lines.append("**Agent:**")
            for rline in response.split("\n"):
                lines.append(f"> {rline}")
        else:
            failures += 1
            lines.append("> *Error during demo execution:*")
            lines.append(f"> _{err}_")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("")
    lines.append(f"**Results: {successes} succeeded, {failures} failed**")

    path = "DEMO.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n\nDemo written to {path} ({successes}/{len(results)} scenarios passed)")

if __name__ == "__main__":
    asyncio.run(main())
