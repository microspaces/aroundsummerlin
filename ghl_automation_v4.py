#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v4
Try clicking on sidebar icons to find location switcher
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

async def main():
    print("=== HighLevel Location Switcher v4 ===\n")
    
    # Get sidebar icons
    print("1. Getting sidebar icons...")
    icons_script = """
        (function() {
            const sidebar = document.querySelector('#sidebar-v2');
            if (!sidebar) return JSON.stringify({error: 'No sidebar'});
            
            const nav = sidebar.querySelector('nav') || sidebar.querySelector('.flex.flex-col');
            if (!nav) return JSON.stringify({error: 'No nav'});
            
            const items = Array.from(nav.querySelectorAll('a, button, div[role="button"]'));
            
            return JSON.stringify({
                itemCount: items.length,
                items: items.slice(0, 20).map((el, i) => {
                    const rect = el.getBoundingClientRect();
                    return {
                        index: i,
                        tag: el.tagName,
                        className: (el.className || '').substring(0, 100),
                        id: el.id,
                        text: (el.innerText || '').trim().substring(0, 50),
                        title: el.getAttribute('title'),
                        ariaLabel: el.getAttribute('aria-label'),
                        x: Math.round(rect.left + rect.width / 2),
                        y: Math.round(rect.top + rect.height / 2),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    };
                })
            });
        })()
    """
    
    result = await evaluate_js(icons_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
        
        # Try clicking on the first few icons to see if any opens a location switcher
        if 'items' in data and len(data['items']) > 0:
            print("\n2. Trying to click on sidebar icons...")
            
            for i, item in enumerate(data['items'][:5]):
                print(f"\n--- Trying icon {i}: {item.get('text', 'no text')} at ({item['x']}, {item['y']}) ---")
                await click_at(item['x'], item['y'])
                await asyncio.sleep(2)
                
                screenshot_name = f"/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v4_icon_{i}.png"
                await take_screenshot(screenshot_name)
                
                # Check if a location dropdown appeared
                check_script = """
                    (function() {
                        const dropdowns = Array.from(document.querySelectorAll('.dropdown-menu, [class*="dropdown"]'));
                        const locationEls = dropdowns.filter(el => {
                            const text = (el.innerText || '').toLowerCase();
                            return text.includes('around summerlin') || text.includes('microspacez');
                        });
                        
                        return JSON.stringify({
                            dropdownsFound: dropdowns.length,
                            locationDropdowns: locationEls.length,
                            texts: dropdowns.slice(0, 3).map(el => el.innerText.substring(0, 100))
                        });
                    })()
                """
                result = await evaluate_js(check_script)
                if result:
                    print(json.dumps(json.loads(result), indent=2))
    
    # Also try looking for a location switcher in the main content area
    print("\n3. Looking for location switcher in main content...")
    main_script = """
        (function() {
            // Look for any element mentioning location switching
            const allElements = Array.from(document.querySelectorAll('*'));
            const switchers = allElements.filter(el => {
                const text = (el.innerText || '').trim().toLowerCase();
                const className = (el.className || '').toLowerCase();
                return (text.includes('switch location') || 
                        text.includes('change location') ||
                        text.includes('select location') ||
                        className.includes('location-switcher')) &&
                        text.length < 100;
            });
            
            return JSON.stringify({
                switchersFound: switchers.length,
                switchers: switchers.slice(0, 5).map(el => ({
                    tag: el.tagName,
                    text: el.innerText.trim().substring(0, 50),
                    className: (el.className || '').substring(0, 50)
                }))
            });
        })()
    """
    
    result = await evaluate_js(main_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
