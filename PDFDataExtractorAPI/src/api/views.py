from django.shortcuts import render
from .models import Candidate
import os
import shutil
import re
import glob
import subprocess
import textract
import xlsxwriter

# Create your views here.


class XYZ:
    def __init__(self):
        self.name = "Shantanu Fadnis"
        self.city = "Johannesburg"


def home(request):
    name = "Sarthak Kale"
    city = "Indore"
    xyz = XYZ()
    my_list = [1, 2, 3, 4, 5]
    other_list = [6, 7, 8, 9, 10]
    is_my_list = True
    values = {
        'name': name,
        'city': city,
        "xyz": xyz,
        'flag': is_my_list,
        'my_list': my_list,
        "other_list": other_list
    }
    return render(request, 'api/home.html', context=values)


def convert_to(folder, source, timeout=None):
    args = ['libreoffice', '--headless', '--convert-to',
            'pdf', '--outdir', folder, source]
    process = subprocess.run(args, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


def convertToPDF(request):
    if request.method == 'POST':
        link = request.POST
    if type(link) == list:
        for file in link:
            shutil.copyfile(src=file, dst="store"+file)
        path = str(os.getcwd())+"store"
    else:
        path = os.listdir(str(os.getcwd())+link)
    for fileName in path:
        if os.path.isdir(link+"/"+fileName):
            continue
        if fileName.split(".")[-1] == "pdf":
            shutil.copyfile(src=link+"/"+fileName,
                            dst='./docToPDF/'+fileName)
        else:
            source = link+"/"+fileName
            convert_to("./docToPDF", source)


def extractData():
    emailRegex = re.compile(
        r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', re.VERBOSE)
    mobileRegex = re.compile(
        r'((0[ -]?)|([(]?\+91[)]?[ -]?)|(\+[(]?91[)]?[ -]?))?((\d{3})[ -]?(\d{3})[ -]?(\d{4}))', re.VERBOSE)
    emails = []
    mobiles = []
    filePaths = []
    for path in glob.iglob('docToPDF/*.pdf'):
        filePaths.append(path)
        data = textract.process(path).decode('utf-8')
        email = emailRegex.findall(data)
        if len(email) == 0:
            continue
        emails.append(email[0])
        for grouplist in mobileRegex.findall(data):
            for mob in grouplist:
                if len(mob) >= 10 and mob not in mobiles:
                    mobiles.append(mob)
    print("Mobiles :", mobiles)
    print("Emails :", emails)
    print("Paths : ", filePaths)
    return (mobiles, emails, filePaths)


def fillDatabase():
    data = extractData()
    mobile = data[0]
    email = data[1]
    location = data[2]
    for row in range(len(email)):
        Candidate.objects.create(
            mobile=mobile[row], email=email[row], location=location[row])
    Candidate.save()
    createSheet()
    return (mobile, email, location)


def createSheet():
    mobile, email, path = fillDatabase()
    workbook = xlsxwriter.Workbook('tmp.xlsx')
    sheet = workbook.add_worksheet()
    sheet.write(0, 0, "Email ID")
    sheet.write(0, 1, "Contact no")
    sheet.write(0, 2, "File Location")
    for row in range(len(mobile)):
        for col in range(3):
            if col == 0:
                sheet.write(row+1, col, mobile[row])
            if col == 1:
                sheet.write(row+1, col, email[row])
            if col == 2:
                sheet.write(row+1, col, path[row].split('/')[-1])
    workbook.close()


def createTable(request):
    createSheet()
    mobiles, emails, paths = extractData()
    values = {
        'mobiles': mobiles,
        'emails': emails,
        'paths': paths
    }
    render(request, 'api/show.html', context=values)
