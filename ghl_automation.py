#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script
Uses Chrome DevTools Protocol (CDP) to interact with the HighLevel dashboard
"""

import asyncio
import websockets
import json
import base64
import sys

CDP_URL = "ws://127.0.0.1:18800/devtools/page/0408AD383CFCEF14738850E130249ACE"

async def send_command(ws, cmd_id, method, params=None):
    """Send a CDP command and return the response"""
    command = {"id": cmd_id, "method": method}
    if params:
        command["params"] = params
    await ws.send(json.dumps(command))
    
    # Wait for response with matching id
    while True:
        msg = await ws.recv()
        data = json.loads(msg)
        if data.get("id") == cmd_id:
            return data
        # Ignore events

async def take_screenshot(filename, clip=None):
    """Take a screenshot of the page"""
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
        else:
            print(f"Screenshot failed: {result}")
            return False

async def evaluate_js(expression):
    """Evaluate JavaScript on the page"""
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Runtime.enable")
        
        result = await send_command(ws, 2, "Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True
        })
        
        if "result" in result and "result" in result["result"]:
            return result["result"]["result"].get("value")
        return None

async def click_element(x, y):
    """Click at specific coordinates"""
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Input.enable")
        
        # Dispatch mouse press
        await send_command(ws, 2, "Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": x,
            "y": y,
            "button": "left",
            "clickCount": 1
        })
        
        # Dispatch mouse release
        await send_command(ws, 3, "Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": x,
            "y": y,
            "button": "left",
            "clickCount": 1
        })
        
        print(f"Clicked at ({x}, {y})")

async def get_element_position(selector):
    """Get the position of an element"""
    script = f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (!el) return null;
            const rect = el.getBoundingClientRect();
            return JSON.stringify({{
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2,
                width: rect.width,
                height: rect.height,
                top: rect.top,
                left: rect.left
            }});
        }})()
    """
    result = await evaluate_js(script)
    if result:
        return json.loads(result)
    return None

async def find_location_switcher():
    """Find the location switcher element"""
    script = """
        (function() {
            // Look for the location switcher in the sidebar
            const sidebar = document.querySelector('#sidebar-v2');
            if (!sidebar) return JSON.stringify({error: 'No sidebar'});
            
            // Get the first few children which might contain the location info
            const children = Array.from(sidebar.children).slice(0, 5);
            
            return JSON.stringify({
                children: children.map((child, i) => ({
                    index: i,
                    tag: child.tagName,
                    id: child.id,
                    className: (child.className || '').substring(0, 100),
                    text: (child.innerText || '').trim().substring(0, 100)
                }))
            });
        })()
    """
    result = await evaluate_js(script)
    if result:
        return json.loads(result)
    return None

async def main():
    print("=== HighLevel Dashboard Automation ===\n")
    
    # First, take a screenshot of the current state
    print("1. Taking initial screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_initial.png")
    
    # Find the location switcher
    print("\n2. Looking for location switcher...")
    switcher_info = await find_location_switcher()
    print(json.dumps(switcher_info, indent=2))
    
    # Try to find and click the location switcher
    # In HighLevel v2, the location switcher is typically at the top of the sidebar
    print("\n3. Attempting to find location switcher position...")
    
    # Try different selectors for the location switcher
    selectors = [
        "#sidebar-v2 > div:first-child",
        "#sidebar-v2 .sidebar-v2-location",
        "[class*='location-switcher']",
        "[class*='agency-name']",
        "#sidebar-v2 > div:first-child > div:first-child"
    ]
    
    for selector in selectors:
        pos = await get_element_position(selector)
        if pos:
            print(f"Found element with selector: {selector}")
            print(f"Position: x={pos['x']}, y={pos['y']}")
            
            # Click on it
            print(f"\n4. Clicking on location switcher at ({pos['x']}, {pos['y']})...")
            await click_element(pos['x'], pos['y'])
            
            # Wait a moment for dropdown to appear
            await asyncio.sleep(2)
            
            # Take screenshot after click
            print("5. Taking screenshot after click...")
            await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_after_click.png")
            break
    else:
        print("Could not find location switcher with known selectors")
        print("Trying to click at common location switcher position (top-left area)...")
        await click_element(50, 50)
        await asyncio.sleep(2)
        await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_after_click.png")

if __name__ == "__main__":
    asyncio.run(main())
