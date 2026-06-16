import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZE DATABASE STATE (If not already present) ---
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
            "last_sold_date": "12-05-2026"
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
            "last_sold_date": "15-06-2026"
        },
        {
            "item_code": "CHOK001",
            "item_name": "Navratri Special Choker",
            "category": "Choker",
            "real_cost": 450.0,
            "selling_price": 900.0,
            "stock_type": "Single Units",
            "packet_stock": 0,
            "loose_stock": 12,
            "total_stock": 12,
            "alert_level": 50,
            "last_sold_date": "10-02-2026" # Dead stock example (>60 days)
        }
    ]

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 👑 Priya Handicraft ERP")
menu = st.sidebar.radio(
    "Navigation Menu",
    ["📊 Dashboard", "📦 Inventory Mgmt", "🧾 Invoice Creation (Locked)", "🚚 Order Status (Locked)", "📈 Reports (Locked)", "🔔 Notification (Locked)"]
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
    
    # Progress Bar
    st.markdown("**Progress Breakdown**")
    st.progress(10,000 / 12,000)
    
    st.markdown("---")
    
    # Monthly Sales Trend Chart & Stock Summary
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
        st.markdown("##### Stock Status")
        
        # Calculate dynamic metrics from session state database
        df_temp = pd.DataFrame(st.session_state.product_db)
        total_designs = len(df_temp)
        total_val = (df_temp['total_stock'] * df_temp['real_cost']).sum()
        out_of_stock = len(df_temp[df_temp['total_stock'] == 0])
        low_stock_count = len(df_temp[df_temp['total_stock'] < df_temp['alert_level']])
        
        st.write(f"**Total Designs:** {total_designs}")
        st.write(f"**Total Stock Value:** ₹{total_val:,.2f}")
        st.write(f"**Out of Stock:** :red[{out_of_stock}]")
        
        # Low stock popup handler
        if low_stock_count > 0:
            if st.button(f"⚠️ {low_stock_count} Low Stock Items Available"):
                st.warning("Low Stock Items List:")
                st.dataframe(df_temp[df_temp['total_stock'] < df_temp['alert_level']][['item_code', 'item_name', 'total_stock']])
                
        # Dead Stock Section (Calculated for 60 Days idle)
        today = datetime.now()
        dead_stock_items = []
        for item in st.session_state.product_db:
            last_date = datetime.strptime(item['last_sold_date'], "%d-%m-%y" if '-' in item['last_sold_date'] and len(item['last_sold_date'].split('-')[2])==2 else "%d-%m-%Y")
            if (today - last_date).days > 60:
                dead_stock_items.append(item)
                
        if len(dead_stock_items) > 0:
            st.error(f"📉 Dead Stock: {len(dead_stock_items)} Items Idle for 60+ Days")
            if st.button("Review Dead Stock"):
                st.dataframe(pd.DataFrame(dead_stock_items)[['item_code', 'item_name', 'last_sold_date', 'total_stock']])

    st.markdown("---")
    
    # Leaderboards
    lead_col1, lead_col2 = st.columns(2)
    with lead_col1:
        st.markdown("##### Most Selling Products")
        st.table(pd.DataFrame([{"Rank": "#1", "Product": "Fabric Tika 105", "Sales": "10,000"}, {"Rank": "#2", "Product": "Nath XYZ", "Sales": "8,500"}]))
    with lead_col2:
        st.markdown("##### Top 5 Customers")
        st.table(pd.DataFrame([{"Rank": "#1", "Customer": "Raj Traders", "Revenue": "₹12,50,000"}, {"Rank": "#2", "Customer": "Shree Ornaments", "Revenue": "₹8,20,000"}]))


# ==================== 📦 INVENTORY MANAGEMENT VIEW ====================
elif menu == "📦 Inventory Mgmt":
    st.title("Inventory Hub")
    
    form_col, list_col = st.columns([2, 3])
    
    with form_col:
        st.markdown("#### Add New Product Form")
        
        # Image input component placeholder
        st.file_uploader("Product Image (Optional)", type=["png", "jpg", "jpeg"])
        
        selected_category = st.selectbox("Category *", [""] + categories_list)
        
        # Auto Code Generation Logic
        generated_code = ""
        if selected_category:
            short_prefix = selected_category[:4].upper().replace(" ", "")
            match_count = sum(1 for x in st.session_state.product_db if x['category'] == selected_category)
            generated_code = f"{short_prefix}{str(match_count + 1).padStart(3, '0')}" if hasattr(str, 'padStart') else f"{short_prefix}{str(match_count + 1).zfill(3)}"
            
        st.text_input("Item Code (Auto)", value=generated_code, disabled=True)
        
        item_name = st.text_input("Item Name *")
        
        cost_col, sell_col = st.columns(2)
        real_cost = cost_col.number_input("Real Cost (₹)", min_value=0.0, step=1.0)
        selling_price = sell_col.number_input("Selling Price (₹)*", min_value=0.0, step=1.0)
        
        # Live Margin Display Tracker
        if selling_price > 0:
            profit = selling_price - real_cost
            margin_pct = (profit / real_cost * 100) if real_cost > 0 else 100.0
            st.info(f"💡 Margin: {margin_pct:.1f}% | Profit: ₹{profit:.2f}")
            
        stock_type = st.radio("Stock Type Selector *", ["Packets", "Single Units", "Both"])
        
        # Dynamic Calculator Logic Fields Matrix
        p_total = 0
        l_total = 0
        
        if stock_type in ["Packets", "Both"]:
            st.markdown("**Packets Allocation Matrix**")
            p_qty = st.number_input("Packet Qty (Pcs/Pack)", min_value=0, step=1)
            n_packs = st.number_input("No. of Packets", min_value=0, step=1)
            p_total = p_qty * n_packs
            
        if stock_type in ["Single Units", "Both"]:
            st.markdown("**Single Units Allocation**")
            l_total = st.number_input("Loose Units Quantity", min_value=0, step=1)
            
        grand_total_stock = p_total + l_total
        st.metric("Total Available Stock Calculated", f"{grand_total_stock} pcs")
        
        alert_level = st.number_input("Min Stock Alert Level *", min_value=0, value=100)
        
        # Form Submission Logic
        if st.button("[ Save ]"):
            if not selected_category or not item_name or selling_price <= 0:
                st.error("Please fill all required inputs correctly.")
            else:
                new_item = {
                    "item_code": generated_code,
                    "item_name": item_name,
                    "category": selected_category,
                    "real_cost": real_cost,
                    "selling_price": selling_price,
                    "stock_type": stock_type,
                    "packet_stock": p_total,
                    "loose_stock": l_total,
                    "total_stock": grand_total_stock,
                    "alert_level": alert_level,
                    "last_sold_date": datetime.now().strftime("%d-%m-%Y")
                }
                st.session_state.product_db.append(new_item)
                st.success(f"Successfully saved {generated_code}!")
                st.rerun()

    with list_col:
        st.markdown("#### Current Inventory List")
        
        # Master Search Box Filter Engine
        search_query = st.text_input("🔍 Search inventory by Code, Name, or Category...").lower().strip()
        
        df_master = pd.DataFrame(st.session_state.product_db)
        
        # Apply filter live mapping input string rules
        if search_query:
            df_filtered = df_master[
                df_master['item_code'].str.lower().str.contains(search_query) |
                df_master['item_name'].str.lower().str.contains(search_query) |
                df_master['category'].str.lower().str.contains(search_query)
            ]
        else:
            df_filtered = df_master
            
        # Display clean view data matrix table layout
        st.dataframe(
            df_filtered[['item_code', 'item_name', 'category', 'selling_price', 'total_stock', 'packet_stock', 'loose_stock']],
            use_container_width=True
        )
        
        # Export Infrastructure Triggers Download Pipelines
        col_ex1, col_ex2 = st.columns(2)
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        col_ex1.download_button("📥 Export CSV / Excel", data=csv_data, file_name="Inventory_Master.csv", mime="text/csv")
        col_ex2.button("📥 Export PDF Report", help="Generates layout summary prints details.")
