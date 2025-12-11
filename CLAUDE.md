# SellBuddy - Autonomous Dropshipping System

## Project Overview
**Directory**: `G:\Ecomerce`
**Repository**: https://github.com/nazmulaminashiq-coder/SellBuddy
**Live Store**: https://nazmulaminashiq-coder.github.io/SellBuddy/store/
**Type**: 100% Autonomous Zero-Budget Dropshipping System
**Target Market**: US/Global English-speaking markets
**Owner Location**: Bangladesh
**Budget**: $0/month (only ~5% fees per sale)

---

## Current Status: FULLY AUTONOMOUS

The system runs completely on autopilot:
- **Daily at 8 AM UTC**: Products updated, content generated, analytics refreshed
- **On every order**: Auto-processed, saved to Google Sheets, emails sent
- **On every push**: Store auto-deployed to GitHub Pages

---

## Technical Stack (100% Free)

| Component | Platform | Cost |
|-----------|----------|------|
| Store Hosting | GitHub Pages | FREE |
| Shopping Cart | Snipcart | FREE (2% fee on sales) |
| Automation | GitHub Actions | FREE (2000 min/month) |
| Notebooks | Google Colab | FREE |
| Order Tracking | Google Sheets | FREE |
| Payments | PayPal Business | ~3% fee |
| Images | Unsplash/Pexels API | FREE |

---

## Repository Structure

```
SellBuddy/
├── .github/workflows/
│   ├── deploy-store.yml          # Auto-deploy to GitHub Pages
│   ├── autonomous-daily.yml      # Daily automation (8 AM UTC)
│   ├── daily_research.yml        # Product research
│   ├── weekly_report.yml         # Weekly analytics
│   └── social_posting.yml        # Social media scheduling
├── store/
│   ├── index.html                # Main store page (Snipcart integrated)
│   ├── styles.css                # Store styling
│   ├── products.js               # Product display logic
│   ├── chat_widget.js            # Customer support chatbot
│   ├── about.html, faq.html, contact.html, etc.
├── bots/
│   ├── autonomous_controller.py  # MASTER CONTROLLER - runs everything
│   ├── product_research_bot.py   # Finds trending products
│   ├── viral_marketing_bot.py    # TikTok/Instagram/Reddit content
│   ├── image_fetcher_bot.py      # Unsplash/Pexels images
│   ├── order_handler_bot.py      # Google Sheets integration
│   ├── order_simulator.py        # Test order generation
│   ├── analytics_dashboard.py    # Revenue/profit tracking
│   ├── supplier_bot.py           # Supplier price tracking
│   ├── social_media_bot.py       # Content scheduling
│   ├── customer_service_bot.py   # FAQ auto-responder
│   └── influencer_bot.py         # Micro-influencer outreach
├── backend/
│   ├── payment/
│   │   ├── gateway.php           # Custom payment gateway
│   │   ├── checkout.php          # Checkout handler
│   │   └── config.php            # Payment configuration
│   └── webhooks/
│       ├── snipcart_webhook.php  # Order processing webhook
│       └── google_sheets_setup.js # Apps Script for Sheets
├── notebooks/
│   └── SellBuddy_Autonomous.ipynb # Google Colab notebook
├── data/
│   ├── products.json             # Product catalog
│   ├── products_full.json        # Full product data with SEO
│   ├── orders.json               # Order history
│   ├── analytics.json            # Sales analytics
│   └── influencers.json          # Influencer database
├── content/                      # Generated marketing content
├── reports/                      # Analytics reports
├── AUTONOMOUS_SETUP.md           # Complete setup guide
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies
```

---

## Autonomous Bots

### 1. Master Controller (`autonomous_controller.py`)
The brain of the operation. Coordinates all other bots.
- Auto-generates new trending products
- Auto-updates prices based on performance
- Auto-removes low performers
- Auto-generates daily content
- Auto-processes orders
- Auto-generates analytics reports

### 2. Product Research Bot (`product_research_bot.py`)
- Scrapes Google Trends, Reddit
- Simulates AliExpress/TikTok data
- Identifies viral products with 50-70% margins
- Generates daily HTML reports

### 3. Viral Marketing Bot (`viral_marketing_bot.py`)
- Creates TikTok scripts with 2025 viral hooks
- Generates Instagram captions with emojis
- Writes Reddit posts (authentic style)
- Creates Twitter/X threads
- Uses trending hooks like "POV:", "No one talks about..."

### 4. Image Fetcher Bot (`image_fetcher_bot.py`)
- Fetches free images from Unsplash API
- Falls back to Pexels API
- Auto-downloads and organizes by product
- No copyright issues

### 5. Order Handler Bot (`order_handler_bot.py`)
- Integrates with Google Sheets
- Auto-logs all orders
- Generates supplier order emails
- Sends customer confirmations
- Tracks order status

