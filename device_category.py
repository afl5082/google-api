

from __future__ import print_function


import argparse
import sys
import csv

from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError

profile_list = ['101048005','50325093','154614149','2257429','30040209','196614429','1737225','171739616','118262710','34063688','119827378','4305603','9913350','47003897','2682865','38256812','45540119','48939291','149156493','9275400']
desktop = ['desktop',0]
mobile = ['mobile',0]
tablet = ['tablet',0]
catchall = 0

def main(argv):
  
  # Authenticate and construct service.


  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Try to make a request to the API. Print the results or handle errors.
  try:
    first_profile_id = '101048005'
    if not first_profile_id:
      print('Could not find a valid profile for this user.')
    else:
      for x in profile_list:
        results = get_top_keywords(service,x)
        print_results(results)
      write_csv()

      #final function to write csv with final numbers
       
        
    

  except TypeError as error:
    # Handle errors in constructing a query.
    print(('There was an error in constructing your query : %s' % error))

  except HttpError as error:
    # Handle API errors.
    print(('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason())))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_top_keywords(service, profile_id):
  """Executes and returns data from the Core Reporting API.

  This queries the API for the top 25 organic search terms by visits.

  Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.

  Returns:
    The response returned from the Core Reporting API.
  """

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='2020-01-01',
      max_results = '10000',
      end_date = '2020-12-31',
      metrics='ga:sessions', 
      dimensions='ga:deviceCategory'
      ).execute()


def print_results(results):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print()
  print('Profile Name: %s' % results.get('profileInfo').get('profileName'))
  print()


  # Write data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      if row[0] == 'desktop':
        global desktop 
        desktop[1] += int(row[1])

      elif row[0] == 'mobile':
        global mobile 
        mobile[1] += int(row[1])

      elif row[0] == 'tablet':
        global tablet 
        tablet[1] += int(row[1])

      else:
        global catchall
        catchall += int(row[1])

      
    
  

def write_csv():
    # Open a file.
  global desktop
  global mobile
  global tablet
  
  filepath = 'C:\\Users\\Adam LaCaria\\Desktop\\google_api'     #change this to your actual file path
  filename = 'gapythondata12.csv'         #change this to your actual file name
  f = open(filepath.strip('\\') + '\\' + filename, 'wt')

  # Wrap file with a csv.writer
  writer = csv.writer(f, lineterminator='\n')
  
  # Write header.
  header = ['deviceCategory', 'sessions']
  writer.writerow(header)

  rows = [desktop,mobile,tablet]

  for row in rows:
    writer.writerow(row)
    print(''.join('%30s' %r for r in row))


  print('\n')
  print ('Success Data Written to CSV File')
  print ('filepath = ' + filepath)
  print ('filename = '+ filename)
  f.close()


if __name__ == '__main__':

  main(sys.argv)
