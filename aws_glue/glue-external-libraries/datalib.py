def readdata(db,tbl,gc):
  df = gc.create_dynamic_frame.from_catalog(database=db,table_name=tbl, redshift_tmp_dir="s3://dojo-dataset/script/")
  return df

def writedata(df,folder,format,gc):
  gc.write_dynamic_frame.from_options(df, connection_type = "s3", connection_options = {"path": "s3://dojo-dataset/" + folder}, format = format)