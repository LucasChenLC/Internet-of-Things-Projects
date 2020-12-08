import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup


def load_file(filepath):
    try:
        html = urlopen(filepath)
    except urllib.error.HTTPError:
        print('Error opening the page, check address')
        return
    soup = BeautifulSoup(html.read(), 'html.parser')
    data = []
    table = soup.find('table')

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    del data[0]
    for s_data in data:
        del s_data[1]
        del s_data[2]
    for s_data in data:
        print(s_data[0], end='')
        index = s_data[1].find('℃')
        index1 = s_data[1].find('℃', index + 1)
        if s_data[1][index1 - 2] != '':
            print(' ', s_data[1][:index], '/', '', s_data[1][index1 - 2:index1])
        else:
            print(' ', s_data[1][:index], '/', '', s_data[1][index1 - 1:index1])
        print()


if __name__ == '__main__':
    in_data = input('Please enter the year and month you want to collect, such as "201111"')
    load_file('http://www.tianqihoubao.com/lishi/beijing/month/' + in_data + '.html')
