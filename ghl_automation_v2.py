#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v2
Focuses on finding and clicking the location switcher
"""

import asyncio
import websockets
import json
import base64

CDP_URL = "ws://127.0.0.1:18800/devtools/page/0408AD383CFCEF14738850E130249ACE"

async def send_command(ws, cmd_id, method, params=None):
    """Send a CDP command and return the response"""
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
    """Take a screenshot"""
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
    """Evaluate JavaScript"""
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
    """Click at coordinates"""
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Input.enable")
        
        await send_command(ws, 2, "Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": x,
            "y": y,
            "button": "left",
            "clickCount": 1
        })
        
        await send_command(ws, 3, "Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": x,
            "y": y,
            "button": "left",
            "clickCount": 1
        })
        
        print(f"Clicked at ({x}, {y})")

async def get_element_rect(selector):
    """Get element bounding rect"""
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
                left: rect.left,
                right: rect.right,
                bottom: rect.bottom
            }});
        }})()
    """
    result = await evaluate_js(script)
    if result:
        return json.loads(result)
    return None

async def main():
    print("=== HighLevel Location Switcher Automation ===\n")
    
    # Get window dimensions
    print("1. Getting window dimensions...")
    window_size = await evaluate_js("JSON.stringify({width: window.innerWidth, height: window.innerHeight})")
    if window_size:
        size = json.loads(window_size)
        print(f"Window size: {size['width']}x{size['height']}")
    
    # Take initial screenshot
    print("\n2. Taking initial screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v2_initial.png")
    
    # Look for the user profile dropdown in the top right
    print("\n3. Looking for user profile dropdown...")
    
    # Try to find the profile dropdown
    profile_script = """
        (function() {
            // Look for dropdown elements in the header
            const header = document.querySelector('.hl_header');
            if (!header) return JSON.stringify({error: 'No header found'});
            
            const dropdowns = Array.from(header.querySelectorAll('.dropdown, [class*="dropdown"], button, [role="button"]'));
            
            return JSON.stringify({
                dropdowns: dropdowns.slice(0, 5).map((el, i) => ({
                    index: i,
                    tag: el.tagName,
                    className: (el.className || '').substring(0, 100),
                    id: el.id,
                    text: (el.innerText || '').trim().substring(0, 50),
                    ariaLabel: el.getAttribute('aria-label')
                }))
            });
        })()
    """
    
    result = await evaluate_js(profile_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Try clicking on the profile dropdown (usually top right)
    print("\n4. Trying to click on profile dropdown...")
    
    # The profile dropdown is typically in the top right corner
    # Let's try clicking at coordinates that would hit it
    if size:
        # Click near the top right where profile icon usually is
        profile_x = size['width'] - 50
        profile_y = 30
        
        print(f"Clicking at profile area ({profile_x}, {profile_y})...")
        await click_at(profile_x, profile_y)
        await asyncio.sleep(2)
        
        print("5. Taking screenshot after profile click...")
        await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v2_profile_click.png")
    
    # Now let's look for "Around Summerlin" in the dropdown
    print("\n6. Looking for location options...")
    location_script = """
        (function() {
            const dropdownMenu = document.querySelector('.dropdown-menu');
            if (!dropdownMenu) return JSON.stringify({error: 'No dropdown menu found'});
            
            const items = Array.from(dropdownMenu.querySelectorAll('*')).filter(el => {
                const text = (el.innerText || '').trim();
                return text.length > 0 && text.length < 100;
            });
            
            return JSON.stringify({
                visible: dropdownMenu.style.display !== 'none',
                items: items.slice(0, 15).map(el => ({
                    tag: el.tagName,
                    text: el.innerText.trim().substring(0, 50),
                    className: (el.className || '').substring(0, 50)
                }))
            });
        })()
    """
    
    result = await evaluate_js(location_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
