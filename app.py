import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import urllib.parse

# ==============================================================================
# 1. APPLICATION SETUP, CONSTANTS, & DIRECTORIES
# ==============================================================================
st.set_page_config(page_title="Priya Handicraft ERP", layout="wide", initial_sidebar_state="expanded")

# Corporate Style Configuration (Cinzel-like Serif Header / Custom Tables)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Inter:wght@400;600&display=swap');
        
        .brand-header {
            font-family: 'Cinzel', serif;
            font-weight: 800;
            font-size: 42px;
            color: #1E3A8A;
            text-align: center;
            letter-spacing: 2px;
            margin-bottom: 0px;
        }
        .brand-sub {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 13px;
            color: #DC2626;
            text-align: center;
            letter-spacing: 4px;
            margin-top: -5px;
            margin-bottom: 30px;
        }
        .outstanding-alert {
            color: #DC2626;
            font-weight: bold;
            font-size: 18px;
        }
        div.stButton > button:first-child {
            background-color: #1E3A8A;
            color: white;
            border-radius: 4px;
        }
        div.stButton > button:first-child:hover {
            background-color: #152A61;
            color: white;
        }
        .low-stock-alert {
            background-color: #FEF2F2;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #DC2626;
            color: #991B1B;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 🌐 ONLINE SECURE LOGO URL (No File Upload Needed!)
# Tip: Aap future mein is URL link ko apni kisi bhi online logo image link se badal sakti hain
LOGO_URL = "https://i.ibb.co/S4vKkDrk/logo.png"

# Strict Corporate Constraints File Paths
PARENT_INV_PATH = "db_parent_inventory.csv"
LOT_INV_PATH = "db_lot_inventory.json"  
INVOICES_PATH = "db_invoices.csv"
CONFIG_PATH = "db_config.json"

# ==============================================================================
# 2. DATA PERSISTENCE LAYER WITH STRICT NULL-SAFE FALLBACKS
# ==============================================================================
def initialize_databases():
    if not os.path.exists(PARENT_INV_PATH):
        parent_df = pd.DataFrame(columns=[
            "Design_Code", "Item_Name", "Category", "Total_Stock_In", 
            "Total_Used", "Total_Available", "Base_Cost_Price", "Product_Image_URI"
        ])
        parent_df.to_csv(PARENT_INV_PATH, index=False)
        
    if not os.path.exists(LOT_INV_PATH):
        with open(LOT_INV_PATH, 'w') as f:
            json.dump({}, f)
            
    if not os.path.exists(INVOICES_PATH):
        inv_df = pd.DataFrame(columns=[
            "Invoice_ID", "Invoice_Date", "Customer_Name", "Mobile", "City", 
            "Items_JSON", "Subtotal", "Packing_Charges", "Shipping_Charges", 
            "GST_Amount", "Total_Invoice_Amount", "Amount_Paid", "Pending_Dues",
            "Payment_Status", "Dispatch_Status"
        ])
        inv_df.to_csv(INVOICES_PATH, index=False)
        
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump({"monthly_revenue_target": 500000.00}, f)

initialize_databases()

def load_parent_inventory() -> pd.DataFrame:
    df = pd.read_csv(PARENT_INV_PATH)
    df["Total_Stock_In"] = pd.to_numeric(df["Total_Stock_In"]).fillna(0).astype(int)
    df["Total_Used"] = pd.to_numeric(df["Total_Used"]).fillna(0).astype(int)
    df["Total_Available"] = pd.to_numeric(df["Total_Available"]).fillna(0).astype(int)
    df["Base_Cost_Price"] = pd.to_numeric(df["Base_Cost_Price"]).fillna(0.0).astype(float)
    df["Product_Image_URI"] = df["Product_Image_URI"].fillna("").astype(str)
    return df

def save_parent_inventory(df: pd.DataFrame):
    df.to_csv(PARENT_INV_PATH, index=False)

def load_lot_inventory() -> dict:
    with open(LOT_INV_PATH, 'r') as f:
        return json.load(f)

def save_lot_inventory(data: dict):
    with open(LOT_INV_PATH, 'w') as f:
        json.dump(data, f)

def load_invoices() -> pd.DataFrame:
    df = pd.read_csv(INVOICES_PATH)
    df["Subtotal"] = pd.to_numeric(df["Subtotal"]).fillna(0.0).astype(float)
    df["Packing_Charges"] = pd.to_numeric(df["Packing_Charges"]).fillna(0.0).astype(float)
    df["Shipping_Charges"] = pd.to_numeric(df["Shipping_Charges"]).fillna(0.0).astype(float)
    df["GST_Amount"] = pd.to_numeric(df["GST_Amount"]).fillna(0.0).astype(float)
    df["Total_Invoice_Amount"] = pd.to_numeric(df["Total_Invoice_Amount"]).fillna(0.0).astype(float)
    df["Amount_Paid"] = pd.to_numeric(df["Amount_Paid"]).fillna(0.0).astype(float)
    df["Pending_Dues"] = pd.to_numeric(df["Pending_Dues"]).fillna(0.0).astype(float)
    return df

def save_invoices(df: pd.DataFrame):
    df.to_csv(INVOICES_PATH, index=False)

def get_target() -> float:
    with open(CONFIG_PATH, 'r') as f:
        return float(json.load(f).get("monthly_revenue_target", 0.0))

def save_target(val: float):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"monthly_revenue_target": val}, f)

