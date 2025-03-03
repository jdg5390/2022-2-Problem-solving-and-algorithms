#문제해결과 알고리즘 러닝페어 1조 암호생성 
#tkinter 최종 코드
import random
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

#tkinter 실행
tk = Tk()
tk.geometry("500x600+120+50")
tk.resizable(True, True)
tk.title("암호 생성기")

#엔트리 관리 클래스 
class EntryManager:
    def __init__(self):
        self.entrys: dict[str, Entry] = {}

    def make_entry(self, name: str, value: str):
        self.entrys[name] = Entry(value)

    def get_entry_by_name(self, name: str):
        return self.entrys[name].get()

    def pack_entry(self, name: str):
        self.entrys[name].pack()
em = EntryManager()

#사용할 Font 정의
important = Font(family='맑은 바탕', size=20, weight='bold')
small = Font(family='굴림', size = 13)

#PW 생성 버튼을 클릭했을 때 전역 변수 값 변경하는 함수
def choose_btn():
    global cipher
    cipher = 'PW'
    open_frame(frame1, frame_cip)

#프레임 변경 함수
def open_frame(frame1, frame2):
    frame2.tkraise()
    frame2.pack(fill='both', expand=True)
    frame1.destroy()
    #변경 후 해당 프레임에 label, entry, button 배치
    label_id = Label(frame_cip, text= f"아래에 몇 자리의 {cipher}를 생성하고 싶은지 입력하세요.\n(잘못 입력 시, 다시 입력하고 입력 완료를 누르면 됩니다.)",
    font=small)
    ent_id1 = Entry(frame_cip)
    btnid_1= Button(frame_cip, text='입력 완료', command = lambda:submit_digit(ent_id1, cipher), font=small)
    label_id.pack()
    ent_id1.pack()
    btnid_1.pack(ipadx=2, ipady=2)

#id생성 함수들
def submit_digit(entry, cipher): #몇 자리로 생성할지
    global digit, num
    digit = entry.get()
    num = int(int(digit) / 2)  #추출할 자릿수 <= 전체 자릿수의 절반. (홀수 입력 시에는 반내림)
    #참고할 기존 ID입력받기
    label_id2 = Label(frame_cip, text=f'아래에 {cipher}생성을 위해 참고할 기존 {cipher} 개수를 입력하세요.', font=small)
    ent_id2 = Entry(frame_cip)
    btnid_2 = Button(frame_cip, text='입력 완료', command = lambda:entry_making(ent_id2, cipher), font=small)
    label_id2.pack()
    ent_id2.pack()
    btnid_2.pack(ipadx=2, ipady=2)

#기존에 사용하던 id 개수, 정보 입력 함수
def entry_making(entry, cipher):
    global ID_num
    label_id3 = Label(frame_cip, text=f'기존에 사용하던 {cipher}를 입력해주세요.', font=small)
    label_id3.pack()
    ID_num = int(entry.get())
    for i in range(0,ID_num): #엔트리 관리 클래스 -> ID입력 받는 엔트리 0,1,2... 생성
        em.make_entry(f'entry_{i}', frame_cip)
        em.pack_entry(f'entry_{i}') 
    btnid_3 = Button(frame_cip, text=f'기존 {cipher} 입력완료', command = lambda:extract(cipher), font=small) #
    btnid_3.pack(ipadx=2, ipady=2) #버튼 생성

