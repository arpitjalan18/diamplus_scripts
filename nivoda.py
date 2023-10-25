import csv
from urllib.parse import urlparse, urlunparse
from ftplib import FTP

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

    if row[index_lab] == "IGI LG":
      row[index_lab] = "IGI"
    

with open('UploadNivodaLabGrown2.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  first_line = True
  for fin in origs:
    spamwriter.writerow(fin)
    
with FTP("ftp.nivoda.net") as ftp:
    ftp.login(user="diamplusinc", passwd="m2w]4q2s") 
    file = open('UploadNivodaLabGrown2.csv', 'rb')
    ftp.cwd("/")
    ftp.storbinary("STOR stocklist.csv", file)
    file.close()
    ftp.quit()
