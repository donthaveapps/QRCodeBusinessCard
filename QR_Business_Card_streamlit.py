# !pip install qrcode[pil]
import profile
import streamlit as st
import qrcode, PIL, io
from qrcode.image.styledpil import StyledPilImage
# https://pypi.org/project/qrcode/
# https://www.geeksforgeeks.org/cropping-an-image-in-a-circular-way-using-python/
# https://docs.streamlit.io/library/api-reference/widgets/st.color_picker

def main():
    # sidebar
    st.sidebar.markdown("### Information for QR Code")
    First_Name = st.sidebar.text_input("First Name")
    Last_Name = st.sidebar.text_input("Last Name")
    Organisation = st.sidebar.text_input("Organisation")
    Title = st.sidebar.text_input("Job Title")
    Phone = st.sidebar.text_input("Phone")
    Email = st.sidebar.text_input("Email")
    logo_im = st.sidebar.file_uploader("Upload logo (.jpg or .png) for QR Code overlay (Optional)", type=['png', 'jpg'])
    profile_im = st.sidebar.file_uploader("Upload profile picture (.jpg or .png) for QR Code Business Card (Optional)", type=['png', 'jpg'])
    card_font_colour = st.sidebar.color_picker("Select font colour for QR Business Card (default: black", value="#000000")
    card_bg_colour = st.sidebar.color_picker("Select background colour for QR Business Card (default: white)", value="#FFFFFF")

    # Persistent header section
    st.markdown("# QR Code Business Card")

    # Section that changes before and after the "Create QR Code" button is pressed
    if st.sidebar.button("Create QR Code"):
        ## Concatenate contact details
        Contact_Detail_Str = f'BEGIN:VCARD\nVERSION:3.0\nN:{Last_Name};{First_Name};;;\nORG:{Organisation}\nTITLE:{Title}\nTEL;TYPE=WORK,VOICE:{Phone}\nEMAIL:{Email}\nEND:VCARD'
        
        ## Create QR Code
        # TODO: if logo_im is not NONE, add logo overlay
        st.write(logo_im)  # To be deleted

        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            # box_size=10,
            # border=4,
            )
        qr.add_data(Contact_Detail_Str)

        if logo_im is not None:
            # Transform logo_im to SQUARE
            qr_im = qr.make_image(image_factory=StyledPilImage, embeded_image_path=logo_im)
        else:
            qr_im = qr.make_image()
        
        img_byte_arr = io.BytesIO()  # Convert PIL image to bytes array
        qr_im.save(img_byte_arr, format='PNG')
        qr_im_byte_arr = img_byte_arr.getvalue()
        

        # img = qrcode.make(Contact_Detail_Str)
        # img_byte_arr = io.BytesIO())
        # img.save(img_byte_arr, format='PNG')
        # img_byte_arr = img_byte_arr.getvalue()

        # Create three-column layout and place image in centre column
        # https://discuss.streamlit.io/t/how-to-center-images-latex-header-title-etc/1946/5
        col1, col2, col3 = st.columns([1,2,4])

        cropped_im = crop2circle(profile_im)

        with col1:
            st.write("")

        with col2:
            st.image(qr_im_byte_arr) #, caption = f"""""")

        with col3:
            if profile_im is not None:
                st.image(cropped_im)

            st.markdown(f"""
            **Name:** {First_Name} {Last_Name}\n
            **Organisation:** {Organisation}\n
            **Job Title:** {Title}\n
            **Phone:** {Phone}\n
            **Email:** {Email}
            """)

        # TODO: QR Code Card preview
        # TODO: Download button for QR Code only
        st.download_button("Download QR Code Business Card", data="hello world!", file_name=f"{First_Name} {Last_Name}.png")
    else:
        st.markdown("As COVID gave the world the necessary nudge to embrace remote working, we have also also come to notice how [out of place](https://www.bbc.co.uk/news/business-58419842) the paper business cards have become.  Embeding professional contact details in QR Codes provides a cheap, more sustainable and remotely sharable solution to this problem.")
        st.markdown("Just input the contact details on the left panel (depending on your device, you might have to tap an arrow bottom at the top left to unhide the panel) and download the QR Code image below.  Enjoy!")


    # Persistent footer section
    st.markdown("_All data and files are only [temporarily stored in memory](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted) and is deleted when the browser tab is closed or refresh. Source code is open for examination [here](https://github.com/donthaveapps/QRCodeBusinessCard)._")
    # st.markdown("Refresh browser tab to reset.")
    st.markdown("_Created by_ [@donthaveapps](https://github.com/donthaveapps/QRCodeBusinessCard)🐙")

def crop2circle(profile_im):
    """Crop image to circle"""
    cropped_im = profile_im
    return cropped_im

if __name__ == "__main__":
    main()
