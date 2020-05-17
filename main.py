import sys
from path import Path
from taxdata import TaxData


if __name__=='__main__':
    data_path = Path(sys.argv[1])
    data_struct = TaxData(data_path)
    # load into tree data structure
    data_struct.load_data()
    print("Enter 'quit' in Prompt to exit program. Enter anything else to continue")
    prompt = ''
    while(prompt != 'quit'):
        name1 = input('Please Enter 1st Organism Name: ')
        name2 = input('Please Enter 2nd Organism Name: ')
        try:
            common_ancestor = data_struct.get_common_ancestor(name1, name2)
        except:
            print("Invalid organism names. Please try again")
            prompt = input('Prompt: ')
        else:
            print(f"Lowest Common Ancestor: {common_ancestor.name}")
            prompt = input('Prompt: ')
    print("Program Exit: Goodbye!")
