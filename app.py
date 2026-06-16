import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Set page configuration layout wide
st.set_page_config(page_title="Priya Handicraft ERP", layout="wide")

# --- 1. INITIALIZE GLOBAL STATE STORAGE ---
if "product_db" not in st.session_state:
    st.session_state.product_db = [
        {
            "item_code": "TIKA001",
            "item_name": "Fabric Tika Standard",
            "category": "Tikka",
            "real_cost": 50.0,
            "selling_price": 90.0,
            "stock_type": "Both",
            "packet_stock": 712,
            "loose_stock": 107,
            "total_stock": 819,
            "alert_level": 100,
            "last_sold_date": "12-05-2026",
            "image_data": None
        },
        {
            "item_code": "NATH002",
            "item_name": "Bridal Nath Heavy",
            "category": "Nath (nosepin)",
            "real_cost": 80.0,
            "selling_price": 150.0,
            "stock_type": "Packets",
            "packet_stock": 450,
            "loose_stock": 0,
            "total_stock": 450,
            "alert_level": 100,
            "last_sold_date": "15-06-2026",
            "image_data": None
        }
    ]

# Target Sales state container logic
if "target_sales_val" not in st.session_state:
    st.session_state.target_sales_val = 12000.0

# Mock invoice state to handle automated calculation rules for paid and delivered items
if "invoice_db" not in st.session_state:
    st.session_state.invoice_db = [
        {"invoice_id": "INV001", "amount": 6000.0, "payment_status": "Paid", "delivery_status": "Delivered"},
        {"invoice_id": "INV002", "amount": 4000.0, "payment_status": "Paid", "delivery_status": "Delivered"},
        {"invoice_id": "INV003", "amount": 2500.0, "payment_status": "Partial", "delivery_status": "Pending"}
    ]

if "temp_packet_lots" not in st.session_state:
    st.session_state.temp_packet_lots = []
if "temp_loose_lots" not in st.session_state:
    st.session_state.temp_loose_lots = []

# --- 2. LOGO CONFIGURATION AREA ---
logo_url = "https://cdn.corenexis.com/f/fHLeDnaTlAV.png" 

# --- 3. SIDEBAR NAVIGATION MENU ---
with st.sidebar:
    st.image(logo_url, width=100)
    st.markdown("### 👑 Priya Handicraft ERP")
    menu = st.radio(
        "Navigation Menu",
        ["📊 Dashboard", "📋 Product Listing", "📦 Inventory Management", "🧾 Invoice Creation (Locked)", "🚚 Order Status (Locked)", "📈 Reports (Locked)", "🔔 Notification (Locked)"]
    )

categories_list = [
    "Nath (nosepin)", "Tikka", "Damni", "Bangles", "Hand kada", "Necklace", 
    "Choker", "Payal (anklets)", "Bracelet", "Hand panja", "Earrings", "Kan", 
    "Kamarbelt", "Phone cover juda", "Purse", "Ring", "Dandiya", 
    "Hair accessories", "Bajubandh", "Pagna panja", "Male jewelry"
]

