# JASHVIORA — Beauty, Fashion & Lifestyle Discovery Website

> **"Discover Your Style, Create Your World."**

Welcome to **JASHVIORA**, a complete, premium, elegant, and fully functional curated lifestyle shopping platform. Visitors discover handpicked products, explore inspiration across beauty, traditional & modern fashion, minimal jewellery, and warm home decor, and click buttons to visit verified external shopping platforms (Amazon India, Nykaa, Myntra, Flipkart, Meesho).

---

## 🌸 Brand Identity & Aesthetic Design

- **Brand Name**: JASHVIORA
- **Brand Personality**: Feminine, Elegant, Minimal, Modern, Classy, Aesthetic, Premium
- **Colour Palette**:
  - **Cream**: `#FFF9F2` (Base background)
  - **Beige**: `#E9DCCF` (Borders & accents)
  - **Blush Pink**: `#EBCFD0` (Pills, badges & highlights)
  - **Dark Brown**: `#49372F` (Headings, primary buttons & footer)
  - **White**: `#FFFFFF` (Card surfaces)
  - **Gold Accent**: `#C5A059` (Editorial stars & flourishes)
- **Typography**:
  - Headings: Editorial luxury serifs (`Playfair Display` & `Cormorant Garamond`)
  - Body & UI: Clean, modern sans-serif (`Plus Jakarta Sans`)
- **Logo Mark**: Refined botanical floral lotus emblem (`public/assets/logo-icon.svg`) paired with uppercase letter-spaced branding.

---

## ✨ Key Features & Sections

### 1. Sticky Luxury Glass Header
- Brand logo with floral emblem.
- Smooth navigation links: **Home**, **Beauty**, **Fashion**, **Jewellery**, **Home Decor**, **How It Works**, **Inspiration**, **About Us**, **Contact**.
- **Live Search Modal**: Search products instantly by title, description, category, or store with popular keyword chips.
- **Saved Wishlist Drawer**: Persistent bookmarking with counter badge and direct 1-click external checkout.
- **Product Management Button**: Switch instantly to the Curator Studio / Admin Dashboard.
- **Mobile Responsive Drawer**: Smooth slide-down menu for phones and tablets.

### 2. Editorial Magazine Hero Section
- High-aesthetic lifestyle photograph with warm sunlight and shadows.
- Editorial volume tag: `VOLUME I • EDITORIAL CURATION • 2026`.
- Headline: *"YOUR WORLD OF BEAUTY & STYLE"*.
- Subheading: *"Find inspiration for your beauty, wardrobe and beautiful home."*.
- Action buttons: **Explore Collections** & **Discover More**.
- Verified retailer reassurance badges (Amazon India, Nykaa, Myntra, Flipkart, Meesho).

### 3. Explore Our Collections (4 Large Image Cards)
Cropped directly from the brand's visual design references:
1. **BEAUTY & MAKEUP**: Luxe skincare, lip pigments, velvety textures & vanity rituals (`public/assets/collections/beauty.jpg`).
2. **FASHION & DRESSES**: Handcrafted Indian suits, festive lehengas & modern silhouettes (`public/assets/collections/fashion.jpg`).
3. **JEWELLERY**: Minimal 18k gold vermeil, sculptural hoops & timeless chains (`public/assets/collections/jewellery.jpg`).
4. **HOME DECOR**: Warm beige aesthetics, sculptural ceramics, candles & cozy nooks (`public/assets/collections/home-decor.jpg`).
- Clicking **Explore [Category]** automatically filters the curated catalog and smooth-scrolls.

### 4. Trending Finds (Curated Shopping Section)
- **Filter Tabs**: All, Beauty & Makeup, Fashion & Dresses, Jewellery, Home Decor.
- **Store Badges**: Filter by Amazon India, Nykaa, Myntra, Flipkart, Meesho.
- **Sort Options**: Trending, Price (Low to High), Price (High to Low), Top Rated.
- **Each Product Card Contains**:
  - Realistic, high-resolution aesthetic photography with image hover scale and fallback protection.
  - Category pill & Branded Store Badge (custom colors matching Nykaa pink, Myntra red, Amazon dark, Flipkart blue, Meesho plum).
  - Product title & curated editorial description.
  - Price in ₹ INR with optional crossed-out retail price.
  - **"Shop Now ↗"** button: Opens the genuine external product URL in a new tab with `target="_blank" rel="noopener noreferrer"`.
  - Reassurance indication: *"Redirects safely to original store: [Store Name]"*.
  - **Quick View Modal**: Deep-dive popup with high-res zoom, star ratings, and direct checkout link.
  - **Heart Icon**: Save to favorite wishlist.

