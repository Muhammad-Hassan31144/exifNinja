import unittest
from app import app, remove_exif
from PIL import Image, ExifTags
import io
import os

class TestRemoveExif(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

        # Ensure directories exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    def tearDown(self):
        # Clean up the directories
        for folder in [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER']]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def test_remove_exif(self):
        # Create an image with EXIF data
        img = Image.new('RGB', (100, 100), color = 'red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95, exif=b"Exif\x00\x00")

        # Check that EXIF data exists in the original image
        img_with_exif = Image.open(io.BytesIO(img_bytes.getvalue()))
        exif_data = img_with_exif._getexif()
        self.assertIsNotNone(exif_data, "The image should have EXIF data")

        # Remove EXIF data using the remove_exif function
        img_without_exif = remove_exif(img_with_exif)
        exif_data_removed = img_without_exif.info.get('exif')
        self.assertIsNone(exif_data_removed, "The EXIF data should be removed from the image")

    def test_upload_and_process_image(self):
        # Create an image with EXIF data
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=95, exif=b"Exif\x00\x00")
        img_bytes.seek(0)

        # Upload the image
        response = self.app.post('/upload', data={
            'photo': (img_bytes, 'test_image.jpg')
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)

        # Process the image
        filenames = 'test_image.jpg'
        response = self.app.get(f'/process/{filenames}')
        self.assertEqual(response.status_code, 200)

        # Check if the processed image exists and verify no EXIF data
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], 'test_image.jpg')
        self.assertTrue(os.path.exists(processed_path), "Processed image should exist")

        img_processed = Image.open(processed_path)
        exif_data = img_processed.info.get('exif')
        self.assertIsNone(exif_data, "The EXIF data should be removed from the processed image")

if __name__ == '__main__':
    unittest.main()
