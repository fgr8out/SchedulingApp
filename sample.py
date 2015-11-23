from xhtml2pdf import pisa
import urllib2

url=urllib2.urlopen('localhost:5000/dashboard')
sourceHtml=url.read()
pisa.showLogging()

outputFilename = "schedule.pdf"

def convertHtmlToPdf(sourceHtml, outputFilename):
    resultFile = open(outputFilename, "w+b")
    pisaStatus = pisa.CreatePDF(sourceHtml,resultFile)
    resultFile.close()
    return pisaStatus.err

if __name__=="__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)