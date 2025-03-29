import os;
from rembg import remove;


def main():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    output_folder =  os.path.join(current_directory,"output_images")

    os.makedirs(output_folder,exist_ok=True)

    for filename in os.listdir(current_directory):
        if filename.endswith((".jpeg",".jpg",".png")):
           input_path = os.path.join(current_directory,filename)
           output_path = os.path.join(output_folder,filename)

           with open(input_path,"rb") as i:
               with open(output_path,"wb") as o:
                   input_data = i.read()
                   output_data = remove(input_data)
                   o.write(output_data)

    print("Background remove complete")


main()