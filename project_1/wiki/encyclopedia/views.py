from django.shortcuts import render
from . import util
import markdown2
import os, random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_page = util.get_entry(title)
    if entry_page is None:
            return render(request, "encyclopedia/error_page.html")
    else:
        return render(request, f"encyclopedia/{title}.html")
    
            
def search(request):
    if request.method == 'POST':
        title = request.POST
        title = title['q']
    searched_page = util.get_entry(title)
    old_entries = util.list_entries()
    new_entries = []
    if searched_page:
        return render(request, f"encyclopedia/{title}.html")
    else:
        for item in old_entries:
            if str.__contains__(item, title):
                new_entries.append(item)
        return render(request, "encyclopedia/index.html", {
        "entries": new_entries})

def create(request):
    return render(request, "encyclopedia/create.html")

def create_page(request):

    if request.method == 'POST':
        wiki_entry = request.POST
    wiki_title = wiki_entry['title']
    wiki_content = wiki_entry['markdown_input']
    if util.get_entry(wiki_title) is None:
        util.save_entry(wiki_title, wiki_content)
        with open(f"entries/{wiki_title}.md", "r") as f:
            read_text = f.read()
            markdown_text = markdown2.markdown(read_text)
            new_doc = {"line0": '{% extends "encyclopedia/layout_entries.html" %}\n',
                   "line1": '\n',
                   "line2": '{% block body %}\n',
                   "line3": markdown_text,
                   "line4": '{% endblock %}\n',
                   "line5": '{% block hidden %}\n',
                   "line6": f'<input name="title" type="hidden" value="{wiki_title}">\n',
                   "line7": '\n',
                   "line8": '{% endblock %}'
                   }
        with open(f"encyclopedia/templates/encyclopedia/{wiki_title}.html", "w+") as f:
            for item in new_doc:
                f.write(new_doc[item])
        return render(request, f"encyclopedia/{wiki_title}.html")
        
    else:
        return render(request, "encyclopedia/error_page.html")

def edit(request):
    if request.method == 'POST':
        document = request.POST
    title = document["title"]
    with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{title}.md", "r+") as f:
        text = f.read()
    return render(request, "encyclopedia/edit.html", {
        "text": text,
        "title": title,
    })
def edit_page(request):
    if request.method == 'POST':
        document = request.POST
    old_title = document["old_title"]
    new_title = document["title"]
    text = document["markdown_input"]
    with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{old_title}.md", 
                  "w+") as f:
        f.write(text)
    if old_title == new_title:
        
        new_doc = {"line0": '{% extends "encyclopedia/layout_entries.html" %}\n',
                   "line1": '\n',
                   "line2": '{% block body %}\n',
                   "line3": markdown2.markdown(text),
                   "line4": '{% endblock %}\n',
                   "line5": '{% block hidden %}\n',
                   "line6": f'<input name="title" type="hidden" value="{new_title}">\n',
                   "line7": '\n',
                   "line8": '{% endblock %}'
                   }
        with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{new_title}.html", "w+") as f:
            for item in new_doc:
                f.write(new_doc[item])
    else:
        os.rename(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{old_title}.md", 
                      f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{new_title}.md")
        # change html
        new_doc = {"line0": '{% extends "encyclopedia/layout_entries.html" %}\n',
                   "line1": '\n',
                   "line2": '{% block body %}\n',
                   "line3": markdown2.markdown(text),
                   "line4": '{% endblock %}\n',
                   "line5": '{% block hidden %}\n',
                   "line6": f'<input name="title" type="hidden" value="{new_title}">\n',
                   "line7": '\n',
                   "line8": '{% endblock %}'
                   }
        with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{old_title}.html", "w+") as f:
            for item in new_doc:
                f.write(new_doc[item])
        os.rename(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{old_title}.html", 
                  f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{new_title}.html")
        
    return render(request, f"encyclopedia/{new_title}.html") 
        
            
    
    
    
    
    
    
    """ 
    # if title did not change
    if old_title == new_title:

        with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{new_title}.md", 
                  "w+") as f:
            f.write(text)
        # change html
        counter = 0
        html_text = markdown2.markdown(text)
        with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{new_title}.html", "w+") as f:
            buffer = f.read(1)
            counter += 1
            block_body = "{% block body %}"
            end_block = "{% endblock %}"
            while buffer:
                f.write("AQUI 1")
                if buffer == "{":
                    f.write("AQUI 2")
                    key_word = "{" + f.read(15)
                    if key_word == block_body:
                        f.write("AQUI 3")
                        counter += 15
                        f.write(html_text)
                        counter += len(html_text)
                        buffer = f.read(1)
                        while buffer == "{":
                            f.write("AQUI 4")
                            f.write("")
                            buffer = f.read(1)
                buffer = f.read(1)
                counter += 1
        # with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{new_title}.html", "w+") as f:
        #     buffer = f.read(counter)
        #     while buffer != '{':
        #         f.write("")
    else:
        with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{old_title}.md", 
                  "w+") as f:
            f.write(text)
            os.rename(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{old_title}.md", 
                      f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/entries/{new_title}.md")
        # change html
        html_text = markdown2.markdown(text)
        os.rename(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{old_title}.html", 
                  f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia{new_title}.html")
        
        with open(f"/home/tomas/Desktop/CS50_web_programming/project_1/wiki/encyclopedia/templates/encyclopedia/{new_title}.html", "r+") as f:
            buffer = f.read(1)
            block_body = "{% block body %}"
            end_block = "{% endblock %}"
            input_name ='<input name="title" type="hidden" value='
            while buffer is not None:
                if buffer == "{":
                    key_word = "{" + f.read(15)
                    if key_word == block_body:
                        f.write(html_text)
                        buffer = f.read(1)
                        while buffer == "{":
                            f.write("")
                            buffer = f.read(1)
                if buffer == "<":
                    input_key_string = "<" + f.read(39)
                    if input_key_string == input_name:
                        f.write(new_title)
                        if len(new_title) > len(old_title):
                            f.write('">')
                        elif len(new_title) < len(old_title):
                            while buffer != '"':
                                f.write("")
                                buffer = f.read(1)
                buffer = f.read(1)
    return entry(request, new_title)  """
    
    
def random_page(request):
    list = util.list_entries()
    number = random.randrange(0, len(list))
    return entry(request, list[number])
        
 