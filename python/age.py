from datetime import date

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

year = int(input("Enter birth year (YYYY): "))
month = int(input("Enter birth month (MM): "))
day = int(input("Enter birth day (DD): "))

birth_date = date(year, month, day)
print("Your age is:", calculate_age(birth_date))
