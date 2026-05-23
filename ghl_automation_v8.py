#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v8
Navigate to agency level to find all locations
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

async def navigate_to(url):
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Page.enable")
        result = await send_command(ws, 2, "Page.navigate", {"url": url})
        print(f"Navigation initiated to {url}")
        return result

async def main():
    print("=== HighLevel Agency Level Navigation ===\n")
    
    # Try to navigate to the agency/company level
    print("1. Navigating to agency level...")
    
    # HighLevel agency URL format
    agency_url = "https://app.gohighlevel.com/v2/company/szhNQrhSTLZ6tSdv8Vf2/dashboard"
    await navigate_to(agency_url)
    await asyncio.sleep(5)
    
    print("2. Taking screenshot of agency level...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_agency_level.png")
    
    # Check the page title and URL
    print("\n3. Checking current page...")
    check_script = """
        (function() {
            return JSON.stringify({
                url: window.location.href,
                title: document.title,
                bodyText: document.body.innerText.substring(0, 500)
            });
        })()
    """
    
    result = await evaluate_js(check_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Look for location list
    print("\n4. Looking for location list...")
    locations_script = """
        (function() {
            const links = Array.from(document.querySelectorAll('a'));
            const locationLinks = links.filter(a => {
                const href = a.getAttribute('href') || '';
                return href.includes('/location/');
            });
            
            return JSON.stringify({
                locationLinks: locationLinks.slice(0, 10).map(a => ({
                    href: a.getAttribute('href'),
                    text: a.innerText.trim().substring(0, 50)
                }))
            });
        })()
    """
    
    result = await evaluate_js(locations_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Try the main dashboard URL to see if there's a location switcher there
    print("\n5. Navigating to main dashboard...")
    await navigate_to("https://app.gohighlevel.com/v2/dashboard")
    await asyncio.sleep(5)
    
    print("6. Taking screenshot of main dashboard...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_main_dashboard.png")
    
    # Check for location switcher
    print("\n7. Looking for location switcher on main dashboard...")
    switcher_script = """
        (function() {
            const allText = document.body.innerText;
            const hasLocationSwitcher = allText.includes('Location') && allText.includes('Switch');
            
            const possibleSwitchers = Array.from(document.querySelectorAll('button, a, div[role="button"]')).filter(el => {
                const text = el.innerText.trim().toLowerCase();
                return text.includes('location') || text.includes('switch');
            });
            
            return JSON.stringify({
                hasLocationSwitcher: hasLocationSwitcher,
                possibleSwitchers: possibleSwitchers.slice(0, 5).map(el => ({
                    tag: el.tagName,
                    text: el.innerText.trim().substring(0, 50),
                    className: (el.className || '').substring(0, 50)
                }))
            });
        })()
    """
    
    result = await evaluate_js(switcher_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
