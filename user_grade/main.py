import requests
import re
import time
from bs4 import BeautifulSoup

header_str = '''
Cookie: bid=qslPNVL8KVE; __yadk_uid=x6rMxdAg7B0u2dVOsdLMtrQWTQ4ifElh; _vwo_uuid_v2=D152A61B581FDD37976848D468E756774|92395dde9e00d52279fb0d6e8f46e567; viewed="1438874"; push_doumail_num=0; push_noty_num=0; ll="128485"; ct=y; __gads=ID=2381e087574308dd-22faeeedfac4000c:T=1606906591:RT=1606906591:S=ALNI_MZN8RV6NZxXEseTX8j_n-oYemM5eg; __utmv=30149280.22572; __utmz=30149280.1606971052.4.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1606971059.39.27.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=30149280; __utma=30149280.299413206.1606906666.1606971052.1606982674.5; __utma=223695111.307071430.1600620354.1606971059.1606982674.40; __utmc=223695111; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1606982675%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=b17b83d1d584e666.1600620354.40.1606982815.1606976799.; dbcl2="225727052:1gGWd0LJtrc"; ck=wAAo
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36
'''

def str_to_dict(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            li2[0] = li2[0].replace(':', '')
            res[li2[0]] = li2[1]
    return res

my_headers = str_to_dict(header_str, '\n', ': ')
my_headers['Accept-Encoding'] = 'gzip'

film_id = {
           '电话': '30346025',
           '姜子牙': '25907124',
           '我想藏起来': '30170195',
           '银河守门员': '30306050',
           '最幸福的季节': '30389671',
           '夺冠': '30128916',
           '末日逃生': '30220799',
           '逃跑': '30243396',
           '无声': '33591810',
           '八佰': '26754233'}

R = [[]]
tempScore = []


def transform(input):
    if input == "rating1-t":
        return 1
    elif input == "rating2-t":
        return 2
    elif input == "rating3-t":
        return 3
    elif input == "rating4-t":
        return 4
    elif input == "rating5-t":
        return 5


def collect(all_user_id):
    for indexofuser, user in enumerate(all_user_id):
        movie_id = []
        R.append([])
        tempScore.append({})
        r = requests.get("https://movie.douban.com/people/"+user+"/collect?sort=time&filter=schedule", headers=my_headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        all_movie = soup.find_all('div', 'info', title=False)
        score = re.compile(r'rating\d-t').findall(str(all_movie))
        t = re.compile(r'https://movie.douban.com/subject/\d+').findall(str(all_movie))

        for x in t:
            movie_id.append(x[33:])
        for i, each_movie in enumerate(movie_id):
            if i < len(score):
                if each_movie not in R[0]:
                    R[0].append(each_movie)
                tempScore[indexofuser][each_movie] = score[i]

        print(indexofuser)
        time.sleep(2)
    for i in range(len(R[0])):
        for j in range(1, len(R)):
            R[j].append(0)
    for indexofuser, user in enumerate(all_user_id):
        for i in tempScore[indexofuser]:
            col = R[0].index(i)
            R[indexofuser+1][col] = transform(tempScore[indexofuser][i])
    with open("info.txt", 'w') as f:
        for t in R:
            f.write(str(t))
            f.write(",\n")


try:
    all_user_id = []
    for movie in film_id:  # 10部电影
        print("正在爬取" + movie)
        r = requests.get("https://movie.douban.com/subject/" + film_id[movie] + "/comments", headers=my_headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        all_user = soup.find_all('a', href=re.compile(r'https://www.douban.com/people/\S+/'), title=False)
        all_user_href = re.compile(r'https://www.douban.com/people/.*?/').findall(str(all_user))
        for user in all_user_href:
           all_user_id.append(user[30:-1])
        time.sleep(2)
    print("共有", len(all_user_id), "个用户")
    collect(all_user_id[:100])
except:
    print('爬取失败')