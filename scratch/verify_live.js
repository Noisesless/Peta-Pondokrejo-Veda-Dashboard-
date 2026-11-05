const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function getChromePath() {
    const paths = [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Users\\ClasNet\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
    ];
    for (const p of paths) {
        if (fs.existsSync(p)) return p;
    }
    return null;
}

(async () => {
    const executablePath = await getChromePath();
    if (!executablePath) {
        console.log("Chrome executable not found for automated test.");
        process.exit(0);
    }

    const browser = await puppeteer.launch({
        executablePath,
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--ignore-certificate-errors']
    });

    const page = await browser.newPage();
    const networkErrors = [];
    const jsErrors = [];

    page.on('response', res => {
        if (res.status() === 403) {
            networkErrors.push(`HTTP 403 at: ${res.url()}`);
        }
    });

    page.on('pageerror', err => {
        jsErrors.push(`JS Error: ${err.message}`);
    });

    // 1. Test Main Page
    console.log("Navigating to https://peta.pondokrejo.id/...");
    await page.goto('https://peta.pondokrejo.id/', { waitUntil: 'networkidle2', timeout: 30000 });

    const mainBasemapBtn = await page.$('#btn-toggle-basemap');
    console.log("Main Page #btn-toggle-basemap found:", !!mainBasemapBtn);

    // Switch to Satelit on Main Page
    console.log("Switching to Satelit on main page...");
    await page.evaluate(() => {
        setBasemap('satelit');
    });
    await new Promise(r => setTimeout(r, 2500));

    const mainBoundaryVisible = await page.evaluate(() => {
        return {
            hasCasing: !!map.getLayer('layer-boundary-casing'),
            hasLine: !!map.getLayer('layer-boundary-line'),
            casingVis: map.getLayoutProperty('layer-boundary-casing', 'visibility') || 'visible'
        };
    });
    console.log("Main Page Boundary after Satelit switch:", mainBoundaryVisible);

    // 2. Test Editor Page
    console.log("\nNavigating to https://peta.pondokrejo.id/editor...");
    // Bypass auth guard by setting sessionStorage
    await page.evaluateOnNewDocument(() => {
        sessionStorage.setItem('isLoggedIn', 'true');
    });
    await page.goto('https://peta.pondokrejo.id/editor', { waitUntil: 'networkidle2', timeout: 30000 });

    const editorBasemapBtn = await page.$('#btn-toggle-basemap');
    console.log("Editor Page #btn-toggle-basemap found:", !!editorBasemapBtn);

    const isLeaflet = await page.evaluate(() => typeof window.L !== 'undefined');
    const isMapLibre = await page.evaluate(() => typeof window.maplibregl !== 'undefined');
    console.log("Editor uses Leaflet:", isLeaflet, "| uses MapLibre:", isMapLibre);

    // Switch to Terang on Editor Page
    console.log("Switching to Terang (positron) on editor page...");
    await page.evaluate(() => {
        setBasemap('positron');
    });
    await new Promise(r => setTimeout(r, 2500));

    const editorBoundaryVisible = await page.evaluate(() => {
        return {
            hasCasing: !!map.getLayer('layer-boundary-casing'),
            hasLine: !!map.getLayer('layer-boundary-line')
        };
    });
    console.log("Editor Page Boundary after Terang switch:", editorBoundaryVisible);

    console.log("\n--- Audit Summary ---");
    console.log("Network 403 errors encountered:", networkErrors.length);
    if (networkErrors.length > 0) console.log(networkErrors);
    console.log("JS Console errors:", jsErrors.length);
    if (jsErrors.length > 0) console.log(jsErrors);

    await browser.close();
    console.log("Verification finished successfully!");
})();

