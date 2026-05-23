#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v13
Navigate to dashboard and take clean screenshot
"""

import asyncio
import websockets
import json
import base64

CDP_URL = "ws://127.0.0.1:18800/devtools/page/0408AD383CFCEF14738850E130249ACE"

async def send_command(ws, cmd_id, method, params=None):
    command = {"id": cmd_id, "method": method}
    if params:
        command["params"] = params
    await ws.send(json.dumps(command))
    
    while True:
        msg = await ws.recv()
        data = json.loads(msg)
        if data.get("id") == cmd_id:
            return data

async def take_screenshot(filename, clip=None):
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Page.enable")
        params = {"format": "png"}
        if clip:
            params["clip"] = clip
        result = await send_command(ws, 2, "Page.captureScreenshot", params)
        if "result" in result and "data" in result["result"]:
            with open(filename, "wb") as f:
                f.write(base64.b64decode(result["result"]["data"]))
            print(f"Screenshot saved: {filename}")
            return True
        return False

async def navigate_to(url):
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Page.enable")
        result = await send_command(ws, 2, "Page.navigate", {"url": url})
        print(f"Navigation initiated to {url}")
        return result

async def main():
    print("=== HighLevel Clean Dashboard Screenshot ===\n")
    
    # Navigate to the dashboard
    print("1. Navigating to dashboard...")
    await navigate_to("https://app.gohighlevel.com/v2/location/q6uX8cA903JnZtei28he/dashboard")
    await asyncio.sleep(5)
    
    print("2. Taking clean dashboard screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_around_summerlin_dashboard.png")
    
    print("\nDone! The dashboard shows the 'Around Summerlin' location.")

if __name__ == "__main__":
    asyncio.run(main())
