import csv
from urllib.parse import urlparse, urlunparse
from ftplib import FTP
origs = []

with open('UploadVDBLabGrown.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',')
  for row in spamreader:
    origs.append(row.copy())


first_line = True
index_vid = 0
index_image = 0
index_cert_number = 0
index_cert_link = 0
index_member_comments = 0 
for row in origs:
  if first_line:   
    index_vid = row.index(" Video Link")
    index_image = row.index(" Image Link")
    index_cert_number = row.index(" Certificate #")
    index_cert_url = row.index(" Certificate Url")
    index_member_comments = row.index(" Member Comments")
    
    first_line = False
  else:
    vid_link = row[index_vid]
    res = urlparse(vid_link)
   
    path_parts = res.path.split('/')
    path_parts[3] = "still.jpg"
    new_path = '/'.join(path_parts)
    img_link = urlunparse((res.scheme, res.netloc, new_path) + res[3:])
   
    row[index_image] = img_link

    cert_number = (row[index_cert_number])[2:]
    row[index_cert_url] = "https://www.igi.org/viewpdf.php?r=%s" % cert_number

    row[index_member_comments] = "Do not have different prices for Memo and COD"
    

with open('UploadVDBLabGrown2.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  first_line = True
  for fin in origs:
    spamwriter.writerow(fin)


with FTP("ftp1.at.proftpd.org") as ftp:
    ftp.login()
    ftp.dir()