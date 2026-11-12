"""
JASHVIORA Backend Server
Curated Lifestyle, Beauty, Fashion, Jewellery & Home Decor Discovery Platform
"""

import os
import json
import uuid
import time
from datetime import datetime, timezone
from flask import Flask, request, jsonify, send_from_directory

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
UPLOAD_DIR = os.path.join(PUBLIC_DIR, "uploads")
ASSETS_DIR = os.path.join(PUBLIC_DIR, "assets")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

PRODUCTS_FILE = os.path.join(DB_DIR, "products.json")
DEFAULT_PRODUCTS_FILE = os.path.join(DB_DIR, "default_products.json")
PINS_FILE = os.path.join(DB_DIR, "pins.json")
SUBSCRIBERS_FILE = os.path.join(DB_DIR, "subscribers.json")
MESSAGES_FILE = os.path.join(DB_DIR, "messages.json")

def read_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return default if default is not None else []

def write_json(path, data):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)

# Enable CORS manually for all endpoints
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# ----------------- STATIC ROUTES -----------------

@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "templates"), "index.html")

@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(ASSETS_DIR, filename)

@app.route("/uploads/<path:filename>")
def serve_uploads(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# ----------------- API ENDPOINTS -----------------

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "brand": "JASHVIORA",
        "tagline": "Discover Your Style, Create Your World.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route("/api/products", methods=["GET"])
def get_products():
    products = read_json(PRODUCTS_FILE, [])
    # Optional filtering
    category = request.args.get("category")
    store = request.args.get("store")
    trending = request.args.get("trending")
    search = request.args.get("search", "").strip().lower()

    filtered = products
    if category and category.lower() != "all":
        filtered = [p for p in filtered if p.get("category", "").lower() == category.lower()]
    if store and store.lower() != "all":
        filtered = [p for p in filtered if p.get("store", "").lower() == store.lower()]
    if trending == "true":
        filtered = [p for p in filtered if p.get("isTrending") is True]
    if search:
        filtered = [
            p for p in filtered
            if search in p.get("title", "").lower()
            or search in p.get("description", "").lower()
            or search in p.get("category", "").lower()
            or any(search in t.lower() for t in p.get("tags", []))
        ]

    return jsonify({"success": True, "count": len(filtered), "products": filtered})

@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    products = read_json(PRODUCTS_FILE, [])
    for p in products:
        if str(p.get("id")) == str(product_id):
            return jsonify({"success": True, "product": p})
    return jsonify({"success": False, "error": "Product not found"}), 404

@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json(force=True, silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"success": False, "error": "Product title is required"}), 400

    products = read_json(PRODUCTS_FILE, [])

    new_id = f"jv-{uuid.uuid4().hex[:8]}"
    category = data.get("category", "Beauty")
    category_labels = {
        "Beauty": "Beauty & Makeup",
        "Fashion": "Fashion & Dresses",
        "Jewellery": "Jewellery",
        "Home Decor": "Home Decor"
    }

    # Store badge color default mappings
    store_name = data.get("store", "Amazon India")
    store_badge_colors = {
        "Amazon India": "#232f3e",
        "Amazon": "#232f3e",
        "Nykaa": "#fc2779",
        "Myntra": "#ff3f6c",
        "Flipkart": "#2874f0",
        "Meesho": "#8b2671",
        "Zara": "#1a1a1a",
        "H&M": "#e50010"
    }

    new_product = {
        "id": new_id,
        "title": title,
        "category": category,
        "categoryLabel": category_labels.get(category, category),
        "price": float(data.get("price") or 0),
        "originalPrice": float(data.get("originalPrice") or 0) if data.get("originalPrice") else None,
        "store": store_name,
        "storeBadgeColor": data.get("storeBadgeColor") or store_badge_colors.get(store_name, "#49372F"),
        "externalUrl": data.get("externalUrl") or f"https://www.google.com/search?q={title}",
        "image": data.get("image") or "/assets/collections/beauty.jpg",
        "fallbackImage": data.get("fallbackImage") or "/assets/collections/beauty.jpg",
        "description": data.get("description", "Handpicked luxury curation for modern living."),
        "isTrending": bool(data.get("isTrending", False)),
        "isFeatured": bool(data.get("isFeatured", False)),
        "rating": float(data.get("rating") or 4.9),
        "reviewsCount": int(data.get("reviewsCount") or 1),
        "tags": data.get("tags") if isinstance(data.get("tags"), list) else [t.strip() for t in str(data.get("tags", "")).split(",") if t.strip()],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    products.insert(0, new_product)
    write_json(PRODUCTS_FILE, products)

    return jsonify({"success": True, "product": new_product}), 201

@app.route("/api/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json(force=True, silent=True) or {}
    products = read_json(PRODUCTS_FILE, [])

    found_idx = None
    for idx, p in enumerate(products):
        if str(p.get("id")) == str(product_id):
            found_idx = idx
            break

    if found_idx is None:
        return jsonify({"success": False, "error": "Product not found"}), 404

    current = products[found_idx]
    # Update allowed fields
    for field in ["title", "category", "price", "originalPrice", "store", "storeBadgeColor",
                  "externalUrl", "image", "fallbackImage", "description", "isTrending", "isFeatured", "tags"]:
        if field in data:
            current[field] = data[field]

    # Category label sync
    category_labels = {
        "Beauty": "Beauty & Makeup",
        "Fashion": "Fashion & Dresses",
        "Jewellery": "Jewellery",
        "Home Decor": "Home Decor"
    }
    current["categoryLabel"] = category_labels.get(current.get("category"), current.get("category"))
    current["updatedAt"] = datetime.now(timezone.utc).isoformat()

    products[found_idx] = current
    write_json(PRODUCTS_FILE, products)

    return jsonify({"success": True, "product": current})

@app.route("/api/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    products = read_json(PRODUCTS_FILE, [])
    initial_len = len(products)
    products = [p for p in products if str(p.get("id")) != str(product_id)]

    if len(products) == initial_len:
        return jsonify({"success": False, "error": "Product not found"}), 404

    write_json(PRODUCTS_FILE, products)
    return jsonify({"success": True, "message": "Product removed successfully"})

@app.route("/api/products/reset", methods=["POST"])
def reset_products():
    default_products = read_json(DEFAULT_PRODUCTS_FILE, [])
    write_json(PRODUCTS_FILE, default_products)
    return jsonify({"success": True, "count": len(default_products), "message": "Catalog restored to default curated list."})

@app.route("/api/pins", methods=["GET"])
def get_pins():
    pins = read_json(PINS_FILE, [])
    category = request.args.get("category")
    if category and category.lower() != "all":
        pins = [p for p in pins if p.get("category", "").lower() == category.lower()]
    return jsonify({"success": True, "pins": pins})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        return jsonify({"success": False, "error": "Invalid image extension"}), 400

    filename = f"item_{int(time.time())}_{uuid.uuid4().hex[:6]}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    return jsonify({
        "success": True,
        "url": f"/uploads/{filename}",
        "filename": filename
    })

@app.route("/api/newsletter", methods=["POST"])
def subscribe_newsletter():
    data = request.get_json(force=True, silent=True) or {}
    email = data.get("email", "").strip().lower()
    if not email or "@" not in email:
        return jsonify({"success": False, "error": "Please provide a valid email address."}), 400

    subscribers = read_json(SUBSCRIBERS_FILE, [])
    if any(s.get("email") == email for s in subscribers):
        return jsonify({"success": True, "message": "You are already subscribed to Jashviora inspirations!"})

    subscribers.append({
        "email": email,
        "subscribedAt": datetime.now(timezone.utc).isoformat()
    })
    write_json(SUBSCRIBERS_FILE, subscribers)
    return jsonify({"success": True, "message": "Thank you for joining JASHVIORA. Your style inspirations are on their way!"})

@app.route("/api/contact", methods=["POST"])
def send_contact():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    subject = data.get("subject", "General Inquiry")

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Please fill out all required fields."}), 400

    messages = read_json(MESSAGES_FILE, [])
    msg_entry = {
        "id": f"msg-{uuid.uuid4().hex[:6]}",
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "receivedAt": datetime.now(timezone.utc).isoformat()
    }
    messages.append(msg_entry)
    write_json(MESSAGES_FILE, messages)

    return jsonify({"success": True, "message": "Thank you! The JASHVIORA editorial team has received your message."})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    products = read_json(PRODUCTS_FILE, [])
    categories = {}
    stores = {}
    for p in products:
        cat = p.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
        st = p.get("store", "Other")
        stores[st] = stores.get(st, 0) + 1

    return jsonify({
        "success": True,
        "totalProducts": len(products),
        "byCategory": categories,
        "byStore": stores
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting JASHVIORA server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