### 5. How JASHVIORA Works (Visual 3-Step Flow)
Visual diagram displaying the clear flow:
$$\text{DISCOVER} \longrightarrow \text{EXPLORE} \longrightarrow \text{SHOP}$$
1. **STEP 1: DISCOVER** — Visitors explore curated beauty, fashion, jewellery, and home decor collections.
2. **STEP 2: EXPLORE** — Visitors view curated products, high-resolution aesthetic images, detailed styling recommendations, and verified store ratings.
3. **STEP 3: SHOP** — Visitors click *Shop Now* and are safely redirected to the original external shopping website to complete checkout.

### 6. Pinterest-Style Inspiration Gallery
- Pinterest masonry grid layout (`columns-1 sm:columns-2 md:columns-3 lg:columns-4`).
- Categories: All, Makeup Looks, Outfit Inspiration, Jewellery Styling, Bedroom Decoration, Aesthetic Lifestyle Ideas.
- Variable card heights with hover overlays, interactive Heart like counters, and external destination links.

### 7. A Little About Us
- Heading: **A LITTLE ABOUT US**
- Brand Quote: *"Jashviora is your little destination for beauty, fashion, jewellery and home inspiration. We bring together beautiful finds and creative ideas to help you discover your personal style and create your dream lifestyle."*
- Accompanied by a beautiful aesthetic lifestyle photograph with warm cream and gold framing.

### 8. Product Management (Curator Studio / Admin Page)
Accessible anytime via the **Manage Products** header button:
- **Add New Products**:
  - Enter Product Name, Category, Retailer Store (Amazon, Nykaa, Myntra, Flipkart, Meesho, Zara, etc.).
  - Enter Price (₹ INR) and Original Price.
  - Paste any custom external URL or affiliate link (`https://amzn.to/...`, `https://www.myntra.com/...`).
  - Image options: Paste image URL or upload directly from your computer (auto-saved to `public/uploads/`).
  - Enter description and tags.
  - Check *Trending* or *Editor's Pick*.
  - **Real-time Live Preview Card** on the right side updates as you type!
- **Manage Existing Catalog**:
  - Edit any product with pre-filled form.
  - Delete products with confirmation.
  - Test external links in 1 click.
  - Search and filter table list.
- **Data Safety & Backup**:
  - **Export Catalog as JSON**: One-click download of your entire product catalog.
  - **Reset to Curated Defaults**: One-click restore to original curated finds.
  - **Persistent Storage**: Changes are saved directly to `database/products.json` via the REST API and mirrored to `localStorage`.

### 9. Newsletter & Legal Modals
- **Newsletter Subscription**: Real-time email validation and storage to `database/subscribers.json` with animated success feedback.
- **Affiliate Disclosure Modal**: Transparent FTC-compliant statement explaining how affiliate links work with zero extra cost to visitors.
- **Contact Us Modal**: Form for brand partnerships, product recommendations, and general feedback.

---

## 🚀 How to Run the Website

### Option 1: Run with Python Flask Server (Recommended)
This runs the full persistent REST API server with image upload support and database storage on disk:

```bash
# In the project directory:
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Option 2: Run Standalone Offline (No Server Required)
Simply double-click the `index.html` file in the project folder to open it in Google Chrome, Microsoft Edge, or any modern web browser. The application runs smoothly with `localStorage` persistence!

---

## 📁 Project Directory Structure

```
c:\Users\Admin\Downloads\Jashviora\
├── app.py                     # Python Flask backend server & REST API
├── index.html                 # Standalone offline-ready React SPA
├── test_app.py                # Automated test suite (10 unit tests)
├── README.md                  # Complete documentation and user guide
├── database/
│   ├── default_products.json  # Master default curated products
│   ├── products.json          # Persistent active product database
│   ├── pins.json              # Pinterest-style inspiration pins
│   ├── subscribers.json       # Newsletter subscribers
│   └── messages.json          # Contact inquiries
├── public/
│   ├── assets/
│   │   ├── collections/       # beauty.jpg, fashion.jpg, jewellery.jpg, home-decor.jpg (user references)
│   │   ├── hero.jpg           # Editorial magazine hero photograph
│   │   ├── about.jpg          # Lifestyle atelier photograph
│   │   └── logo-icon.svg      # Botanical floral logo symbol
│   └── uploads/               # User-uploaded product photos
├── templates/
│   └── index.html             # Flask template for the React application
└── static/
    └── css/
        └── style.css          # Custom typography, animations & brand styling
```

---

## 🧪 Testing

Run the automated test suite anytime:
```bash
python test_app.py
```
All 10 unit tests verify homepage rendering, API endpoints, product creation, editing, deletion, category/store filters, pins, and asset serving.
