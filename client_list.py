from __future__ import print_function
import argparse
import sys
import csv
import pandas as pd
from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError



def main(argv):
    #calling google api service
    service, flags = sample_tools.init(argv, 'analytics', 'v3', __doc__, __file__, scope='https://www.googleapis.com/auth/analytics.readonly')
    
    #return dataframe unused 
    dataframe = get_ga_accounts(service)
    
#gathers all web properties under analytics access, merges accountname and writes to csv
def get_ga_accounts(service):

  prop_data =[]
  account_data= []

  #dataFrame unique record for each ga web property 
  df = pd.DataFrame(prop_data, columns =['AccountID','PropertyID', 'PropertyName','PropertyProfileCount','PropertyVertical','PropertyInternalID','PropertyLevel','WebsiteURL','Created','Updated'])

  #properties object via service, collecting all accounts under analytics
  properties = service.management().webproperties().list(
    accountId='~all').execute()
  
  for property in properties.get('items', []):
      internal_data = []  
      accountid = property.get('accountId')
      print ('Account ID ' + str(accountid))

      propid = property.get('id')
      print ('Property ID ' + str(propid))

      propname = property.get('name')
      print ('Property Name ' + str(propname))

      profilec = property.get('profileCount')
      print ('Property Profile Count ' + str(profilec))

      vertical = property.get('industryVertical')
      print ('Property Industry Vertical ' + str(vertical))

      internalid = property.get('internalWebPropertyId')
      print ('Property Internal Id ' + str(internalid))

      proplevel = property.get('level')
      print ('Property Level ' + str(proplevel))

      if property.get('websiteUrl'):
          url = property.get('websiteUrl')
          print ('Property URL ' + str(url))
      else:
        url = None

      created = property.get('created')
      print ('Created ' + str(created))

      updated = property.get('updated')
      print ('Updated ' + str(updated))

      #extend, adding multiple variables to the list
      internal_data.extend((accountid,propid,propname,profilec,vertical,internalid,proplevel,url,created,updated))
      to_append = internal_data
      df_length = len(df)

      #unique web property added to end of dataFrame
      df.loc[df_length] = to_append
       
  
  df2 = pd.DataFrame(account_data,columns =['AccountID','AccountName'])

 
  accounts = service.management().accounts().list().execute()
  for account in accounts.get('items',[] ):
    internal_account = []
    account_name = account.get('name')
    account_id = account.get('id')
    
    #unique account added to list 
    internal_account.extend((account_id,account_name))

    to_append2 = internal_account
    df2_length = len(df2)

    #unique account added to end of account dataFrame
    df2.loc[df2_length] = to_append2

  #vlookup to match accountName from df2, properties object did not have accountName just accountID
  left_join = pd.merge(df,df2,on ='AccountID',how = 'left')
  
  #writing to csv from dataFrame method 'to_csv'
  left_join.to_csv(r'C:\Users\Adam LaCaria\Desktop\google_api\client_list.csv', index=False,header=True)
  return left_join
  
if __name__ == '__main__':
  main(sys.argv)
