from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime
import uuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64
from time import localtime
from reportlab.lib.units import cm

def generate_birth_certificate_pdf(birth_certificate, user=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin_left = 2 * cm
    margin_right = width - 2 * cm
    y = height - 3 * cm
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, y, "People's Democratic Republic of Algeria")
    y -= 1 * cm
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "BIRTH CERTIFICATE")
    y -= 2 * cm

    # Section: Personal Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Personal Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"First Name: {birth_certificate.first_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Last Name: {birth_certificate.last_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Date of Birth: {birth_certificate.birth_date}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Time of Birth: {birth_certificate.birth_time}")
    y -= 1 * cm

    # Section: Location
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Birthplace")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Wilaya: {birth_certificate.birth_wilaya}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Commune: {birth_certificate.birth_commune}")
    y -= 1 * cm

    # Section: Parents
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Parent Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Father's Name: {birth_certificate.father_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Mother's Name: {birth_certificate.mother_name}")
    y -= 1 * cm

    # Birth Number
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Official Details")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Birth Number: {birth_certificate.birth_number}")
    
    # Signature at bottom
    c.setFont("Helvetica-Oblique", 10)
    if user:
        signature_text = f"Signed by: {user.info.get_organization().name}-{user.info.Organization} - {user.username}"
    else:
        signature_text = "Signature"
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    c.drawRightString(margin_right, 2 * cm, signature_text)
    c.drawRightString(margin_right, 1.5 * cm, f"Date: {timestamp}")

    # Finalize
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def generate_death_certificate_pdf(death_certificate, user=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin_left = 2 * cm
    margin_right = width - 2 * cm
    y = height - 3 * cm

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, y, "People's Democratic Republic of Algeria")
    y -= 1 * cm
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "DEATH RECORD CERTIFICATE")
    y -= 2 * cm

    # Section: Personal Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Personal Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"First Name: {death_certificate.first_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Last Name: {death_certificate.last_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Sex: {death_certificate.sex}")
    y -= 1 * cm

    # Section: Birth Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Birth Details")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Date of Birth: {death_certificate.birth_date}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Wilaya: {death_certificate.birth_wilaya}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Commune: {death_certificate.birth_commune}")
    y -= 1 * cm

    # Section: Death Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Death Details")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Date of Death: {death_certificate.death_date}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Time of Death: {death_certificate.death_time}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Wilaya: {death_certificate.death_wilaya}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Commune: {death_certificate.death_commune}")
    y -= 1 * cm

    # Section: Family Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Family Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Father's Name: {death_certificate.father_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Mother's Name: {death_certificate.mother_name}")
    y -= 1 * cm

    # Other
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Other Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Death Number: {death_certificate.death_number}")

    # Signature at the bottom
    c.setFont("Helvetica-Oblique", 10)
    if user:
        signature_text = f"Signed by: {user.info.get_organization().name}-{user.info.Organization} - {user.username}"
    else:
        signature_text = "Signature"
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    c.drawRightString(margin_right, 2 * cm, signature_text)
    c.drawRightString(margin_right, 1.5 * cm, f"Date: {timestamp}")

    # Finalize
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def generate_burial_permit_pdf(burial_permit, user=None):
    death_certificate = burial_permit.certificate

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin_left = 2 * cm
    margin_right = width - 2 * cm
    y = height - 3 * cm

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, y, "People's Democratic Republic of Algeria")
    y -= 1 * cm

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "BURIAL PERMIT")
    y -= 2 * cm

    # Section: Deceased Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Deceased Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"First Name: {death_certificate.first_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Last Name: {death_certificate.last_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Sex: {death_certificate.sex}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Date of Birth: {death_certificate.birth_date}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Date of Death: {death_certificate.death_date}")
    y -= 1 * cm

    # Section: Death Location
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Death Location")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Wilaya: {death_certificate.death_wilaya}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Commune: {death_certificate.death_commune}")
    y -= 1 * cm

    # Section: Family Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Family Information")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Father's Name: {death_certificate.father_name}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Mother's Name: {death_certificate.mother_name}")
    y -= 1 * cm

    # Section: Approval Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, "Burial Permit Info")
    y -= 1 * cm

    c.setFont("Helvetica", 12)
    c.drawString(margin_left, y, f"Approved: {'Yes' if burial_permit.approved else 'No'}")
    y -= 0.8 * cm
    c.drawString(margin_left, y, f"Death Certificate Number: {death_certificate.certificate_number}")
    y -= 1 * cm

    # Signature
    c.setFont("Helvetica-Oblique", 10)
    if user:
        signature_text = f"Signed by: {user.info.get_organization().name}-{user.info.Organization} - {user.username}"
    else:
        signature_text = "Signature"
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    c.drawRightString(margin_right, 2 * cm, signature_text)
    c.drawRightString(margin_right, 1.5 * cm, f"Date: {timestamp}")

    # Finalize
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer



def sign_pdf(pdf_buffer):

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get PDF content
    pdf_content = pdf_buffer.getvalue()
    
    # Create a signature
    signature = private_key.sign(
        pdf_content,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    # For a real implementation, you would embed this signature in the PDF
    # Here, we'll just return both
    return {
        'pdf': pdf_content,
        'signature': base64.b64encode(signature).decode('utf-8')
    }
