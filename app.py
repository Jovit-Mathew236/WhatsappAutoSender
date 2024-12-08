import streamlit as st
import pandas as pd
import os
import time
import sys
import subprocess
import pyautogui

# Attempt to install missing dependencies
def install_dependencies():
    dependencies = [
        'pywhatkit',
        'pyautogui',
        'python-xlib',  # for Linux/Mac
        'pypiwin32',      # for Windows clipboard support
        'openpyxl'
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            st.info(f"Installed {dep} successfully")
        except Exception as e:
            st.error(f"Could not install {dep}: {e}")

# Check and install dependencies
try:
    import pywhatkit
    import pyautogui
except ImportError:
    st.warning("Missing dependencies. Attempting to install...")
    install_dependencies()
    
    # Retry imports
    try:
        import pywhatkit
        import pyautogui
    except ImportError:
        st.error("Failed to install required dependencies. Please install manually.")
        st.stop()

def send_whatsapp_message(phone_number, message, image_path=None):
    """
    Send WhatsApp message with optional image using PyWhatKit
    """
    try:
        # Clean phone number (remove non-digit characters)
        cleaned_number = ''.join(filter(str.isdigit, str(phone_number)))
        
        # Ensure the number is in the correct format (with country code)
        formatted_number = f"+91{cleaned_number}"
        
        # Send message
        if image_path and os.path.exists(image_path):
            # Send message with image
            pywhatkit.sendwhats_image(
                receiver=formatted_number, 
                img_path=image_path, 
                caption=message, 
                wait_time=10  # Wait time in seconds before sending
            )
        else:
            # Send text message only
            pywhatkit.sendwhatmsg_instantly(
                phone_no=formatted_number, 
                message=message,
                wait_time=10  # Wait time in seconds before sending
            )
        
        return True
    
    except Exception as e:
        st.error(f"Error sending message to {phone_number}: {e}")
        return False

def main():
    st.title("WhatsApp Bulk Message Sender (PyWhatKit)")

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    # Excel file upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel File", 
        type=['xlsx', 'xls'],
        help="Excel file must contain 'Name' and 'Phone Number' columns"
    )

    # Image file upload
    uploaded_image = st.sidebar.file_uploader(
        "Upload Image (Optional)", 
        type=['png', 'jpg', 'jpeg'],
        help="Image to send along with the message"
    )

    # Message input
    message_template = st.sidebar.text_area(
        "Message Template", 
        "Hello {{Name}}, this is a test message!",
        help="Use {{Name}} for personalization"
    )

    # Send button
    if st.sidebar.button("Send Messages"):
        # Validate file upload
        if uploaded_file is not None:
            try:
                # Save uploaded image temporarily if provided
                image_path = None
                if uploaded_image:
                    # Create temp directory if it doesn't exist
                    os.makedirs('temp', exist_ok=True)
                    image_path = os.path.join('temp', uploaded_image.name)
                    with open(image_path, 'wb') as f:
                        f.write(uploaded_image.getbuffer())

                # Read Excel file
                df = pd.read_excel(uploaded_file)
                
                # Validate columns
                required_columns = ['Name', 'Phone Number']
                if not all(col in df.columns for col in required_columns):
                    st.error("Excel sheet must contain 'Name' and 'Phone Number' columns.")
                    return

                # Print dataframe for debugging
                st.write("Contacts DataFrame:")
                st.write(df)

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Flag to check if WhatsApp Web is already open
                whatsapp_open = False

                # Send messages
                total_contacts = len(df)
                for idx, row in df.iterrows():
                    try:
                        # Personalize message
                        personalized_message = message_template.replace("{{Name}}", str(row['Name']))
                        
                        # Open WhatsApp Web only if it's not already open
                        if not whatsapp_open:
                            # Open WhatsApp Web in the first tab
                            pyautogui.hotkey('ctrl', 't')  # Open new tab
                            pyautogui.typewrite("https://web.whatsapp.com")  # Navigate to WhatsApp Web
                            pyautogui.press('enter')
                            time.sleep(15)  # Wait for WhatsApp Web to load
                            whatsapp_open = True

                        # Send message
                        success = send_whatsapp_message(
                            str(row['Phone Number']), 
                            personalized_message,
                            image_path
                        )

                        # Update progress
                        progress = (idx + 1) / total_contacts
                        progress_bar.progress(progress)
                        status_text.text(f"Sending message {idx + 1}/{total_contacts}")

                        # Wait between messages to avoid rate limiting
                        time.sleep(10)  # Adjusted sleep time for smoother operation

                        # Close tab after each message is sent
                        if success:
                            pyautogui.hotkey('ctrl', 'w')  # Close current tab
                            time.sleep(5)  # Allow time for tab to close
                            # Keep WhatsApp Web open in the same tab for next message

                    except Exception as inner_e:
                        st.error(f"Error processing contact {row['Name']}: {inner_e}")

                # Final status
                st.success("Message sending completed!")

            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            finally:
                # Remove temporary image
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
    2. Optional: Upload an image to send
    3. Enter your message template
    4. Click 'Send Messages'
    5. IMPORTANT: Keep WhatsApp Web open in your default browser
    
    Note: Messages will be sent automatically using PyWhatKit.
    Ensure phone numbers are for Indian numbers (starting with +91)
    """)

if __name__ == "__main__":
    main()