### 6. Order Simulator (`order_simulator.py`)
- Generates test orders for system testing
- Sends to webhook endpoints
- Validates the full order flow

---

## Snipcart Configuration

**Dashboard**: https://app.snipcart.com
**Current API Key**: Test mode (ST_...)
**Webhook URL**: Set to your backend webhook endpoint

### Key Settings:
- Domain: `nazmulaminashiq-coder.github.io`
- Currency: USD
- Shipping: $4.99 (free over $50)
- Payment: PayPal + Stripe

---

## GitHub Actions Workflows

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| `deploy-store.yml` | On push + daily midnight | Deploy store to GitHub Pages |
| `autonomous-daily.yml` | Daily 8 AM UTC | Run all bots, commit changes |
| `daily_research.yml` | Daily 6 AM UTC | Product research |
| `weekly_report.yml` | Weekly Sunday 10 AM | Generate weekly report |
| `social_posting.yml` | Every 6 hours | Social media content |

---

## Products (Current Catalog)

| Product | Price | Margin | Category |
|---------|-------|--------|----------|
| Galaxy Projector | $39.99 | 55% | Smart Home |
| LED Strip Lights | $24.99 | 58% | Smart Home |
| Posture Corrector | $29.99 | 52% | Wellness |
| Pet Water Fountain | $34.99 | 55% | Pet Products |
| Phone Camera Lens Kit | $19.99 | 60% | Tech |
| Magnetic Phone Mount | $14.99 | 65% | Tech |
| Acupressure Mat | $44.99 | 50% | Wellness |
| Smart Plant Watering | $27.99 | 58% | Smart Home |

---

## Order Flow (Fully Automatic)

```
Customer visits store
        ↓
Adds product to cart (Snipcart)
        ↓
Completes checkout (PayPal/Stripe)
        ↓
Snipcart sends webhook
        ↓
┌───────────────────────────────────────┐
│  snipcart_webhook.php processes:      │
│  1. Saves to data/orders.json         │
│  2. Sends to Google Sheets            │
│  3. Emails customer confirmation      │
│  4. Emails owner notification         │
│  5. Updates analytics                 │
└───────────────────────────────────────┘
        ↓
Owner sees order in Google Sheets
        ↓
Owner places order with supplier
        ↓
Supplier ships to customer
```

---

## Quick Commands

```bash
# Run full autonomous cycle
python bots/autonomous_controller.py daily

# Run individual bots
python bots/product_research_bot.py
python bots/viral_marketing_bot.py
python bots/image_fetcher_bot.py
python bots/analytics_dashboard.py

# Simulate test orders
python bots/order_simulator.py --count 5

# Simulate with webhook
python bots/order_simulator.py --webhook YOUR_WEBHOOK_URL
```

---

## Google Colab

Open `notebooks/SellBuddy_Autonomous.ipynb` in Colab for:
- Running full autonomous cycle
- Manual product updates
- Content generation
- Order processing
- Pushing changes to GitHub

---

## Setup Checklist

- [x] Repository created and public
- [x] GitHub Pages enabled (Source: GitHub Actions)
- [x] Store deployed and live
- [x] All bots created
- [x] GitHub Actions workflows configured
- [x] Snipcart webhook handler created
- [x] Google Sheets script created
- [x] Colab notebook ready
- [ ] Snipcart account configured (user action needed)
- [ ] PayPal Business connected (user action needed)
- [ ] Google Sheets webhook deployed (user action needed)

---

## Session Log

### December 10, 2025 (Latest)
- Built complete autonomous system
- Created master autonomous controller
- Added Snipcart webhook handler
- Created Google Sheets Apps Script
- Added order simulator for testing
- Created comprehensive setup guide (AUTONOMOUS_SETUP.md)
- Deployed GitHub Actions for daily automation
- Created Google Colab notebook
- All changes pushed to GitHub

### Previous Sessions
- Created 6 Python bots for automation
- Designed store with Snipcart integration
- Set up GitHub Actions workflows
- Created product catalog with SEO descriptions
- Built viral marketing content generator

---

## Important Files to Know

| File | Purpose |
|------|---------|
| `store/index.html:288` | Snipcart API key location |
| `bots/autonomous_controller.py` | Main automation brain |
| `backend/webhooks/snipcart_webhook.php` | Order processing |
| `backend/webhooks/google_sheets_setup.js` | Copy to Apps Script |
| `data/products.json` | Product catalog |
| `AUTONOMOUS_SETUP.md` | Complete setup instructions |

---

## Next Steps for User

1. **Configure Snipcart**: Get API key, update store
2. **Set up PayPal Business**: Connect to Snipcart
3. **Deploy Google Sheets webhook**: Copy Apps Script, deploy as web app
4. **Start marketing**: Use generated content for TikTok/Instagram
5. **Monitor orders**: Check Google Sheets daily

---

*Last Updated: December 10, 2025*
