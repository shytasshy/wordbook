a = [1,2,3,4,6,7,8]
j = 0
hitj = 0
while j < len(a) or hitj == 0:
    print("a")
    j += 1
    for i in range(0,len(a)-1):
        flag = 0
        if a[i] == j:
            print("hit")
            break
        flag = 1
    if flag == 1:
        hitj = j
    print(hitj)

print(hitj)