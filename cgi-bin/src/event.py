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
                self.url=''    
        
        def load_from_file(self, input_file):
                values = open(input_file, "r").read().splitlines()
                self.event_type = values[0]
                self.country = values[1]
                self.state = values[2]
                self.city = values[3]
                self.name = values[4]
                self.day = values[5]
                self.month = values[6]
                self.year = values[7]

        def formated_string(self):
                return ''+self.url+'|'+ self.event_type+'|'+ self.country+'|'+self.state+'|'+ self.city+'|'+self.name+'|'+str(self.day)+'|'+str(self.month)+'|'+str(self.year)+'\n'

        def set_url(self, urlToSet):
            self.url = urlToSet 

        def to_string(self):
                print self.event_type
                print '\t' + 'Location'
                print '\t\t' + self.country
                print '\t\t' + self.state
                print '\t\t' + self.city
                print '\t' + 'Name'
                print '\t\t' + self.name
                print '\t' + 'Date'
                print '\t\t' + str(self.day)
                print '\t\t' + str(self.month)
                print '\t\t' + str(self.year)

        def clear_data(self):
                self.event_type=''                
                self.country=''
                self.state=''
                self.city=''
                self.name=''
                self.day=''
                self.month=''
                self.year=''
                self.url=''
