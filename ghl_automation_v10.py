#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v10
Click on the location switcher dropdown at the top of sidebar
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
    print("=== HighLevel Location Switcher Click ===\n")
    
    # First, let's find the location switcher dropdown
    print("1. Finding location switcher dropdown...")
    switcher_script = """
        (function() {
            const sidebar = document.querySelector('#sidebar-v2');
            if (!sidebar) return JSON.stringify({error: 'No sidebar'});
            
            // Look for the agency logo container or location dropdown
            const logoContainer = sidebar.querySelector('.agency-logo-container');
            const dropdown = sidebar.querySelector('.dropdown');
            
            // Get the first few elements in the sidebar that might be the location switcher
            const sidebarContent = sidebar.querySelector('.flex.flex-col.flex-grow');
            const firstElements = sidebarContent ? Array.from(sidebarContent.children).slice(0, 3) : [];
            
            return JSON.stringify({
                logoContainerFound: !!logoContainer,
                dropdownFound: !!dropdown,
                firstElements: firstElements.map(el => {
                    const rect = el.getBoundingClientRect();
                    return {
                        tag: el.tagName,
                        className: (el.className || '').substring(0, 100),
                        id: el.id,
                        text: el.innerText.trim().substring(0, 100),
                        x: Math.round(rect.left + rect.width / 2),
                        y: Math.round(rect.top + rect.height / 2),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    };
                })
            });
        })()
    """
    
    result = await evaluate_js(switcher_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
        
        # Click on the first element which should be the location switcher
        if 'firstElements' in data and len(data['firstElements']) > 0:
            switcher = data['firstElements'][0]
            print(f"\n2. Clicking on location switcher at ({switcher['x']}, {switcher['y']})...")
            await click_at(switcher['x'], switcher['y'])
            await asyncio.sleep(2)
            
            print("3. Taking screenshot after clicking location switcher...")
            await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v10_switcher_open.png")
            
            # Look for "Around Summerlin" option in the dropdown
            print("\n4. Looking for location options...")
            options_script = """
                (function() {
                    const dropdownMenus = Array.from(document.querySelectorAll('.dropdown-menu'));
                    const allOptions = [];
                    
                    dropdownMenus.forEach(menu => {
                        const items = Array.from(menu.querySelectorAll('a, div, span, li')).filter(el => {
                            const text = el.innerText.trim();
                            return text.length > 0 && text.length < 100;
                        });
                        
                        allOptions.push(...items.map(el => ({
                            tag: el.tagName,
                            text: el.innerText.trim().substring(0, 50),
                            className: (el.className || '').substring(0, 50)
                        })));
                    });
                    
                    return JSON.stringify({
                        optionsFound: allOptions.length,
                        options: allOptions.slice(0, 15)
                    });
                })()
            """
            
            result = await evaluate_js(options_script)
            if result:
                print(json.dumps(json.loads(result), indent=2))
            
            # Also look for any element containing "Around Summerlin"
            print("\n5. Looking for 'Around Summerlin' text on page...")
            around_script = """
                (function() {
                    const elements = Array.from(document.querySelectorAll('*')).filter(el => {
                        const text = el.innerText || '';
                        return text.includes('Around Summerlin') && el.children.length === 0;
                    });
                    
                    return JSON.stringify({
                        found: elements.length,
                        elements: elements.map(el => ({
                            tag: el.tagName,
                            text: el.innerText.trim().substring(0, 50),
                            className: (el.className || '').substring(0, 50)
                        }))
                    });
                })()
            """
            
            result = await evaluate_js(around_script)
            if result:
                print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
