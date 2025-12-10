#!/usr/bin/env python3
"""
SellBuddy Order Handler Bot
Handles orders via Google Sheets (free), sends supplier emails, tracks fulfillment.
Works with Google Forms for order intake.

ZERO COST SETUP:
1. Create Google Sheet for orders
2. Create Google Form linked to sheet
3. Set up email notifications via Google Apps Script
"""

import json
import csv
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

# ============================================
# CONFIGURATION
# ============================================

# Your email for notifications (use Gmail)
STORE_EMAIL = "your-store@gmail.com"
STORE_NAME = "SellBuddy"

# Supplier email template
SUPPLIER_EMAIL = "supplier@aliexpress-seller.com"

# Google Sheets URLs (replace with your actual sheets)
ORDERS_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
GOOGLE_FORM_URL = "https://forms.gle/YOUR_FORM_ID"

# Order statuses
ORDER_STATUSES = [
    "pending",
    "paid",
    "processing",
    "shipped",
    "delivered",
    "cancelled",
    "refunded"
]


# ============================================
# ORDER MANAGEMENT
# ============================================

def generate_order_id():
    """Generate unique order ID."""
    timestamp = datetime.now().strftime("%y%m%d")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"SB-{timestamp}-{random_suffix}"


def create_order(customer_data, cart_items):
    """Create a new order."""
    order = {
        "order_id": generate_order_id(),
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "customer": {
            "name": customer_data.get("name", ""),
            "email": customer_data.get("email", ""),
            "phone": customer_data.get("phone", ""),
            "address": {
                "line1": customer_data.get("address_line1", ""),
                "line2": customer_data.get("address_line2", ""),
                "city": customer_data.get("city", ""),
                "state": customer_data.get("state", ""),
                "zip": customer_data.get("zip", ""),
                "country": customer_data.get("country", "US")
            }
        },
        "items": cart_items,
        "subtotal": sum(item["price"] * item["quantity"] for item in cart_items),
        "shipping": 0 if sum(item["price"] * item["quantity"] for item in cart_items) >= 50 else 4.99,
        "total": 0,
        "payment": {
            "method": customer_data.get("payment_method", "paypal"),
            "transaction_id": None,
            "paid_at": None
        },
        "fulfillment": {
            "supplier_order_id": None,
            "tracking_number": None,
            "carrier": None,
            "shipped_at": None,
            "estimated_delivery": None
        }
    }

    order["total"] = order["subtotal"] + order["shipping"]

    return order


def update_order_status(order, new_status, notes=None):
    """Update order status with history tracking."""
    if "status_history" not in order:
        order["status_history"] = []

    order["status_history"].append({
        "status": order["status"],
        "changed_to": new_status,
        "timestamp": datetime.now().isoformat(),
        "notes": notes
    })

    order["status"] = new_status
    order["updated_at"] = datetime.now().isoformat()

    return order


# ============================================
# EMAIL NOTIFICATIONS
# ============================================

