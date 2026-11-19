import os

try:
    import cloudinary  # type: ignore[import-not-found]
    import cloudinary.uploader  # type: ignore[import-not-found]
except ImportError:
    class _FallbackUploader:
        @staticmethod
        def upload(*args, **kwargs):
            raise RuntimeError(
                "cloudinary package is not installed. Install it with: pip install cloudinary"
            )

    class _FallbackCloudinary:
        uploader = _FallbackUploader()

        @staticmethod
        def config(*args, **kwargs):
            return None

    cloudinary = _FallbackCloudinary()

cloud_name = "mm5d2lhr"
api_key = "347276294234512"
api_secret = "gVBzHGEBbsWCY0qM7nAgQVVfZ4A"

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
)


def upload_pdf(transaction_code):
    try:
        file_path = f"receipts/{transaction_code}.pdf"
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None

        response = cloudinary.uploader.upload(file_path, resource_type="raw")
        receipt_url = response.get("secure_url")

        print("Successful upload to Cloudinary!")
        print(f"URL: {receipt_url}")

        # Optional: send email (won't crash if send_email.py is missing)
        try:
            from send_email import email
            email(
                "frankmulandi5758@gmail.com",
                "Payment received",
                f"Thank you, we have received your payment.\n\nReceipt: {receipt_url}",
            )
        except ImportError:
            pass

        return receipt_url

    except Exception as e:
        print(f"Upload failed: {e}")
        return None