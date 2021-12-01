# !pip install qrcode[pil]
import streamlit as st
import qrcode

def main():
    # sidebar
    st.sidebar.markdown("# Input")
    First_Name = st.sidebar.text_input("First Name")
    Last_Name = st.sidebar.text_input("Last Name")
    Organisation = st.sidebar.text_input("Organisation")
    Title = st.sidebar.text_input("Job Title")
    Phone = st.sidebar.text_input("Phone")
    Email = st.sidebar.email("Email")

    # main body
    st.markdown("# QR Code Business Card Generator")

    ## Concatenate contact details
    Contact_Detail_Str = f'BEGIN:VCARD\nVERSION:3.0\nN:{Last_Name};{First_Name};;;\nORG:{Organisation}\nTITLE:{Title}\nTEL;TYPE=WORK,VOICE:{Phone}\nEMAIL:{Email}\nEND:VCARD'
    img = qrcode.make(Contact_Detail_Str)
    st.image(img)

if __name__ == "__main__":
    main()