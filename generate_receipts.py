import os

try:
    from fpdf import FPDF  # pyright: ignore[reportMissingModuleSource]
except ImportError as exc:
    raise RuntimeError(
        "The 'fpdf' package is required to generate PDF receipts. Install it with: pip install fpdf"
    ) from exc

from cloudinary_service import upload_pdf

def create_pdf(payment_data, transaction_code):
    # 1. Create a NEW PDF object each time (fixes the global crash)
    pdf = FPDF()
    pdf.add_page()
    
    # 2. Ensure receipts folder exists
    if not os.path.exists("receipts"):
        os.makedirs("receipts")
        
    # 3. Add Title
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="M-PESA PAYMENT RECEIPT", ln=True, align='C')
    pdf.ln(10)
    
    # 4. Add Payment Details
    pdf.set_font('Arial', size=12)
    if isinstance(payment_data, dict):
        details = [
            f"Transaction Code: {payment_data.get('transaction_code', 'N/A')}",
            f"Amount: KES {payment_data.get('amount', 'N/A')}",
            f"Date: {payment_data.get('date', 'N/A')}",
            f"Phone: {payment_data.get('phone', 'N/A')}",
            f"Status: {payment_data.get('status', 'Completed')}"
        ]
        text_to_print = "\n".join(details)
    else:
        text_to_print = str(payment_data)
    
    pdf.multi_cell(0, 10, txt=text_to_print, align='L')
    
    # 5. Save the PDF locally
    filepath = f'receipts/{transaction_code}.pdf'
    pdf.output(filepath)
    print(f"PDF saved locally at: {filepath}")
    
    # 6. Upload to Cloudinary and RETURN the actual URL
    return upload_pdf(transaction_code)