def generate_order_confirmation_email(order):
    """Generate order confirmation email for customer."""
    items_html = ""
    for item in order["items"]:
        items_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{item['name']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{item['quantity']}</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">${item['price']:.2f}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
            .order-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ text-align: left; padding: 10px; background: #f3f4f6; }}
            .total {{ font-size: 24px; color: #6366f1; font-weight: bold; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Thank You for Your Order!</h1>
                <p>Order #{order['order_id']}</p>
            </div>
            <div class="content">
                <p>Hi {order['customer']['name']},</p>
                <p>We've received your order and are getting it ready! You'll receive another email when your order ships.</p>

                <div class="order-box">
                    <h3>Order Summary</h3>
                    <table>
                        <tr>
                            <th>Product</th>
                            <th>Qty</th>
                            <th>Price</th>
                        </tr>
                        {items_html}
                    </table>
                    <hr>
                    <p>Subtotal: ${order['subtotal']:.2f}</p>
                    <p>Shipping: ${order['shipping']:.2f}</p>
                    <p class="total">Total: ${order['total']:.2f}</p>
                </div>

                <div class="order-box">
                    <h3>Shipping Address</h3>
                    <p>
                        {order['customer']['name']}<br>
                        {order['customer']['address']['line1']}<br>
                        {order['customer']['address']['line2']}<br>
                        {order['customer']['address']['city']}, {order['customer']['address']['state']} {order['customer']['address']['zip']}<br>
                        {order['customer']['address']['country']}
                    </p>
                </div>

                <p><strong>Estimated Delivery:</strong> 10-15 business days</p>
                <p>Questions? Reply to this email or contact support@sellbuddy.com</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 SellBuddy. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return {
        "to": order["customer"]["email"],
        "subject": f"Order Confirmed! #{order['order_id']} - SellBuddy",
        "html": html
    }


def generate_supplier_order_email(order):
    """Generate order email to send to supplier."""
    items_text = ""
    for item in order["items"]:
        items_text += f"""
Product: {item['name']}
SKU: {item.get('sku', 'N/A')}
Quantity: {item['quantity']}
Variant: {item.get('variant', 'Standard')}
---
"""

    text = f"""
NEW ORDER - {order['order_id']}

Please fulfill the following order:

{items_text}

SHIP TO:
{order['customer']['name']}
{order['customer']['address']['line1']}
{order['customer']['address']['line2']}
{order['customer']['address']['city']}, {order['customer']['address']['state']} {order['customer']['address']['zip']}
{order['customer']['address']['country']}
Phone: {order['customer']['phone']}

SHIPPING METHOD: ePacket / Standard

Please provide tracking number once shipped.

Thank you,
SellBuddy Orders
"""

    return {
        "to": SUPPLIER_EMAIL,
        "subject": f"New Order #{order['order_id']} - Please Fulfill",
        "text": text
    }


def generate_shipping_notification(order):
    """Generate shipping notification email."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #10b981; color: white; padding: 30px; text-align: center; border-radius: 8px; }}
            .tracking-box {{ background: #f0fdf4; border: 2px solid #10b981; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; }}
            .tracking-number {{ font-size: 24px; font-weight: bold; color: #059669; letter-spacing: 2px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Order Has Shipped!</h1>
            </div>
            <p>Hi {order['customer']['name']},</p>
            <p>Great news! Your order #{order['order_id']} is on its way!</p>

            <div class="tracking-box">
                <p>Tracking Number:</p>
                <p class="tracking-number">{order['fulfillment']['tracking_number']}</p>
                <p>Carrier: {order['fulfillment']['carrier']}</p>
            </div>

            <p><strong>Estimated Delivery:</strong> {order['fulfillment']['estimated_delivery']}</p>

            <p>Track your package: <a href="https://track.example.com/{order['fulfillment']['tracking_number']}">Click Here</a></p>

            <p>Thanks for shopping with SellBuddy!</p>
        </div>
    </body>
    </html>
    """

    return {
        "to": order["customer"]["email"],
        "subject": f"Your Order Has Shipped! #{order['order_id']}",
        "html": html
    }


# ============================================
# GOOGLE SHEETS INTEGRATION (via CSV export)
# ============================================

def export_orders_to_csv(orders, filename="orders_export.csv"):
    """Export orders to CSV for Google Sheets import."""
    fieldnames = [
        "order_id", "created_at", "status", "customer_name", "customer_email",
        "customer_phone", "address", "city", "state", "zip", "country",
        "items", "subtotal", "shipping", "total", "payment_method",
        "transaction_id", "tracking_number", "shipped_at"
    ]

    output_path = Path(__file__).parent.parent / "data" / filename

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for order in orders:
            items_str = "; ".join([f"{i['name']} x{i['quantity']}" for i in order.get("items", [])])

            row = {
                "order_id": order.get("order_id", ""),
                "created_at": order.get("created_at", ""),
                "status": order.get("status", ""),
                "customer_name": order.get("customer", {}).get("name", ""),
                "customer_email": order.get("customer", {}).get("email", ""),
                "customer_phone": order.get("customer", {}).get("phone", ""),
                "address": order.get("customer", {}).get("address", {}).get("line1", ""),
                "city": order.get("customer", {}).get("address", {}).get("city", ""),
                "state": order.get("customer", {}).get("address", {}).get("state", ""),
                "zip": order.get("customer", {}).get("address", {}).get("zip", ""),
                "country": order.get("customer", {}).get("address", {}).get("country", ""),
                "items": items_str,
                "subtotal": order.get("subtotal", 0),
                "shipping": order.get("shipping", 0),
                "total": order.get("total", 0),
                "payment_method": order.get("payment", {}).get("method", ""),
                "transaction_id": order.get("payment", {}).get("transaction_id", ""),
                "tracking_number": order.get("fulfillment", {}).get("tracking_number", ""),
                "shipped_at": order.get("fulfillment", {}).get("shipped_at", "")
            }
            writer.writerow(row)

    print(f"Orders exported to: {output_path}")
    return str(output_path)


# ============================================
# GOOGLE APPS SCRIPT FOR AUTOMATION
# ============================================

GOOGLE_APPS_SCRIPT = '''
/**
 * SellBuddy Order Automation - Google Apps Script
 *
 * SETUP:
 * 1. Open your Google Sheet with orders
 * 2. Go to Extensions > Apps Script
 * 3. Paste this code
 * 4. Set up triggers for onFormSubmit and dailyReport
 */

// Configuration
const STORE_EMAIL = "your-store@gmail.com";
const STORE_NAME = "SellBuddy";

/**
 * Triggered when a new order comes in via Google Form
 */
function onFormSubmit(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();

  // Generate order ID
  const orderId = "SB-" + Utilities.formatDate(new Date(), "GMT", "yyMMdd") + "-" +
                  Math.random().toString(36).substring(2, 6).toUpperCase();

  // Set order ID in column A
  sheet.getRange(lastRow, 1).setValue(orderId);

  // Set status to "pending"
  sheet.getRange(lastRow, 3).setValue("pending");

  // Send confirmation email
  const customerEmail = sheet.getRange(lastRow, 5).getValue();
  const customerName = sheet.getRange(lastRow, 4).getValue();

  sendOrderConfirmation(orderId, customerName, customerEmail);

  // Notify store owner
  notifyNewOrder(orderId, customerName);
}

/**
 * Send order confirmation to customer
 */
function sendOrderConfirmation(orderId, customerName, customerEmail) {
  const subject = `Order Confirmed! #${orderId} - ${STORE_NAME}`;
  const body = `
Hi ${customerName},

Thank you for your order!

Order Number: ${orderId}
Status: Processing

We'll send you another email when your order ships.

Estimated delivery: 10-15 business days

Questions? Reply to this email.

Thanks,
${STORE_NAME} Team
  `;

  GmailApp.sendEmail(customerEmail, subject, body);
}

/**
 * Notify store owner of new order
 */
function notifyNewOrder(orderId, customerName) {
  const subject = `New Order! #${orderId}`;
  const body = `New order received from ${customerName}. Check your sheet for details.`;

  GmailApp.sendEmail(STORE_EMAIL, subject, body);
}

/**
 * Daily report - run via time-based trigger
 */
function dailyReport() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();

  let pendingCount = 0;
  let todayRevenue = 0;
  const today = new Date().toDateString();

  for (let i = 1; i < data.length; i++) {
    if (data[i][2] === "pending") pendingCount++;

    const orderDate = new Date(data[i][1]).toDateString();
    if (orderDate === today) {
      todayRevenue += parseFloat(data[i][14]) || 0;
    }
  }

  const report = `
Daily Report - ${today}

Orders pending fulfillment: ${pendingCount}
Today's revenue: $${todayRevenue.toFixed(2)}
Total orders: ${data.length - 1}

Check your dashboard for details.
  `;

  GmailApp.sendEmail(STORE_EMAIL, `${STORE_NAME} Daily Report`, report);
}

/**
 * Create menu for manual actions
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('SellBuddy')
    .addItem('Send Daily Report', 'dailyReport')
    .addItem('Export for Supplier', 'exportForSupplier')
    .addToUi();
}

/**
 * Export pending orders for supplier
 */
function exportForSupplier() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();

  let exportText = "SUPPLIER ORDER EXPORT\\n\\n";

  for (let i = 1; i < data.length; i++) {
    if (data[i][2] === "paid" || data[i][2] === "pending") {
      exportText += `
Order: ${data[i][0]}
Customer: ${data[i][3]}
Address: ${data[i][6]}, ${data[i][7]}, ${data[i][8]} ${data[i][9]}, ${data[i][10]}
Items: ${data[i][11]}
---
`;
    }
  }

  GmailApp.sendEmail(STORE_EMAIL, "Supplier Export - Pending Orders", exportText);
  SpreadsheetApp.getUi().alert("Export sent to your email!");
}
'''


# ============================================
# SIMULATED ORDER PROCESSING
# ============================================

def simulate_order_flow():
    """Simulate the complete order flow for testing."""
    print("=" * 60)
    print("SellBuddy Order Flow Simulation")
    print("=" * 60)

    # 1. Create sample order
    customer = {
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "+1-555-123-4567",
        "address_line1": "123 Main Street",
        "address_line2": "Apt 4B",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US",
        "payment_method": "paypal"
    }

    items = [
        {"id": "galaxy-star-projector-pro", "name": "Galaxy Star Projector Pro", "sku": "GSP-001", "price": 34.99, "quantity": 1, "variant": "Black"},
        {"id": "led-strip-lights-smart", "name": "Smart LED Strip Lights 65ft", "sku": "LSL-001", "price": 29.99, "quantity": 1, "variant": "Standard"}
    ]

    print("\n1. Creating order...")
    order = create_order(customer, items)
    print(f"   Order ID: {order['order_id']}")
    print(f"   Total: ${order['total']:.2f}")

    # 2. Generate confirmation email
    print("\n2. Generating confirmation email...")
    conf_email = generate_order_confirmation_email(order)
    print(f"   To: {conf_email['to']}")
    print(f"   Subject: {conf_email['subject']}")

    # 3. Update to paid
    print("\n3. Payment received...")
    order = update_order_status(order, "paid", "PayPal payment confirmed")
    order["payment"]["transaction_id"] = "PAY-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    order["payment"]["paid_at"] = datetime.now().isoformat()
    print(f"   Transaction ID: {order['payment']['transaction_id']}")

    # 4. Generate supplier order
    print("\n4. Generating supplier order email...")
    supplier_email = generate_supplier_order_email(order)
    print(f"   To: {supplier_email['to']}")
    print(f"   Subject: {supplier_email['subject']}")

    # 5. Update to processing
    print("\n5. Order sent to supplier...")
    order = update_order_status(order, "processing", "Sent to supplier")
    order["fulfillment"]["supplier_order_id"] = "ALI-" + ''.join(random.choices(string.digits, k=10))
    print(f"   Supplier Order ID: {order['fulfillment']['supplier_order_id']}")

    # 6. Update to shipped
    print("\n6. Order shipped...")
    order = update_order_status(order, "shipped", "Tracking provided by supplier")
    order["fulfillment"]["tracking_number"] = "YT" + ''.join(random.choices(string.digits, k=16))
    order["fulfillment"]["carrier"] = "Yanwen / USPS"
    order["fulfillment"]["shipped_at"] = datetime.now().isoformat()
    order["fulfillment"]["estimated_delivery"] = (datetime.now() + timedelta(days=12)).strftime("%B %d, %Y")
    print(f"   Tracking: {order['fulfillment']['tracking_number']}")

    # 7. Generate shipping notification
    print("\n7. Generating shipping notification...")
    ship_email = generate_shipping_notification(order)
    print(f"   Subject: {ship_email['subject']}")

    # 8. Save order
    print("\n8. Saving order...")
    orders_path = Path(__file__).parent.parent / "data" / "orders.json"

    try:
        with open(orders_path, "r") as f:
            orders_data = json.load(f)
    except:
        orders_data = {"orders": []}

    orders_data["orders"].append(order)

    with open(orders_path, "w") as f:
        json.dump(orders_data, f, indent=2)

    print(f"   Saved to: {orders_path}")

    # 9. Export to CSV
    print("\n9. Exporting to CSV...")
    export_orders_to_csv(orders_data["orders"])

    print("\n" + "=" * 60)
    print("Order flow simulation complete!")
    print("=" * 60)

    return order


def main():
    """Main function."""
    print("=" * 60)
    print("SellBuddy Order Handler Bot")
    print("=" * 60)

    # Run simulation
    order = simulate_order_flow()

    # Print Google Apps Script
    print("\n\nGOOGLE APPS SCRIPT FOR AUTOMATION:")
    print("-" * 40)
    print("Copy the following to your Google Sheet's Apps Script:")
    print("-" * 40)
    print(GOOGLE_APPS_SCRIPT[:500] + "...")
    print("\n(Full script saved to: bots/google_apps_script.js)")

    # Save Google Apps Script
    script_path = Path(__file__).parent / "google_apps_script.js"
    with open(script_path, "w") as f:
        f.write(GOOGLE_APPS_SCRIPT)

    print("\n" + "=" * 60)
    print("Order handler ready!")
    print("=" * 60)


if __name__ == "__main__":
    main()
