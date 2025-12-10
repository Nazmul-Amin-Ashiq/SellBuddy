/**
 * SellBuddy Product Catalog v2.0
 * Full SEO-optimized product listings with reviews, badges, and quick view
 */

const STORE_URL = 'https://nazmulaminashiq-coder.github.io/SellBuddy/store';

// Enhanced product catalog
const products = [
    {
        id: "galaxy-star-projector-pro",
        name: "Galaxy Star Projector Pro",
        category: "Smart Home",
        description: "Transform any room into a mesmerizing galaxy with 16 million colors, built-in Bluetooth speaker, and smart timer. The #1 TikTok viral product of 2025.",
        price: 34.99,
        originalPrice: 59.99,
        discount: 42,
        image: "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=600&h=600&fit=crop&q=80",
        rating: 4.8,
        reviews: 2847,
        badge: "BESTSELLER",
        features: ["16M colors", "Bluetooth speaker", "Timer", "Remote control"]
    },
    {
        id: "posture-corrector-pro",
        name: "Posture Corrector Pro",
        category: "Health & Wellness",
        description: "Fix your posture naturally with our doctor-recommended back brace. Invisible under clothes, comfortable for all-day wear.",
        price: 24.99,
        originalPrice: 44.99,
        discount: 44,
        image: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=600&fit=crop&q=80",
        rating: 4.7,
        reviews: 3421,
        badge: "TOP RATED",
        features: ["Invisible design", "Breathable mesh", "Adjustable", "Doctor recommended"]
    },
    {
        id: "led-strip-lights-smart",
        name: "Smart LED Strip Lights 65ft",
        category: "Smart Home",
        description: "65ft of stunning RGB LED lights with app control, music sync, and Alexa compatibility. Transform any room into an aesthetic paradise.",
        price: 29.99,
        originalPrice: 54.99,
        discount: 45,
        image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=600&fit=crop&q=80",
        rating: 4.6,
        reviews: 5234,
        badge: "VIRAL",
        features: ["65ft length", "Music sync", "App control", "Works with Alexa"]
    },
    {
        id: "portable-blender-usb",
        name: "Portable Blender USB-C",
        category: "Kitchen",
        description: "Fresh smoothies anywhere! USB-C rechargeable blender with 6 powerful blades. Perfect for gym, office, or travel.",
        price: 27.99,
        originalPrice: 49.99,
        discount: 44,
        image: "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=600&h=600&fit=crop&q=80",
        rating: 4.7,
        reviews: 4102,
        badge: "GYM ESSENTIAL",
        features: ["USB-C charging", "6 blades", "20oz capacity", "15+ blends/charge"]
    },
    {
        id: "no-pull-dog-harness",
        name: "No-Pull Dog Harness",
        category: "Pet Supplies",
        description: "Adjustable, breathable mesh harness with reflective straps for night walks. Stops pulling instantly.",
        price: 24.99,
        originalPrice: 44.99,
        discount: 44,
        image: "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600&h=600&fit=crop&q=80",
        rating: 4.8,
        reviews: 2156,
        badge: "PET FAVORITE",
        features: ["No-pull design", "Reflective", "Breathable", "All sizes"]
    },
    {
        id: "photo-projection-necklace",
        name: "Photo Projection Necklace",
        category: "Accessories",
        description: "Custom photo projection pendant. Upload your favorite photo and we'll create a magical memory you can wear.",
        price: 29.99,
        originalPrice: 54.99,
        discount: 45,
        image: "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=600&fit=crop&q=80",
        rating: 4.9,
        reviews: 1823,
        badge: "PERFECT GIFT",
        features: ["Custom photo", "Sterling silver", "Adjustable chain", "Gift box"]
    },
    {
        id: "sunset-projection-lamp",
        name: "Sunset Projection Lamp",
        category: "Smart Home",
        description: "Instagram-famous sunset lamp. Create stunning golden hour vibes any time of day. 180° rotation, USB powered.",
        price: 22.99,
        originalPrice: 39.99,
        discount: 43,
        image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=600&fit=crop&q=80",
        rating: 4.6,
        reviews: 3567,
        badge: "INSTAGRAM FAMOUS",
        features: ["180° rotation", "USB powered", "Multiple colors", "Perfect for photos"]
    },
    {
        id: "ice-roller-face",
        name: "Ice Roller Face Massager",
        category: "Beauty Tools",
        description: "Depuff and refresh your skin instantly with our ice roller. Reduces puffiness, tightens pores. TikTok skincare essential!",
        price: 14.99,
        originalPrice: 29.99,
        discount: 50,
        image: "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=600&fit=crop&q=80",
        rating: 4.7,
        reviews: 4521,
        badge: "50% OFF",
        features: ["Reduces puffiness", "Tightens pores", "Stainless steel", "Stays cold"]
    }
];

/**
 * Render star rating
 */
function renderStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalf = rating % 1 >= 0.5;
    let stars = '★'.repeat(fullStars);
    if (hasHalf) stars += '½';
    stars += '☆'.repeat(5 - fullStars - (hasHalf ? 1 : 0));
    return stars;
}

/**
 * Render products to the grid
 */
function renderProducts(productList) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;

    grid.innerHTML = productList.map(product => `
        <div class="product-card" data-product-id="${product.id}">
            ${product.badge ? `<span class="product-badge">${product.badge}</span>` : ''}
            <div class="product-image-wrapper">
                <img src="${product.image}" alt="${product.name}" class="product-image" loading="lazy"
                     onerror="this.src='https://via.placeholder.com/400x400?text=Product'">
            </div>
            <div class="product-info">
                <span class="product-category">${product.category}</span>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-rating">
                    <span class="stars">${renderStars(product.rating)}</span>
                    <span class="rating-text">${product.rating} (${product.reviews.toLocaleString()})</span>
                </div>
                <div class="product-price">
                    <span class="current-price">$${product.price.toFixed(2)}</span>
                    <span class="original-price">$${product.originalPrice.toFixed(2)}</span>
                    <span class="discount-badge">${product.discount}% OFF</span>
                </div>
                <button class="add-to-cart snipcart-add-item"
                    data-item-id="${product.id}"
                    data-item-name="${product.name}"
                    data-item-price="${product.price}"
                    data-item-url="${STORE_URL}/index.html"
                    data-item-description="${product.description}"
                    data-item-image="${product.image}">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="9" cy="21" r="1"></circle>
                        <circle cx="20" cy="21" r="1"></circle>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                    </svg>
                    Add to Cart
                </button>
            </div>
        </div>
    `).join('');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    renderProducts(products);
});
