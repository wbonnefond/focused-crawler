import urllib2
import nltk
import ner
import subprocess
import scorer
import operator
import string
import pycountry
import geonamescache
import re
from time import strptime
from TFIDF import TFIDF
from bs4 import BeautifulSoup
from zss import simple_distance, Node
from Filter import *

class Event:
        def __init__(self):
                self.event_type=''                
                self.country=''
                self.state=''
                self.city=''
                self.name=''
                self.day=''
                self.month=''
                self.year=''
                
                self.base_event_type=''                
                self.base_country=''
                self.base_state=''
                self.base_city=''
                self.base_name=''
                self.base_day=''
                self.base_month=''
                self.base_year=''         

        def reload_data(self):
                self.event_type=''                
                self.country=''
                self.state=''
                self.city=''
                self.name=''
                self.day=''
                self.month=''
                self.year=''       
        
        def loadfromfilename(self, input_file):
                values = open(input_file, "r").read().splitlines()
                self.base_event_type = values[0]
                self.base_country = values[1]
                self.base_state = values[2]
                self.base_city = values[3]
                self.base_name = values[4]
                self.base_day = values[5]
                self.base_month = values[6]
                self.base_year = values[7]

        def to_string(self):
                print self.event_type.title()
                print '\t' + 'Location'
                print '\t\t' + self.country.title()
                print '\t\t' + self.state.title()
                print '\t\t' + self.city.title()
                print '\t' + 'Name'
                print '\t\t' + self.name.title()
                print '\t' + 'Date'
                print '\t\t' + str(self.day)
                print '\t\t' + str(self.month)
                print '\t\t' + str(self.year)

        def calculate_score(self, page_text):
                self.reload_data()
                #print page_text           
                the_event = build_event(page_text)
                
                A = build_tree(the_event)
                B = self.build_base_tree()
                simp_dist = simple_distance(A, B)
                if simp_dist == 0:
                        return 1
                if 1.0/(1.1423*simp_dist) > 0.5:
                        the_event.to_string()
                        print 1.0/(1.1423*simp_dist)
                return 1.0/(1.1423*simp_dist)

        def calculate_smart_score(self, page_text):
                self.reload_data()
                #print page_text           
                the_event = build_event(page_text)
                print "your mom " + the_event.base_day
                the_event.to_string()
                A = build_tree_no_date(the_event)
                B = self.build_base_tree_no_date()
                simp_dist = simple_distance(A, B)
                print "simp_dist before inversing: "+str(simp_dist)
                if simp_dist != 0:
                        simp_dist = 1.0/(1.25*simp_dist)
                else:
                        simp_dist = 1
                     
                # set null date values to zero           
                tempday = the_event.day
                if(tempday == ''):
                        tempday = 0
                tempmonth = the_event.month
                if(tempmonth == ''):
                        tempmonth = 0
                tempyear = the_event.year
                if(tempyear == ''):
                        tempyear = 0

                # do same for basedate
                tempbaseday = the_event.base_day
                if(tempbaseday == ''):
                        tempbaseday = 0
                tempbasemonth = the_event.base_month
                if(tempbasemonth == ''):
                        tempbasemonth = 0
                tempbaseyear = the_event.base_year
                if(tempbaseyear == ''):
                        tempbaseyear = 0

                daysdelta = abs(int(tempbaseday)-int(tempday))+(30*(abs(int(tempmonth)-int(tempbasemonth))))+(365*(abs(int(tempyear)-int(tempbaseyear))))
                date_contrib = pow(daysdelta,.2)
                if date_contrib != 0:
                        date_contrib = 1.0 / date_contrib
                else:
                        date_contrib = 1

                print "Found Date: " + str(tempday) +"/"+str(tempmonth)+"/"+str(tempyear)
                print "Found Date Obj: " + the_event.day +"/"+the_event.month+"/"+the_event.year
                print "Base Date: " + str(tempbaseday) +"/"+str(tempbasemonth)+"/"+str(tempbaseyear)
                print "date_contrib: " + str(date_contrib)
                print "simp_dist: " + str(simp_dist)
                return (.2*date_contrib) * (.8*simp_dist)
                
        def build_base_tree(self):
                A = (
                    Node(self.base_event_type.lower())
                        .addkid(Node("Location")
                            .addkid(Node(self.base_country.lower()))
                            .addkid(Node(self.base_state.lower()))
                            .addkid(Node(self.base_city.lower())))
                        .addkid(Node("Name")
                                .addkid(Node(self.base_name.lower())))
                        .addkid(Node("Date")
                                .addkid(Node(self.base_day.lower()))
                                .addkid(Node(self.base_month.lower()))
                                .addkid(Node(self.base_year.lower())))
                    )
                return A

        def build_base_tree_no_date(self):
                A = (
                    Node(self.base_event_type.lower())
                        .addkid(Node("Location")
                            .addkid(Node(self.base_country.lower()))
                            .addkid(Node(self.base_state.lower()))
                            .addkid(Node(self.base_city.lower())))
                        .addkid(Node("Name")
                                .addkid(Node(self.base_name.lower())))
                    )
                return A

