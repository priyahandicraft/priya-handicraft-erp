import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

# CONFIGURATION FOR LOGO AND STATIC IMAGES
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 1. CORE IMMUTABLE MEMORY ENGINE (MOCKING RELATIONAL SQL REGISTRIES)
# Parent Inventory Registry mapped with structural child arrays
inventory_db = {
    "TIKA-001": {
        "name": "Navratri Designer Tika",
        "category": "Tika",
        "total_in": 250,
        "total_used": 140,
        "total_available": 110,
        "cost_per_piece": 5.0,
        "base_sell_price": 10.0,
        "image_path": "/static/images/tika001.jpg",
        "lots": [
            {"type": "Packet", "size": 50, "count": 1},
            {"type": "Packet", "size": 25, "count": 2},
            {"type": "Single Unit", "size": 1, "count": 10}
        ]
    },
    "BELT-002": {
        "name": "Oxidized Heavy Kamar Belt",
        "category": "Kamar Belt",
        "total_in": 100,
        "total_used": 40,
        "total_available": 60,
        "cost_per_piece": 12.0,
        "base_sell_price": 25.0,
        "image_path": "",
        "lots": [
            {"type": "Packet", "size": 12, "count": 4},
            {"type": "Single Unit", "size": 1, "count": 12}
        ]
    }
}

# Invoices and Operational Financial Ledger Storage Array
bills_registry = [
    {
        "date": "10-06-2026",
        "name": "Radhe Choice Bulk",
        "mobile": "9876543210",
        "city": "Surat",
        "bill_amount": 50000.0,
        "amount_paid": 30000.0,
        "pending_dues": 20000.0,
        "payment_status": "Partial",
        "dispatch_status": "Dispatched"
    },
    {
        "date": "12-06-2026",
        "name": "Ma Krupa Fancy Store",
        "mobile": "9123456789",
        "city": "Baroda",
        "bill_amount": 8500.0,
        "amount_paid": 8500.0,
        "pending_dues": 0.0,
        "payment_status": "Paid",
        "dispatch_status": "Dispatched"
    }
]

# Manual Goal Metrics Variable
app_config_metrics = {
    "monthly_revenue_target": 500000.0
}


# 2. ENDPOINT ROUTES CONTROLLERS
@app.route('/')
def index():
    """Renders the single page application visual command center."""
    return render_template('index.html', config=app_config_metrics)


@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """API endpoint to stream complete multi-tier nested database arrays."""
    return jsonify(inventory_db)


@app.route('/api/billing/submit', methods=['POST'])
def submit_billing():
    """Processes incoming checkout orders with custom packet lot matching deductions."""
    data = request.json
    try:
        design_code = data.get('design_code')
        pack_size = int(data.get('pack_size', 0))
        pack_qty = int(data.get('pack_qty', 0))
        loose_qty = int(data.get('loose_qty', 0))
        custom_rate = float(data.get('custom_rate', 0))
        
        packing_charges = float(data.get('packing_charges', 0))
        shipping_charges = float(data.get('shipping_charges', 0))
        gst_percent = int(data.get('gst_percent', 0))
        
        customer_name = data.get('customer_name')
        customer_mobile = data.get('customer_mobile')
        customer_city = data.get('customer_city')
        
        payment_status = data.get('payment_status')
        manual_paid_input = float(data.get('amount_paid', 0))
        dispatch_status = data.get('dispatch_status', 'Pending')
        invoice_date = data.get('invoice_date', datetime.now().strftime('%d-%m-%Y'))

        # Calculations formula implementation
        total_pieces_sold = (pack_size * pack_qty) + loose_qty
        base_item_total = total_pieces_sold * custom_rate
        gst_calculated = (base_item_total * gst_percent) / 100.0
        grand_total = base_item_total + packing_charges + shipping_charges + gst_calculated

        # Resolve paid vs partial vs pending dues allocation structures
        amount_collected = 0.0
        if payment_status == "Paid":
            amount_collected = grand_total
        elif payment_status == "Partial":
            amount_collected = manual_paid_input
        
        remaining_dues = max(0.0, grand_total - amount_collected)
        
        # Enforce automated zero write constraints if numeric drops
        if remaining_dues <= 0:
            remaining_dues = 0.0

        # Run inventory tier deductions engine if item match exists
        if design_code in inventory_db:
            target_product = inventory_db[design_code]
            target_product["total_used"] += total_pieces_sold
            target_product["total_available"] = max(0, target_product["total_in"] - target_product["total_used"])
            
            # Internal structural lot matching reduction algorithm inside nested loops
            for lot in target_product["lots"]:
                if pack_qty > 0 and lot["type"] == "Packet" and lot["size"] == pack_size:
                    lot["count"] = max(0, lot["count"] - pack_qty)
                elif loose_qty > 0 and lot["type"] == "Single Unit":
                    lot["count"] = max(0, lot["count"] - loose_qty)

        # Log entry to master arrays file
        new_invoice_log = {
            "date": invoice_date,
            "name": customer_name,
            "mobile": customer_mobile,
            "city": customer_city,
            "bill_amount": grand_total,
            "amount_paid": amount_collected,
            "pending_dues": remaining_dues,
            "payment_status": "Paid" if remaining_dues == 0.0 else payment_status,
            "dispatch_status": dispatch_status
        }
        bills_registry.append(new_invoice_log)

        return jsonify({"status": "Success", "message": "Transaction synchronized!", "invoice": new_invoice_log})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 400


@app.route('/api/finance/metrics', methods=['GET', 'POST'])
def finance_metrics():
    """Handles manual revenue targeting overrides and dynamic metrics compilation."""
    if request.method == 'POST':
        data = request.json
        app_config_metrics["monthly_revenue_target"] = float(data.get('target', 500000.0))

    # Automated aggregate financial loops
    total_sales_turnover = 0.0
    total_cost_outlay = 0.0
    strict_achieved_target = 0.0

    for bill in bills_registry:
        total_sales_turnover += bill["bill_amount"]
        # Mock calculation parsing manufacturing cost architectures
        total_cost_outlay += (bill["bill_amount"] * 0.45)
        
        # Strict logic target parameter check filtering
        if bill["payment_status"] == "Paid" and bill["dispatch_status"] == "Dispatched":
            strict_achieved_target += bill["bill_amount"]

    net_profit_margin = total_sales_turnover - total_cost_outlay
    target_percentage = 0
    if app_config_metrics["monthly_revenue_target"] > 0:
        target_percentage = int((strict_achieved_target / app_config_metrics["monthly_revenue_target"]) * 100)

    return jsonify({
        "monthly_target": app_config_metrics["monthly_revenue_target"],
        "achieved_target": strict_achieved_target,
        "achievement_percentage": target_percentage,
        "sales_turnover": total_sales_turnover,
        "manufacturing_cost": total_cost_outlay,
        "net_profit": net_profit_margin,
        "dues_ledger": [b for b in bills_registry if b["pending_dues"] > 0]
    })


if __name__ == '__main__':
    # Initializing server listener ports locally
    app.run(debug=True, port=5000)