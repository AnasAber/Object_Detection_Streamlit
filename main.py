import io
from dotenv import load_dotenv
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import os
import time

load_dotenv()

def objectDetection(image_path):
    """
        A function to perform object detection on an image.
        It returns a list of dictionaries, where each dictionary contains the following:
        - label: The label of the detected object
        - score: The confidence score of the detected object
        - box: The bounding box coordinates of the detected object
    """

    object_detection = pipeline("object-detection", model="ciasimbaya/ObjectDetection")
    try:
        ob = object_detection(image_path)
        return ob
    except Exception as e:
        st.error(f"Error during object detection: {e}")
        return []



def annotate_image_with_boxes(image, annotations):
    """
        A function to annotate an image with bounding boxes and labels.
        It returns the path to the annotated image.
    """


    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    for annotation in annotations:
        label = annotation['label']
        score = annotation['score']
        confidence = f"{score:.2f}"
        # Determine color and length of pipe based on confidence score
        if score >= 0.8:
            color = "green"
            pipe_length = "80px"  # Long pipe for high confidence
        elif score >= 0.5:
            color = "orange"
            pipe_length = "60px"  # Medium pipe for moderate confidence
        else:
            color = "red"
            pipe_length = "30px"   # Short pipe for low confidence

        text = f"{label} : "
        pipe_html = f'<hr style="height: 5px; background-color: {color}; width: {pipe_length}; border: none; display: inline-block; margin: 0px 10px;">'
        st.markdown(f"{text} {pipe_html} {confidence}", unsafe_allow_html=True)

        box = annotation['box']
        draw.rectangle([(box['xmin'], box['ymin']), (box['xmax'], box['ymax'])], outline='red', width=3)
        draw.text((box['xmin'], box['ymin'] - 28), label, fill='red', font=font)

    annotated_image_path = 'result/annotated_photo.jpg'
    os.makedirs(os.path.dirname(annotated_image_path), exist_ok=True)
    image.save(annotated_image_path)
    return annotated_image_path




# Streamlit app styling
st.markdown(
    """
    <style>
    .main {
        margin-left: -10rem;
    }
    .stApp {
        background-color: #EBE4D1;
    }
    .sidebar-content {
        background-color: #EADBC8;
    }
    .stButton>button {
        background-color: #26577C;
        color: white;
    }
    .stButton>button:hover {
        background-color: #EBE4D1;
    }
    .stButton>button:focus {
        background-color: #EBE4D1;
    }
    </style>
    """, unsafe_allow_html=True
)


# Streamlit app
st.title("The Eying App 👀")
st.markdown("An object detection app 🔥, try uploading an image and see for yourself 😋. The code is open source and available in [here](https://github.com/AnasAber/Object_Detection_Streamlit) on Github", unsafe_allow_html=True)

# Sidebar for image upload
st.sidebar.markdown("<h2 style='color: #E55604;'>Upload Desired Image</h2>", unsafe_allow_html=True)
image_path = st.sidebar.file_uploader("Choose an image...🧐", type=["jpg", "jpeg", "png"])


# Sqmple Image
button_placeholder = st.sidebar.empty()
if button_placeholder.button("Sample Image"):

    # the dynamic "Detecting Results..." header
    header_placeholder = st.empty()
    header_text = "Detecting Results..."
    typed_text = ""
    for char in header_text:
        typed_text += char
        header_placeholder.write(typed_text, unsafe_allow_html=True)
        time.sleep(0.07) 
    
    image_path = "photo.jpg"
    image = Image.open(image_path)
    results = objectDetection(image)

    header_placeholder.empty()
    st.markdown("<h2 style='text-align: center;'>Detection Results</h2>", unsafe_allow_html=True)


    # Display images side by side
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption='Uploaded Image.', use_column_width=True)

    annotated_image_path = annotate_image_with_boxes(image, results)
    annotated_image = Image.open(annotated_image_path)

    with col2:
        st.image(annotated_image, caption='Annotated Image.', use_column_width=True)

    annotated_image_bytes = io.BytesIO()
    annotated_image.save(annotated_image_bytes, format='JPEG')
    annotated_image_bytes.seek(0)  # Reset the stream position to the beginning
    st.sidebar.download_button(
        label="Download Annotated Image",
        data=annotated_image_bytes,
        file_name="annotated_photo.jpg",
        mime="image/jpeg"
    )
    button_placeholder.empty()



# Perform object detection if an image is uploaded
if image_path is not None:

    image = Image.open(image_path)
    analysis_placeholder = st.empty()
    if analysis_placeholder.button('Analyse Photo'):

        # the dynamic "Detecting Results..." header
        header_placeholder = st.empty()
        header_text = "Detecting Results..."
        typed_text = ""
        for char in header_text:
            typed_text += char
            header_placeholder.write(typed_text, unsafe_allow_html=True)
            time.sleep(0.07) 


        results = objectDetection(image)

        if results:
            header_placeholder.empty()
           
            st.markdown("<h2 style='text-align: center;'>Detection Results</h2>", unsafe_allow_html=True)

            # Display images side by side
            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption='Uploaded Image.', use_column_width=True)

            annotated_image_path = annotate_image_with_boxes(image, results)
            annotated_image = Image.open(annotated_image_path)

            with col2:
                st.image(annotated_image, caption='Annotated Image.', use_column_width=True)

        # Download button for annotated image
        annotated_image_bytes = io.BytesIO()
        annotated_image.save(annotated_image_bytes, format='JPEG')
        annotated_image_bytes.seek(0)  # Reset the stream position to the beginning
        st.sidebar.download_button(
            label="Download Annotated Image",
            data=annotated_image_bytes,
            file_name="annotated_photo.jpg",
            mime="image/jpeg"
        )
        analysis_placeholder.empty()

 