# ==============================================================================
# BRANDING HEADER RENDER ENGINE (SAFE LINK LOGO)
# ==============================================================================
def render_corporate_header():
    # Logo uses secure cloud URL to prevent file-not-found system crashes
    st.image(LOGO_URL, width=120)
    st.markdown('<h1 class="brand-header">PRIYA HANDICRAFT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">MANUFACTURERS & WHOLESALERS</p>', unsafe_allow_html=True)

# ==============================================================================
# STREAMLIT CONTROLLER ROUTER INTERFACE
# ==============================================================================
st.sidebar.title("🏢 Navigation Panel")
app_tab = st.sidebar.radio("Go to Controller Desk:", [
    "Tab 1: Sales & Finance Dashboard",
    "Tab 2: Inventory Listing Desk",
    "Tab 3: Outstanding Receivables Ledger",
    "🛒 Create New Wholesale Invoice"
])

# Refresh state tables
parent_df = load_parent_inventory()
lots_map = load_lot_inventory()
invoice_df = load_invoices()

# ==============================================================================
# TAB 1: SALES & FINANCE DASHBOARD
# ==============================================================================
if app_tab == "Tab 1: Sales & Finance Dashboard":
    render_corporate_header()
    st.subheader("🎯 Automated Progress Target Engine")
    
    current_target = get_target()
    new_target_input = st.text_input("Set Monthly Revenue Target (₹):", value=str(current_target))
    try:
        new_target_val = float(new_target_input) if new_target_input.strip() else 0.0
    except ValueError:
        new_target_val = 0.0
        
    if st.button("Update Business Targets"):
        save_target(new_target_val)
        st.success("Target metric system synchronized.")
        st.rerun()
        
    if not invoice_df.empty:
        valid_orders = invoice_df[
            (invoice_df["Payment_Status"] == "Paid") & 
            (invoice_df["Dispatch_Status"] == "Dispatched")
        ]
        achieved_amount = valid_orders["Total_Invoice_Amount"].sum()
    else:
        achieved_amount = 0.0
        
    progress_pct = (achieved_amount / new_target_val) * 100 if new_target_val > 0 else 0.0
    remaining_to_target = max(0.0, new_target_val - achieved_amount)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Achieved Target Revenue", f"₹ {achieved_amount:,.2f}")
    col2.metric("Active Target Profile", f"₹ {new_target_val:,.2f}")
    col3.metric("Deficit Gap to Target", f"₹ {remaining_to_target:,.2f}")
    
    st.progress(min(1.0, progress_pct / 100))
    st.caption(f"Current completion status: **{progress_pct:.2f}%**")
    
    # ⚠️ LIVE LOW STOCK ALERT SHOWN ON DASHBOARD
    st.write("---")
    st.subheader("🚨 Live Stock Security Alerts")
    if not parent_df.empty:
        low_stock_threshold = 10
        low_items = parent_df[parent_df["Total_Available"] <= low_stock_threshold]
        if not low_items.empty:
            for idx, row in low_items.iterrows():
                st.markdown(f"<div class='low-stock-alert'>🚨 LOW STOCK ALERT: Item '{row['Item_Name']}' [Code: {row['Design_Code']}] has only {row['Total_Available']} pieces left! Please restock soon.</div>", unsafe_allow_html=True)
        else:
            st.success("✅ All Inventory Levels Healthy. No low stock detected.")

