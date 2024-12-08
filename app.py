import streamlit as st
import pandas as pd
import os
import time
import pyautogui
import pywhatkit

def send_whatsapp_message(phone_number, message, image_path=None):
    """
    Send WhatsApp message with optional image using PyWhatKit.
    """
    try:
        cleaned_number = ''.join(filter(str.isdigit, str(phone_number)))
        formatted_number = f"+91{cleaned_number}"

        if image_path and os.path.exists(image_path):
            pywhatkit.sendwhats_image(
                receiver=formatted_number,
                img_path=image_path,
                caption=message,
                wait_time=10
            )
        else:
            pywhatkit.sendwhatmsg_instantly(
                phone_no=formatted_number,
                message=message,
                wait_time=10
            )
        return True

    except Exception as e:
        st.error(f"Error sending message to {phone_number}: {e}")
        return False

def main():
    st.title("WhatsApp Bulk Message Sender (PyWhatKit)")

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel File",
        type=['xlsx', 'xls'],
        help="Excel file must contain 'Name' and 'Phone Number' columns"
    )

    uploaded_image = st.sidebar.file_uploader(
        "Upload Image (Optional)",
        type=['png', 'jpg', 'jpeg'],
        help="Image to send along with the message"
    )

    message_template = st.sidebar.text_area(
        "Message Template",
        "Hello {{Name}}, this is a test message!",
        help="Use {{Name}} for personalization"
    )

    if st.sidebar.button("Send Messages"):
        if uploaded_file is not None:
            try:
                image_path = None
                if uploaded_image:
                    os.makedirs('temp', exist_ok=True)
                    image_path = os.path.join('temp', uploaded_image.name)
                    with open(image_path, 'wb') as f:
                        f.write(uploaded_image.getbuffer())

                df = pd.read_excel(uploaded_file)
                required_columns = ['Name', 'Phone Number']
                if not all(col in df.columns for col in required_columns):
                    st.error("Excel sheet must contain 'Name' and 'Phone Number' columns.")
                    return

                progress_bar = st.progress(0)
                status_text = st.empty()
                whatsapp_open = False

                total_contacts = len(df)
                for idx, row in df.iterrows():
                    try:
                        personalized_message = message_template.replace("{{Name}}", str(row['Name']))
                        if not whatsapp_open:
                            pyautogui.hotkey('ctrl', 't')
                            pyautogui.typewrite("https://web.whatsapp.com")
                            pyautogui.press('enter')
                            time.sleep(15)
                            whatsapp_open = True

                        success = send_whatsapp_message(
                            str(row['Phone Number']),
                            personalized_message,
                            image_path
                        )

                        progress = (idx + 1) / total_contacts
                        progress_bar.progress(progress)
                        status_text.text(f"Sending message {idx + 1}/{total_contacts}")
                        time.sleep(10)

                        if success:
                            pyautogui.hotkey('ctrl', 'w')
                            time.sleep(5)

                    except Exception as inner_e:
                        st.error(f"Error processing contact {row['Name']}: {inner_e}")

                st.success("Message sending completed!")

            except Exception as e:
                st.error(f"An error occurred: {e}")

            finally:
                if 'image_path' in locals() and image_path and os.path.exists(image_path):
                    os.remove(image_path)

        else:
            st.error("Please upload an Excel file before sending messages.")

    # Additional instructions
    st.sidebar.info("""
    ## Instructions
    1. Prepare an Excel file with columns:
       - Name
       - Phone Number
    2. Optional: Upload an image to send.
    3. Enter your message template.
    4. Click 'Send Messages'.
    5. IMPORTANT: Keep WhatsApp Web open in your default browser.
    
    Note: Messages will be sent automatically using PyWhatKit.
    Ensure phone numbers are for Indian numbers (starting with +91).
    """)

if __name__ == "__main__":
    main()