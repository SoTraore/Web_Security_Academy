print("[", end="\n")

with open(r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\password.txt', "r") as file:
    passList = file.read().splitlines()
    file.close()
    
for password in passList :
    print(f'"{password}",', end="\n")
    
print("]")