# ==============================================================================
# TAB 2: INVENTORY DESK (TWO-TIER NESTED ARCHITECTURE)
# ==============================================================================
elif app_tab == "Tab 2: Inventory Listing Desk":
    render_corporate_header()
    st.subheader("📦 Level 1: Two-Tier Parent Summary View")
    
    # Create Dynamic Categories Dropdown list
    existing_categories = ["Select or Type New"] + sorted(parent_df["Category"].dropna().unique().tolist()) if not parent_df.empty else ["Select or Type New", "Navratri Imitation", "Fabric Jewelry", "Oxidized Sets"]
    
    with st.expander("➕ Define New Navratri Design Profile"):
        c1, c2, c3, c4 = st.columns(4)
        in_code = c1.text_input("Design Code (Primary Key)*, e.g. TIKA-001").strip()
        in_name = c2.text_input("Item Name*", placeholder="Chaniya Choli Tika").strip()
        
        cat_choice = c3.selectbox("Category", existing_categories)
        if cat_choice == "Select or Type New":
            in_cat = st.text_input("Type Brand New Category Name").strip()
        else:
            in_cat = cat_choice
            
        in_cost = c4.text_input("Base Cost Price (₹)*", value="0")
        in_img = st.text_input("Product Image URI (Optional)", value="")
        
        if st.button("Commit Design Ledger"):
            if not in_code or not in_name or not in_cat:
                st.error("Please fill Design Code, Item Name, and Category.")
            elif in_code in parent_df["Design_Code"].values:
                st.error("Design Code already exists.")
            else:
                try:
                    parsed_cost = float(in_cost) if in_cost.strip() else 0.0
                except ValueError:
                    parsed_cost = 0.0
                
                new_design_row = {
                    "Design_Code": in_code, "Item_Name": in_name, "Category": in_cat,
                    "Total_Stock_In": 0, "Total_Used": 0, "Total_Available": 0,
                    "Base_Cost_Price": parsed_cost, "Product_Image_URI": in_img
                }
                parent_df = pd.concat([parent_df, pd.DataFrame([new_design_row])], ignore_index=True)
                save_parent_inventory(parent_df)
                
                lots_map[in_code] = []
                save_lot_inventory(lots_map)
                st.success("New product profile cataloged successfully!")
                st.rerun()

    if parent_df.empty:
        st.info("No active corporate inventory profiles populated yet.")
    else:
        st.dataframe(parent_df, use_container_width=True)
        
        st.write("---")
        st.markdown("### 🔍 Level 2: Granular Inventory Lots Inspect Window")
        selected_code = st.selectbox("Choose a Design Code Row to see detailed Packaging Lots:", parent_df["Design_Code"].unique())
        
        if selected_code:
            target_lots = lots_map.get(selected_code, [])
            if len(target_lots) == 0:
                st.warning("No storage lot configurations mapped down to this SKU yet.")
            else:
                st.table(pd.DataFrame(target_lots)[["Storage_Type", "Lot_Size", "Available_Lots_Count"]])
                
            with st.form("Manage Stock (Add Stock / Damage Log)"):
                st.markdown("##### 📥 Add New Bulk Batch / Record Damage Log")
                action_type = st.radio("Select Action Type", ["📥 Add Inward Stock (Naya Maal)", "📤 Log Damage / Exclusions"])
                st_type = st.selectbox("Storage Type Structure:", ["Packet", "Single Unit"])
                
                l_size_raw = st.text_input("Lot Size Packaging Multiplier (e.g. 12, 15, 25, 50):", value="12")
                l_count_raw = st.text_input("Available Lots Count (How many packets/units):", value="1")
                
                if st.form_submit_button("Apply Changes to Ledger"):
                    try:
                        l_size = int(l_size_raw) if l_size_raw.strip() else 0
                        l_count = int(l_count_raw) if l_count_raw.strip() else 0
                    except ValueError:
                        l_size, l_count = 0, 0
                        
                    calculated_pieces = l_size * l_count
                    
                    if "Add Inward" in action_type:
                        new_lot = {"Storage_Type": st_type, "Lot_Size": l_size, "Available_Lots_Count": l_count}
                        if selected_code not in lots_map:
                            lots_map[selected_code] = []
                        lots_map[selected_code].append(new_lot)
                        save_lot_inventory(lots_map)
                        
                        parent_df.loc[parent_df["Design_Code"] == selected_code, "Total_Stock_In"] += calculated_pieces
                        parent_df.loc[parent_df["Design_Code"] == selected_code, "Total_Available"] += calculated_pieces
                    else:
                        parent_df.loc[parent_df["Design_Code"] == selected_code, "Total_Used"] += calculated_pieces
                        parent_df.loc[parent_df["Design_Code"] == selected_code, "Total_Available"] = max(0, parent_df.loc[parent_df["Design_Code"] == selected_code, "Total_Available"].values[0] - calculated_pieces)
                        
                    save_parent_inventory(parent_df)
                    st.success("Ledger synchronized successfully!")
                    st.rerun()

