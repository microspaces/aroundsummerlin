#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v11
Click on the actual location switcher dropdown
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
    print("=== HighLevel Location Switcher v11 ===\n")
    
    # Click on the location switcher dropdown (the element with id="location-switcher-sidbar-v2")
    print("1. Clicking on location switcher dropdown at (112, 93)...")
    await click_at(112, 93)
    await asyncio.sleep(3)
    
    print("2. Taking screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v11_switcher_clicked.png")
    
    # Check if a dropdown appeared with location options
    print("\n3. Checking for location dropdown...")
    dropdown_script = """
        (function() {
            // Look for dropdown menus
            const dropdowns = Array.from(document.querySelectorAll('.dropdown-menu, [class*="dropdown"]'));
            
            // Look for any element that might be a location list
            const locationLists = Array.from(document.querySelectorAll('ul, div[role="list"]')).filter(el => {
                const text = el.innerText.toLowerCase();
                return text.includes('location') || text.includes('around') || text.includes('microspacez');
            });
            
            return JSON.stringify({
                dropdownsFound: dropdowns.length,
                dropdowns: dropdowns.slice(0, 5).map(d => ({
                    visible: d.style.display !== 'none',
                    text: d.innerText.substring(0, 200),
                    className: d.className.substring(0, 50)
                })),
                locationListsFound: locationLists.length,
                locationLists: locationLists.slice(0, 3).map(l => ({
                    text: l.innerText.substring(0, 200)
                }))
            });
        })()
    """
    
    result = await evaluate_js(dropdown_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Look for any clickable elements that appeared after clicking
    print("\n4. Looking for newly appeared elements...")
    new_elements_script = """
        (function() {
            const allElements = Array.from(document.querySelectorAll('a, button, div[role="button"], li'));
            const clickableElements = allElements.filter(el => {
                const rect = el.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0 && rect.top > 100 && rect.top < 500;
            }).map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    text: el.innerText.trim().substring(0, 50),
                    className: (el.className || '').substring(0, 50),
                    x: Math.round(rect.left + rect.width / 2),
                    y: Math.round(rect.top + rect.height / 2)
                };
            });
            
            return JSON.stringify({
                elementsFound: clickableElements.length,
                elements: clickableElements.slice(0, 10)
            });
        })()
    """
    
    result = await evaluate_js(new_elements_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Try to find the location switcher element and see its HTML
    print("\n5. Examining location switcher element...")
    switcher_html_script = """
        (function() {
            const switcher = document.querySelector('#location-switcher-sidbar-v2');
            if (!switcher) return JSON.stringify({error: 'No switcher found'});
            
            return JSON.stringify({
                html: switcher.outerHTML,
                hasDropdown: switcher.querySelector('.dropdown') !== null,
                childCount: switcher.children.length
            });
        })()
    """
    
    result = await evaluate_js(switcher_html_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
