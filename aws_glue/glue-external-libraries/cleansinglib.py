from awsglue.transforms import *

def renamefield(df,oldname,newname):
  df = RenameField.apply(df, oldname, newname) 
  return df