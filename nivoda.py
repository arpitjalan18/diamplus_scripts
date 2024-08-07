import csv
from urllib.parse import urlparse, urlunparse
from ftplib import FTP
import shutil

origs = []

with open('../Nivoda/UploadNivodaLabGrown.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',')
  for row in spamreader:
    origs.append(row.copy())


first_line = True
index_vid = 0
index_image = 0
for row in origs:
  if first_line:   
    index_vid = row.index("Diamond Video")
    index_image = row.index("Diamond Image")
    index_lab = row.index("Lab")
    first_line = False
  else:
    vid_link = row[index_vid]

    if "https://mycertdiamvids.com/Videos" in vid_link:
      res = urlparse(vid_link)
      path_parts = res.path.split('/')
      if len(path_parts) > 3:
        path_parts[3] = "still.jpg"
      new_path = '/'.join(path_parts)
      img_link = urlunparse((res.scheme, res.netloc, new_path) + res[3:])
      row[index_image] = img_link
    elif len(vid_link) > 0:
      res = urlparse(vid_link)
      path_parts = res.path.split('/')
      if len(path_parts) > 2:
        path_parts[2] = "still.jpg"
      new_path = '/'.join(path_parts)
      img_link = urlunparse((res.scheme, res.netloc, new_path) + res[3:])
      row[index_image] = img_link

    if row[index_lab] == "IGI LG":
      row[index_lab] = "IGI"
    

with open('UploadNivodaLabGrown2.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  first_line = True
  for fin in origs:
    spamwriter.writerow(fin)
    
print("CSV succesfully generated, trying FTP upload now ...")
with FTP("ftp.nivoda.net") as ftp:
    ftp.login(user="diamplusinc", passwd="m2w]4q2s") 
    ftp.dir()
    with open('UploadNivodaLabGrown2.csv', 'rb') as file_upload:
      ftp.storbinary("STOR stocklist.csv", file_upload)
      file_upload.close()
    ftp.dir()
    ftp.quit()

print("Nivoda FTP done")