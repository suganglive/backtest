import random
import time

lst = ['가타카나 아','가타카나 이', '가타카나 우', '가타카나 에', '가타카나 오', '가타카나 카', '가타카나 키', '가타카나 쿠', '가타카나 케', '가타카나 코', '가타카나 사', '가타카나 시', '가타카나 스', '가타카나 세', '가타카나 소', '히라가나 아','히라가나 이', '히라가나 우', '히라가나 에', '히라가나 오', '히라가나 카', '히라가나 키', '히라가나 쿠', '히라가나 케', '히라가나 코', '히라가나 사', '히라가나 시', '히라가나 스', '히라가나 세', '히라가나 소']

random.shuffle(lst)
a = 0
for i in range(1, 31):
    print(i, lst.pop())
    time.sleep(5)
