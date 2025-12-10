#!/usr/bin/env python3
"""
SellBuddy Viral Marketing Bot
Generates viral social media content for TikTok, Instagram, Reddit, Twitter/X.
Creates complete post copy, captions, scripts, and scheduling.

ZERO COST - Uses free APIs and manual posting strategies.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============================================
# VIRAL CONTENT DATABASE (2025 Trends)
# ============================================

VIRAL_HOOKS_2025 = {
    "curiosity": [
        "Wait why is nobody talking about this...",
        "I'm actually shook rn",
        "This just changed everything for me",
        "You've been doing it wrong this whole time",
        "The thing nobody tells you about {product}",
        "I found the thing TikTok keeps deleting...",
        "This is why you're still struggling with {problem}",
        "3AM purchase but it actually slaps",
        "My therapist said get one of these",
    ],
    "pov": [
        "POV: You finally give in and buy the {product}",
        "POV: Your room after the {product} arrives",
        "POV: Me showing my friends what I impulse bought",
        "POV: It's 2AM and you just set up your new {product}",
        "POV: The {product} actually works",
        "POV: When the thing from TikTok is actually good",
    ],
    "listicle": [
        "Things that will change your life for under $40",
        "Products that live in my head rent free",
        "Purchases that actually improved my life",
        "Things I bought that weren't a waste of money",
        "My 'I don't need it but I need it' purchases",
        "Things every {demographic} needs",
        "Amazon finds that are actually worth it 2025",
        "Stuff that hits different when you're an adult",
    ],
    "transformation": [
        "Room before vs after the {product}",
        "The glow up my room needed",
        "Turning my room into an aesthetic paradise",
        "How I transformed my space for under $50",
        "Small changes that made my room go viral",
    ],
    "storytelling": [
        "I was today years old when I found out about this",
        "So my friend recommended this and...",
        "Story time: Why I'll never go back",
        "The purchase that broke my TikTok algorithm",
        "How this $30 purchase changed my life (not clickbait)",
    ],
    "question": [
        "Why did no one tell me this existed?",
        "Am I the only one who didn't know about this?",
        "How is this not more popular?",
        "Where has this been all my life?",
    ],
    "relatable": [
        "When you finally buy the thing everyone's been talking about",
        "Me pretending I didn't just spend money on TikTok finds",
        "Things that make no sense but you need anyway",
        "My 'treat yourself' is getting out of hand",
    ]
}

TRENDING_SOUNDS_2025 = [
    "original sound - aestheticallypleasing",
    "Aesthetic - Tollan Kim",
    "Dissolve - Absofacto",
    "Snowfall - Øneheart & reidenshi",
    "Cupid - Twin Ver. - FIFTY FIFTY",
    "original sound - cozyvibes",
    "Sweater Weather - The Neighbourhood",
    "after hours - tiktok version",
    "original sound - room transformation",
]

HASHTAGS_BY_NICHE = {
    "galaxy-projector": [
        "#galaxyprojector", "#roomdecor", "#aestheticroom", "#roommakeover",
        "#bedroomdecor", "#ledlights", "#starlight", "#cozybedroom",
        "#roomtour", "#amazonfinds", "#tiktokfinds", "#roominspo",
        "#auroraprojector", "#nightlight", "#fyp", "#viral"
    ],
    "led-lights": [
        "#ledlights", "#roomsetup", "#gamingsetup", "#rgblights",
        "#neonlights", "#roomaesthetic", "#ledstrip", "#desksetup",
        "#gamerroom", "#pcsetup", "#twitchstreamer", "#contentcreator",
        "#roomdecor", "#fyp", "#viral"
    ],
    "posture-corrector": [
        "#posturecorrector", "#backpain", "#officelife", "#wfh",
        "#workfromhome", "#healthtok", "#wellnesstok", "#selfcare",
        "#deskjob", "#painrelief", "#healthylifestyle", "#ergonomic",
        "#fyp", "#viral"
    ],
    "portable-blender": [
        "#portableblender", "#smoothie", "#fitnesstok", "#gymtok",
        "#proteinshake", "#healthylifestyle", "#mealprep", "#fitness",
        "#gym", "#workout", "#healthyfood", "#amazonfinds",
        "#fyp", "#viral"
    ]
}

DEMOGRAPHICS = {
    "galaxy-projector": ["girl", "guy", "college student", "parent", "gamer"],
    "led-lights": ["gamer", "streamer", "content creator", "guy", "girl"],
    "posture-corrector": ["office worker", "remote worker", "student", "adult"],
    "portable-blender": ["gym bro", "fitness girl", "health enthusiast", "busy person"]
}


# ============================================
# CONTENT GENERATORS
# ============================================

def generate_tiktok_script(product_id, product_name, key_feature, price):
    """Generate a complete TikTok video script."""

    hook_category = random.choice(list(VIRAL_HOOKS_2025.keys()))
    hook = random.choice(VIRAL_HOOKS_2025[hook_category])
    hook = hook.replace("{product}", product_name).replace("{problem}", "this")
    demographic = random.choice(DEMOGRAPHICS.get(product_id, ["person"]))
    hook = hook.replace("{demographic}", demographic)

    sound = random.choice(TRENDING_SOUNDS_2025)

    script = f"""
{'='*60}
TIKTOK VIDEO SCRIPT - {product_name.upper()}
{'='*60}

