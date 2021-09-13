from bcr_api.bwproject import BWProject, BWUser
from bcr_api.bwresources import BWQueries, BWGroups, BWAuthorLists, BWSiteLists, BWLocationLists, BWTags, BWCategories, BWRules, BWMentions, BWSignals
from datetime import datetime
from pytz import timezone
from time import sleep
import pandas as pd
import logging
logger = logging.getLogger("bcr_api")
logger.setLevel(logging.ERROR)

class Brandwatch:
    
    version = "1.0"
    
    # Set default parameter
    def __init__(self, token = None, token_path = 'tokens.txt', username = None, password = None, terminate = False, logger = None):
        self.__token = token
        self.__token_path = token_path
        self.__username = username
        self.__password = password
        self.__user = None
        self.__projects = None
        self.__project = None
        self.__groups = None
        self.__queries = None
        self.__groups_queries = None
        self.__mentions = None
        self.__delay = 30
        self.__terminate = terminate
        self.__logger = logger
        
    # Allow pandas dataframe display all rows and columns, default to 60 rows and 20 columns
    def set_display_all(self, flag = True):
        if flag is True:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
        else:
            pd.set_option('display.max_rows', 60)
            pd.set_option('display.max_columns', 20)

    # Set delay time to retry if rate limit reach, default to 30 seconds
    def set_delay(self, delay = 30):
        self.__delay = delay
        
    # Set terminate signal when using GUI to interrupt
    def terminate(self, flag):
        self.__terminate = flag

    # Set logger to update log info to GUI
    def setLogger(self, logger):
        self.__logger = logger

    # Get user object with username/password or token
    def getUser(self):
        self.__user = None
        if self.__terminate:
            return self.__user
        try:
            self.__user = BWUser(username = self.__username, password = self.__password, token = self.__token, token_path = self.__token_path)
            self.__token = self.__user.token
        except Exception as e:
            if 'Invalid access token' in str(e):
                logging.info('Token is invalid or expired')
                if self.__logger is not None:
                    self.__logger.emit('Token is invalid or expired')
                self.__user = None
            elif 'rate limit exceeded' in str(e):
                logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                if self.__logger is not None:
                    self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s...')
                self.__user = None
                sleep(self.__delay)
                self.getUser()
            else:
                logging.info('Error: '+ str(e))
                if self.__logger is not None:
                    self.__logger.emit('Error: '+str(e))
        return self.__user
    
    # Get BWProject object list, need to extract 'name' attr
    def getProjects(self):
        self.__projects = None
        if self.__terminate:
            return self.__projects
        if self.__user is None or self.__user.token != self.__token:
            self.getUser()
        if self.__user is not None:
            try:
                projects = self.__user.get_projects()
                if 'rate limit exceeded' in str(projects) or 'Invalid access token' in str(projects):
                    raise Exception(projects)
                else:
                    self.__projects = projects
            except Exception as e:
                if 'Invalid access token' in str(e):
                    logging.info('Token is invalid or expired')
                    if self.__logger is not None:
                        self.__logger.emit('Token is invalid or expired')
                    self.__user = None
                elif 'rate limit exceeded' in str(e):
                    logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                    if self.__logger is not None:
                        self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s...')
                    self.__projects = None
                    sleep(self.__delay)
                    self.getProjects()
                else:
                    logging.info('Error: '+ str(e))
                    if self.__logger is not None:
                        self.__logger.emit('Error: '+str(e))
        return self.__projects
        
    # Get BWProject object
    def getProject(self, project):
        self.__project = None
        if self.__terminate:
            return self.__project
        try:
            self.__project = BWProject(project=project, username = self.__username, password = self.__password, token = self.__token, token_path = self.__token_path)
        except Exception as e:
            if 'Invalid access token' in str(e):
                logging.info('Token is invalid or expired')
                if self.__logger is not None:
                    self.__logger.emit('Token is invalid or expired')
                self.__user = None
            elif 'rate limit exceeded' in str(e):
                logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                if self.__logger is not None:
                    self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s...')
                self.__project = None
                sleep(self.__delay)
                self.getProject(project)
            else:
                logging.info('Error: '+ str(e))
                if self.__logger is not None:
                    self.__logger.emit('Error: '+str(e))
        return self.__project

    # Get BWGroup object based on BWProject
    def getGroupInst(self, project):
        self.__groups = None
        if self.__terminate:
            return self.__groups
        try:
            self.__groups = BWGroups(project)
        except Exception as e:
            if 'Invalid access token' in str(e):
                logging.info('Token is invalid or expired')
                if self.__logger is not None:
                    self.__logger.emit('Token is invalid or expired')
                self.__user = None
            elif 'rate limit exceeded' in str(e):
                logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                if self.__logger is not None:
                    self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                self.__groups = None
                sleep(self.__delay)
                self.getGroupInst(project)
            else:
                logging.info('Error: '+ str(e))
                if self.__logger is not None:
                    self.__logger.emit('Error: '+str(e))
        return self.__groups
        
    # Get BWGroup object list, need to extract 'name' attr
    def getGroups(self, project):
        self.__groups = None
        if self.__terminate:
            return self.__groups
        if self.__project is None or self.__project.project_name != project:
            self.getProject(project)
        if self.__project is not None:
            self.getGroupInst(self.__project)
        return self.__groups
        
    # Get BWQuery object
    def getQueryInst(self, project):
        self.__queries = None
        if self.__terminate:
            return self.__queries
        try:
            self.__queries = BWQueries(project)
        except Exception as e:
            if 'Invalid access token' in str(e):
                logging.info('Token is invalid or expired')
                if self.__logger is not None:
                    self.__logger.emit('Token is invalid or expired')
                self.__user = None
            elif 'rate limit exceeded' in str(e):
                logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                if self.__logger is not None:
                    self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s...')
                self.__queries = None
                sleep(self.__delay)
                self.getQueryInst(project)
            else:
                logging.info('Error: '+ str(e))
                if self.__logger is not None:
                    self.__logger.emit('Error: '+str(e))
        return self.__queries
    
    # Get BWQueries object list, need to extract 'name' attr
    def getQueries(self, project):
        self.__queries = None
        if self.__terminate:
            return self.__queries
        if self.__project is None or self.__project.project_name != project:
            self.getProject(project)
        if self.__project is not None:
            self.getQueryInst(self.__project)
        return self.__queries

    # Get BWQueries object list by group name, need to extract 'name' attr
    def getQueriesByGroup(self, group):
        self.__groups_queries = None
        if self.__terminate:
            return self.__groups_queries
        if self.__groups is not None:
            try:
                groups_queries = self.__groups.get_group_queries(name=group)
                if 'rate limit exceeded' in str(groups_queries) or 'Invalid access token' in str(groups_queries):
                    raise Exception(groups_queries)
                else:
                    self.__groups_queries = groups_queries
            except Exception as e:
                if 'Invalid access token' in str(e):
                    logging.info('Token is invalid or expired')
                    if self.__logger is not None:
                        self.__logger.emit('Token is invalid or expired')
                    self.__user = None
                elif 'rate limit exceeded' in str(e):
                    logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                    if self.__logger is not None:
                        self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s...')
                    self.__groups_queries = None
                    sleep(self.__delay)
                    self.getQueriesByGroup(group)
                else:
                    logging.info('Error: '+ str(e))
                    if self.__logger is not None:
                        self.__logger.emit('Error: '+str(e))
        else:
            logging.info('Please retrieve groups by project first ...')
        return self.__groups_queries
        
    # Get mentions with project name,  query name, start and end time
    def getMentions(self, project, name, start, end):
        self.__mentions = None
        if self.__terminate:
            return self.__mentions
        if self.__queries is None:
            self.getQueries(project)
        if self.__queries is not None:
            try:
                mentions = self.__queries.get_mentions(name = name, startDate = start, endDate = end)
                if 'rate limit exceeded' in str(mentions) or 'Invalid access token' in str(mentions):
                    raise Exception(mentions)
                else:
                    self.__mentions = mentions
            except Exception as e:
                if 'Invalid access token' in str(e):
                    logging.info('Token is invalid or expired')
                    if self.__logger is not None:
                        self.__logger.emit('Token is invalid or expired')
                    self.__user = None
                elif 'rate limit exceeded' in str(e):
                    logging.info('Rate limit exceeded, please wait '+str(self.__delay)+'s ...')
                    if self.__logger is not None:
                        self.__logger.emit('Rate limit exceeded, please wait '+str(self.__delay)+'s...')
                    self.__mentions = None
                    sleep(self.__delay)
                    self.getMentions(project, name, start, end)
                else:
                    logging.info('Error: '+ str(e))
                    if self.__logger is not None:
                        self.__logger.emit('Error: '+str(e))
        return self.__mentions

    # Convert projects raw data from json to dataframe
    def ProjectsDF(self):
        df = pd.DataFrame(self.__projects)
        return df

    # Convert groups raw data from json to dataframe    
    def GroupsDF(self):
        if self.__groups is not None:
            df = pd.DataFrame([[k,v] for k, v in self.__groups.names.items()], columns = ["id", "name"])
        else:
            df = pd.DataFrame(self.__groups)
        return df

    # Convert queries raw data from json to dataframe    
    def QueriesDF(self):
        if self.__queries is not None:
            df = pd.DataFrame([[k, v] for k, v in self.__queries.names.items()], columns = ["id", "name"])
        else:
            df = pd.DataFrame(self.__queries)
        return df
   
    # Convert queries raw data from json to dataframe
    def GroupQueriesDF(self):
        if self.__groups_queries is not None:
            df = pd.DataFrame([[v, k] for k, v in self.__groups_queries.items()], columns = ["id", "name"])
        else:
            df = pd.DataFrame(self.__groups_queries)
        return df

    # Convert mentions raw data from json to dataframe  
    def MentionsDF(self):
        df = pd.DataFrame(self.__mentions)
        return df
    
    # Print groups 
    def displayGroups(self):
        print(self.GroupsDF())
 
    # Print projects
    def displayProjects(self):
        print(self.ProjectsDF())
    
    # Print queries
    def displayQueries(self):
        print(self.QueryDF())

    # Print queries
    def displayGroupQueries(self):
        print(self.QueryDF())

    # Print mentions    
    def displayMentions(self):
        print(self.ProjectsDF())
 
    # Convert time with timezone to UTC
    def timeconvertToUTC(self, timestr, tz):
        original = timezone(tz).localize(datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
        utc = original.astimezone(timezone('UTC'))
        return utc.strftime('%Y-%m-%dT%H:%M:%S')

    # Convert time with timezone from UTC
    def timeconvertFromUTC(self, timestr, tz):
        utc = timezone('UTC').localize(datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S'))
        dest = utc.astimezone(timezone(tz))
        return dest.strftime('%Y-%m-%d %H:%M:%S')

    # Convert NZT to UTC
    def NZT2UTC(self, timestr):
        return self.timeconvertToUTC(timestr, 'Pacific/Auckland')

    # Convert UTC to NZT
    def UTC2NZT(self, timestr):
        return self.timeconvertFromUTC(timestr, 'Pacific/Auckland')