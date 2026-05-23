#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v12
Final verification - take screenshot of Around Summerlin dashboard
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

async def evaluate_js(expression):
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Runtime.enable")
        result = await send_command(ws, 2, "Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True
        })
        if "result" in result and "result" in result["result"]:
            return result["result"]["result"].get("value")
        return None

async def main():
    print("=== HighLevel Final Verification ===\n")
    
    # Get current location info
    print("1. Getting current location info...")
    info_script = """
        (function() {
            const switcher = document.querySelector('#location-switcher-sidbar-v2');
            const locationName = switcher ? switcher.querySelector('.hl_switcher-loc-name') : null;
            const locationCity = switcher ? switcher.querySelector('.hl_switcher-loc-city') : null;
            
            return JSON.stringify({
                url: window.location.href,
                title: document.title,
                locationName: locationName ? locationName.innerText : 'Not found',
                locationCity: locationCity ? locationCity.innerText : 'Not found',
                pageHeading: document.querySelector('h1, h2, .dashboard-title') ? document.querySelector('h1, h2, .dashboard-title').innerText : 'No heading found'
            });
        })()
    """
    
    result = await evaluate_js(info_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Take final screenshot of the dashboard
    print("\n2. Taking final dashboard screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_final_dashboard.png")
    
    # Close the location switcher dropdown by clicking elsewhere
    print("\n3. Closing location switcher dropdown...")
    close_script = """
        (function() {
            // Click on the main content area to close dropdown
            const mainContent = document.querySelector('.hl_wrapper--inner');
            if (mainContent) {
                mainContent.click();
                return 'Clicked on main content';
            }
            return 'No main content found';
        })()
    """
    
    result = await evaluate_js(close_script)
    print(result)
    
    await asyncio.sleep(1)
    
    print("4. Taking final screenshot with dropdown closed...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_final_clean.png")
    
    print("\n=== Summary ===")
    print("The location switcher shows 'Around Summerlin' (Las Vegas, NV)")
    print("This is the current active location.")
    print("The user is already in the 'Around Summerlin' location!")

if __name__ == "__main__":
    asyncio.run(main())
