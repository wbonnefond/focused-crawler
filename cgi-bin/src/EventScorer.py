import urllib2
import nltk
import ner
import subprocess
#import scorer
import operator
import string
import pycountry
import geonamescache
import re
import event
from time import strptime
from TFIDF import TFIDF
from bs4 import BeautifulSoup
from zss import simple_distance, Node
from Filter import *

last_run_file = 'last-run-trees.txt'

class EventScorer:

        def __init__(self):
                self.base_event = event.Event()
                self.current_event = event.Event()
                self.base_event.load_from_file('event-details.txt')
                self.threshold = 0
                days_file = open("days.txt", "r")
                self.days_of_week_list = days_file.read().splitlines()
                days_file.close()
                full_months_file = open("full-month.txt", "r")
                self.full_months = full_months_file.read().splitlines()
                full_months_file.close()
                abbrev_months_file = open("abbrev-month.txt", "r")
                self.abbrev_months = abbrev_months_file.read().splitlines()
                abbrev_months_file.close()
                disaster_list_file = open("disaster-list.txt", "r")
                self.disaster_list = disaster_list_file.read().splitlines()
                disaster_list_file.close()
                countries_file = open("countries.txt", "r")
                self.country_list = countries_file.read().splitlines()
                countries_file.close()
                state_list_file = open("us-states.txt", "r")
                self.state_list = state_list_file.read().splitlines()
                state_list_file.close()
                self.sent_detector = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
                # reset last-run-trees.txt
                f = open(last_run_file, 'w')
                f.close()
		
        def set_threshold(self, thresh):
            	self.threshold = thresh
        
        def calculate_score(self, page_text, url):
                self.current_event.clear_data()
                #print page_text
                self.current_event.set_url(url) 
                self.build_event(page_text)
                A = self.build_tree(self.current_event)
                B = self.build_tree(self.base_event)
                simp_dist = simple_distance(A, B)
                if simp_dist == 0:
                        return 1
                self.current_event.to_string()
                #print 1.0/(1.1423*simp_dist)
                score = 1.0/(1.1423*simp_dist)
                if score > self.threshold:
                    f = open(last_run_file, 'a')
                    f.write(self.current_event.formated_string())
                    f.close()
                return score

        def calculate_smart_score(self, page_text, url):
                self.current_event.clear_data()
                #print page_text
                self.current_event.set_url(url)
                self.build_event(page_text)
                #self.current_event.to_string()
                A = self.build_tree_no_date(self.current_event)
                B = self.build_tree_no_date(self.base_event)
		score = 0
		if (self.current_event.event_type == self.base_event.event_type):
			score += .40
		if (self.current_event.name == self.base_event.name):
			score += .10
		if (self.current_event.country == self.base_event.country):
			score += .15
		if (self.current_event.city == self.base_event.city):
			score += .05
		if (self.current_event.state == self.base_event.state):
			score += .05
                #print "simp_dist before inversing: "+str(simp_dist)
                #if simp_dist != 0:
                #        simp_dist = 1.0/(1.25*simp_dist)
                #else:
                #        simp_dist = 1
		#print score
                # set null date values to zero           
                tempday = self.current_event.day
                if(tempday == ''):
                        tempday = 0
                tempmonth = self.current_event.month
                if(tempmonth == ''):
                        tempmonth = 0
                tempyear = self.current_event.year
                if(tempyear == ''):
                        tempyear = 0
		
                # do same for basedate
                tempbaseday = self.base_event.day
                #if(tempbaseday == ''):
                #        tempbaseday = 0
                tempbasemonth = self.base_event.month
                #if(tempbasemonth == ''):
                #        tempbasemonth = 0
                tempbaseyear = self.base_event.year
                #if(tempbaseyear == ''):
                #        tempbaseyear = 0

                daysdelta = abs(int(tempbaseday)-int(tempday))+(30*(abs(int(tempmonth)-int(tempbasemonth))))+(365*(abs(int(tempyear)-int(tempbaseyear))))               
    	        date_contrib = pow(daysdelta,.2)               
    	        if date_contrib != 0:
                        date_contrib = 1.0 / date_contrib
                else:
                        date_contrib = 1
                # catch case where no date was extracted from article
                if tempday == 0 and tempmonth == 0 and tempyear == 0:
                        date_contrib = 0
                #print "Found Date: " + str(tempday) +"/"+str(tempmonth)+"/"+str(tempyear)               
                #print "Base Date: " + str(tempbaseday) +"/"+str(tempbasemonth)+"/"+str(tempbaseyear)
                #print "date_contrib: " + str(date_contrib)
                #print "simp_dist: " + str(simp_dist)
                #print (.2*date_contrib) + (.8*simp_dist)
                new_score = (.25*date_contrib) + score
                if new_score > self.threshold:
                    f = open(last_run_file, 'a')
                    f.write(self.current_event.formated_string())
                    f.close()
                return new_score

        def build_event(self, page_text):
                self.set_event_date(page_text, self.current_event)
                ent = self.get_entities(page_text)
                eventType = self.set_event_type(page_text, self.current_event)
                eventName = self.set_event_name(page_text, eventType, self.current_event)
                self.set_event_location(ent, self.current_event)

        def build_tree(self, event):
                A = (
                    Node(event.event_type.lower())
                        .addkid(Node(event.country.lower()))
                        .addkid(Node(event.state.lower()))
                        .addkid(Node(event.city.lower()))
                        .addkid(Node(event.name.lower()))
                        .addkid(Node(event.day.lower()))
                        .addkid(Node(event.month.lower()))
                        .addkid(Node(event.year.lower()))
                    )
                return A

        def build_tree_no_date(self, event):
                A = (
                    Node(event.event_type.lower())
                        .addkid(Node(event.country.lower()))
                        .addkid(Node(event.state.lower()))
                        .addkid(Node(event.city.lower()))
                        .addkid(Node(event.name.lower()))
                    )
                return A
                        

        # Takes a URL and returns the raw HTML document
        def get_html_page(self, url):
                html = urllib2.urlopen(url).read()    
                return html

        def set_event_date(self, pageText, event):
                days_list = []
                months_list =[]
                years_list = []
                year_regex = re.compile("[0-9]{4}$")
                day_regex = re.compile("[0-9]$|([0-9][0-9]$)")
                sentences = self.sent_detector.tokenize(pageText.strip())
                                
                for sentence in sentences:
                        ent = self.get_entities(sentence)
                        date = self.get_entity('DATE', ent)
                        
                        if date != []:
                                #print date
                                for x in date:
                                        if x not in self.days_of_week_list:
                                                new_text = self.strip_punctuation(x)
                                                split_text = new_text.split(' ')
                                                for word in split_text:
                                                        if word in self.full_months:
                                                                for i in range(len(split_text)):
                                                                        months_list.append(strptime(word,'%B').tm_mon) 
                                                        elif word in self.abbrev_months:
                                                                for i in range(len(split_text)):
                                                                        months_list.append(strptime(word,'%b').tm_mon)
                                                        elif year_regex.match(word):
                                                                for i in range(len(split_text)):
                                                                        years_list.append(int(word))
                                                        elif day_regex.match(word):
                                                                for i in range(len(split_text)):
                                                                        days_list.append(int(word))
                                                
                sorted_days = self.get_frequency(days_list)
                sorted_months = self.get_frequency(months_list)
                sorted_years = self.get_frequency(years_list)
                
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
        def get_text_from_html(self, html):
                soup = BeautifulSoup(html)
                paras = soup.findAll('p')
                text = ""
                for para in paras:
                        text = text + " " + para.text
                return text

        # Uses pyNER to extract Names/Dates/Location etc
        def get_entities(self, pageText):
                tagger = ner.SocketNER(host='localhost', port=8080)
                entities = tagger.get_entities(pageText)
                return entities

        # Given entity list and category type, return the list associated with that category
        def get_entity(self, categor, entities):
                for k,v in entities.iteritems():
                        if k == categor:
                                return v
                return []

        # Returns count number of keywords from web page text
        def get_keywords(self, pageText, count):
                mytfidf = TFIDF()
                tokenPageText = getTokenizedDocs([pageText])
                token_bow = [mytfidf.doc2bow(doc) for doc in tokenPageText]
                mytfidf.buildVocabIndex(token_bow)
                selected = mytfidf.selectImportantWords_tf(count)
                wordsList = mytfidf.index.keys()
                selected_words = [wordsList[k[1]] for k in selected]
                return selected_words

        # Given a list return a sorted list of tuples based on frequency
        def get_frequency(self, li):
                keyword_dict = {}
                for l in li:
                        if l in keyword_dict:
                                keyword_dict[l] = keyword_dict[l]+1
                        else:
                                keyword_dict[l] = 1
                sorted_dict = sorted(keyword_dict.items(), key=operator.itemgetter(1), reverse=True)
                return sorted_dict

        # Takes in an HTML document and pulls the type of disaster from the header tags
        def set_event_type(self, text, event):
                text = self.strip_punctuation(text)
                for word in text.split():
                        if word.lower() in self.disaster_list:
                                event.event_type = word.lower()
                                return event.event_type
                                               

        # Takes in an HTML document and disaster type and pulls the name of the event
        def set_event_name(self, text, eventType, event):
                text = self.strip_punctuation(text)
                list_of_words = text.lower().split()
                if eventType in list_of_words:
                        if eventType == 'hurricane' or eventType == 'typhoon':
                                eventName = list_of_words[list_of_words.index(eventType) + 1]
                                event.name = eventName
                                return event.name


        def set_event_location(self, ent, event):
                locationDict = self.get_frequency(self.get_entity('LOCATION', ent))
                #print locationDict
                country = self.find_event_country(locationDict)
                gc = geonamescache.GeonamesCache()
                # If we find a country, find a city
                if country != '':
                        for place,v in locationDict:
                                if place != country:
                                        if self.is_city_in_country(place, country):
                                                event.city = place
                                                break
                        event.country = country
                # If find no country, find a city and set the country        
                else:
                        for place,v in locationDict:
                                if self.is_city_valid(place):
                                        event.city = place
                                        break
                if event.country == 'United States' or event.country == '':
                        state = self.find_event_state(locationDict)
                        if state != '':
                                event.state = state
                                event.country = 'United States'
                                
                

        # Given a sorted location dictionary by occurence return the country
        def find_event_country(self, locationDict):
                for place,v in locationDict:
                        if place in self.country_list:
                                return place
                return ''

        # Given a sorted location dictionary return the US State
        def find_event_state(self, locationDict):
                for place,v in locationDict:
                        if place in self.state_list:
                                return place
                return ''

        # Checks if the country has a city of that name
        def is_city_in_country(self, city_name, country):
                gc = geonamescache.GeonamesCache()
                cities = gc.get_cities_by_name(city_name)
                for city in cities:
                        for k,v in city.iteritems():
                                if country == pycountry.countries.get(alpha2=v.get('countrycode')).name:
                                        return True
                return False

        # Check if given name is potentially a valid city name
        def is_city_valid(self, city_name):
                gc = geonamescache.GeonamesCache()
                return len(gc.get_cities_by_name(city_name)) > 0

        # Strips punctuation from text to make keyword analysis easier
        def strip_punctuation(self, text):
                text = text.replace("-", " ")
                text = text.replace("\t", " ")
                exclude = set(string.punctuation)
                text = ''.join(ch for ch in text if ch not in exclude)
                return text

