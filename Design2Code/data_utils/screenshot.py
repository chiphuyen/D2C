from playwright.sync_api import sync_playwright
import os
from tqdm import tqdm
from PIL import Image

def take_screenshot(url, output_file="screenshot.png", do_it_again=False):
    # Convert local path to file:// URL if it's a file
    if os.path.exists(url):
        url = "file://" + os.path.abspath(url)

    # whether to overwrite existing screenshots
    if os.path.exists(output_file) and not do_it_again:
        print(f"{output_file} exists!")
        return

    try:
        with sync_playwright() as p:
            # Choose a browser, e.g., Chromium, Firefox, or WebKit
            browser = p.chromium.launch()
            page = browser.new_page()

            # Navigate to the URL
            page.goto(url, timeout=60000)

            # Take the screenshot
            page.screenshot(path=output_file, full_page=True, animations="disabled", timeout=60000)

            browser.close()
    except Exception as e: 
        print(f"Failed to take screenshot due to: {e}. Generating a blank image.")
        # Generate a blank image 
        img = Image.new('RGB', (1280, 960), color = 'white')
        img.save(output_file)


if __name__ == "__main__":
    workspace = '/Users/chip/dev/anyscale'
    partition = 'train-00000-of-00738-80a58552f2fb3344-small'
    outdir = f'{workspace}/{partition}'
    imgdir = f'{outdir}/image'
    os.makedirs(imgdir, exist_ok=True)
    fnames = [f for f in os.listdir(outdir) if f.endswith('html') and os.path.isfile(os.path.join(outdir, f))]
    for fname in tqdm(fnames):
        take_screenshot(os.path.join(outdir, fname), os.path.join(imgdir, fname.replace(".html", ".png")))
