#!/usr/bin/env python3
"""
HighLevel Dashboard Automation Script v6
Find Around Summerlin location ID and switch to it
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
        print(f"Navigation initiated")
        return result

async def wait_for_load():
    async with websockets.connect(CDP_URL) as ws:
        await send_command(ws, 1, "Page.enable")
        result = await send_command(ws, 2, "Page.getNavigationHistory")
        return result

async def main():
    print("=== HighLevel Location Switcher v6 ===\n")
    
    # Get active locations from localStorage
    print("1. Getting active locations from localStorage...")
    locations_script = """
        (function() {
            const activeLocations = localStorage.getItem('activeLocations');
            if (!activeLocations) return JSON.stringify({error: 'No activeLocations'});
            
            try {
                const data = JSON.parse(activeLocations);
                return JSON.stringify({
                    locations: data.map(loc => ({
                        id: loc.id,
                        name: loc.name,
                        companyId: loc.companyId,
                        agencyId: loc.agencyId
                    }))
                });
            } catch (e) {
                return JSON.stringify({error: e.message, raw: activeLocations.substring(0, 200)});
            }
        })()
    """
    
    result = await evaluate_js(locations_script)
    if result:
        data = json.loads(result)
        print(json.dumps(data, indent=2))
        
        if 'locations' in data:
            around_summerlin = None
            for loc in data['locations']:
                if 'Around Summerlin' in loc.get('name', ''):
                    around_summerlin = loc
                    break
            
            if around_summerlin:
                print(f"\n2. Found 'Around Summerlin' location:")
                print(f"   ID: {around_summerlin['id']}")
                print(f"   Name: {around_summerlin['name']}")
                
                # Navigate to Around Summerlin dashboard
                target_url = f"https://app.gohighlevel.com/v2/location/{around_summerlin['id']}/dashboard"
                print(f"\n3. Navigating to: {target_url}")
                
                await navigate_to(target_url)
                
                # Wait for page to load
                print("4. Waiting for page to load...")
                await asyncio.sleep(5)
                
                print("5. Taking screenshot of Around Summerlin dashboard...")
                await take_screenshot("/Users/openclaw/.openclaw/agents/aroundsummerlin/workspace/ghl_around_summerlin_dashboard.png")
                
                # Verify we're on the right page
                verify_script = """
                    (function() {
                        return JSON.stringify({
                            url: window.location.href,
                            title: document.title
                        });
                    })()
                """
                result = await evaluate_js(verify_script)
                if result:
                    print(f"\n6. Verification:")
                    print(json.dumps(json.loads(result), indent=2))
            else:
                print("\n'Around Summerlin' not found in active locations")
                print("Available locations:")
                for loc in data['locations']:
                    print(f"  - {loc.get('name', 'Unknown')} ({loc.get('id', 'no-id')})")

if __name__ == "__main__":
    asyncio.run(main())
