import unittest
from brandwatch import Brandwatch

class TestTimeConvert(unittest.TestCase):

  def testConvertToUTC(self):
    BW = Brandwatch()
    time = BW.timeconvertToUTC('2021-07-01 00:00:00', 'Asia/Hong_Kong')
    expected = '2021-06-30T16:00:00'
    self.assertEqual(time, expected)
    print('Time convert to UTC correctly.')
  
  def testConvertFromUTC(self):
    BW = Brandwatch()
    time = BW.timeconvertFromUTC('2021-07-01T00:00:00', 'Asia/Hong_Kong')
    expected = '2021-07-01 08:00:00'
    self.assertEqual(time, expected)
    print('Time convert from UTC correctly.')

  def testNZT2UTC(self):
    BW = Brandwatch()
    time = BW.NZT2UTC('2021-07-01 00:00:00')
    expected = '2021-06-30T12:00:00'
    self.assertEqual(time, expected)
    print('NZT convert to UTC correctly.')

  def testUTC2NZT(self):
    BW = Brandwatch()
    time = BW.UTC2NZT('2021-06-30T12:00:00')
    expected = '2021-07-01 00:00:00'
    self.assertEqual(time , expected)
    print('UTC convert to NZT correctly.')

if __name__ == '__main__':
  unittest.main()