HOOK TYPE: {hook_category.title()}
SUGGESTED SOUND: {sound}
DURATION: 15-30 seconds

---

📱 SCREEN TEXT (0-3 sec):
"{hook}"

🎬 SHOT 1 - THE HOOK (0-3 sec):
[Close-up of product in packaging OR dramatic reveal]
- Keep it mysterious
- Dark/aesthetic lighting
- Quick zoom effect

🎬 SHOT 2 - THE PROBLEM (3-7 sec):
[Show the "before" or pain point]
TEXT: "I was struggling with..."
- If projector: boring plain room
- If posture: hunched at desk
- If blender: chunky protein shake

🎬 SHOT 3 - THE REVEAL (7-15 sec):
[Unbox or turn on product]
TEXT: "Until I found this..."
- Satisfying unboxing sounds
- Slow-mo of product in action
- {key_feature}

🎬 SHOT 4 - THE RESULT (15-22 sec):
[Show transformation/reaction]
TEXT: "Now look at this..."
- Aesthetic final shot
- Your genuine reaction
- Show it in use

🎬 SHOT 5 - CTA (22-30 sec):
[Point to product or screen]
TEXT: "Only ${price} - Link in bio"
- Direct eye contact
- Clear call to action

---

CAPTION:
{generate_caption(product_id, product_name, hook_category)}

HASHTAGS:
{' '.join(HASHTAGS_BY_NICHE.get(product_id, ['#fyp', '#viral'])[:10])}

---

