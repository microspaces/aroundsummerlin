#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v9
Navigate back to working dashboard and explore settings for location switcher
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

async def main():
    print("=== HighLevel Location Switcher Exploration ===\n")
    
    # Navigate back to the working dashboard
    print("1. Navigating back to working dashboard...")
    await navigate_to("https://app.gohighlevel.com/v2/location/q6uX8cA903JnZtei28he/dashboard")
    await asyncio.sleep(5)
    
    print("2. Taking screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v9_dashboard.png")
    
    # Look for settings icon in sidebar
    print("\n3. Looking for settings icon...")
    settings_script = """
        (function() {
            const sidebar = document.querySelector('#sidebar-v2');
            if (!sidebar) return JSON.stringify({error: 'No sidebar'});
            
            const settingsLink = sidebar.querySelector('a[href*="settings"], a[id*="settings"], a[title*="Settings"]');
            
            if (settingsLink) {
                const rect = settingsLink.getBoundingClientRect();
                return JSON.stringify({
                    found: true,
                    href: settingsLink.getAttribute('href'),
                    id: settingsLink.id,
                    x: Math.round(rect.left + rect.width / 2),
                    y: Math.round(rect.top + rect.height / 2)
                });
            }
            
            // Look for gear icon or settings-related classes
            const allLinks = Array.from(sidebar.querySelectorAll('a'));
            const settingsLinks = allLinks.filter(a => {
                const className = (a.className || '').toLowerCase();
                const id = (a.id || '').toLowerCase();
                return className.includes('setting') || id.includes('setting');
            });
            
            return JSON.stringify({
                found: false,
                settingsLinks: settingsLinks.map(a => ({
                    href: a.getAttribute('href'),
                    id: a.id,
                    className: a.className
                }))
            });
        })()
    """
    
    result = await evaluate_js(settings_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
        
        if data.get('found'):
            print(f"\n4. Clicking on settings at ({data['x']}, {data['y']})...")
            await click_at(data['x'], data['y'])
            await asyncio.sleep(3)
            
            print("5. Taking screenshot after settings click...")
            await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v9_settings.png")
    
    # Try to find location settings
    print("\n6. Looking for location-related settings...")
    location_settings_script = """
        (function() {
            const allLinks = Array.from(document.querySelectorAll('a'));
            const locationLinks = allLinks.filter(a => {
                const href = (a.getAttribute('href') || '').toLowerCase();
                const text = (a.innerText || '').toLowerCase();
                return href.includes('location') || text.includes('location');
            });
            
            return JSON.stringify({
                locationLinks: locationLinks.slice(0, 10).map(a => ({
                    href: a.getAttribute('href'),
                    text: a.innerText.trim().substring(0, 50)
                }))
            });
        })()
    """
    
    result = await evaluate_js(location_settings_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Look at the full page to see if there's a location switcher we missed
    print("\n7. Examining full page structure...")
    structure_script = """
        (function() {
            const header = document.querySelector('.hl_header');
            const sidebar = document.querySelector('#sidebar-v2');
            
            return JSON.stringify({
                headerHTML: header ? header.outerHTML.substring(0, 1000) : 'No header',
                sidebarHTML: sidebar ? sidebar.outerHTML.substring(0, 1000) : 'No sidebar'
            });
        })()
    """
    
    result = await evaluate_js(structure_script)
    if result:
        data = json.loads(result)
        print("Header (first 1000 chars):")
        print(data.get('headerHTML', 'N/A')[:500])
        print("\nSidebar (first 1000 chars):")
        print(data.get('sidebarHTML', 'N/A')[:500])

if __name__ == "__main__":
    asyncio.run(main())
