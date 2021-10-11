from datetime import datetime

name='김혜린'
age='25'
hello='제 이름은 '+name+'이구요'
hello2=f'제 이름은 {name}입니다. 나이는 {age}입니다.'
print(hello2)

today=datetime.now()
mytime=today.strftime('%Y-%m-%d %H:%M:%S')
print(mytime)

filename=f'file-{mytime}'
print(filename)