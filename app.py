import streamlit as st
import pandas as pd
from datetime import datetime

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
            "packet_stock": 700,
            "loose_stock": 105,
            "total_stock": 805,
            "alert_level": 100,
            "last_sold_date": "12-05-2026",
            "image_url": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"
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
            "image_url": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"
        }
    ]

if "temp_packet_lots" not in st.session_state:
    st.session_state.temp_packet_lots = []
if "temp_loose_lots" not in st.session_state:
    st.session_state.temp_loose_lots = []

# --- 2. LOGO LINK CONFIGURATION AREA ---
# ⚠️ PASTE YOUR LOGO IMAGE URL LINK HERE
logo_url = "https://cdn.corenexis.com/f/y6S7Wj5sFjn.png" 

# --- 3. SIDEBAR NAVIGATION MENU ---
with st.sidebar:
    st.image(logo_url, width=100)
    st.markdown("### 👑 Priya Handicraft ERP")
    menu = st.radio(
        "Navigation Menu",
        ["📊 Dashboard", "📋 Listing", "📦 Inventory Management", "🧾 Invoice Creation (Locked)", "🚚 Order Status (Locked)", "📈 Reports (Locked)", "🔔 Notification (Locked)"]
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
    
    # Target Metrics Rows
    col1, col2, col3 = st.columns(3)
    col1.metric("Target Sales", "12,000")
    col2.metric("Achieved Sales", "10,000", delta="83.3% Achieved")
    col3.metric("Gap Remaining", "2,000", delta="-16.7%", delta_color="inverse")
    
    # Progress Bar (FIXED: Uses float 0.0 to 1.0 logic to prevent crashes)
    st.markdown("**Progress Breakdown**")
    st.progress(10000 / 12000)
    
    st.markdown("---")
    
    chart_col, stock_col = st.columns([2, 1])
    
    with chart_col:
        st.markdown("##### Monthly Sales Trend")
        chart_data = pd.DataFrame(
            [20, 40, 60, 80, 100, 120, 140, 160, 180],
            index=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            columns=["Sales"]
        )
        st.bar_chart(chart_data)
        
    with stock_col:
        st.markdown("##### Stock Status & Metrics")
        df_temp = pd.DataFrame(st.session_state.product_db)
        total_designs = len(df_temp)
        total_val = (df_temp['total_stock'] * df_temp['real_cost']).sum()
        out_of_stock = len(df_temp[df_temp['total_stock'] == 0])
        low_stock_count = len(df_temp[df_temp['total_stock'] < df_temp['alert_level']])
        
        st.write(f"**Total Designs:** {total_designs}")
        st.write(f"**Total Stock Value:** ₹{total_val:,.2f}")
        st.write(f"**Out of Stock:** :red[{out_of_stock}]")
        
        if low_stock_count > 0:
            if st.button(f"⚠️ View {low_stock_count} Low Stock Items"):
                st.warning("Low Stock Items List:")
                st.dataframe(df_temp[df_temp['total_stock'] < df_temp['alert_level']][['item_code', 'item_name', 'total_stock']])
                
        # 60 Days Dead Stock Automated Alert
        today = datetime.now()
        dead_stock_items = []
        for item in st.session_state.product_db:
            last_date = datetime.strptime(item['last_sold_date'], "%d-%m-%Y")
            if (today - last_date).days > 60:
                dead_stock_items.append(item)
                
        if len(dead_stock_items) > 0:
            st.error(f"📉 Dead Stock Alert: {len(dead_stock_items)} Items Idle for 60+ Days")
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

# ==================== 📋 LISTING MENU ====================
elif menu == "📋 Listing":
    st.title("Product Registry Listing")
    st.markdown("Use this menu form to create and register new design codes into your catalog.")
    
    with st.form("listing_form", clear_on_submit=True):
        img_url_input = st.text_input("Product Image URL Link (Optional)", value="https://cdn-icons-png.flaticon.com/512/3081/3081559.png")
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
        
        submit_btn = st.form_submit_with_rows_actions = st.form_submit_button("[ Save Design Registry ]")
        
        if submit_btn:
            if not selected_category or not item_name or selling_price <= 0:
                st.error("Please fill all required design entry fields properly.")
            else:
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
                    "image_url": img_url_input if img_url_input.strip() else "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"
                }
                st.session_state.product_db.append(new_design)
                st.success(f"Success: Registered {generated_code} into the database registry.")