POSTING TIPS:
- Best times: 7-9 PM, 11 AM-1 PM (your audience's timezone)
- Reply to comments in first hour
- Pin a comment with "Link in bio!"
- Duet/stitch trending videos about the product

"""
    return script


def generate_caption(product_id, product_name, style="curiosity"):
    """Generate viral caption."""

    templates = {
        "curiosity": f"I finally caved and got the {product_name} everyone's been talking about... and wow 🤯\n\nLink in bio to get yours!",
        "pov": f"POV: The {product_name} just arrived and you're about to transform your whole vibe ✨\n\n(link in bio)",
        "listicle": f"Things I didn't know I needed until I got them:\n1. This {product_name}\n2. That's it. That's the list.\n\nLink in bio 🛒",
        "transformation": f"My room literally went from 0 to 100 with this {product_name} 😭✨\n\nYou NEED this - link in bio!",
        "storytelling": f"Story time: I bought this {product_name} at 3AM and it's the best decision I've ever made 💀\n\nGrab yours 👆",
        "question": f"Why did NO ONE tell me about this {product_name}?? 😩\n\nI could've had this aesthetic SO much sooner\n\nLink. In. Bio.",
        "relatable": f"Me: I need to stop buying things from TikTok\nAlso me: *adds {product_name} to cart*\n\n(it was worth it tho)\nLink in bio 🛍️"
    }

    return templates.get(style, templates["curiosity"])


def generate_instagram_content(product_id, product_name, features):
    """Generate Instagram Reel caption and story content."""

    content = f"""
{'='*60}
INSTAGRAM CONTENT - {product_name.upper()}
{'='*60}

📸 REEL CAPTION:
---
✨ The {product_name} is giving everything I needed and more ✨

Here's why this is my new favorite purchase:
{''.join([f'{chr(10)}▪️ {f}' for f in features[:4]])}

Would you try this? Drop a 🌟 if you want the link!

.
.
.
{' '.join(HASHTAGS_BY_NICHE.get(product_id, ['#aestheticroom', '#roomdecor', '#amazonfinds'])[:15])}
---

📱 STORY SEQUENCE (5 slides):

SLIDE 1: Poll
"Have you seen this {product_name} on TikTok?"
[Yes / Not yet]

SLIDE 2: Product Shot
[Aesthetic photo of product]
"Finally got mine 😍"

SLIDE 3: In Action
[Video/boomerang of product working]
"It's even better IRL"

SLIDE 4: Link Sticker
[Product photo with link]
"Link to shop 👆"

SLIDE 5: Question Box
"What should I get next?"
[Question sticker]

---

📌 CAROUSEL POST IDEA:
Slide 1: "5 Things That Changed My Room"
Slide 2: The {product_name} (main shot)
Slide 3: Before vs After
Slide 4: Features breakdown
Slide 5: "Link in bio to shop!"

"""
    return content


def generate_reddit_posts(product_id, product_name):
    """Generate Reddit-appropriate posts (non-spammy, value-first)."""

    subreddits = {
        "galaxy-projector": ["r/CozyPlaces", "r/malelivingspace", "r/AmateurRoomPorn", "r/battlestations", "r/HomeDecorating"],
        "led-lights": ["r/battlestations", "r/pcmasterrace", "r/malelivingspace", "r/Twitch", "r/AverageBattlestations"],
        "posture-corrector": ["r/posture", "r/backpain", "r/WorkOnline", "r/remotework", "r/Ergonomics"],
        "portable-blender": ["r/fitness", "r/MealPrepSunday", "r/EatCheapAndHealthy", "r/gainit", "r/xxfitness"]
    }

    posts = f"""
{'='*60}
REDDIT STRATEGY - {product_name.upper()}
{'='*60}

🎯 TARGET SUBREDDITS:
{chr(10).join(subreddits.get(product_id, ['r/BuyItForLife']))}

---

📝 POST TYPE 1: Room/Setup Showcase
---
Title: "Finally upgraded my setup, pretty happy with how it turned out"
or: "6 months of slowly improving my room, here's where I'm at"

[Post a photo of your room/setup featuring the product]

Body: Share the journey, mention what you changed, let people ask about specific items. When someone asks about the {product_name}, THEN share where you got it.

Key: Never make it about selling. Make it about sharing your space.

---

📝 POST TYPE 2: Advice Request
---
Title: "What small purchases actually improved your daily life?"
or: "Looking for recommendations - what's actually worth buying?"

Body: Ask genuinely. Engage with responses. Eventually mention what worked for you.

---

📝 POST TYPE 3: Review Post
---
Title: "[Review] I've been using X for 3 months - here's my honest take"

Body:
"I bought this after seeing it everywhere online. Here's my unfiltered review after actually using it daily...

Pros:
- [genuine benefit]
- [genuine benefit]
- [genuine benefit]

Cons:
- [be honest about any issues]
- [shipping time if applicable]

Overall: [honest rating]/10

Happy to answer questions if anyone's considering it."

---

⚠️ REDDIT RULES:
- Never direct link to your store (instant ban)
- Build karma first by being helpful
- 90% value, 10% subtle mention
- Use aged accounts if possible
- Read each subreddit's rules first

"""
    return posts


def generate_twitter_x_thread(product_id, product_name, features, price):
    """Generate Twitter/X thread content."""

    thread = f"""
{'='*60}
TWITTER/X THREAD - {product_name.upper()}
{'='*60}

🧵 THREAD FORMAT:

TWEET 1 (HOOK):
"I spent ${price} on something I saw on TikTok and I need to talk about it

A thread 🧵"

---

TWEET 2:
"So I kept seeing this {product_name} everywhere

At first I thought it was just another overhyped product

But after a month of seeing it... I caved"

---

TWEET 3:
"Here's what I was expecting:
- Cheap quality
- Not as good as videos
- Buyer's remorse

Here's what I got:"

---

TWEET 4:
"The {features[0] if features else 'quality'} is actually insane

Like I genuinely didn't expect it to be THIS good for the price"

[Attach photo/video]

---

TWEET 5:
"My favorite part? {features[1] if len(features) > 1 else 'How easy it is to use'}

This alone made it worth it for me"

---

TWEET 6:
"The only con I can think of:
- Shipping took about 2 weeks
- That's literally it

---

TWEET 7:
"Would I recommend it?

Absolutely.

If you've been on the fence, this is your sign.

Link if anyone wants it: [bio link]"

---

TWEET 8:
"Drop a 🔥 if you want me to share more finds like this

I've been testing a bunch of these viral products lately"

---

📊 BEST POSTING TIMES FOR TWITTER:
- 8-10 AM (morning scroll)
- 12-1 PM (lunch break)
- 5-6 PM (commute)
- 8-10 PM (evening wind-down)

"""
    return thread


def generate_weekly_content_calendar():
    """Generate a complete weekly content calendar."""

    products = [
        {"id": "galaxy-projector", "name": "Galaxy Star Projector"},
        {"id": "led-lights", "name": "LED Strip Lights"},
        {"id": "posture-corrector", "name": "Posture Corrector"},
        {"id": "portable-blender", "name": "Portable Blender"}
    ]

    today = datetime.now()
    calendar = []

    content_types = [
        {"type": "TikTok Video", "platform": "TikTok", "time": "7:00 PM"},
        {"type": "Instagram Reel", "platform": "Instagram", "time": "8:00 PM"},
        {"type": "TikTok Video", "platform": "TikTok", "time": "12:00 PM"},
        {"type": "Twitter Thread", "platform": "Twitter/X", "time": "10:00 AM"},
        {"type": "Instagram Story", "platform": "Instagram", "time": "9:00 PM"},
        {"type": "TikTok Video", "platform": "TikTok", "time": "6:00 PM"},
        {"type": "Reddit Post", "platform": "Reddit", "time": "11:00 AM"},
    ]

    for i in range(14):  # 2 weeks
        day = today + timedelta(days=i)
        content = content_types[i % len(content_types)]
        product = products[i % len(products)]

        calendar.append({
            "date": day.strftime("%A, %B %d"),
            "day_num": i + 1,
            "platform": content["platform"],
            "content_type": content["type"],
            "posting_time": content["time"],
            "product": product["name"],
            "product_id": product["id"],
            "status": "Scheduled"
        })

    return calendar


# ============================================
# MAIN OUTPUT
# ============================================

def main():
    """Generate all marketing content."""
    print("=" * 60)
    print("SellBuddy Viral Marketing Bot")
    print("=" * 60)
    print(f"Generated: {datetime.now()}")

    # Products to generate content for
    products = [
        {
            "id": "galaxy-projector",
            "name": "Galaxy Star Projector",
            "key_feature": "16 million colors + Bluetooth speaker",
            "features": ["16 million LED colors", "Built-in Bluetooth speaker", "Timer function", "Remote control"],
            "price": 34.99
        },
        {
            "id": "led-lights",
            "name": "Smart LED Strip Lights",
            "key_feature": "65ft with music sync",
            "features": ["65ft total length", "Music sync", "App control", "Works with Alexa"],
            "price": 29.99
        }
    ]

    output_dir = Path(__file__).parent.parent / "content"
    output_dir.mkdir(exist_ok=True)

    all_content = {}

    for product in products:
        print(f"\n{'='*50}")
        print(f"Generating content for: {product['name']}")
        print('='*50)

        content = {
            "product": product,
            "tiktok_script": generate_tiktok_script(
                product["id"], product["name"], product["key_feature"], product["price"]
            ),
            "instagram": generate_instagram_content(
                product["id"], product["name"], product["features"]
            ),
            "reddit": generate_reddit_posts(product["id"], product["name"]),
            "twitter": generate_twitter_x_thread(
                product["id"], product["name"], product["features"], product["price"]
            )
        }

        all_content[product["id"]] = content

        # Save individual product content
        product_file = output_dir / f"{product['id']}_content.txt"
        with open(product_file, "w", encoding="utf-8") as f:
            f.write(content["tiktok_script"])
            f.write("\n\n")
            f.write(content["instagram"])
            f.write("\n\n")
            f.write(content["reddit"])
            f.write("\n\n")
            f.write(content["twitter"])

        print(f"Saved: {product_file}")

    # Generate content calendar
    print("\n" + "="*50)
    print("Generating 2-week content calendar...")
    calendar = generate_weekly_content_calendar()

    calendar_text = "SELLBUDDY 2-WEEK CONTENT CALENDAR\n" + "="*50 + "\n\n"
    for day in calendar:
        calendar_text += f"""
Day {day['day_num']} - {day['date']}
Platform: {day['platform']}
Content: {day['content_type']}
Time: {day['posting_time']}
Product: {day['product']}
Status: {day['status']}
---
"""

    calendar_file = output_dir / "content_calendar.txt"
    with open(calendar_file, "w", encoding="utf-8") as f:
        f.write(calendar_text)

    print(f"Saved: {calendar_file}")

    # Save JSON version
    json_file = output_dir / "marketing_content.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "calendar": calendar,
            "products": [p["id"] for p in products]
        }, f, indent=2)

    print(f"Saved: {json_file}")

    # Print sample content
    print("\n" + "="*60)
    print("SAMPLE TIKTOK SCRIPT (Galaxy Projector):")
    print("="*60)
    print(all_content["galaxy-projector"]["tiktok_script"][:1500])

    print("\n" + "="*60)
    print("Content generation complete!")
    print(f"All files saved to: {output_dir}")
    print("="*60)


if __name__ == "__main__":
    main()
