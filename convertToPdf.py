import os
import sys
import subprocess
import re


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
        print()
        print(self.output)
        print()


if __name__ == "__main__":
    folderPath = os.listdir(str(os.getcwd())+"/CVSet")
    for fileName in folderPath:
        if fileName.split(".")[-1] == "pdf":
            continue
        else:
            source = "./CVSet/"+fileName
            print("It is a word file:", source)
            convert_to("./docToPDF", source)
    # convert_to(
    #     "./docToPDF", "./CVSet/akash.gupta13920.gmail@naukri.comakashDotgupta13920@gmailDotcom.docx")
