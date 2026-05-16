import express from "express";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";
import puppeteer from "puppeteer";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distDir = path.join(__dirname, "dist");
const port = 41776;

const app = express();
app.use(express.static(distDir));

const screenshotDir = fs.mkdtempSync(path.join(os.tmpdir(), "orbit-slide-"));
console.log(`SCREENSHOT_DIR=${screenshotDir}`);

const server = app.listen(port, async () => {
  try {
    const browser = await puppeteer.launch({
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1600, height: 1400, deviceScaleFactor: 1 });
    await page.goto(`http://localhost:${port}`, { waitUntil: "networkidle2" });
    await page.waitForSelector("[data-slide-id]");
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const slideHandles = await page.$$("[data-slide-id]");
    console.log(`Found ${slideHandles.length} slides for screenshot capture.`);
    for (let i = 0; i < slideHandles.length; i += 1) {
      const handle = slideHandles[i];
      const box = await handle.boundingBox();
      if (!box) continue;
      const screenshotPath = path.join(
        screenshotDir,
        `slide-${String(i + 1).padStart(2, "0")}.png`,
      );
      await page.screenshot({
        path: screenshotPath,
        clip: box,
        omitBackground: false,
      });
      console.log(`Captured slide image: ${screenshotPath}`);
    }

    await browser.close();
  } catch (error) {
    console.error("Render failed:", error);
    process.exit(1);
  } finally {
    server.close();
  }
});
