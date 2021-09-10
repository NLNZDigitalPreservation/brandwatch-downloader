import unittest
from unittest.mock import MagicMock
from brandwatch import Brandwatch

class TestMethods(unittest.TestCase):

  def testUserWithoutToken(self):
    BW = Brandwatch()
    user = BW.getUser()
    self.assertEqual(user, None)
    print('Get user failed without token')
  
  def testUserWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    user = BW.getUser()
    self.assertEqual(user, None)
    print('Get user failed with invalid token')

  def testUserWithValidToken(self):
    class mockClass:
      def __init__(self, username):
          self.username = username
    BW = Brandwatch(token='valid token')
    BW.getUser = MagicMock(return_value=mockClass('Test user'))
    user = BW.getUser()
    self.assertEqual(user.__dict__['username'], 'Test user')
    print('Get user with valid token')

  def testProjectsWithoutToken(self):
    BW = Brandwatch()
    projects = BW.getProjects()
    self.assertEqual(projects, None)
    print('Get projects failed without token')
  
  def testProjectsWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    projects = BW.getProjects()
    self.assertEqual(projects, None)
    print('Get projects failed with invalid token')

  def testProjectsWithValidToken(self):
    class mockClass:
      def __init__(self):
          self.projects = [{'id': 1, 'name':'test1'}, {'id': 2, 'name':'test2'}]
      def get_projects(self):
        return self.projects
    BW = Brandwatch(token='valid token')
    BW.getUser = MagicMock(return_value=mockClass())
    BW.getProjects = MagicMock(return_value=BW.getUser().get_projects())
    projects = BW.getProjects()
    self.assertEqual(list(map(lambda x: str(x['name']), projects)), ['test1','test2'])
    print('Get projects with valid token')

  def testProjectWithoutToken(self):
    BW = Brandwatch()
    project = BW.getProject('sample project')
    self.assertEqual(project, None)
    print('Get project failed without token')
  
  def testProjectsWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    project = BW.getProject('sample project')
    self.assertEqual(project, None)
    print('Get project failed with invalid token')

  def testGroupsWithoutToken(self):
    BW = Brandwatch()
    groups = BW.getGroups('sample group')
    self.assertEqual(groups, None)
    print('Get groups failed without token')
  
  def testGroupsWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    groups = BW.getGroups('sample group')
    self.assertEqual(groups, None)
    print('Get groups failed with invalid token')
  
  def testQueriesWithoutToken(self):
    BW = Brandwatch()
    queries = BW.getQueries('sample project')
    self.assertEqual(queries, None)
    print('Get queries failed without token')
  
  def testQueriesWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    queries = BW.getQueries('sample project')
    self.assertEqual(queries, None)
    print('Get queries failed with invalid token')

  def testQueriesByGroupWithoutToken(self):
    BW = Brandwatch()
    queries = BW.getQueriesByGroup('sample group')
    self.assertEqual(queries, None)
    print('Get queries failed without token')
  
  def testQueriesByGroupWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    queries = BW.getQueriesByGroup('sample group')
    self.assertEqual(queries, None)
    print('Get queries failed with invalid token')
  
  def testMentionsWithoutToken(self):
    BW = Brandwatch()
    start = BW.NZT2UTC('2021-07-01 00:00:00')
    end = BW.NZT2UTC('2021-07-01 02:59:59')
    queries = BW.getMentions('sample project', 'sample name', start, end)
    self.assertEqual(queries, None)
    print('Get queries failed without token')
  
  def testMentionsWithInvalidToken(self):
    BW = Brandwatch(token='invalid')
    start = BW.NZT2UTC('2021-07-01 00:00:00')
    end = BW.NZT2UTC('2021-07-01 02:59:59')
    queries = BW.getMentions('sample project', 'sample name', start, end)
    self.assertEqual(queries, None)
    print('Get queries failed with invalid token')

if __name__ == '__main__':
  unittest.main()