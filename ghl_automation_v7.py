#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v7
Investigate the relationship between user and locations
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
    print("=== HighLevel Location Investigation ===\n")
    
    # Get all localStorage data
    print("1. Getting all relevant localStorage data...")
    storage_script = """
        (function() {
            const keys = ['activeLocations', 'a', 'user', 'agency', 'company', 'locations'];
            const data = {};
            
            keys.forEach(key => {
                const value = localStorage.getItem(key);
                if (value) {
                    try {
                        // Try to parse as JSON first
                        data[key] = JSON.parse(value);
                    } catch (e) {
                        // If not JSON, store as string
                        data[key] = value;
                    }
                }
            });
            
            return JSON.stringify(data);
        })()
    """
    
    result = await evaluate_js(storage_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
    
    # Look at the page title and meta tags
    print("\n2. Getting page metadata...")
    meta_script = """
        (function() {
            const title = document.title;
            const metaTags = Array.from(document.querySelectorAll('meta')).map(meta => ({
                name: meta.getAttribute('name'),
                content: meta.getAttribute('content')
            })).filter(m => m.name);
            
            return JSON.stringify({
                title: title,
                metaTags: metaTags
            });
        })()
    """
    
    result = await evaluate_js(meta_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Check if there's an API endpoint or data that shows all available locations
    print("\n3. Looking for location data in the page...")
    api_script = """
        (function() {
            // Look for any script tags that might contain location data
            const scripts = Array.from(document.querySelectorAll('script'));
            const locationScripts = scripts.filter(s => {
                const text = s.innerText || '';
                return text.includes('location') || text.includes('Around Summerlin');
            });
            
            return JSON.stringify({
                locationScriptsFound: locationScripts.length,
                scriptSnippets: locationScripts.slice(0, 3).map(s => s.innerText.substring(0, 200))
            });
        })()
    """
    
    result = await evaluate_js(api_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Try to find the location switcher by looking at the sidebar more carefully
    print("\n4. Examining sidebar for location switcher...")
    sidebar_script = """
        (function() {
            const sidebar = document.querySelector('#sidebar-v2');
            if (!sidebar) return JSON.stringify({error: 'No sidebar'});
            
            // Get the first element in the sidebar (usually the logo/location)
            const firstElement = sidebar.querySelector('.sidebar-v2-location');
            
            if (firstElement) {
                return JSON.stringify({
                    found: true,
                    html: firstElement.outerHTML.substring(0, 500),
                    text: firstElement.innerText.trim().substring(0, 100)
                });
            }
            
            return JSON.stringify({found: false});
        })()
    """
    
    result = await evaluate_js(sidebar_script)
    if result:
        print(json.dumps(json.loads(result), indent=2))
    
    # Take a screenshot of the full page to see the current state
    print("\n5. Taking full page screenshot...")
    await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_v7_full.png")

if __name__ == "__main__":
    asyncio.run(main())