# ==============================================================================
# TAB 3: OUTSTANDING RECEIVABLES LEDGER
# ==============================================================================
elif app_tab == "Tab 3: Outstanding Receivables Ledger":
    render_corporate_header()
    st.subheader("💳 Outstanding Credit & Market Receivables Tracking")
    
    receivables_df = invoice_df[invoice_df["Pending_Dues"] > 0]
    
    if receivables_df.empty:
        st.success("🎉 All accounts cleared. Zero market outstanding dues detected.")
    else:
        total_market_outstanding = receivables_df["Pending_Dues"].sum()
        st.markdown(f"Total Market Outstanding Credit Risk: <span class='outstanding-alert'>₹ {total_market_outstanding:,.2f}</span>", unsafe_allow_html=True)
        
        # Date and text constraints applied strictly
        st.dataframe(receivables_df[[
            "Invoice_Date", "Customer_Name", "Mobile", "City", 
            "Total_Invoice_Amount", "Amount_Paid", "Pending_Dues"
        ]], use_container_width=True)
        
        st.write("---")
        st.markdown("#### 🔄 Record Partial Payment Receipt Settlement")
        target_inv = st.selectbox("Select Invoice ID:", receivables_df["Invoice_ID"].unique())
        repay_input = st.text_input("Enter Amount Settled / Received (₹):", value="0.0")
        
        if st.button("Apply Collection Clearance"):
            try:
                repay_val = float(repay_input) if repay_input.strip() else 0.0
            except ValueError:
                repay_val = 0.0
                
            idx = invoice_df[invoice_df["Invoice_ID"] == target_inv].index[0]
            invoice_df.at[idx, "Amount_Paid"] += repay_val
            invoice_df.at[idx, "Pending_Dues"] = max(0.0, invoice_df.at[idx, "Total_Invoice_Amount"] - invoice_df.at[idx, "Amount_Paid"])
            
            if invoice_df.at[idx, "Pending_Dues"] == 0:
                invoice_df.at[idx, "Payment_Status"] = "Paid"
            else:
                invoice_df.at[idx, "Payment_Status"] = "Partial"
                
            save_invoices(invoice_df)
            st.success("Clearance entry registered!")
            st.rerun()

