# !pip install qrcode[pil]
import streamlit as st
import qrcode, PIL, io

def main():
    # sidebar
    st.sidebar.markdown("# Input")
    First_Name = st.sidebar.text_input("First Name")
    Last_Name = st.sidebar.text_input("Last Name")
    Organisation = st.sidebar.text_input("Organisation")
    Title = st.sidebar.text_input("Job Title")
    Phone = st.sidebar.text_input("Phone")
    Email = st.sidebar.text_input("Email")

    # main body
    st.markdown("# QR Code Business Card")
    st.markdown("As COVID gave the world the necessary nudge to embrace remote working, we have also also come to notice how [out of place](https://www.bbc.co.uk/news/business-58419842) the paper business cards have become.  Embeding professional contact details in QR Codes provides a cheap, more sustainable and remotely sharable solution to this problem.")
    st.markdown("Just input the contact details on the left and download the QR Code image below.  Enjoy!")
    st.write("")

    ## Concatenate contact details
    Contact_Detail_Str = f'BEGIN:VCARD\nVERSION:3.0\nN:{Last_Name};{First_Name};;;\nORG:{Organisation}\nTITLE:{Title}\nTEL;TYPE=WORK,VOICE:{Phone}\nEMAIL:{Email}\nEND:VCARD'
    img = qrcode.make(Contact_Detail_Str)
    img_byte_arr = io.BytesIO()  # Convert PIL image to bytes array
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Create three-column layout and place image in centre column
    # https://discuss.streamlit.io/t/how-to-center-images-latex-header-title-etc/1946/5
    col1, col2, col3 = st.columns([1,2,4])

    with col1:
        st.write("")

    with col2:
        st.image(img_byte_arr) #, caption = f"""""")

    with col3:
        st.markdown(f"""
        **Name:** {First_Name} {Last_Name}\n
        **Organisation:** {Organisation}\n
        **Job Title:** {Title}\n
        **Phone:** {Phone}\n
        **Email:** {Email}
        """)

    st.write("")
    st.markdown("_Created by_ @donthaveapps🐙")

if __name__ == "__main__":
    main()