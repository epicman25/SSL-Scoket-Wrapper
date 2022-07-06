n = int(input())
str = []
res = 0
for i in bin(n)[2:]:
    if i=='1':
        res += 1
        str.append(i)
    else:
        str.append(i)
print(res)
for i in range(0,len(str)):
    if str[i]=='1':
        print(i+1)