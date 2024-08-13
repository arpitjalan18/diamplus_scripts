import csv
from urllib.parse import urlparse, urlunparse
from ftplib import FTP
origs = []

import paramiko

with open('../VDB/UploadVDBLabGrown.csv', newline='') as csvfile:
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
    index_lab = row.index(" Lab")
    
    first_line = False
  else:
    vid_link = row[index_vid]
    res = urlparse(vid_link)
   
    path_parts = res.path.split('/')
    path_parts[-1] = "still.jpg"
    new_path = '/'.join(path_parts)
    img_link = urlunparse((res.scheme, res.netloc, new_path) + res[3:])
   
    row[index_image] = img_link

    cert_number = (row[index_cert_number])[2:]
    row[index_cert_url] = "https://www.igi.org/viewpdf.php?r=%s" % cert_number

    row[index_member_comments] = "Do not have different prices for Memo and COD"

    #change lab
    if index_lab >= 0 and row[index_lab] == "IGI LG":
      row[index_lab] = "IGI"
    

with open('UploadVDBLabGrown2.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  first_line = True
  for fin in origs:
    spamwriter.writerow(fin)

print("Sucesfully created file to upload, trying FTP now ...")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#key = paramiko.RSAKey.from_private_key_file('vdb_pem_key.pem')
ssh.connect('ftphost.vdbapp.com', username='diamplus_inc@yahoo.com', password = 'VdbFTP@2024')#, pkey=key)
print("succesful login to sftp server")
sftp = ssh.open_sftp()
sftp.put('UploadVDBLabGrown2.csv', '/Root Folder')
print('success')