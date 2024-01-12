# PROJECTS
#QR CODE GENERATING PROJECT
import qrcode

# Taking the UPI ID as input from user
upi_id = input("Enter your UPI ID = ")

# Defining the payment URL based on the UPI ID and the payment app

phonepe_url = f'upi://pay?pa={upi_id}&pn=Recipient%2eName&mc=1234'
paytm_url = f'upi://pay?pa={upi_id}&pn=Recipient%2eName&mc=1234'
google_pay_url = f'upi://pay?pa={upi_id}&pn=Recipient%2eName&mc=1234'

# Creating  QR Codes for each payment app
phonepe_qr = qrcode.make(phonepe_url)
paytm_qr = qrcode.make(paytm_url)
google_pay_qr = qrcode.make(google_pay_url)

# Saving the QR codes to image files 
phonepe_qr.save('phonepe_qr.png')
paytm_qr.save('paytm_qr.png')
google_pay_qr.save('google_pay_qr.png')