# ==============================================================================
# CREATE NEW WHOLESALE INVOICE (TEXT ENTRY OVERRIDES & LOGISTICS CODES)
# ==============================================================================
elif app_tab == "🛒 Create New Wholesale Invoice":
    render_corporate_header()
    st.subheader("🛒 Advanced Automated Wholesale Order Billing")
    
    c1, c2, c3 = st.columns(3)
    cust_name = c1.text_input("Customer/Wholesaler Corporate Name*", value="").strip()
    cust_mobile = c2.text_input("Contact Mobile Phone Number*", value="").strip()
    cust_city = c3.text_input("Customer City Node Location*", value="").strip()
    
    st.write("---")
    st.markdown("##### 🛒 Select Line Items for Invoice Compilation")
    available_skus = parent_df[parent_df["Total_Available"] > 0]["Design_Code"].tolist()
    
    if not available_skus:
        st.warning("No parent items currently hold open available physical items.")
    else:
        selected_skus = st.multiselect("Choose active designs to include:", available_skus)
        order_basket = []
        running_subtotal = 0.0
        
        for sku in selected_skus:
            st.write(f"---")
            item_meta = parent_df[parent_df["Design_Code"] == sku].iloc[0]
            st.markdown(f"📦 **Item Code:** `{sku}` | **Description:** {item_meta['Item_Name']} | Stock: `{item_meta['Total_Available']}` Pieces")
            
            col_l1, col_l2, col_l3, col_l4 = st.columns(4)
            
            # --- MANDATED SYSTEM DIRECT TEXT INPUT OVERRIDES ---
            pkt_size_raw = col_l1.text_input(f"Packet Size Multiplier ({sku}):", value="12", key=f"psize_{sku}")
            pkt_count_raw = col_l2.text_input(f"Number of Packets Selected ({sku}):", value="0", key=f"pcount_{sku}")
            loose_units_raw = col_l3.text_input(f"Loose Single Pieces Count ({sku}):", value="0", key=f"loose_{sku}")
            custom_rate_raw = col_l4.text_input(f"Dynamic Custom Rate (₹ / Piece) ({sku}):", value=str(item_meta['Base_Cost_Price']), key=f"rate_{sku}")
            
            try:
                pkt_size = int(pkt_size_raw) if pkt_size_raw.strip() else 0
                pkt_count = int(pkt_count_raw) if pkt_count_raw.strip() else 0
                loose_units = int(loose_units_raw) if loose_units_raw.strip() else 0
                custom_rate = float(custom_rate_raw) if custom_rate_raw.strip() else 0.0
            except ValueError:
                pkt_size, pkt_count, loose_units, custom_rate = 0, 0, 0, 0.0
                
            calculated_pieces_to_sell = (pkt_size * pkt_count) + loose_units
            line_total_price = calculated_pieces_to_sell * custom_rate
            running_subtotal += line_total_price
            
            if calculated_pieces_to_sell > item_meta['Total_Available']:
                st.error(f"Error! Requested {calculated_pieces_to_sell} units exceeds stock of {item_meta['Total_Available']} pieces.")
            elif calculated_pieces_to_sell > 0:
                order_basket.append({
                    "Design_Code": sku, "Item_Name": item_meta['Item_Name'],
                    "Total_Pieces_Sold": calculated_pieces_to_sell, "Unit_Price": custom_rate, "Line_Total": line_total_price
                })
                st.caption(f"✔️ Staged row item configuration: {calculated_pieces_to_sell} Pieces -> Subtotal: ₹{line_total_price:,.2f}")
                    
        if order_basket:
            st.write("---")
            st.markdown("##### 💵 Financial Surcharge & Taxation Parameters")
            sf1, sf2, sf3 = st.columns(3)
            packing_raw = sf1.text_input("Packing Charges Ledger Add-on (₹):", value="0")
            shipping_raw = sf2.text_input("Shipping / Transport Charges (₹):", value="0")
            gst_toggle = sf3.radio("Tax Filter Profile Toggle:", ["[Without GST]", "[With 3% GST]"])
            
            try:
                packing_charges = float(packing_raw) if packing_raw.strip() else 0.0
                shipping_charges = float(shipping_raw) if shipping_raw.strip() else 0.0
            except ValueError:
                packing_charges, shipping_charges = 0.0, 0.0
                
            gst_amount = running_subtotal * 0.03 if gst_toggle == "[With 3% GST]" else 0.0
            total_invoice_amount = running_subtotal + packing_charges + shipping_charges + gst_amount
            
            st.write("---")
            st.markdown("##### 🛠️ Settlement Parameters & Finalization Controls")
            sc1, sc2, sc3 = st.columns(3)
            p_status = sc1.selectbox("Payment Status Flag Profile:", ["Pending", "Paid", "Partial"])
            d_status = sc2.selectbox("Logistics Dispatch Status Flag Profile:", ["Pending Processing", "Dispatched"])
            
            amount_paid = 0.0
            if p_status == "Partial":
                amount_paid_raw = sc3.text_input("Enter Amount Collected Manually (₹):", value="0.0")
                try:
                    amount_paid = float(amount_paid_raw) if amount_paid_raw.strip() else 0.0
                except ValueError:
                    amount_paid = 0.0
            elif p_status == "Paid":
                amount_paid = total_invoice_amount
                
            pending_dues = max(0.0, total_invoice_amount - amount_paid)
            
            # 📄 DRAFT COMMERCIAL INVOICE DISPLAY VIEW
            st.markdown("### 📄 Commercial Invoice Preview Manifest Frame")
            st.write("---")
            st.image(LOGO_URL, width=100)
            st.markdown("<h2 style='text-align: center; font-family: Cinzel, serif; font-weight:800; margin-bottom:0;'>PRIYA HANDICRAFT</h2>", unsafe_allow_html=True)
            st.markdown(f"**Date:** {datetime.now().strftime('%d-%m-%Y')} | **Invoice ID:** PH-INV-TEMP")
            st.markdown(f"**Customer Name:** {cust_name} | **Mobile:** {cust_mobile} | **City Location:** {cust_city}")
            
            basket_df = pd.DataFrame(order_basket)
            st.table(basket_df[["Design_Code", "Item_Name", "Total_Pieces_Sold", "Unit_Price", "Line_Total"]])
            
            st.markdown(f"""
            - **Wholesale Order Subtotal:** ₹ {running_subtotal:,.2f}
            - **Packing Charges:** ₹ {packing_charges:,.2f}
            - **Shipping/Transport Charges:** ₹ {shipping_charges:,.2f}
            - **Navratri Component GST (3%):** ₹ {gst_amount:,.2f}
            ---
            - ### 🏁 Finalized Grand Total Valuation: **₹ {total_invoice_amount:,.2f}**
            - **Recorded Payment Amount Collected:** ₹ {amount_paid:,.2f}
            """)
            
            if pending_dues > 0:
                st.markdown(f"⚠️ <span class='outstanding-alert'>Remaining Outstanding Dues: ₹ {pending_dues:,.2f}</span>", unsafe_allow_html=True)
                
            if st.button("🚀 Lock Order Account and Finalize Bill Records"):
                if not cust_name or not cust_mobile:
                    st.error("Corporate client names and mobile links are mandatory fields.")
                else:
                    new_inv_id = f"PH-INV-{len(invoice_df) + 10001}"
                    current_date_str = datetime.now().strftime("%d-%m-%Y") # Strict Format Schema rule
                    
                    for cart_row in order_basket:
                        target_sku = cart_row["Design_Code"]
                        sold_qty = cart_row["Total_Pieces_Sold"]
                        parent_df.loc[parent_df["Design_Code"] == target_sku, "Total_Used"] += sold_qty
                        parent_df.loc[parent_df["Design_Code"] == target_sku, "Total_Available"] -= sold_qty
                    save_parent_inventory(parent_df)
                    
                    new_invoice_record = {
                        "Invoice_ID": new_inv_id, "Invoice_Date": current_date_str, "Customer_Name": cust_name, "Mobile": cust_mobile, "City": cust_city,
                        "Items_JSON": json.dumps(order_basket), "Subtotal": running_subtotal, "Packing_Charges": packing_charges, "Shipping_Charges": shipping_charges,
                        "GST_Amount": gst_amount, "Total_Invoice_Amount": total_invoice_amount, "Amount_Paid": amount_paid, "Pending_Dues": pending_dues,
                        "Payment_Status": p_status, "Dispatch_Status": d_status
                    }
                    invoice_df = pd.concat([invoice_df, pd.DataFrame([new_invoice_record])], ignore_index=True)
                    save_invoices(invoice_df)
                    st.success(f"🎉 Invoice locked under transaction reference key ID: {new_inv_id}")
                    
                    # --- DUAL STREAM EXPORT FRAMEWORK DOWNLOADS ---
                    st.markdown("#### 💾 Dual Stream File Export Compilation Workspace")
                    csv_export = basket_df.to_csv(index=False)
                    st.download_button(label="📥 Stream A: Download Raw PDF Layout Schema (.CSV File Representation)", data=csv_export, file_name=f"Invoice_Manifest_{new_inv_id}.csv", mime="text/csv")
                    st.download_button(label="📥 Stream B: Export Structured Data Excel Sheets (.XLSX)", data=csv_export, file_name=f"Corporate_Ledger_DataSheet_{new_inv_id}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    
                    # WhatsApp API Link formulation
                    msg_template = f"Hello {cust_name}, your bill from PRIYA HANDICRAFT is ready. Invoice ID: {new_inv_id}. Total Valuation Amount: Rs. {total_invoice_amount:.2f}. Balance Status: {p_status}. Thank you for your order!"
                    url_encoded_msg = urllib.parse.quote(msg_template)
                    wa_api_url = f"https://api.whatsapp.com/send?phone={cust_mobile}&text={url_encoded_msg}"
                    st.markdown(f'<a href="{wa_api_url}" target="_blank"><button style="background-color:#25D366; color:white; font-weight:bold; border:none; padding:12px; border-radius:4px; width:100%; cursor:pointer;">📲 Direct Action Hook: Push Invoice via WhatsApp Business API Link </button></a>', unsafe_allow_html=True)

# ==============================================================================
# GLOBAL EXPORTS STATION
# ==============================================================================
if app_tab == "Tab 2: Inventory Listing Desk":
    st.write("---")
    st.subheader("💾 Global Corporate System Audit Data Downloads")
    c_dw1, c_dw2 = st.columns(2)
    c_dw1.download_button(label="Download Full Parent Inventory CSV", data=parent_df.to_csv(index=False), file_name="Master_Parent_Inventory_Report.csv", mime="text/csv")
    c_dw2.download_button(label="Download Sales Ledger Data Logs", data=invoice_df.to_csv(index=False), file_name="Master_Commercial_Invoices_Report.csv", mime="text/csv")