def extract(cipher):
    global list_join, idx, inputLen
    for i in range(0,ID_num):
        word = em.get_entry_by_name(f'entry_{i}')  #엔트리에 입력받은 데이터를 word에 저장
        length = len(word) #word에 저장한 ID/PW의 길이를 변수로 저장.
        for j in range(0,length):  #입력한 id를 한글자씩 뽑아서 dictionary에 빈도 수 저장
            letter = word[j]  #인덱스 0에 위치한 첫 번째 문자부터 letter 변수로 초기화
            if letter not in dic.keys(): #해당 인덱스의 문자가, 추출하여 저장한 딕셔너리에 없으면 value == 1(True)로 추가.
                dic[letter] = 1
            else:
                dic[letter] = dic[letter]+1 #해당 인덱스의 문자가, 추출하여 저장한 딕셔너리에 이미 있으면 value에 1추가
    #dic.items() #딕셔너리 형식의 dic에서 key와 value를 리스트 속 튜플로 객체 반환. ex) {'a':3,'b':3} -> [('a',3),('b',3)]
    sortedDic = sorted(dic.items(), key = lambda x:x[1], reverse = True) #dic에서의 value(사용 빈도)를 기준(key)으로, 내림차순(빈도수 높은 순) 초기화.
    out = [item for _ in sortedDic for item in _] #dic의 키와 밸류를 각각의 데이터로 딕셔너리 생성. ex) [('a',3), ('b',3)] -> ['a',3,'b',3]

    list = [] #빈도수 높은 순으로 'digit - num' 개의 데이터를 저장할 리스트 생성
    idx = min(num, len(sortedDic)) #기존 ID가 num보다 자릿수가 적을 때는 기존 ID를 기준으로 추출해야하므로,
                                #추출할 자릿수와 정리된 dic 데이터 수 중 작은 값을 변수로 초기화

    for i in range(0,idx):  #입력한 자리수 / 2 만큼 뽑아내기 (빈도 순으로 정렬)
        list.append(out[i*2]) #out이 ['a',3,'b',3]의 형태이므로 dic에서 key였던 문자는 짝수 인덱스에 존재함 -> *2로 인덱싱해서 append

        #list 요소 하나의 문자열로 병합 후 중간 출력하기. (사용자에게 익숙한 문자열)
    list_join = ''.join(list) # list 요소를 하나의 문자열로 합쳐서 초기화. ex) ['a','b','c','d'] -> abcd
    fin_list.append(list_join) #합친 문자열 fin_list에 추가
    inputLen = int(digit) - idx #추가로 입력 받을 자릿수 계산하여 초기화

    extracted_str = Message(frame_cip, text=f'추출된 문자열: {list_join}', relief = 'groove',
     width = 1000, justify = 'left', bd=2, bg='#ffe500', fg='blue', font = important) #추출된 문자열 출력.
    extracted_str.pack(padx = 2, pady= 2) #배치
    if cipher == 'ID':
        blank = ''
    else:
        blank = '특수문자, '
    add_label = Label(frame_cip, text=f"나머지 {inputLen}자리에 추가할 문자를 입력하세요.\n({blank}영어 대소문자, 숫자)",font=small) #남은 자리 input 받아서 문자열로 초기화
    add_label.pack()
    em.make_entry('add_str', frame_cip)
    em.pack_entry('add_str')
    add_btn = Button(frame_cip, text='새로운 암호 생성', command=lambda:fin_shuffle(),font=small)
    add_btn.pack()

#마지막 단계: 무작위 셔플 후 생성된 암호 출력
def fin_shuffle():
    global count
    if count == -1: #첫 실행일 때: 입력받은 str 추가.
        added = em.get_entry_by_name('add_str')
        added_list = added[:inputLen] #사용자가 실수로 더 많이 추가 했을 수도 있으므로, 추가로 입력 받을 자릿수만큼만 인덱싱해서 초기화.
        for i in range(0,len(added_list)): #입력 받은 문자들을 인덱싱하여 하나씩 fin_list에 추가하는 반복문.
            fin_list.append(added[i])
        random.shuffle(fin_list)  #리스트 요소 무작위 셔플
        result_ID = ''.join(fin_list) #섞은 리스트 요소를 하나의 문자열로 병합
    else:   #두 번 이상 실행 시: 순서 무작위 배열 반복
        random.shuffle(fin_list)  #리스트 요소 무작위 셔플
        result_ID = ''.join(fin_list) #섞은 리스트 요소를 하나의 문자열로 병합
    result_msg = messagebox.askyesno(title = '암호 생성 결과', message= f'생성된 암호:   {result_ID}', 
    detail='해당 암호를 사용하려면 \'예\', 재생성하려면 \'아니오\'를 눌러주세요.') #결과 출력, 종료 버튼 or frame1로 돌아가는 messagebox 생성.
    if result_msg:
        exit()
    else:
        count = 0
        fin_shuffle()

#변수 초기화
cipher = 'ID' #암호 선택의 기본 값은 ID로 초기화, 이후 PW생성 선택 시 값 변화.
dic = {} #입력 받은 ID 중, 빈도수가 높은 순으로 추출하여 저장할 딕셔너리 초기화.
fin_list = [] #최종적으로 랜덤 셔플 될 요소를 저장하는 리스트 초기화.
count = -1 #첫 실행인지 아닌지 구분하기 위한 카운트 초기화.

#프레임 생성
frame1 = Frame(tk, relief = 'solid', bd=10) #메인 메뉴 프레임
frame_cip = Frame(tk, relief = 'solid', bd=10) #id 생성 프레임

#메인 화면 label 배치
label1 = Label(frame1, text='생성하고자 하는 암호를 선택하세요.', relief = 'groove', font=important)
label1.pack()

#각 생성 및 종료 버튼
btn1 = Button(frame1, text = 'ID 생성', command = lambda:[open_frame(frame1, frame_cip)], font=small) #lambda: 버튼 생성되자마자 바로 실행되는 걸 막는다.
btn2 = Button(frame1, text = 'PW 생성', command = lambda:[choose_btn()], font=small)
btn_quit = Button(frame1, text = '프로그램 종료', command = quit, font=small)

btn1.pack(ipadx=2, ipady=2)
btn2.pack(ipadx=2, ipady=2)
btn_quit.pack(ipadx=2, ipady=2)

#메인 화면 프레임 pack
frame1.pack(fill='both', expand=True)
tk.mainloop()