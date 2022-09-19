# !pip install qrcode[pil]
import profile
import streamlit as st
import qrcode, io
from PIL import Image
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
    logo_file = st.sidebar.file_uploader("Upload logo (.jpg or .png) for QR Code overlay (Optional)", type=['png', 'jpg'])
    profile_file = st.sidebar.file_uploader("Upload profile picture (.jpg or .png) for QR Code Business Card (Optional)", type=['png', 'jpg'])
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
        st.write(logo_file)  # To be deleted

        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            # box_size=10,
            # border=4,
            )
        qr.add_data(Contact_Detail_Str)

        if logo_file is not None:
            # qr_im = qr.make_image(image_factory=StyledPilImage, embeded_image_path=logo_im)
            # TODO: PLAN B - resize logo to square
            logo_im = Image.open(logo_file)
            qr_im = qr.make_image()
            qr_file = qr_im.save(io.BytesIO(), format='PNG')
            print(f"qr_im = {qr_im}")
            qr_im.show()
            qr_im = Image.open(qr_file)
            qr_im = add_logo_on_image(logo_im, qr_im)
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

        if profile_file is not None:
            profile_im = Image.open(profile_file)
            cropped_im = crop2circle(profile_im)

        with col1:
            st.write("")

        with col2:
            st.image(qr_im_byte_arr) #, caption = f"""""")

        with col3:
            if profile_file is not None:
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
    """
    Take a profile_im PIL image object
    Crop image to circle and return cropped_im PIL image object
    """
    cropped_im = profile_im
    return cropped_im

def add_logo_on_image(logo_im, image_im):
    """
    Take a 'logo' PIL image object and an 'image' PIL image object
    Resize logo (if needed) and paste it onto the centre of the image
    Return overlaid_im PIL image object
    """

    logo_size_limit = 140

    logo_width, logo_height = logo_im.size
    print(f"Logo size = {logo_width} x {logo_height}")

    image_width, image_height = image_im.size
    print(f"QR code size = {image_width} x {image_height}")

    # Check if logo needs to be resized
    if logo_width > logo_size_limit or logo_height > logo_size_limit:
        if logo_width > logo_height:
            logo_new_width = logo_size_limit
            logo_new_height = int(logo_size_limit * logo_height / logo_width)
        else:
            logo_new_height = logo_size_limit
            logo_new_width = int(logo_size_limit * logo_width / logo_height)

        # Resize logo
        print(f"Resizing logo to w={logo_new_width} x h={logo_new_height}")
        logo_im = logo_im.resize((logo_new_width, logo_new_height))
    logo_im.show()

    # Add the logo
    print(f"logo_im = {logo_im}")
    print(f"image_im = {image_im}")
    overlaid_im = Image.Image.paste(image_im, logo_im) #TODO, (int((image_width - logo_new_width)/2), int((image_height - logo_new_height)/2)))
    # .Image.paste(image_im, logo_im, (int((image_width - logo_new_width)/2), int((image_height - logo_new_height)/2)))
    print(f"overlaid_im = {overlaid_im}")

    return overlaid_im

if __name__ == "__main__":
    main()
