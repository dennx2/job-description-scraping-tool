# from scripts import rbc
import json
import subprocess


def main():

    data = ""

    # get a user input
    url = input("Enter job desc url: ")
    
    # check the url of the job description page and determine which module to use
    with open("url-mapping.json") as file:
        data = json.load(file)

    for key in data.keys():
        if key in url:
            subprocess.call(["python", f"scripts\{data[key]}", url])
            break
    else:
        print("Entered url is not supported")

if __name__ == "__main__":
    main()