# ==================== 📊 DASHBOARD VIEW ====================
if menu == "📊 Dashboard":
    st.title("Business Dashboard")
    
    # Auto calculation from invoice data mapping rules (Fully Paid & Delivered)
    achieved_sales = sum(inv['amount'] for inv in st.session_state.invoice_db if inv['payment_status'] == "Paid" and inv['delivery_status'] == "Delivered")
    
    # Editable Target Sales Field Input
    st.session_state.target_sales_val = st.number_input("Edit Target Sales Target (₹)", min_value=1.0, value=float(st.session_state.target_sales_val), step=500.0)
    gap_remaining = max(0.0, st.session_state.target_sales_val - achieved_sales)
    
    # Target Metrics Rows Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Target Sales", f"₹ {st.session_state.target_sales_val:,.2f}")
    
    pct_achieved = (achieved_sales / st.session_state.target_sales_val * 100) if st.session_state.target_sales_val > 0 else 0.0
    col2.metric("Achieved Sales", f"₹ {achieved_sales:,.2f}", delta=f"{pct_achieved:.1f}% Achieved")
    
    pct_gap = (gap_remaining / st.session_state.target_sales_val * 100) if st.session_state.target_sales_val > 0 else 0.0
    col3.metric("Gap Remaining", f"₹ {gap_remaining:,.2f}", delta=f"-{pct_gap:.1f}%", delta_color="inverse")
    
    # Progress Bar
    st.markdown("**Progress Breakdown**")
    progress_ratio = min(1.0, max(0.0, achieved_sales / st.session_state.target_sales_val)) if st.session_state.target_sales_val > 0 else 0.0
    st.progress(progress_ratio)
    
    st.markdown("---")
    
    # Monthly Sales Trend Chart Full Width Layout View Component
    st.markdown("##### Monthly Sales Trend")
    chart_data = pd.DataFrame(
        [20, 40, 60, 80, 100, 120, 140, 160, 180],
        index=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
        columns=["Sales"]
    )
    st.bar_chart(chart_data, use_container_width=True)
    
    st.markdown("---")
    
    # REPOSITIONED ELEMENT: Stock Metrics placed horizontally line-wise directly beneath chart frame
    st.markdown("#### Stock Status & Metrics Summary")
    df_temp = pd.DataFrame(st.session_state.product_db)
    total_designs = len(df_temp)
    total_val = (df_temp['total_stock'] * df_temp['real_cost']).sum()
    out_of_stock = len(df_temp[df_temp['total_stock'] == 0])
    low_stock_count = len(df_temp[df_temp['total_stock'] < df_temp['alert_level']])
    
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    m_col1.metric("Total Designs", f"{total_designs}")
    m_col2.metric("Total Stock Value", f"₹{total_val:,.2f}")
    m_col3.metric("Out of Stock Count", f"{out_of_stock}")
    
    with m_col4:
        st.write("")
        if low_stock_count > 0:
            if st.button(f"⚠️ View {low_stock_count} Low Stock Items"):
                st.warning("Low Stock Items List:")
                st.dataframe(df_temp[df_temp['total_stock'] < df_temp['alert_level']][['item_code', 'item_name', 'total_stock']])
                
    with m_col5:
        # 60 Days Dead Stock Automated Alert
        today = datetime.now()
        dead_stock_items = []
        for item in st.session_state.product_db:
            last_date = datetime.strptime(item['last_sold_date'], "%d-%m-%Y")
            if (today - last_date).days > 60:
                dead_stock_items.append(item)
                
        if len(dead_stock_items) > 0:
            st.error(f"📉 Dead Stock: {len(dead_stock_items)} Items")
            if st.button("Review Dead Stock List"):
                st.dataframe(pd.DataFrame(dead_stock_items)[['item_code', 'item_name', 'last_sold_date', 'total_stock']])

    st.markdown("---")
    lead_col1, lead_col2 = st.columns(2)
    with lead_col1:
        st.markdown("##### Most Selling Products")
        st.table(pd.DataFrame([{"Rank": "#1", "Product": "Fabric Tika 105", "Sales": "10,000"}, {"Rank": "#2", "Product": "Nath XYZ", "Sales": "8,500"}]))
    with lead_col2:
        st.markdown("##### Top 5 Customers")
        st.table(pd.DataFrame([{"Rank": "#1", "Customer": "Raj Traders", "Revenue": "₹12,50,000"}, {"Rank": "#2", "Customer": "Shree Ornaments", "Revenue": "₹8,20,000"}]))

