import asyncio
from playwright.async_api import async_playwright

def sp(msg):
    try:
        print(str(msg).encode('ascii', 'ignore').decode('ascii'), flush=True)
    except Exception:
        pass

async def debug_meta_ad_links():
    sp("====================================================================")
    sp(" [DEBUGGING EXACT META AD LIBRARY URL ANCHORS & DOM LINKS]")
    sp("====================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="es-CL"
        )
        page = await context.new_page()

        url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=CL&is_targeted_country=false&media_type=all&q=parcelas&search_type=keyword_unordered"
        sp(f"\n[1] Navigating to: {url}")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)

        # Scroll down to load ad cards
        await page.mouse.wheel(0, 2000)
        await asyncio.sleep(3)

        # Extract all <a> hrefs and buttons in the ad cards
        links = await page.evaluate('''() => {
            const anchors = Array.from(document.querySelectorAll('a'));
            return anchors.map(a => ({
                text: a.innerText.trim(),
                href: a.href
            })).filter(item => item.href.includes('ads/library') || item.href.includes('facebook.com') || item.href.includes('id='));
        }''')

        sp(f"\n[2] Found {len(links)} ad-related anchor links in the page:")
        for idx, l in enumerate(links[:20], 1):
            sp(f"  #{idx} [{l['text']}] -> {l['href']}")

        # Extract view_all_page_id links
        page_ids = await page.evaluate('''() => {
            const html = document.body.innerHTML;
            const matches = html.match(/view_all_page_id=(\\d+)/g) || [];
            return Array.from(new Set(matches));
        }''')
        sp(f"\n[3] Found View All Page ID links: {page_ids[:10]}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_meta_ad_links())
