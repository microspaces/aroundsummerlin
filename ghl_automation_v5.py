#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v5
Try to find and use the location switcher through various methods
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

async def click_at(x, y):
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Input.enable")
        await send_command(ws, 2, "Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1
        })
        await send_command(ws, 3, "Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1
        })
        print(f"Clicked at ({x}, {y})")

async def navigate_to(url):
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Page.enable")
        result = await send_command(ws, 2, "Page.navigate", {"url": url})
        print(f"Navigation result: {json.dumps(result, indent=2)[:200]}")

async def main():
    print("=== HighLevel Location Switcher v5 ===\n")
    
    # First, let's try to find the location ID for "Around Summerlin"
    print("1. Looking for location information in the page...")
    
    # Check if there's any location data in the window object
    location_script = """
        (function() {
            // Check various places where location data might be stored
            const checks = {
                currentUrl: window.location.href,
                locationId: window.location.pathname.match(/location\/([^\/]+)/)?.[1],
                hasLocationData: !!window.locationData,
                hasAppData: !!window.appData,
                hasUserData: !!window.userData,
                localStorageKeys: Object.keys(localStorage).slice(0, 10),
                sessionStorageKeys: Object.keys(sessionStorage).slice(0, 10)
            };
            
            // Try to get location data from localStorage
            const locationData = localStorage.getItem('location');
            const userData = localStorage.getItem('user');
            const agencyData = localStorage.getItem('agency');
            
            return JSON.stringify({
                ...checks,
                locationData: locationData ? JSON.parse(locationData) : null,
                userData: userData ? JSON.parse(userData) : null,
                agencyData: agencyData ? JSON.parse(agencyData) : null
            });
        })()
    """
    
    result = await evaluate_js(location_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
    
    # Try to navigate directly to Around Summerlin location
    # First, let's see if we can find the location ID
    print("\n2. Trying to find 'Around Summerlin' location ID...")
    
    # Look in the user dropdown for location links
    find_script = """
        (function() {
            const links = Array.from(document.querySelectorAll('a'));
            const locationLinks = links.filter(a => {
                const href = a.getAttribute('href') || '';
                return href.includes('location') && href.includes('around');
            });
            
            return JSON.stringify({
                locationLinks: locationLinks.map(a => ({
                    href: a.getAttribute('href'),
                    text: a.innerText.trim()
                }))
            });
        })()
    """
    
    result = await evaluate_js(find_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Try clicking on the user avatar to see if there's a location switcher there
    print("\n3. Clicking on user avatar to check for location options...")
    await click_at(1889, 25)
    await asyncio.sleep(2)
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v5_avatar_click.png")
    
    # Check what's in the dropdown
    dropdown_script = """
        (function() {
            const dropdown = document.querySelector('.dropdown-menu');
            if (!dropdown) return JSON.stringify({error: 'No dropdown'});
            
            const items = Array.from(dropdown.querySelectorAll('a, div, span')).map(el => ({
                tag: el.tagName,
                text: el.innerText.trim().substring(0, 50),
                href: el.getAttribute('href'),
                className: (el.className || '').substring(0, 50)
            }));
            
            return JSON.stringify({items: items.slice(0, 10)});
        })()
    """
    
    result = await evaluate_js(dropdown_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Try to find if there's a location switcher by looking at the page structure
    print("\n4. Looking for location switcher in page structure...")
    structure_script = """
        (function() {
            // Look for elements that might be a location switcher
            const possibleSwitchers = [
                ...document.querySelectorAll('[class*="location"]'),
                ...document.querySelectorAll('[class*="agency"]'),
                ...document.querySelectorAll('[id*="location"]'),
                ...document.querySelectorAll('[id*="agency"]')
            ];
            
            return JSON.stringify({
                possibleSwitchers: possibleSwitchers.slice(0, 10).map(el => ({
                    tag: el.tagName,
                    className: (el.className || '').substring(0, 100),
                    id: el.id,
                    text: el.innerText.trim().substring(0, 50)
                }))
            });
        })()
    """
    
    result = await evaluate_js(structure_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
