# The Eying App 👀

The Eying App is an object detection application built using Streamlit 🎪, capable of analyzing images for objects and annotating them with bounding boxes.

This app uses the Hugging Face Transformers library with `Facebook detr-resnet-101` object detection model.

Although it's not working due to a small error that needs to be fixed, here's the link, stay tuned:
### Eying App: [here](https://eying-object-detection-tool.streamlit.app/)

## Features

- **Object Detection**: Upload an image and detect objects present in the image.
- **Annotation**: Annotate detected objects with bounding boxes and confidence scores.
- **Download Annotated Image**: Download the annotated image with detected objects highlighted.
- **Interactive Interface**: User-friendly interface with options to upload images, analyze them, and view results.

## Installation

To run the app locally, follow these steps:

1. Clone the repository:
  
     ```bash
     git clone https://github.com/your-username/eying-app.git
     cd eying-app

2. Get an HUGGINGFACE_HUB API KEY to run the model used in this application:
     - Visit https://huggingface.co/
     - Create an Account
     - Go to settings
     - Go to Access tokens
     - Generate a token

4. Create a .env file inside eying-app and write:
      HUGGINGFACE_HUB_API_KEY="your-api-key"

5. Create a virtual environment and activate it following these steps:

     ```bash
     python -m venv name_of_env
     source name_of_env\Scripts\activate

6. install all the requirements:

    ```bash
    pip install -r requirements.txt

8. Get Streamlit working:

    ```bash
     streamlit run main.py

9. Be my guest and Enjoyy! ✨