# ==================== 📋 PRODUCT LISTING MENU ====================
elif menu == "📋 Product Listing":
    st.title("Product Listing")
    st.markdown("Use this menu form to register new design configurations into your catalog warehouse.")
    
    with st.form("listing_form", clear_on_submit=True):
        st.markdown("##### 📸 Product Image Selection")
        
        # CHANGED: Native hardware options camera inputs or gallery image loading configuration rules
        image_mode = st.radio("Choose Capture Method", ["Upload from Gallery / Files", "Take Live Snapshot with Camera"])
        uploaded_img_raw = None
        if image_mode == "Take Live Snapshot with Camera":
            uploaded_img_raw = st.camera_input("Snapshot")
        else:
            uploaded_img_raw = st.file_uploader("Choose File image", type=["png", "jpg", "jpeg"])
            
        selected_category = st.selectbox("Category *", [""] + categories_list)
        
        # Auto Sequence Code Generation Logic
        generated_code = ""
        if selected_category:
            short_prefix = selected_category[:4].upper().replace(" ", "").replace("(", "")
            match_count = sum(1 for x in st.session_state.product_db if x['category'] == selected_category)
            generated_code = f"{short_prefix}{str(match_count + 1).zfill(3)}"
            
        st.text_input("Item Code (Auto-Generated)", value=generated_code, disabled=True)
        item_name = st.text_input("Item Name / Title *")
        
        c1, c2 = st.columns(2)
        real_cost = c1.number_input("Real Cost Price (₹)", min_value=0.0, step=1.0)
        selling_price = c2.number_input("Selling Price (₹) *", min_value=0.0, step=1.0)
        alert_level = st.number_input("Min Stock Alert Level *", min_value=0, value=100)
        
        submit_btn = st.form_submit_button("[ Save Design Registry ]")
        
        if submit_btn:
            if not selected_category or not item_name or selling_price <= 0:
                st.error("Please fill all required design fields properly.")
            else:
                bytes_data = uploaded_img_raw.getvalue() if uploaded_img_raw else None
                
                new_design = {
                    "item_code": generated_code,
                    "item_name": item_name,
                    "category": selected_category,
                    "real_cost": real_cost,
                    "selling_price": selling_price,
                    "stock_type": "Single Units",
                    "packet_stock": 0,
                    "loose_stock": 0,
                    "total_stock": 0,
                    "alert_level": alert_level,
                    "last_sold_date": datetime.now().strftime("%d-%m-%Y"),
                    "image_data": bytes_data
                }
                st.session_state.product_db.append(new_design)
                st.success(f"Success: Registered {generated_code} into the catalog.")

