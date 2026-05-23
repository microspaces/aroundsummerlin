#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v3
Focus on finding the actual location switcher (not user profile)
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
    print("=== HighLevel Location Switcher v3 ===\n")
    
    # Get detailed header info
    print("1. Examining header structure...")
    header_script = """
        (function() {
            const header = document.querySelector('.hl_header');
            if (!header) return JSON.stringify({error: 'No header'});
            
            // Look for the location picker specifically
            const picker = header.querySelector('.hl_header--picker');
            
            // Get all buttons and clickable elements in header
            const allElements = Array.from(header.querySelectorAll('button, a, div, span'));
            const clickableElements = allElements.filter(el => {
                const style = window.getComputedStyle(el);
                return el.offsetWidth > 0 && el.offsetHeight > 0;
            }).map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    className: (el.className || '').substring(0, 100),
                    id: el.id,
                    text: (el.innerText || '').trim().substring(0, 50),
                    x: Math.round(rect.left + rect.width / 2),
                    y: Math.round(rect.top + rect.height / 2),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                };
            });
            
            return JSON.stringify({
                pickerFound: !!picker,
                pickerHTML: picker ? picker.outerHTML.substring(0, 300) : 'No picker',
                clickableElements: clickableElements.slice(0, 15)
            });
        })()
    """
    
    result = await evaluate_js(header_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
    
    # Look at the sidebar structure more carefully
    print("\n2. Examining sidebar structure...")
    sidebar_script = """
        (function() {
            const sidebar = document.querySelector('#sidebar-v2');
            if (!sidebar) return JSON.stringify({error: 'No sidebar'});
            
            // Get the main content area of sidebar
            const mainContent = sidebar.querySelector('.relative.flex.flex-col.h-screen.w-14');
            
            if (!mainContent) return JSON.stringify({error: 'No main content'});
            
            // Get all children
            const children = Array.from(mainContent.children);
            
            return JSON.stringify({
                childCount: children.length,
                children: children.map((child, i) => {
                    const rect = child.getBoundingClientRect();
                    return {
                        index: i,
                        tag: child.tagName,
                        className: (child.className || '').substring(0, 100),
                        id: child.id,
                        text: (child.innerText || '').trim().substring(0, 50),
                        x: Math.round(rect.left + rect.width / 2),
                        y: Math.round(rect.top + rect.height / 2),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    };
                })
            });
        })()
    """
    
    result = await evaluate_js(sidebar_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
    
    # Try clicking on the location picker if found
    print("\n3. Looking for location picker to click...")
    
    # The location picker might be the bootstrap-select element
    picker_script = """
        (function() {
            const picker = document.querySelector('.hl_header--picker');
            if (picker) {
                const rect = picker.getBoundingClientRect();
                return JSON.stringify({
                    found: true,
                    x: Math.round(rect.left + rect.width / 2),
                    y: Math.round(rect.top + rect.height / 2),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    text: picker.innerText.trim().substring(0, 50)
                });
            }
            return JSON.stringify({found: false});
        })()
    """
    
    result = await evaluate_js(picker_script)
    if result:
        picker_data = json.loads(result)
        print(json.dumps(picker_data, indent=2))
        
        if picker_data.get('found'):
            print(f"\n4. Clicking on location picker at ({picker_data['x']}, {picker_data['y']})...")
            await click_at(picker_data['x'], picker_data['y'])
            await asyncio.sleep(2)
            
            print("5. Taking screenshot after picker click...")
            await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v3_picker_click.png")
            
            # Look for "Around Summerlin" option
            print("\n6. Looking for location options...")
            option_script = """
                (function() {
                    const options = Array.from(document.querySelectorAll('li, a, div, span')).filter(el => {
                        const text = (el.innerText || '').trim();
                        return text === 'Around Summerlin' || text.includes('Around Summerlin');
                    });
                    
                    return JSON.stringify({
                        found: options.length > 0,
                        count: options.length,
                        options: options.slice(0, 5).map(el => ({
                            tag: el.tagName,
                            text: el.innerText.trim().substring(0, 50),
                            className: (el.className || '').substring(0, 50),
                            x: Math.round(el.getBoundingClientRect().left + el.getBoundingClientRect().width / 2),
                            y: Math.round(el.getBoundingClientRect().top + el.getBoundingClientRect().height / 2)
                        }))
                    });
                })()
            """
            
            result = await evaluate_js(option_script)
            if result:
                print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
