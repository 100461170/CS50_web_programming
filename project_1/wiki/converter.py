import markdown2
import os


origin_directory = "/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries"
destination_directory = "/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia"

for filename in os.listdir(origin_directory):
    file = origin_directory + "/" + filename
    file_html = filename[:-2] + "html"
    file_dest = destination_directory + "/" + file_html
    with open(file, "r+") as f:
        markdown_text = f.read()
        converted_text = markdown2.markdown(markdown_text)
    with open(file_dest, "w+") as f:
        f.write(converted_text)