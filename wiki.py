from random import choice
from bs4 import BeautifulSoup
import cloudscraper
import sys
import re
import keyboard
import webbrowser


if 2 > len(sys.argv) < 4:
    print('검색어를 함께 입력해주세요.')
    print('예시) wiki "구글"')
    sys.exit()
else:
    if len(sys.argv) == 3 and sys.argv[1] == '-i':    
        argv = sys.argv[2]
    else:
        argv = sys.argv[1]

if sys.argv[1] == '-h':
    print('옵션)')
    print('\t-i : interactive (대화형 모드)')
    print('\t\t사용예시) wiki -i "검색어"')
    sys.exit()


def pause():
    print('계속하려면 <Enter>키를 누르십시오 . . .')
    keyboard.wait('Enter')
    

def print_heading(text):
    regex = re.compile('[ㄱ-ㅎ가-힣]')
    kor = regex.findall(text)
    length = len(text) - len(kor) + len(kor) * 2 + 2

    print('┏' + '━' * length + '┓' )
    print('┃ ' + text + ' ┃')
    print('┗' + '━' * length + '┛' )


def print_menu():
    print('문서 열람: [문서 번호] ┃ 웹 이동: [O]pen ┃ 나가기:[E]xit')

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'}


base_url = 'https://namu.wiki/w/'

url = base_url + argv

scraper = cloudscraper.create_scraper()


if __name__ == '__main__':
    
    response = scraper.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        headings = soup.select('.toc-item')
        contents = soup.select('.wiki-heading-content')

        index = 0

        if len(sys.argv) == 3 and sys.argv[1] == '-i':
            while True:
                heading_nums = {}
                for heading in headings:
                    print_heading(heading.text)
                    heading_num = heading.text.split(' ')[0]
                    heading_nums[heading_num] = index
                
                    heading_num = heading.text.split(' ')[0][:-1]
                    heading_nums[heading_num] = index

                    index += 1
                
                print_menu()

                try:
                    choice_menu = input('>> ')
                except KeyboardInterrupt as e:
                    print('나가기\n')
                    sys.exit()
                print()

                if choice_menu in heading_nums:
                    index = heading_nums[choice_menu]
                    print_heading(headings[index].text)
                    
                    if len(contents[index].text) <= 0:
                        print('<비어있음>')
                    else:
                        for content in contents[index]:
                            print(content.text)
                        
                    print()
                    pause()
                if choice_menu.lower() == 'o':
                    print( '\"' + url + '\"' + '으로 이동합니다.')                    
                    webbrowser.open(url)
                    pause()
                    
                if choice_menu.lower() == 'e':
                    sys.exit()

                index = 0
        else:
            for heading in headings:
                print_heading(heading.text)

                if len(contents[index].text) <= 0:
                    print('<비어있음>')
                else:
                    for content in contents[index]:
                        print(content.text)

                index += 1
                print()

    else:
        print('에러 코드:', response.status_code)

        if response.status_code == 404:
            print('존재하지 않는 페이지입니다.')