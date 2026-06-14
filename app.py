import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# ==============================================================================
# 1. CORE SYSTEM CONFIGURATION & THEMING
# ==============================================================================
st.set_page_config(
    page_title="Priya Handicraft Enterprise ERP",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Priya Handicraft Elegant Color Theme (Deep Royal Indigo Blue & Gold)
st.markdown("""
    <style>
        .reportview-container .main .block-container { padding-top: 2rem; }
        .stButton>button { 
            background-color: #1A365D; color: white; border-radius: 6px; 
            font-weight: bold; border: none; padding: 0.5rem 1rem;
        }
        .stButton>button:hover { background-color: #2b6cb0; color: white; }
        .metric-card { 
            background-color: #F7FAFC; border: 1px solid #E2E8F0; 
            padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SEEDING SYSTEM MOCK DATA (Simulating Live Cloud Database Infrastructure)
# ==============================================================================
if 'inventory_db' not in st.session_state:
    st.session_state.inventory_db = pd.DataFrame([
        {"Item Code": "OX-TIKA-09", "Category": "Oxidized Tika", "Cost Price": 60.0, "Wholesale Price": 120.0, "Pack Size": 25, "Bulk Packs": 12, "Loose Units": 18, "Alert Limit": 5},
        {"Item Code": "FAB-EAR-02", "Category": "Fabric Earring", "Cost Price": 40.0, "Wholesale Price": 90.0, "Pack Size": 12, "Bulk Packs": 5, "Loose Units": 0, "Alert Limit": 5}
    ])

if 'orders_db' not in st.session_state:
    seven_days_ago = datetime.now() - timedelta(days=7)
    st.session_state.orders_db = pd.DataFrame([
        {"Invoice ID": "INV-1024", "Customer": "Ramesh Bhai Wholesale", "Subtotal": 7500.0, "GST Base": 2000.0, "GST Amt": 360.0, "Freight": 350.0, "Packing": 150.0, "Grand Total": 8360.0, "Payment State": "Fully Paid", "Fulfillment State": "Dispatched", "Logistics Date": seven_days_ago, "Net Profit": 4320.0},
        {"Invoice ID": "INV-1025", "Customer": "Priya Shah Retail", "Subtotal": 360.0, "GST Base": 0.0, "GST Amt": 0.0, "Freight": 0.0, "Packing": 0.0, "Grand Total": 360.0, "Payment State": "Pending Payment", "Fulfillment State": "In Packing", "Logistics Date": datetime.now(), "Net Profit": 0.0}
    ])

# ==============================================================================
# 3. ENTERPRISE SIDEBAR NAVIGATION BAR (ZipERP Layout Blueprint)
# ==============================================================================
st.sidebar.markdown("<h2 style='color:#1A365D; text-align:center; font-family:serif;'>Priya Handicraft</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#E53E3E; text-align:center; font-size:11px; font-weight:bold; letter-spacing:1px;'>IMITATION JEWELLERY MANUFACTURER</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "SYSTEM MANAGEMENT MODULES",
    ["📊 Executive MIS Dashboard", "📦 Central Inventory Control", "📄 New Invoice Desk", "💳 Revenue Reporting Desk"]
)

# ==============================================================================
# MODULE A: EXECUTIVE MIS DASHBOARD
# ==============================================================================
if app_mode == "📊 Executive MIS Dashboard":
    st.title("Enterprise Management Information System (MIS)")
    
    # Financial Analytics Core - Compute Pure Realized Gains (Paid & Dispatched/Delivered)
    annual_target = 1000000.0
    realized_profit = float(st.session_state.orders_db[
        (st.session_state.orders_db["Payment State"] == "Fully Paid") & 
        (st.session_state.orders_db["Fulfillment State"].isin(["Dispatched", "Delivered"]))
    ]["Net Profit"].sum())
    deficit = annual_target - realized_profit
    completion_percentage = min((realized_profit / annual_target), 1.0)
    
    st.markdown("### 📈 Annual Profit Target Monitor")
    col_target1, col_target2, col_target3 = st.columns([2, 1, 1])
    with col_target1:
        st.markdown(f"**Fiscal Progress:** ₹{realized_profit:,.2f} achieved / Target ₹{annual_target:,.2f}")
        st.progress(completion_percentage)
    with col_target2:
        st.metric("Realized Earnings", f"₹{realized_profit:,.2f}", delta=f"{completion_percentage*100:.1f}%")
    with col_target3:
        st.metric("Target Deficit Variance", f"₹{deficit:,.2f}")
        
    st.markdown("---")
    
    # Inventory & Outstanding Balances Summary Grids
    col_inv, col_fin = st.columns(2)
    with col_inv:
        st.markdown("<div class='metric-card'><h4>📦 Inventory Health Ledger</h4>", unsafe_allow_html=True)
        total_skus = len(st.session_state.inventory_db)
        low_stock_count = len(st.session_state.inventory_db[st.session_state.inventory_db["Loose Units"] == 0])
        st.write(f"• Total System Monitored SKUs: **{total_skus}**")
        st.write(f"• Critical Stock Reorders Needed: <span style='color:red; font-weight:bold;'>{low_stock_count} SKUs</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_fin:
        st.markdown("<div class='metric-card'><h4>💳 Aging Receivables Traffic</h4>", unsafe_allow_html=True)
        total_pending_cash = float(st.session_state.orders_db[st.session_state.orders_db["Payment State"] == "Pending Payment"]["Grand Total"].sum())
        total_settled_cash = float(st.session_state.orders_db[st.session_state.orders_db["Payment State"] == "Fully Paid"]["Grand Total"].sum())
        st.write(f"• Total Remittances Settled: **₹{total_settled_cash:,.2f}**")
        st.write(f"• Total Outstanding Dues: <span style='color:red; font-weight:bold;'>To Collect: ₹{total_pending_cash:,.2f}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Automated Tracking & Courier Alerts Engine
    st.markdown("### ⚠️ Automated Core System Notifications & Alerts")
    for idx, row in st.session_state.orders_db.iterrows():
        if row["Fulfillment State"] == "Dispatched" and (datetime.now() - row["Logistics Date"]).days >= 7:
            st.warning(f"⏳ **LOGISTICS ALERT:** Invoice **#{row['Invoice ID']}** ({row['Customer']}) has been in **[DISPATCHED]** status for 7+ days. Action Required: Confirm parcel arrival with transport carrier.")
            col_action1, col_action2 = st.columns([1, 6])
            with col_action1:
                if st.button("Mark Delivered", key=f"del_{idx}"):
                    st.session_state.orders_db.at[idx, "Fulfillment State"] = "Delivered"
                    st.rerun()

# ==============================================================================
# MODULE B: CENTRAL INVENTORY CONTROL
# ==============================================================================
elif app_mode == "📦 Central Inventory Control":
    st.title("Centralized Product Repository")
    
    # Rapid Search Filtering Bar
    search_term = st.text_input("🔍 Execute Search by SKU Item Code, Product Grouping, or Category Key...")
    
    # Add Damaged Stock Allocation Feature
    st.markdown("### ⚠️ Process Stock Adjustments / Write-Off Damages")
    col_dmg1, col_dmg2, col_dmg3 = st.columns(3)
    with col_dmg1:
        sku_to_dmg = st.selectbox("Select Target Product Code", st.session_state.inventory_db["Item Code"].unique())
    with col_dmg2:
        qty_to_dmg = st.number_input("Damaged Pieces Found (Deducted from Loose Box Only)", min_value=1, step=1)
    with col_dmg3:
        st.write("</br>", unsafe_allow_html=True)
        if st.button("Execute Damage Deduction"):
            idx = st.session_state.inventory_db[st.session_state.inventory_db["Item Code"] == sku_to_dmg].index[0]
            current_loose = st.session_state.inventory_db.at[idx, "Loose Units"]
            if current_loose >= qty_to_dmg:
                st.session_state.inventory_db.at[idx, "Loose Units"] -= qty_to_dmg
                st.success(f"Successfully deducted {qty_to_dmg} units from {sku_to_dmg} Loose Stock.")
                st.rerun()
            else:
                st.error("Insufficient loose inventory units to execute damage write-off.")

    st.markdown("---")
    st.markdown("#### Live Godown Ledger Records")
    
    # Filter display data based on search input
    display_df = st.session_state.inventory_db
    if search_term:
        display_df = display_df[display_df["Item Code"].str.contains(search_term, case=False) | display_df["Category"].str.contains(search_term, case=False)]
        
    st.dataframe(display_df, use_container_width=True)

# ==============================================================================
# MODULE C: NEW INVOICE DESK
# ==============================================================================
elif app_mode == "📄 New Invoice Desk":
    st.title("Sales Billing Desk")
    
    col_cust1, col_cust2 = st.columns(2)
    with col_cust1:
        customer_input = st.text_input("Client Account Name Description", value="New Wholesale Buyer")
    with col_cust2:
        invoice_id_gen = f"INV-{len(st.session_state.orders_db) + 1024}"
        st.markdown(f"**Assigned Billing ID:** `{invoice_id_gen}`")
        
    st.markdown("---")
    st.markdown("#### Basket Line Items Input Grid")
    
    col_li1, col_li2, col_li3, col_li4 = st.columns(4)
    with col_li1:
        target_sku = st.selectbox("Item SKU Identification Link", st.session_state.inventory_db["Item Code"].unique())
        sku_data = st.session_state.inventory_db[st.session_state.inventory_db["Item Code"] == target_sku].iloc[0]
    with col_li2:
        packs_ordered = st.number_input(f"Bulk Packets Ordered (Packs of {sku_data['Pack Size']})", min_value=0, step=1)
    with col_li3:
        loose_ordered = st.number_input("Loose Individual Pieces Ordered", min_value=0, step=1)
    with col_li4:
        custom_price = st.number_input("Wholesale Unit Base Rate Override (Per Piece)", value=float(sku_data["Wholesale Price"]))

    # Calculations Logic Sequence Engine
    total_pieces = (packs_ordered * sku_data["Pack Size"]) + loose_ordered
    item_subtotal = total_pieces * custom_price
    
    st.markdown("---")
    st.markdown("#### Dynamic Financial Freight & Customs Layering")
    col_tax1, col_tax2, col_tax3 = st.columns(3)
    with col_tax1:
        assessable_gst_base = st.number_input("Custom Assessable GST Base Amount Value", min_value=0.0, max_value=float(item_subtotal), value=0.0)
        calculated_gst_value = assessable_gst_base * 0.18  # Automated 18% GST Layering rule
        st.write(f"Computed Custom GST Layer (18%): **₹{calculated_gst_value:,.2f}**")
    with col_tax2:
        packing_fees = st.number_input("Pass-Through Internal Packaging Fees Charged", min_value=0.0, value=0.0)
    with col_tax3:
        freight_charges = st.number_input("Pass-Through Courier / Freight Shipping Fees Charged", min_value=0.0, value=0.0)
        
    grand_total_calculated = item_subtotal + calculated_gst_value + packing_fees + freight_charges
    st.markdown(f"### 🧾 FINAL PAYABLE GRAND TOTAL: **₹{grand_total_calculated:,.2f}**")
    
    st.markdown("---")
    st.markdown("#### Operational System Tracking Tags Configuration")
    col_tag1, col_tag2 = st.columns(2)
    with col_tag1:
        payment_tag = st.selectbox("Assign Current Financial Payment Status Tag", ["Draft", "No Advance", "Advance Received", "Pending Payment", "Pending Shipping Payment", "Fully Paid"])
    with col_tag2:
        fulfillment_tag = st.selectbox("Assign Current Fulfillment & Logistics Logistics Status Tag", ["Pending Packing", "In Packing", "Packed - Ready to Ship", "Dispatched", "Delivered"])
        
    if st.button("Commit Ledger Transaction & Issue Invoice"):
        # Realized net profit calculation formula injection rule
        total_cost_basis = total_pieces * sku_data["Cost Price"]
        calculated_profit_basis = item_subtotal - total_cost_basis
        
        new_order_entry = {
            "Invoice ID": invoice_id_gen,
            "Customer": customer_input,
            "Subtotal": item_subtotal,
            "GST Base": assessable_gst_base,
            "GST Amt": calculated_gst_value,
            "Freight": freight_charges,
            "Packing": packing_fees,
            "Grand Total": grand_total_calculated,
            "Payment State": payment_tag,
            "Fulfillment State": fulfillment_tag,
            "Logistics Date": datetime.now(),
            "Net Profit": calculated_profit_basis if (payment_tag == "Fully Paid" and fulfillment_tag in ["Dispatched", "Delivered"]) else 0.0
        }
        
        # Deduct physical item boxes counts values from inventory master framework
        inv_idx = st.session_state.inventory_db[st.session_state.inventory_db["Item Code"] == target_sku].index[0]
        st.session_state.inventory_db.at[inv_idx, "Bulk Packs"] -= packs_ordered
        st.session_state.inventory_db.at[inv_idx, "Loose Units"] -= loose_ordered
        
        # Append record entries
        st.session_state.orders_db = pd.concat([st.session_state.orders_db, pd.DataFrame([new_order_entry])], ignore_index=True)
        st.sidebar.success(f"Invoice Transaction Record #{invoice_id_gen} committed successfully!")
        st.rerun()

# ==============================================================================
# MODULE D: REVENUE REPORTING DESK
# ==============================================================================
elif app_mode == "💳 Revenue Reporting Desk":
    st.title("Data Export Control Panel")
    st.markdown("Review records or extract native formatting documents for audit processes instantly below.")
    
    st.dataframe(st.session_state.orders_db, use_container_width=True)
    
    # Excel binary byte stream generation logic code block
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        st.session_state.orders_db.to_excel(writer, sheet_name='Master Invoices Log', index=False)
    excel_data = excel_buffer.getvalue()
    
    st.markdown("#### Execute Native System Exports")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Download Master Spreadsheet File (.XLSX)",
            data=excel_data,
            file_name=f"Priya_Handicrafts_Master_Ledger_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        st.info("💡 **System Integration Note:** PDF invoice copies can be generated natively by printing or saving direct dashboard matrix frames through unified browser extensions dynamically.")
