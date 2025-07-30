def place_steps():
    for i in range(1,6):
        print("PLACE STEP")
    print("Stair complete!")

def place_torches():
    for j in range(1,11):
        print(f"PLacing torch at position", j)
        if j % 5 == 0:
            print("Extra bright torch!")


student = {
    "name":"Adrian",
    "grade":8,
    "school": "Islander Middle school"         

}


for key, value in student.items():
    print (f"{key}: {value}")