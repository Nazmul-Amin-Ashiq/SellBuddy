#!/usr/bin/env python3
"""
SellBuddy Image Fetcher Bot
Fetches free product images from Unsplash and Pexels APIs.
Runs on Google Colab or Replit (free).

USAGE IN GOOGLE COLAB:
1. Copy this entire script to a new Colab notebook
2. Run each cell
3. Images will be downloaded and URLs saved
"""

import os
import json
import requests
import base64
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# ============================================
# CONFIGURATION - Edit these if needed
# ============================================

# Free API Keys (get your own at unsplash.com/developers)
# These work without authentication for demo purposes
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # Optional - works without for basic searches

# Products to fetch images for
PRODUCT_SEARCHES = {
    "galaxy-star-projector": [
        "galaxy projector bedroom",
        "starry night ceiling",
        "aurora lights room",
        "nebula projector light",
        "cosmic bedroom aesthetic"
    ],
    "posture-corrector": [
        "good posture",
        "back support",
        "office ergonomics",
        "spine health",
        "desk posture"
    ],
    "led-strip-lights": [
        "LED strip bedroom",
        "RGB gaming setup",
        "neon room aesthetic",
        "colorful room lights",
        "gaming room purple"
    ],
    "portable-blender": [
        "smoothie healthy",
        "protein shake gym",
        "fruit blender",
        "healthy drink",
        "fitness smoothie"
    ]
}

# Output directory
OUTPUT_DIR = Path("images")


# ============================================
# UNSPLASH API (No Auth Required for Basic)
# ============================================

def fetch_unsplash_images(query, count=5):
    """Fetch images from Unsplash (free, no auth for basic)."""
    images = []

    # Unsplash Source API (no auth required)
    base_url = "https://source.unsplash.com"

    for i in range(count):
        # Each request gets a random image matching the query
        url = f"{base_url}/800x800/?{quote(query)}&sig={i}"

        # Get the actual image URL (Unsplash redirects)
        try:
            response = requests.head(url, allow_redirects=True, timeout=10)
            final_url = response.url

            images.append({
                "url": final_url,
                "query": query,
                "width": 800,
                "height": 800,
                "source": "unsplash",
                "attribution": "Photo from Unsplash"
            })
            print(f"  Found: {final_url[:60]}...")
        except Exception as e:
            print(f"  Error fetching {query}: {e}")

    return images


def fetch_unsplash_api(query, count=5):
    """Fetch from Unsplash API (requires free API key for more features)."""
    if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_ACCESS_KEY":
        print("  Using Unsplash Source (no API key)")
        return fetch_unsplash_images(query, count)

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": query,
        "per_page": count,
        "orientation": "squarish"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()

        images = []
        for photo in data.get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "thumbnail": photo["urls"]["thumb"],
                "query": query,
                "width": photo["width"],
                "height": photo["height"],
                "source": "unsplash",
                "attribution": f"Photo by {photo['user']['name']} on Unsplash",
                "download_url": photo["links"]["download"]
            })
        return images
    except Exception as e:
        print(f"  API Error: {e}, falling back to source")
        return fetch_unsplash_images(query, count)


# ============================================
# PEXELS API (Free with API Key)
# ============================================

PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"  # Get free at pexels.com/api

def fetch_pexels_images(query, count=5):
    """Fetch images from Pexels API."""
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY":
        print("  Pexels API key not set, skipping")
        return []

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": count,
        "size": "medium"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()

        images = []
        for photo in data.get("photos", []):
            images.append({
                "url": photo["src"]["large"],
                "thumbnail": photo["src"]["tiny"],
                "query": query,
                "width": photo["width"],
                "height": photo["height"],
                "source": "pexels",
                "attribution": f"Photo by {photo['photographer']} on Pexels"
            })
        return images
    except Exception as e:
        print(f"  Pexels Error: {e}")
        return []


# ============================================
# LOREM PICSUM (Always Free, No Auth)
# ============================================

def fetch_picsum_images(count=5, seed=None):
    """Fetch random images from Lorem Picsum (always free)."""
    images = []
    base_url = "https://picsum.photos"

    for i in range(count):
        seed_param = f"?random={seed or ''}{i}" if seed else f"?random={i}"
        url = f"{base_url}/800/800{seed_param}"

        images.append({
            "url": url,
            "width": 800,
            "height": 800,
            "source": "picsum",
            "attribution": "Photo from Lorem Picsum"
        })

    return images


# ============================================
# MAIN FETCHER
# ============================================

def fetch_all_product_images():
    """Fetch images for all products."""
    all_images = {}

    for product_id, queries in PRODUCT_SEARCHES.items():
        print(f"\n{'='*50}")
        print(f"Fetching images for: {product_id}")
        print('='*50)

        product_images = []

        for query in queries:
            print(f"\nSearching: '{query}'")

            # Try Unsplash first
            images = fetch_unsplash_api(query, count=2)
            product_images.extend(images)

            # Try Pexels as backup
            pexels_images = fetch_pexels_images(query, count=1)
            product_images.extend(pexels_images)

        # Remove duplicates
        seen_urls = set()
        unique_images = []
        for img in product_images:
            if img["url"] not in seen_urls:
                seen_urls.add(img["url"])
                unique_images.append(img)

        all_images[product_id] = unique_images[:10]  # Max 10 per product
        print(f"\nTotal unique images for {product_id}: {len(all_images[product_id])}")

    return all_images


