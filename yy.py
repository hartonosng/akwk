import streamlit as st
import pandas as pd

# Contoh data
data = {
    'customerid': ['C001', 'C002', 'C003'],
    'customername': ['Customer A', 'Customer B', 'Customer C']
}
df = pd.DataFrame(data)

# Buat menu di sidebar
selected_menu = st.sidebar.radio(
    "Select Menu",
    ["General Summary", "Company Level Summary"]
)

# Fungsi untuk menampilkan General Summary
def show_general_summary():
    st.write("General Summary")
    
    # Tampilkan DataFrame dengan hyperlink
    def make_clickable(val):
        # Membuat hyperlink yang menyimpan customer ID ke dalam session state
        return f'<a href="#" onclick="document.getElementById(\'{val}\').click()">{val}</a>'

    # Menambahkan ID pada setiap baris untuk click event
    df_clickable = df.copy()
    df_clickable['customerid'] = df_clickable['customerid'].apply(make_clickable)

    # Menampilkan DataFrame dengan hyperlink
    st.write(df_clickable.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Menyimpan state ID yang di-click
    for idx, row in df.iterrows():
        if st.markdown(f'<a id="{row["customerid"]}" href="#" onclick="window.location.href=\'/?menu=Company%20Level%20Summary&customerid={row["customerid"]}\'">Click</a>', unsafe_allow_html=True):
            st.session_state.selected_customer = row['customerid']

# Fungsi untuk menampilkan Company Level Summary
def show_company_level_summary():
    if 'selected_customer' in st.session_state:
        selected_customer = st.session_state.selected_customer
        st.write(f"Company Level Summary for Customer ID: {selected_customer}")

        # Menampilkan detail customer yang dipilih
        customer_details = df[df['customerid'] == selected_customer]
        st.dataframe(customer_details)
    else:
        st.write("No customer selected")

# Logika untuk menampilkan halaman sesuai menu yang dipilih
if selected_menu == "General Summary":
    show_general_summary()
elif selected_menu == "Company Level Summary":
    show_company_level_summary()
