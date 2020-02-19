import requests
from bs4 import BeautifulSoup
import csv 

#所有使用时可以修改的部分
url = 'http://webf10.gw.com.cn/SH/B8/SH601628_B8.html'
fieldnames = ['姓名', '性别', '学历', '职务', '出生日期', '任职日期', '简历']
target_list = ['董事长','总裁','副总裁']
file_name = 'resume.csv'


resume_file =  open(file_name, mode = 'w')
writer = csv.writer(resume_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(fieldnames)
record_list = []
is_target = 0
# 判断是否是我们所需要的对象身份
is_next = 0
# 判断下一个‘简历’是否是我们需要保存的

r = requests.get(url)
content = r.content
soup = BeautifulSoup(content)
for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    for i in range(len(tds)):
        content = str(tds[i].contents[0]).split('</pre>')[0].split('<pre>')[-1].split(':')
        # 判断并保存部分
        print(content[-1])
        for target in target_list:
            if content[-1].split(' ')[-1] == target:
                is_target = 1
        
        if is_next == 1 and is_target == 1:
            result_list = record_list[0:6]
            result_list.append(content[0])
            writer.writerow(result_list)
            is_next = 0
            is_target = 0
            record_list = []

        if content[0] == '简历' and is_target == 1:
            is_next = 1


        record_list.append(content[-1])

        if len(record_list) == 8 and is_next == 0:
            record_list = record_list[1:8]
        # 记录所有已经读取的信息，为了节约内存，数组长度控制在7


        