# ==================== 📦 INVENTORY MANAGEMENT VIEW ====================
elif menu == "📦 Inventory Management":
    st.title("Inventory Management Hub")
    
    # 1. LOT STOCK ALLOCATION WORKSPACE PANEL
    st.markdown("### ➕ Allocate & Add Stock Batches")
    
    product_codes_list = [p['item_code'] for p in st.session_state.product_db]
    selected_product_code = st.selectbox("Select Registered Item Code to Update Stock *", [""] + product_codes_list)
    
    if selected_product_code:
        # Fetch current data record index reference
        p_idx = next(i for i, x in enumerate(st.session_state.product_db) if x['item_code'] == selected_product_code)
        target_product = st.session_state.product_db[p_idx]
        
        st.info(f"Updating Stock For: **{target_product['item_name']}** | Current Total Stock: {target_product['total_stock']} pcs")
        stock_type = st.radio("Stock Type Selector *", ["Packets", "Single Units", "Both"], index=2)
        
        # --- PACKETS LOT SECTION WITH RIGHT-SIDE ADD BUTTON ---
        if stock_type in ["Packets", "Both"]:
            st.markdown("##### Packets Allocation Matrix")
            p_col1, p_col2, p_col3 = st.columns([2, 2, 1])
            p_qty = p_col1.number_input("Packet Qty (Pcs/Pack)", min_value=0, step=1, key="p_qty_in")
            n_packs = p_col2.number_input("No. of Packets", min_value=0, step=1, key="n_packs_in")
            
            # Button aligned right to add lots instantly
            if p_col3.button("➕ Add More Packet Lot", use_container_width=True):
                if p_qty > 0 and n_packs > 0:
                    st.session_state.temp_packet_lots.append({"pcs_per_pack": p_qty, "num_packs": n_packs})
                    st.toast(f"Added batch: {n_packs} packs of {p_qty} pcs")
                    
            if st.session_state.temp_packet_lots:
                st.caption("Pending Packet Lots Array:")
                st.write(st.session_state.temp_packet_lots)
        
        # --- LOOSE UNITS SECTION WITH RIGHT-SIDE ADD BUTTON ---
        if stock_type in ["Single Units", "Both"]:
            st.markdown("##### Single Units Allocation")
            l_col1, l_col2 = st.columns([4, 1])
            loose_qty = l_col1.number_input("Loose Units Quantity", min_value=0, step=1, key="loose_in")
            
            # Button aligned right to add loose unit entries
            if l_col2.button("➕ Add More Unit Lot", use_container_width=True):
                if loose_qty > 0:
                    st.session_state.temp_loose_lots.append(loose_qty)
                    st.toast(f"Added loose unit batch: {loose_qty} pcs")
                    
            if st.session_state.temp_loose_lots:
                st.caption("Pending Loose Units Array lots:")
                st.write(st.session_state.temp_loose_lots)
        
        # --- LIVE COMPILATION ANALYSIS SHEET ENGINE ---
        calc_packet_sum = sum(lot['pcs_per_pack'] * lot['num_packs'] for lot in st.session_state.temp_packet_lots)
        calc_loose_sum = sum(st.session_state.temp_loose_lots)
        
        # Handle single on-screen inputs that weren't added to arrays yet
        if stock_type in ["Packets", "Both"] and 'p_qty_in' in locals():
            calc_packet_sum += (p_qty * n_packs) if len(st.session_state.temp_packet_lots) == 0 else 0
        if stock_type in ["Single Units", "Both"] and 'loose_in' in locals():
            calc_loose_sum += loose_qty if len(st.session_state.temp_loose_lots) == 0 else 0
            
        grand_total_calculated = calc_packet_sum + calc_loose_sum
        st.metric("Total Available Stock Calculated", f"{grand_total_calculated} pcs")
        
        # FINAL COMMIT SAVE BUTTON
        if st.button("💾 COMMIT ALLOCATED LOT STOCK TO LIVE INVENTORY"):
            st.session_state.product_db[p_idx]['packet_stock'] += calc_packet_sum
            st.session_state.product_db[p_idx]['loose_stock'] += calc_loose_sum
            st.session_state.product_db[p_idx]['total_stock'] += grand_total_calculated
            st.session_state.product_db[p_idx]['stock_type'] = stock_type
            
            # Flush temporary lot scratch arrays
            st.session_state.temp_packet_lots = []
            st.session_state.temp_loose_lots = []
            st.success(f"Stock successfully committed and updated for {selected_product_code}!")
            st.rerun()

    st.markdown("---")
    
    # 2. MASTER ACTIVE INVENTORY DATA SHEET TABLE WITH EMBEDDED PREVIEW IMAGES
    st.markdown("### 📋 Active Master Inventory Sheet")
    
    search_query = st.text_input("🔍 Search active stock sheet by Code, Name, or Category Filters...").lower().strip()
    df_master = pd.DataFrame(st.session_state.product_db)
    
    if search_query:
        df_filtered = df_master[
            df_master['item_code'].str.lower().str.contains(search_query) |
            df_master['item_name'].str.lower().str.contains(search_query) |
            df_master['category'].str.lower().str.contains(search_query)
        ]
    else:
        df_filtered = df_master

    # EXPORT BUTTONS SUBFRAME LAYER
    col_ex1, col_ex2 = st.columns(2)
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    col_ex1.download_button("📥 Download Excel Sheet (CSV Data)", data=csv_data, file_name="Live_Inventory_Balance.csv", mime="text/csv")
    
    # HTML Printing script helper to force layout image paths conversion into downloadable file prints
    html_report = f"<h2>Priya Handicraft Master Inventory Report</h2><table border='1'><tr><th>Image</th><th>Code</th><th>Item Name</th><th>Price</th><th>Total Stock</th></tr>"
    for _, r in df_filtered.iterrows():
        html_report += f"<tr><td><img src='{r['image_url']}' width='40'/></td><td>{r['item_code']}</td><td>{r['item_name']}</td><td>₹{r['selling_price']}</td><td>{r['total_stock']}</td></tr>"
    html_report += "</table>"
    col_ex2.download_button("📥 Download PDF Inventory Statement Report", data=html_report.encode('utf-8'), file_name="Inventory_Report.html", mime="text/html")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Streamlit data grid table layout view showing running images natively
    st.data_editor(
        df_filtered[['image_url', 'item_code', 'item_name', 'category', 'selling_price', 'total_stock', 'packet_stock', 'loose_stock']],
        column_config={
            "image_url": st.column_config.ImageColumn("Preview Image", width="medium"),
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
