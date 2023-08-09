from secrets import choice
from chaos import Chaos, DNA
from matplotlib import pyplot

pyplot.figure(figsize=(9, 8))
pyplot.figure(1).tight_layout()

#User Inputs
num_of_dots = None
distance_to_move = None
polygon_sides = None

def take_inputs(sequence:str= 'r') -> None:
    """
    Take Necessary Inputs from user.
    Parameters:
        sequence [type: str] = Is used to change the inputs to be asked
    """
    global num_of_dots, distance_to_move, polygon_sides

    recived_data = False
    while not recived_data:
        if sequence == 'r':
            polygon_sides_input = input("Number Of Side: ")
            num_of_dots_input = input("Number Of Dots To Plot: ")

        distance_to_move_input = input("Fraction of Distance To Move Between Points and Vertex. Must Be: 0 < r < 1. \nEnter: ")

        try:
            if sequence == 'r':
                num_of_dots = int(num_of_dots_input)
                polygon_sides = int(polygon_sides_input)
                
            distance_to_move = float(distance_to_move_input)

            if (distance_to_move <= 0 or distance_to_move >= 1): 
                raise Exception("Fraction of Distance To Move Between Points and Vertex. Must Be: 0 < r < 1.")

            recived_data = True

        except Exception as exp:
            print(f"\n{exp}\n")

def ask_choice(*choices):
    while True:
        for count, choice in enumerate(choices,1):
            print(f"{count} --> {choice}")

        choice = input("Enter a Number: ").replace(" ","")

        if len(choice) == 1:
            one = ord("1")
            last = ord(str(len(choices)))
            choice_ascii = ord(choice)

            if (choice_ascii >= one) and (choice_ascii <= last): return choices[int(choice_ascii) - int(one)]

        print(f"PLEASE ENTER NUMBER BETWEEN 1 AND {len(choices)}\n")

def check_file(path: str):
    try:
        open(path, 'r')
        return True
    except:
        print(f"Failed to locate {path}\nPLEASE CHECK IF {path} AND CODE IS IN THE SAME FOLDER\n")
        return False


print("WELCOME TO CHAOS GAME\n")

#Asking to choose Random or Genetic Sequence
choices = ("Random Sequenec", "Genetic Sequence", "Exit")
choice = ask_choice(*choices)

if choice == "Exit": exit()

sequence = choice[0]
#Creating Diffrent Classes based on choosen Sequence
if sequence == 'R':
    take_inputs()

    chaos = Chaos(num_of_dots, distance_to_move, polygon_sides)
    chaos.run()

elif sequence == 'G':
    file_exsists = False
    while not file_exsists:
        choices = ("SmallHumanY_data.txt","HumanY_data.txt", "Exit")
        choice = ask_choice(*choices)

        if choice == "Exit":
            exit()

        file_path = choice
        file_exsists = check_file(file_path)

    take_inputs(sequence)

    dna = DNA(file_path, distance_to_move)
    dna.run(0.005 if file_path == "HumanY_data.txt" else 0.1)

pyplot.show()

