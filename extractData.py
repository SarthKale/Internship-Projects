import re
import PyPDF2

# ([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+) Email
emailRegex = re.compile(
    r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', re.VERBOSE)
# (^[+0-9]{1,3})*([0-9]{10,11}$) Mobile
mobileRegex = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)', re.VERBOSE)

stringEmail = '''boleh di kirim ke email saya ekoprasetyo.crb@outlook.com tks...
boleh minta kirim ke db.maulana@gmail.com. 
dee.wien@yahoo.com. .
deninainggolan@yahoo.co.id Senior Quantity Surveyor
Fajar.rohita@hotmail.com, terimakasih bu Cindy Hartanto
firmansyah1404@gmail.com saya mau dong bu cindy
fransiscajw@gmail.com  
Hi Cindy ...pls share the Salary guide to donny_tri_wardono@yahoo.co.id thank'''

emailIds = emailRegex.findall(stringEmail)
print(emailIds)
print()
pdfObj = open(
    './CVSet/abhishek.sahu0724.gmail@naukri.comabhishekDotsahuDotcer12@iitbhuDotacDotin.pdf', mode='rb')
pdf = PyPDF2.PdfFileReader(pdfObj)
string = pdf.getPage(0).extractText()
print(string)
pdfObj.close()
print(mobileRegex.findall(string))
