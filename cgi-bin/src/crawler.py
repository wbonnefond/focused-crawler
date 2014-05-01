
from webpage import Webpage
import urllib2
from bs4 import BeautifulSoup
import socket
import os

class Crawler:
    def __init__(self,priorityQueue,scorer,options):
        self.visited = []        
        #self.relevantPages=[]
        #self.relevantPagesCount = len(priorityQueue.queue)
        self.relevantPagesCount = 0
        self.totalPagesCount = len(priorityQueue.queue)
        self.pagesCount = 0
        self.priorityQueue = priorityQueue
        self.scorer = scorer
        self.url_scorer = None
        self.pageScoreThreshold = options['pageScoreThreshold']
        self.urlScoreThreshold = options['urlScoreThreshold']
        self.pagesLimit = options['num_pages']


    def set_url_scorer(self, url_scorer):
        self.url_scorer = url_scorer
    
    def crawl(self):
        #start crawling
        #myopener = MyOpener()
        self.harvestRatioData = []
        self.relevantPages = []
        while self.pagesCount <  self.pagesLimit and not self.priorityQueue.isempty():
            work_url = self.priorityQueue.pop()
            self.visited.append(work_url[1])
            #print ("%s, %s") % (-1 * work_url[0], work_url[1])
            #page = urllib2.urlopen(work_url)
            '''page = myopener.open(work_url)
            self.pagesCount += 1
            soup = BeautifulSoup(page)
            links = soup.find_all('a')'''
            page = Webpage(work_url,self.pagesCount)
            if len(page.text) > 0:
                page_score = self.scorer.calculate_score(page.text)
            else:
                page_score = 0
            
            self.pagesCount += 1
            if (page_score > self.pageScoreThreshold):
                page.getUrls()
                self.relevantPagesCount += 1
                self.relevantPages.append(page)
                self.harvestRatioData.append((self.relevantPagesCount,self.pagesCount))
                print ("%s|"+ str(page_score)+"|%s") % (-1.0 * work_url[0], work_url[1])
                for link in page.outgoingUrls:
                    url = link.address
                    if url != None and url != '':
                        if url.find('?')!= -1:
                            url = url.split('?')[0]
                        if url.find('#') != -1:
                            url = url.split('#')[0]
                        
#                         if url.startswith('http') == False:
#                             parts = page.pageUrl[1].split("://")
#                             baseUrl = parts[1].split("/")[0]
#                             baseUrl = parts[0] +"://" + baseUrl
#                             url = baseUrl + url
                        
                        #if not self.existsInVisited(url,self.visited): 
                        if url not in self.visited:
                            #if url.startswith('http:') and url.find('#') == -1 and not self.exists(url,self.priorityQueue.queue):                            
                            if url.startswith('http') and not self.exists(url,self.priorityQueue.queue):
                                url_score = self.scorer.calculate_score(link.getAllText())
                                self.totalPagesCount +=1
                                #tot_score = (page_score + url_score)/2.0
                                #tot_score = page_score + url_score
                                tot_score = url_score
                                if tot_score > self.urlScoreThreshold:
                                    #self.priorityQueue.push(((-1 * url_score),url))
                                    self.priorityQueue.push(((-1 * tot_score),url,page.pageId))
                                    #self.relevantPagesCount += 1
            #if self.pagesCount%10 == 0:
            #    print 'Visited: ' + str(self.pagesCount)
            #    print 'Accepted: ' + str(len(self.relevantPages))  
    #def existsInVisited(self,url,alist):
        #urlList = [v for p,v,k in alist]
        #return url in urlList
        #return url in alist

    def enhanced_crawl(self):
            socket.setdefaulttimeout(10)
            #start crawling
            #myopener = MyOpener()
            self.harvestRatioData = []
            self.relevantPages = []
            while self.pagesCount <  self.pagesLimit and not self.priorityQueue.isempty():
                work_url = self.priorityQueue.pop()
                self.visited.append(work_url[1])
                               
                #print ("%s, %s") % (-1 * work_url[0], work_url[1])
                #page = urllib2.urlopen(work_url)
                '''page = myopener.open(work_url)
                self.pagesCount += 1
                soup = BeautifulSoup(page)
                links = soup.find_all('a')'''
                #print work_url[1]
                try:
                    req = urllib2.Request(work_url[1])
                    # create a request object

                    handle = urllib2.urlopen(req)
                    # and open it to return a handle on the url
                except urllib2.URLError:
                    pass
                    #print "Oops, timed out?"
                except socket.timeout:
                    pass
                    #print "Timed out!"
                except:
                    pass
                    #print "other error"

                else:
                    
                    html = handle.read()
                    soup = BeautifulSoup(html)
                    paras = soup.findAll('p')
                    #print paras
                    text = ""
                    for para in paras:
                            text = text + " " + para.text
                    try:                
                        page = Webpage(work_url,self.pagesCount)
                    except:
                        #print 'second catch'
                        pass
                    else:
                        if len(page.text) > 0:
                            page_score = self.scorer.calculate_smart_score(text, work_url[1])
                        else:
                            page_score = 0
                            
                        self.pagesCount += 1
                        if (page_score > self.pageScoreThreshold):
                            page.getUrls()
                            self.relevantPagesCount += 1
                            self.relevantPages.append(page)
                            
                            self.harvestRatioData.append((self.relevantPagesCount,self.pagesCount))
                            print ("%s|"+ str(page_score)+"|%s") % (-1.0 * work_url[0], work_url[1])
                            for link in page.outgoingUrls:
                                url = link.address
                                if url != None and url != '':
                                    if url.find('?')!= -1:
                                        url = url.split('?')[0]
                                    if url.find('#') != -1:
                                        url = url.split('#')[0]
                                        
                #                         if url.startswith('http') == False:
                #                             parts = page.pageUrl[1].split("://")
                #                             baseUrl = parts[1].split("/")[0]
                #                             baseUrl = parts[0] +"://" + baseUrl
                #                             url = baseUrl + url
                                        
                                        #if not self.existsInVisited(url,self.visited): 
                                    if url not in self.visited:
                                            #if url.startswith('http:') and url.find('#') == -1 and not self.exists(url,self.priorityQueue.queue):                            
                                        if url.startswith('http') and not self.exists(url,self.priorityQueue.queue):
                                            url_score = self.url_scorer.calculate_score(link.getAllText())
                                            self.totalPagesCount +=1
                                            #tot_score = (page_score + url_score)/2.0
                                            #tot_score = page_score + url_score
                                            tot_score = url_score
                                            if tot_score > self.urlScoreThreshold:
                                                #self.priorityQueue.push(((-1 * url_score),url))
                                                self.priorityQueue.push(((-1 * tot_score),url,page.pageId))
                                                #self.relevantPagesCount += 1
                        #if self.pagesCount%10 == 0:
                        #        print 'Visited: ' + str(self.pagesCount)
                        #        print 'Accepted: ' + str(len(self.relevantPages))         
                #def existsInVisited(self,url,alist):
                    #urlList = [v for p,v,k in alist]
                    #return url in urlList
                    #return url in alist



    def exists(self,url,alist):
        urlList = [v for p,v,k in alist]
        return url in urlList
