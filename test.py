#조건 입력 인풋(나이대, 성별) - 리스트로 만들어서 조건과 가장 가까운것 점수 + 1
user = [['M', 10, 'science'], ['F', 20, 'math']]
score = [0, 0]

gender = input("gender(M or F): ")
age = int(input("age: "))
major = input("major: ")

for i in range(len(user)):
    if gender == user[i][0]:
        score[i] += 1
    else:
        score[i] += 0

    score[i] = score[i]*0.4

    age_score = age - user[i][1]

    #age
    if age_score > 50:
        age_score = 0
    elif age_score < 50 and age_score > 0:
        age_score = age_score*0.5
    else:
        score[i] += (-age_score) * 0.3

    score[i] += (age_score * 0.4)

    #major
    if major == user[i][2]:
        score[i] += 1
    else:
        score[i] += 0

    score[i] = score[i]*0.6

for i in range(len(score)):
    for i in range(len(score)-1):
        if score[i] <= score[i+1]:
            score[i], score[i+1] = score[i+1], score[i]
        b = 0
        for i in range(len(score)):
            if score[b] > score[i]:
                b = i
print(score)

print("score", score[i])
print("user", user[i])