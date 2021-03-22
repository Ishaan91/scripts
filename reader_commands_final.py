# coding: utf-8
# import libraries

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
from BeautifulSoup import BeautifulSoup as bs
import os
import validators
from readcommands import read_commands

user = os.getlogin()
if not os.path.exists("/users/"+user+"/Desktop/Book"):
    os.makedirs("/users/"+user+"/Desktop/Book")

mydict = {}

# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________

# read_commands method is used to read the commands, chapter by chapter from the configuration guide
# it takes the book url and the tablename as arguments

def read_commands(url, tablename):

    # specify the url
    bookurl = url

    # query the website and return the html to the variable ‘page’
    page = urllib2.urlopen(bookurl)

    # parse the html using beautiful soap and store in variable `soup`
    html_source = page.read()

    parsed_html = bs(html_source)

    reportfile = open('/users/'+user+'/Desktop/Book/'+tablename+'.txt', "w+")

    command_list = []
    page_title = (parsed_html.find('title')).text

    print "\n\n\tParsing chapter: ", page_title

    # for command in parsed_html.findAll('kbd', attrs={'class': 'var'}):
    #     command_list.append(command.text)

    synph_list = parsed_html.findAll('span', attrs={'class': 'synph'})
    for synphs in synph_list:
        command_string = ""
        kwd_list = synphs.findAll('span', attrs={'class': 'kwd'})
        for kwds in kwd_list:
            # print kwds.text.strip()
            command_string = command_string + " " + (kwds.text.strip())
        #print command_string
        command_list.append(command_string)

    # for command in parsed_html.findAll('span', attrs={'class': 'kwd'}):
    #     command_list.append(command.text)

    # for command in parsed_html.findAll('kbd', attrs={'class': 'userinput'}):
    #     command_list.append(command.text)

    print "\n\t", command_list.__len__(), "commands found \n\t"
    print "\t", set(command_list).__len__(), "unique commands\n\n"

    mydict = {tablename: set(command_list)}

    for key in mydict:
         print "\n\t", key, "\n"
         for element in mydict[key]:
            # print "\t\t", element
            reportfile.write("\n%s" % element)

# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________

def parser(page_address):


    page = urllib2.urlopen(page_address)

    # parse the html using beautiful soap and store in variable 'soup'
    html_source = page.read()
    parsed_html = bs(html_source)

    page_list = []

    for item in parsed_html.findAll('ul', attrs={'id': 'bookToc'}):
        for link in item.findAll('a', href=True):
            page_list.append(link.get('href'))

    print "\nFound", page_list.__len__(), "chapters in the book\n"

    for i in range(page_list.__len__()):
        page_list[i] = 'http://www.cisco.com' + page_list[i]
        print page_list[i]
        tablename = "chapter%d" % (i+1)

        #   read_commands method is used to parse the configuration guide,
        #   extract commands from it and stores them in a dictionary mapped to their respective
        #   chapters as keys
        #   It takes chapter name and the tablename as arguments
        #    read_commands(page_list[i], tablename)

        read_commands(page_list[i], tablename)

# ask the user for a URL
page_address = raw_input("\n\tEnter the URL of the book: ")

# validate the entered URL and call method parser() if valid
if validators.url(page_address):
    print "\n\tURL is valid. Working on it now..."
    parser(page_address)
else:
    print "\n\tPlease enter a valid URL."
