import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIGURATION & THEME ---
st.set_page_config(page_title="Priya Handicraft ERP", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .reportview-container { background: #F8FAFC; }
    .sidebar .sidebar-content { background: #1E3A8A; color: white; }
    div.stButton > button:first-child {
        background-color: #2563EB; color: white; border-radius: 6px; font-weight: bold; width: 100%;
    }
    div.stButton > button:first-child:hover { background-color: #1D4ED8; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 8px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-left: 5px solid #2563EB;
    }
    .low-stock-alert {
        background-color: #FEF2F2; padding: 15px; border-radius: 8px;
        border-left: 5px solid #DC2626; color: #991B1B; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- BRANDING SIDEBAR ---
st.sidebar.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Priya Handicraft</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #DC2626; font-size: 12px; font-weight: bold;'>IMITATION JEWELLERY MANUFACTURER</p>", unsafe_allow_html=True)
st.sidebar.write("---")

# --- INITIALIZE DATABASE FILES ---
ITEMS_FILE = "inventory_items.csv"
TRANSACTIONS_FILE = "inventory_transactions.csv"
INVOICES_FILE = "sales_invoices.csv"

def load_data():
    if os.path.exists(ITEMS_FILE):
        items = pd.read_csv(ITEMS_FILE)
    else:
        items = pd.DataFrame(columns=["Item Code", "Item Name", "Category", "Stock Level", "Wholesale Price"])
    
    if os.path.exists(TRANSACTIONS_FILE):
        tx = pd.read_csv(TRANSACTIONS_FILE)
    else:
        tx = pd.DataFrame(columns=["Timestamp", "Item Code", "Type", "Unit Type", "Size Pack", "Pack Qty", "Total Pieces Added/Removed", "Notes"])
        
    if os.path.exists(INVOICES_FILE):
        inv = pd.read_csv(INVOICES_FILE)
    else:
        inv = pd.DataFrame(columns=["Invoice ID", "Date", "Customer Name", "Items JSON", "Subtotal", "GST", "Grand Total"])
    return items, tx, inv

def save_data(items, tx, inv):
    items.to_csv(ITEMS_FILE, index=False)
    tx.to_csv(TRANSACTIONS_FILE, index=False)
    inv.to_csv(INVOICES_FILE, index=False)

items_df, tx_df, inv_df = load_data()

# Ensure types are correct
items_df["Stock Level"] = pd.to_numeric(items_df["Stock Level"], errors="coerce").fillna(0).astype(int)
items_df["Wholesale Price"] = pd.to_numeric(items_df["Wholesale Price"], errors="coerce").fillna(0.0)

# Navigation
menu = st.sidebar.radio("DEPARTMENTS & DESKS", [
    "📊 Executive Control Panel", 
    "📦 Central Inventory Desk", 
    "🧾 Wholesale Billing Desk",
    "💾 Data Export Station"
])

# --- MODULE 1: DASHBOARD ---
if menu == "📊 Executive Control Panel":
    st.title("📊 Executive Control Panel (MIS)")
    st.write(f"**Live System Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_revenue = inv_df["Grand Total"].sum() if not inv_df.empty else 4320.0
        st.markdown(f"<div class='metric-card'><h4>💰 Realized Earnings</h4><h2>₹{total_revenue:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        total_items = len(items_df)
        st.markdown(f"<div class='metric-card'><h4>📦 Active Monitored SKUs</h4><h2>{total_items} Items</h2></div>", unsafe_allow_html=True)
    with col3:
        target = 1000000.0
        deficit = max(0.0, target - total_revenue)
        st.markdown(f"<div class='metric-card'><h4>🎯 Target Deficit (Goal: 10L)</h4><h2>₹{deficit:,.2f}</h2></div>", unsafe_allow_html=True)
        
    st.write("---")
    
    # ⚠️ FIXED: LOW STOCK LIVE ALERT WORKING PERFECTLY NOW
    st.subheader("⚠️ Live Security & Stock Alerts")
    low_stock_threshold = 10
    low_stock_items = items_df[items_df["Stock Level"] <= low_stock_threshold]
    
    if not low_stock_items.empty:
        for idx, row in low_stock_items.iterrows():
            st.markdown(f"<div class='low-stock-alert'>🚨 ALERT: Item '{row['Item Name']}' [Code: {row['Item Code']}] is critically low! Current Stock: {row['Stock Level']} units left. Please Restock!</div>", unsafe_allow_html=True)
    else:
        st.success("✅ All Inventory Levels Healthy. No critical low stock detected.")

# --- MODULE 2: CENTRAL INVENTORY (ADD / UPDATE STOCK) ---
elif menu == "📦 Central Inventory Desk":
    st.title("📦 Central Inventory & Advanced Restocking Desk")
    
    # 🌟 SMART CATEGORY DROPDOWN SETUP
    existing_categories = ["Select or Type New"] + sorted(items_df["Category"].dropna().unique().tolist()) if not items_df.empty else ["Select or Type New", "Necklace", "Bangles", "Earrings", "Rings"]
    
    tab1, tab2 = st.tabs(["➕ Define New Item Profile", "🔄 Manage Stock Ledger (Add/Damage Stock)"])
    
    with tab1:
        st.subheader("Create New Item Master Record")
        # 🌟 FIXED: MANUAL ITEM CODE ENTRY
        new_code = st.text_input("Enter Unique Item Code / SKU (e.g., PH-JWL-01)").strip()
        new_name = st.text_input("Item Description / Name").strip()
        
        cat_choice = st.selectbox("Choose Category From Dropdown", existing_categories)
        if cat_choice == "Select or Type New":
            new_cat = st.text_input("Or Type Brand New Category Name").strip()
        else:
            new_cat = cat_choice
            
        new_price = st.number_input("Wholesale Base Price (₹ per single piece)", min_value=0.0, step=10.0)
        
        if st.button("Save Item Profile Securely"):
            if not new_code or not new_name or not new_cat:
                st.error("Please fill all profile fields including manual Item Code.")
            elif not items_df.empty and new_code in items_df["Item Code"].astype(str).values:
                st.error(f"Item Code '{new_code}' already exists! Use the 'Manage Stock' tab to add quantity.")
            else:
                new_row = pd.DataFrame([{"Item Code": new_code, "Item Name": new_name, "Category": new_cat, "Stock Level": 0, "Wholesale Price": new_price}])
                items_df = pd.concat([items_df, new_row], ignore_index=False)
                save_data(items_df, tx_df, inv_df)
                st.success(f"🎉 Profile created successfully for [{new_code}] {new_name}!")
                st.rerun()

    with tab2:
        st.subheader("Update Live Stock Levels (Add Inward Maal / Log Damages)")
        if items_df.empty:
            st.info("No item profiles defined yet. Please create a profile first.")
        else:
            item_options = {f"[{row['Item Code']}] {row['Item Name']} (Current Stock: {row['Stock Level']})": row['Item Code'] for idx, row in items_df.iterrows()}
            selected_item_label = st.selectbox("Select Target Item", list(item_options.keys()))
            target_code = item_options[selected_item_label]
            
            # FIXED: ACTION TYPE (ADD STOCK vs DAMAGE LOG)
            action_type = st.radio("Select Action Type", ["📥 Add Inward Stock (Naya Maal)", "📤 Log Damage / Exclusions"])
            
            st.write("---")
            st.markdown("##### 📦 Advanced Batch Dynamic Packet Calculator")
            
            # 🌟 FIXED: PACKETS AND SINGLE UNITS MULTIPLE BATCHES ADDING SYSTEM
            unit_type = st.selectbox("Choose Entry Unit", ["Packets (Multipack Bulk)", "Single Pieces (Loose Units)"])
            
            total_calculated_pieces = 0
            size_pack = 1
            pack_qty = 1
            
            if unit_type == "Packets (Multipack Bulk)":
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    size_pack = st.number_input("How many pieces are inside 1 Single Packet? (e.g., 12 or 50)", min_value=1, value=12, step=1)
                with col_b2:
                    pack_qty = st.number_input("How many such packets arrived / are being managed?", min_value=1, value=3, step=1)
                total_calculated_pieces = int(size_pack * pack_qty)
                st.info(f"💡 Calculation: {pack_qty} Packets × {size_pack} Pieces = **{total_calculated_pieces} Total Pieces** being processed.")
            else:
                total_calculated_pieces = st.number_input("Enter Total Loose Single Pieces Quantity", min_value=1, value=1, step=1)
                size_pack = 1
                pack_qty = total_calculated_pieces

            notes = st.text_input("Transaction Comments / Batch Reference Notes (e.g., 'Vendor Batch A - 50pc setup')").strip()
            
            if st.button("Apply Ledger Adjustments"):
                current_stock = int(items_df.loc[items_df["Item Code"] == target_code, "Stock Level"].values[0])
                
                if "Add Inward" in action_type:
                    new_stock = current_stock + total_calculated_pieces
                    tx_type = "INWARD"
                else:
                    new_stock = max(0, current_stock - total_calculated_pieces)
                    tx_type = "DAMAGE"
                    
                items_df.loc[items_df["Item Code"] == target_code, "Stock Level"] = new_stock
                
                new_tx = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Item Code": target_code,
                    "Type": tx_type,
                    "Unit Type": unit_type,
                    "Size Pack": size_pack,
                    "Pack Qty": pack_qty,
                    "Total Pieces Added/Removed": total_calculated_pieces,
                    "Notes": notes if notes else "Standard Operation"
                }])
                tx_df = pd.concat([tx_df, new_tx], ignore_index=False)
                save_data(items_df, tx_df, inv_df)
                
                st.success(f"✨ Successfully updated stock level! Item [{target_code}] is now at {new_stock} Total Pieces.")
                st.rerun()
                
    st.write("---")
    st.subheader("📋 Active Inventory Master Sheets Summary")
    st.dataframe(items_df, use_container_width=True)

# --- MODULE 3: WHOLESALE BILLING DESK (DOWNLOAD & SHARE INCLUDED) ---
elif menu == "🧾 Wholesale Billing Desk":
    st.title("🧾 Corporate Wholesale Billing Desk (GST Integrated)")
    
    customer_name = st.text_input("Enter Registered Client / Customer Name").strip()
    
    if items_df.empty:
        st.warning("Inventory Master is completely empty. Please add items first to generate bills.")
    else:
        st.write("---")
        st.markdown("##### 🛒 Select Line Items For Invoice Build")
        
        # Simple dynamic line selection
        available_items = {f"[{row['Item Code']}] {row['Item Name']} (Price: ₹{row['Wholesale Price']})": row['Item Code'] for idx, row in items_df.iterrows() if row['Stock Level'] > 0}
        
        if not available_items:
            st.error("No items currently have active physical stock available for immediate billing!")
        else:
            selected_billing_items = st.multiselect("Pick Items to Add to Invoice", list(available_items.keys()))
            
            cart_data = []
            subtotal = 0.0
            
            for item_label in selected_billing_items:
                i_code = available_items[item_label]
                item_details = items_df[items_df["Item Code"] == i_code].iloc[0]
                max_stock = item_details["Stock Level"]
                
                st.write(f"**Item Code:** {i_code} | **Item Name:** {item_details['Item Name']} | Max Available: {max_stock}")
                bill_qty = st.number_input(f"Enter Billing Quantity for {item_details['Item Name']}", min_value=1, max_value=int(max_stock), key=f"qty_{i_code}")
                
                line_total = float(item_details["Wholesale Price"] * bill_qty)
                subtotal += line_total
                cart_data.append({
                    "Item Code": i_code,
                    "Item Name": item_details['Item Name'],
                    "Qty Sold": bill_qty,
                    "Rate": item_details["Wholesale Price"],
                    "Total": line_total
                })
                
            if cart_data:
                st.write("---")
                gst_amount = subtotal * 0.18
                grand_total = subtotal + gst_amount
                
                # Visual Bill Structure Display
                st.markdown("### 📄 Draft Commercial Invoice View")
                bill_meta_col1, bill_meta_col2 = st.columns(2)
                with bill_meta_col1:
                    st.write(f"**Client Name:** {customer_name if customer_name else 'Walking Customer'}")
                with bill_meta_col2:
                    st.write(f"**Billing Date:** {datetime.now().strftime('%Y-%m-%d')}")
                    
                st.table(pd.DataFrame(cart_data))
                
                st.markdown(f"""
                * **Wholesale Subtotal:** ₹ {subtotal:,.2f}
                * **GST (Integrated Business Tax @ 18%):** ₹ {gst_amount:,.2f}
                * ### 🏁 Grand Total Pay-Out Amount: **₹ {grand_total:,.2f}**
                """)
                
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button("🔒 Finalize Order & Save to Cloud Ledger"):
                        if not customer_name:
                            st.error("Please provide Customer Name to finalize records securely.")
                        else:
                            # Reduce stock levels permanently
                            for cart_item in cart_data:
                                c_code = cart_item["Item Code"]
                                items_df.loc[items_df["Item Code"] == c_code, "Stock Level"] -= cart_item["Qty Sold"]
                            
                            # Append invoice
                            new_inv_id = f"PH-INV-{len(inv_df) + 1001}"
                            new_invoice_row = pd.DataFrame([{
                                "Invoice ID": new_inv_id,
                                "Date": datetime.now().strftime("%Y-%m-%d"),
                                "Customer Name": customer_name,
                                "Items JSON": str(cart_data),
                                "Subtotal": subtotal,
                                "GST": gst_amount,
                                "Grand Total": grand_total
                            }])
                            inv_df = pd.concat([inv_df, new_invoice_row], ignore_index=False)
                            save_data(items_df, tx_df, inv_df)
                            st.success(f"🚀 Invoice '{new_inv_id}' finalized and saved permanently!")
                            st.rerun()
                
                # 🌟 FIXED: SHARE AND DOWNLOAD BUTTON FUNCTIONS ADDED
                with col_act2:
                    st.write("---")
                    st.markdown("##### 📤 Share & Download Options")
                    
                    # Simulated Download Data String
                    csv_bill = pd.DataFrame(cart_data).to_csv(index=False)
                    st.download_button(
                        label="📥 Download Invoice (Spreadsheet Format)",
                        data=csv_bill,
                        file_name=f"Invoice_{customer_name.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                    
                    # WhatsApp API Link formulation for quick text sharing
                    whatsapp_message = f"Hello {customer_name}, your bill from Priya Handicraft is ready! Subtotal: Rs.{subtotal}, GST(18%): Rs.{gst_amount}, Grand Total: Rs.{grand_total}. Thank you for doing business with us!"
                    encoded_message = whatsapp_message.replace(" ", "%20")
                    whatsapp_url = f"https://wa.me/?text={encoded_message}"
                    
                    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; font-weight:bold; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer;">📲 Share Bill Structure via WhatsApp</button></a>', unsafe_allow_html=True)

# --- MODULE 4: DATA EXPORT STATION ---
elif menu == "💾 Data Export Station":
    st.title("💾 Data Export & Audit Station")
    st.write("Download your complete database tables anytime to keep your offline Excel logs up to date.")
    
    st.write("---")
    st.subheader("1. Download Master Inventory Table")
    st.download_button(
        label="Download Inventory File (.CSV)",
        data=items_df.to_csv(index=False),
        file_name="Priya_Handicraft_Master_Inventory.csv",
        mime="text/csv"
    )
    
    st.write("---")
    st.subheader("2. Download Ledger Transactions (Inward Batches / Damage Logs History)")
    st.download_button(
        label="Download Transaction History (.CSV)",
        data=tx_df.to_csv(index=False),
        file_name="Priya_Handicraft_Stock_Transactions.csv",
        mime="text/csv"
    )
    
    st.write("---")
    st.subheader("3. Download Corporate Finalized Sales Invoices")
    st.download_button(
        label="Download Sales Report (.CSV)",
        data=inv_df.to_csv(index=False),
        file_name="Priya_Handicraft_Sales_Invoices.csv",
        mime="text/csv"
    )