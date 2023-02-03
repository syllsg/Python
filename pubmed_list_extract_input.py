

#importing packages and librarys 
import requests
from bs4 import BeautifulSoup
import csv

#defining global variable
page_adress = "strain"

#defining functions

#function getting Last name and initials from user and saving the adress to access pubmed
def get_name_user(): 
    user_name = input("Type your last name: ")
    print(user_name)
    user_initial = input("Type your initials: ")
    print(user_initial)
    global page_adress
    page_adress = "https://pubmed.ncbi.nlm.nih.gov/?term="+user_name+" " + user_initial+"&page="

# function getting the different pages of pubmed website from input
def get_url(page_num):
    page_num = str(page_num)
    print(page_adress + page_num )
    return page_adress + page_num

# function extracting and returning text 
def scrape_text(element):
    list = []
    for el in element:
        list.append(el.get_text())
        #print(el.get_text())
    return list

#function creating a csv file with a header to save title, authors list and journal informations for each article
def create_csv(file_name):
    header = ["Title", "Authors list", "Journal"]
    with open(file_name, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(header)
        
#append lines to the csv file       
def append_csv(file_name, title, author, citation):        
    with open(file_name, "a", encoding="utf-8") as csv_file:
        writer_object = csv.writer(csv_file, delimiter = ",")
        for Title, Author, Journal in zip(title, author, citation):
            line = [Title, Author, Journal]
            writer_object.writerow(line)

def scrape_page(page_num):
    #creating request and soup objects
    reponse = requests.get(get_url(page_num))
    page = reponse.content
    soup = BeautifulSoup(page, 'html.parser')

    #search specific items and save their content in lists
    titles = soup.find_all("a", class_="docsum-title")
    authors_list = soup.find_all("span", class_="docsum-authors full-authors")
    journal_citation_short = soup.find_all("span", class_="docsum-journal-citation short-journal-citation")

    #extract text
    titles = scrape_text(titles)
    authors_list = scrape_text(authors_list)
    journal_citation_short = scrape_text(journal_citation_short)
  
    append_csv("articles_list.csv", titles, authors_list, journal_citation_short)

# loop to scrape the first two pages
print(page_adress)
create_csv("articles_list.csv")
get_name_user()
for n in range(1,4) :
    scrape_page(n)

print("Success!")
    