def build_event(page_text):
        event = Event()
        set_event_date(page_text, event)
        ent = get_entities(page_text)
        eventType = set_event_type(page_text, event)
        eventName = set_event_name(page_text, eventType, event)
        set_event_location(ent, event)
        return event

def build_tree(event):
        A = (
            Node(event.event_type.lower())
                .addkid(Node("Location")
                    .addkid(Node(event.country.lower()))
                    .addkid(Node(event.state.lower()))
                    .addkid(Node(event.city.lower())))
                .addkid(Node("Name")
                        .addkid(Node(event.name.lower())))
                .addkid(Node("Date")
                        .addkid(Node(event.day.lower()))
                        .addkid(Node(event.month.lower()))
                        .addkid(Node(event.year.lower())))
            )
        return A

def build_tree_no_date(event):
        A = (
            Node(event.event_type.lower())
                .addkid(Node("Location")
                    .addkid(Node(event.country.lower()))
                    .addkid(Node(event.state.lower()))
                    .addkid(Node(event.city.lower())))
                .addkid(Node("Name")
                        .addkid(Node(event.name.lower())))
            )
        return A
                

# Takes a URL and returns the raw HTML document
def get_html_page(url):
        html = urllib2.urlopen(url).read()    
        return html

def set_event_date(pageText, event):
        days_list = []
        months_list =[]
        years_list = []
        year_regex = re.compile("[0-9]{4}")
        day_regex = re.compile("[0-9]$|([0-9][0-9]$)")
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_detector.tokenize(pageText.strip())
        week_text_file = open("days.txt", "r")
        days_of_week_list = week_text_file.read().splitlines()
        full_months_text = open("full-month.txt", "r")
        abbrev_months_text = open("abbrev-month.txt", "r")
        full_months = full_months_text.read().splitlines()
        abbrev_months = abbrev_months_text.read().splitlines()
        
        week_text_file.close()
        full_months_text.close()
        abbrev_months_text.close()
        
        for sentence in sentences:
                ent = get_entities(sentence)
                date = get_entity('DATE', ent)
                
                if date != []:
                        #print date
                        for x in date:
                                if x not in days_of_week_list:
                                        new_text = strip_punctuation(x)
                                        split_text = new_text.split(' ')
                                        for word in split_text:
                                                if word in full_months:
                                                        for i in range(len(split_text)):
                                                                months_list.append(strptime(word,'%B').tm_mon) 
                                                elif word in abbrev_months:
                                                        for i in range(len(split_text)):
                                                                months_list.append(strptime(word,'%b').tm_mon)
                                                elif year_regex.match(word):
                                                        for i in range(len(split_text)):
                                                                years_list.append(int(word))
                                                elif day_regex.match(word):
                                                        for i in range(len(split_text)):
                                                                days_list.append(int(word))
                                        
        sorted_days = get_frequency(days_list)
        sorted_months = get_frequency(months_list)
        sorted_years = get_frequency(years_list)
        
        if len(sorted_days) == 1:
                event.day = str((sorted_days[0])[0])
        elif len(sorted_days) > 1:
                if (sorted_days[0])[1] > 1:
                        event.day = str((sorted_days[0])[0])

        if len(sorted_months) == 1:
                event.month = str((sorted_months[0])[0])
        elif len(sorted_months) > 1:
                if (sorted_months[0])[1] > 1:
                        event.month = str((sorted_months[0])[0])

        if len(sorted_years) == 1:
                event.year = str((sorted_years[0])[0])
        elif len(sorted_years) > 1:
                if (sorted_years[0])[1] > 1:
                        event.year = str((sorted_years[0])[0])
        
        if event.month == '' and event.year == '':
                event.day = ''
        
        
        
                                                        
# Takes an HTMl document and returns all text located in paragraphs
def get_text_from_html(html):
        soup = BeautifulSoup(html)
        paras = soup.findAll('p')
        text = ""
        for para in paras:
                text = text + " " + para.text
        return text