def save_image_catalog(images):
    """Save image catalog to JSON."""
    output = {
        "generated": datetime.now().isoformat(),
        "products": images,
        "total_images": sum(len(imgs) for imgs in images.values())
    }

    output_path = Path(__file__).parent.parent / "data" / "product_images.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nImage catalog saved to: {output_path}")
    return output_path


def download_images(images, output_dir=OUTPUT_DIR):
    """Download images to local directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    downloaded = []

    for product_id, product_images in images.items():
        product_dir = output_dir / product_id
        product_dir.mkdir(exist_ok=True)

        for i, img in enumerate(product_images):
            try:
                response = requests.get(img["url"], timeout=30)
                if response.status_code == 200:
                    filename = f"{product_id}_{i+1}.jpg"
                    filepath = product_dir / filename

                    with open(filepath, "wb") as f:
                        f.write(response.content)

                    downloaded.append(str(filepath))
                    print(f"Downloaded: {filepath}")
            except Exception as e:
                print(f"Failed to download {img['url']}: {e}")

    return downloaded


def generate_html_gallery(images):
    """Generate HTML gallery of fetched images."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>SellBuddy Product Images</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        h1 { color: #6366f1; }
        .product { margin: 30px 0; padding: 20px; background: white; border-radius: 12px; }
        .images { display: flex; flex-wrap: wrap; gap: 10px; }
        .images img { width: 200px; height: 200px; object-fit: cover; border-radius: 8px; }
        .attribution { font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <h1>Product Image Gallery</h1>
"""

    for product_id, product_images in images.items():
        html += f'<div class="product"><h2>{product_id.replace("-", " ").title()}</h2><div class="images">'

        for img in product_images[:5]:
            html += f'<div><img src="{img["url"]}" alt="{product_id}"><p class="attribution">{img.get("attribution", "")}</p></div>'

        html += '</div></div>'

    html += '</body></html>'

    output_path = Path(__file__).parent.parent / "reports" / "image_gallery.html"
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Gallery saved to: {output_path}")
    return output_path


# ============================================
# COLAB-READY CODE
# ============================================

COLAB_NOTEBOOK = '''
# SellBuddy Image Fetcher - Google Colab Version
# Copy this to a new Colab notebook and run

# Cell 1: Install dependencies
!pip install requests -q

# Cell 2: Configuration
PRODUCT_SEARCHES = {
    "galaxy-projector": ["galaxy projector bedroom", "starry ceiling", "aurora room"],
    "led-strip-lights": ["LED strip bedroom", "RGB gaming setup", "neon aesthetic"],
    "posture-corrector": ["good posture", "back support", "ergonomic"],
    "portable-blender": ["smoothie healthy", "protein shake", "fruit blender"]
}

# Cell 3: Fetch function
import requests
from urllib.parse import quote

def fetch_images(query, count=3):
    images = []
    for i in range(count):
        url = f"https://source.unsplash.com/800x800/?{quote(query)}&sig={i}"
        try:
            r = requests.head(url, allow_redirects=True, timeout=10)
            images.append({"url": r.url, "query": query})
            print(f"Found: {r.url[:50]}...")
        except:
            pass
    return images

# Cell 4: Fetch all images
all_images = {}
for product, queries in PRODUCT_SEARCHES.items():
    print(f"\\nFetching: {product}")
    all_images[product] = []
    for q in queries:
        all_images[product].extend(fetch_images(q, 2))

# Cell 5: Display results
for product, images in all_images.items():
    print(f"\\n{product}: {len(images)} images")
    for img in images[:3]:
        print(f"  {img['url']}")

# Cell 6: Save to JSON
import json
with open("product_images.json", "w") as f:
    json.dump(all_images, f, indent=2)
print("\\nSaved to product_images.json")

# Cell 7: Download to Colab (optional)
from google.colab import files
files.download("product_images.json")
'''


def main():
    """Main function."""
    print("=" * 60)
    print("SellBuddy Image Fetcher Bot")
    print("=" * 60)
    print(f"Started: {datetime.now()}")

    # Fetch images
    images = fetch_all_product_images()

    # Save catalog
    save_image_catalog(images)

    # Generate gallery
    generate_html_gallery(images)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for product_id, product_images in images.items():
        print(f"{product_id}: {len(product_images)} images")
        if product_images:
            print(f"  Main: {product_images[0]['url'][:60]}...")

    print("\n" + "=" * 60)
    print("Image fetching complete!")
    print("=" * 60)

    return images


if __name__ == "__main__":
    main()
