# Image EXIF Remover Flask App

This Flask application allows users to upload images, processes them to remove EXIF data, and provides the processed images for download. The application ensures that no EXIF data remains in the uploaded images.

## Features
- Upload images with EXIF data.
- Process images to remove EXIF data.
- Download processed images without EXIF data.
- Scan and process images in a folder.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/image-exif-remover.git
    cd image-exif-remover
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask app:**
    ```bash
    python app.py
    ```

2. **Open your browser and go to:**
    ```
    http://127.0.0.1:5000/
    ```

3. **Upload an image and process it to remove EXIF data.**

## Testing

To run the unit tests to ensure EXIF data removal functionality, use the following command:

```bash
python -m unittest test_app.py