# Uses pyNER to extract Names/Dates/Location etc
def get_entities(pageText):
        tagger = ner.SocketNER(host='localhost', port=8080)
        entities = tagger.get_entities(pageText)
        return entities

# Given entity list and category type, return the list associated with that category
def get_entity(categor, entities):
        for k,v in entities.iteritems():
                if k == categor:
                        return v
        return []

# Returns count number of keywords from web page text
def get_keywords(pageText, count):
        mytfidf = TFIDF()
        tokenPageText = getTokenizedDocs([pageText])
        token_bow = [mytfidf.doc2bow(doc) for doc in tokenPageText]
        mytfidf.buildVocabIndex(token_bow)
        selected = mytfidf.selectImportantWords_tf(count)
        wordsList = mytfidf.index.keys()
        selected_words = [wordsList[k[1]] for k in selected]
        return selected_words

# Given a list return a sorted list of tuples based on frequency
def get_frequency(li):
        keyword_dict = {}
        for l in li:
                if l in keyword_dict:
                        keyword_dict[l] = keyword_dict[l]+1
                else:
                        keyword_dict[l] = 1
        sorted_dict = sorted(keyword_dict.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_dict

# Takes in an HTML document and pulls the type of disaster from the header tags
def set_event_type(text, event):
        text_file = open("disaster-list.txt", "r")
        disaster_list = text_file.read().splitlines()
        text_file.close()
        text = strip_punctuation(text)
        for word in text.split():
                if word.lower() in disaster_list:
                        event.event_type = word.lower()
                        return event.event_type
        
                
        
                

# Takes in an HTML document and disaster type and pulls the name of the event
def set_event_name(text, eventType, event):
        text = strip_punctuation(text)
        list_of_words = text.lower().split()
        if eventType in list_of_words:
                if eventType == 'hurricane' or eventType == 'typhoon':
                        eventName = list_of_words[list_of_words.index(eventType) + 1]
                        event.name = eventName
                        return event.name


def set_event_location(ent, event):
        locationDict = get_frequency(get_entity('LOCATION', ent))
        #print locationDict
        country = find_event_country(locationDict)
        gc = geonamescache.GeonamesCache()
        # If we find a country, find a city
        if country != '':
                for place,v in locationDict:
                        if place != country:
                                if is_city_in_country(place, country):
                                        event.city = place
                                        break
                event.country = country
        # If find no country, find a city and set the country        
        else:
                for place,v in locationDict:
                        if is_city_valid(place):
                                event.city = place
                                break
        if event.country == 'United States' or event.country == '':
                state = find_event_state(locationDict)
                if state != '':
                        event.state = state
                        event.country = 'United States'
                        
        

# Given a sorted location dictionary by occurence return the country
def find_event_country(locationDict):
        text_file = open("countries.txt", "r")
        country_list = text_file.read().splitlines()
        text_file.close()
        for place,v in locationDict:
                if place in country_list:
                        return place
        return ''

# Given a sorted location dictionary return the US State
def find_event_state(locationDict):
        text_file = open("us-states.txt", "r")
        state_list = text_file.read().splitlines()
        text_file.close()
        for place,v in locationDict:
                if place in state_list:
                        return place
        return ''

# Checks if the country has a city of that name
def is_city_in_country(city_name, country):
        gc = geonamescache.GeonamesCache()
        cities = gc.get_cities_by_name(city_name)
        for city in cities:
                for k,v in city.iteritems():
                        if country == pycountry.countries.get(alpha2=v.get('countrycode')).name:
                                return True
        return False

# Get country of most populus city possiblity
#
# Change to check if city exists
#
#
def is_city_valid(city_name):
        gc = geonamescache.GeonamesCache()
        return len(gc.get_cities_by_name(city_name)) > 0

# Strips punctuation from text to make keyword analysis easier
def strip_punctuation(text):
        text = text.replace("-", " ")
        text = text.replace("\t", " ")
        exclude = set(string.punctuation)
        text = ''.join(ch for ch in text if ch not in exclude)
        return text

def test():
        html = get_html_page('http://en.wikipedia.org/wiki/Typhoon_Haiyan')
        contents = get_text_from_html(html)
        event = Event()
        event.loadfromfilename('sample-event.txt')
        print event.calculate_smart_score(contents)
        

if __name__ == "__main__":
    #baseFC()
    #main()
    test()
    #getPosFiles()
    #getStats()



