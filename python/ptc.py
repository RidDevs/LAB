from datetime import date

def age(birthday):
    today=date.today
    age= today.year-birthday.year
    if(today.month, today.day )<(birthday.month,birthday.day)
        age=age-1
    return age    

year = input("input birth year")
month =input("input birth month")
day = input("input day ")

birthday= date(year,month,day)

printf("age is", age(birthday))