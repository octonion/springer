import sys
import os
import requests
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#print('Getting cwd.')

filename = sys.argv[1]
folder = sys.argv[2]

folder = os.getcwd() + f"/{folder}/"

print(folder)
if not os.path.exists(folder):
    os.mkdir(folder)

with open(filename, 'r', encoding='utf8') as f:
    all_data=f.read()

lines=all_data.split('\n')

data_rows=[]    
for l in  csv.reader(lines, quotechar='"', delimiter=',',
    quoting=csv.QUOTE_ALL, skipinitialspace=False):

    data_rows.append(l)

print('Download started.')
completed=0
total=len(data_rows)
for line in data_rows[1:]:
    #import pdb;pdb.set_trace()
    url = line[18]
    title = line[0]
    author = line[1]
    pk_name = line[11]
    
    try:

        progress=int(100*completed/total)
        print(title + ' - (' + str(progress) + '%)')
        new_folder = folder + pk_name + '/'

        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        r = requests.get(url) 
        new_url = r.url

        new_url = new_url.replace('/book/','/content/pdf/')

        new_url = new_url.replace('%2F','/')
        new_url = new_url + '.pdf'

        final = new_url.split('/')[-1]
        final = title.replace(',','-').replace('.','').replace('/',' ') + ' - ' + author.replace(',','-').replace('.','').replace('/',' ') + ' - ' + final

        myfile = requests.get(new_url, allow_redirects=True)
        open(new_folder+final, 'wb').write(myfile.content)
        
        #download epub version too if exists
        new_url = r.url

        new_url = new_url.replace('/book/','/download/epub/')
        new_url = new_url.replace('%2F','/')
        new_url = new_url + '.epub'

        final = new_url.split('/')[-1]
        final = title.replace(',','-').replace('.','').replace('/',' ') + ' - ' + author.replace(',','-').replace('.','').replace('/',' ') + ' - ' + final
        
        request = requests.get(new_url)
        if request.status_code == 200:
            myfile = requests.get(new_url, allow_redirects=True)
            open(new_folder+final, 'wb').write(myfile.content)
    except:
        print('Error when fetching book ' + str(title))
    completed=completed+1
print('Download finished.')