# ==================== 📦 INVENTORY MANAGEMENT VIEW ====================
elif menu == "📦 Inventory Management":
    st.title("Inventory Management")
    
    # 1. LOT STOCK ALLOCATION WORKSPACE PANEL
    st.markdown("### ➕ Allocate & Add Stock Batches")
    
    product_codes_list = [p['item_code'] for p in st.session_state.product_db]
    selected_product_code = st.selectbox("Select Registered Item Code to Update Stock *", [""] + product_codes_list)
    
    if selected_product_code:
        p_idx = next(i for i, x in enumerate(st.session_state.product_db) if x['item_code'] == selected_product_code)
        target_product = st.session_state.product_db[p_idx]
        
        st.info(f"Updating Stock For: **{target_product['item_name']}** | Current Total Stock: {target_product['total_stock']} pcs")
        stock_type = st.radio("Stock Type Selector *", ["Packets", "Single Units", "Both"], index=2)
        
        # --- PACKETS LOT SECTION WITH CLEAN ALIGNED ROW VIEW ---
        if stock_type in ["Packets", "Both"]:
            st.markdown("##### Packets Allocation Matrix")
            p_col1, p_col2, p_col3 = st.columns([2, 2, 1])
            p_qty = p_col1.number_input("Packet Qty (Pcs/Pack)", min_value=0, step=1, key="p_qty_in")
            n_packs = p_col2.number_input("No. of Packets", min_value=0, step=1, key="n_packs_in")
            
            if p_col3.button("➕ Add More Packet Lot", use_container_width=True):
                if p_qty > 0 and n_packs > 0:
                    st.session_state.temp_packet_lots.append({"Packet Qty": p_qty, "No. of Packets": n_packs, "Subtotal (Pcs)": p_qty * n_packs})
                    st.toast(f"Added batch: {n_packs} packs of {p_qty} pcs")
                    
            if st.session_state.temp_packet_lots:
                st.caption("📋 Current Pending Packet Batches:")
                # FIXED: Displays a clean tabular table view instead of random JSON string blocks
                st.table(pd.DataFrame(st.session_state.temp_packet_lots))
        
        # --- LOOSE UNITS SECTION WITH CLEAN ALIGNED ROW VIEW ---
        if stock_type in ["Single Units", "Both"]:
            st.markdown("##### Single Units Allocation")
            l_col1, l_col2 = st.columns([4, 1])
            loose_qty = l_col1.number_input("Loose Units Quantity", min_value=0, step=1, key="loose_in")
            
            if l_col2.button("➕ Add More Unit Lot", use_container_width=True):
                if loose_qty > 0:
                    st.session_state.temp_loose_lots.append({"Batch No": len(st.session_state.temp_loose_lots) + 1, "Loose Units Qty": loose_qty})
                    st.toast(f"Added loose unit batch: {loose_qty} pcs")
                    
            if st.session_state.temp_loose_lots:
                st.caption("📋 Current Pending Loose Batches:")
                st.table(pd.DataFrame(st.session_state.temp_loose_lots))
        
        # Live summary display compiler logic
        calc_packet_sum = sum(lot['Subtotal (Pcs)'] for lot in st.session_state.temp_packet_lots)
        calc_loose_sum = sum(lot['Loose Units Qty'] for lot in st.session_state.temp_loose_lots)
        
        if stock_type in ["Packets", "Both"] and len(st.session_state.temp_packet_lots) == 0:
            calc_packet_sum += (p_qty * n_packs)
        if stock_type in ["Single Units", "Both"] and len(st.session_state.temp_loose_lots) == 0:
            calc_loose_sum += loose_qty
            
        grand_total_calculated = calc_packet_sum + calc_loose_sum
        st.metric("Total Available Stock Calculated", f"{grand_total_calculated} pcs")
        
        if st.button("💾 COMMIT ALLOCATED LOT STOCK TO LIVE INVENTORY"):
            st.session_state.product_db[p_idx]['packet_stock'] += calc_packet_sum
            st.session_state.product_db[p_idx]['loose_stock'] += calc_loose_sum
            st.session_state.product_db[p_idx]['total_stock'] += grand_total_calculated
            st.session_state.product_db[p_idx]['stock_type'] = stock_type
            
            st.session_state.temp_packet_lots = []
            st.session_state.temp_loose_lots = []
            st.success(f"Stock successfully committed and updated for {selected_product_code}!")
            st.rerun()

    st.markdown("---")
    
    # 2. MASTER ACTIVE INVENTORY DATA SHEET TABLE
    st.markdown("### 📋 Active Master Inventory Sheet")
    
    search_query = st.text_input("🔍 Search active stock sheet by Code, Name, or Category Filters...").lower().strip()
    
    # Build clean dataset without unnecessary index rows or missing column fragments
    clean_export_list = []
    for item in st.session_state.product_db:
        clean_export_list.append({
            "item_code": item["item_code"],
            "item_name": item["item_name"],
            "category": item["category"],
            "selling_price": item["selling_price"],
            "total_stock": item["total_stock"],
            "packet_stock": item["packet_stock"],
            "loose_stock": item["loose_stock"],
            "image_data": item["image_data"]
        })
        
    df_master = pd.DataFrame(clean_export_list)
    
    if search_query:
        df_filtered = df_master[
            df_master['item_code'].str.lower().str.contains(search_query) |
            df_master['item_name'].str.lower().str.contains(search_query) |
            df_master['category'].str.lower().str.contains(search_query)
        ]
    else:
        df_filtered = df_master

    # EXPORT PIPELINE SETUP (FIXED: Cleaner sheet extraction output layer tracking parameters mapping data structures)
    # Removing raw image binary data track to ensure Excel table structure downloads cleanly
    df_excel_ready = df_filtered[['item_code', 'item_name', 'category', 'selling_price', 'total_stock', 'packet_stock', 'loose_stock']].copy()
    
    csv_buffer = io.StringIO()
    df_excel_ready.to_csv(csv_buffer, index=False) # Index=False completely drops the broken first numeric tracker column!
    csv_data = csv_buffer.getvalue().encode('utf-8')
    
    st.download_button("📥 Download Excel Sheet (Clean CSV Data Rows)", data=csv_data, file_name="Live_Inventory_Balance.csv", mime="text/csv")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Native display grid renderer showcasing thumbnail assets cleanly
    st.data_editor(
        df_filtered[['image_data', 'item_code', 'item_name', 'category', 'selling_price', 'total_stock', 'packet_stock', 'loose_stock']],
        column_config={
            "image_data": st.column_config.ImageColumn("Preview Image", width="medium"),
            "item_code": "Item Code",
            "item_name": "Design Title",
            "category": "Category",
            "selling_price": "Price (₹)",
            "total_stock": "Total Balance",
            "packet_stock": "Packed Qty",
            "loose_stock": "Loose Units"
        },
        disabled=True,
        use_container_width=True,
        key="master_grid_editor"
    )
