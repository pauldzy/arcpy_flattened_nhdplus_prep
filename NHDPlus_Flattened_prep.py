"""
NHDPlus Flattened Preprocessing

"""

import sys,re,os,time;
import getopt;

#####################################################################################################
#
#
author = "Paul Dziemiela";
version = "1.0";
last_mod = "04/06/2015";
#
#####################################################################################################
def usage():
   sys.stderr.write("\n");
   sys.stderr.write(sys.argv[0] + "\n");
   sys.stderr.write("version " + version + "\n");
   sys.stderr.write("by " + author + ", Indus Corporation\n");
   sys.stderr.write("last modified: " + last_mod + "\n");
   sys.stderr.write("\n");
   sys.stderr.write("  --input_fgdb      input NHDPlus flattened workspace (usually fgdb) \n");
   sys.stderr.write("  --output_fgdb     output file geodatabase \n");
   sys.stderr.write("\n");
   sys.exit(10);
   
try:
   import arcpy;
   from arcpy import env;
   
except:
   sys.stderr.write("Unable to load arcpy module\n");
   sys.stderr.write("Does this workstation have ArcGIS desktop installed?\n");
   sys.exit(99);

class maps:
   
   ##################################################################################################
   def __init__(self):
      None;
      
   ##################################################################################################
   def nhdpoint(self):
      
      return [ \
          ("COMID"                         ,"ComID"                        ,"Long"   ,11    ,True)
         ,("FDATE"                         ,"FDate"                        ,None     ,None  ,False)
         ,("RESOLUTION"                    ,"Resolution"                   ,None     ,None  ,False)
         ,("GNIS_ID"                       ,"GNIS_ID"                      ,None     ,None  ,True)
         ,("GNIS_NAME"                     ,"GNIS_Name"                    ,None     ,None  ,True)
         ,("REACHCODE"                     ,"ReachCode"                    ,None     ,None  ,True)
         ,("FTYPE"                         ,"FType"                        ,None     ,None  ,True)
         ,("FCODE"                         ,"FCode"                        ,"Long"   ,5     ,True) 
      ];
                
   ##################################################################################################
   def nhdline(self):
      
      return [ \
          ("COMID"                         ,"ComID"                        ,"Long"   ,11    ,True)
         ,("FDATE"                         ,"FDate"                        ,None     ,None  ,False)
         ,("RESOLUTION"                    ,"Resolution"                   ,None     ,None  ,False)
         ,("GNIS_ID"                       ,"GNIS_ID"                      ,None     ,None  ,True)
         ,("GNIS_NAME"                     ,"GNIS_Name"                    ,None     ,None  ,True)
         ,("LENGTHKM"                      ,"LengthKM"                     ,"Double" ,None  ,False)
         ,("FTYPE"                         ,"FType"                        ,None     ,None  ,True)
         ,("FCODE"                         ,"FCode"                        ,"Long"   ,5     ,True) 
      ];
                
   ##################################################################################################
   def nhdarea(self):
      
      return [ \
          ("COMID"                         ,"ComID"                        ,"Long"   ,11    ,True)
         ,("FDATE"                         ,"FDate"                        ,None     ,None  ,False)
         ,("RESOLUTION"                    ,"Resolution"                   ,None     ,None  ,False)
         ,("GNIS_ID"                       ,"GNIS_ID"                      ,None     ,None  ,True)
         ,("GNIS_NAME"                     ,"GNIS_Name"                    ,None     ,None  ,True)
         ,("AREASQKM"                      ,"AreaSQKM"                     ,"Double" ,None  ,False)
         ,("ELEVATION"                     ,"Elevation"                    ,"Double" ,None  ,False)
         ,("FTYPE"                         ,"FType"                        ,None     ,None  ,True)
         ,("FCODE"                         ,"FCode"                        ,"Long"   ,5     ,True)
         ,("ONOFFNET"                      ,"OnOffNet"                     ,"Short"  ,None  ,True)
         ,("PurpCode"                      ,"PurpCode"                     ,None     ,None  ,False)
         ,("PurpDesc"                      ,"PurpDesc"                     ,None     ,None  ,False)
      ];
                
   ##################################################################################################
   def nhdflowline_network(self):
      
      return [ \
          ("COMID"                         ,"ComID"                        ,"Long"   ,11    ,True)
         ,("FDATE"                         ,"FDate"                        ,None     ,None  ,False)
         ,("RESOLUTION"                    ,"Resolution"                   ,None     ,None  ,False)
         ,("GNIS_ID"                       ,"GNIS_ID"                      ,None     ,None  ,True)
         ,("GNIS_NAME"                     ,"GNIS_Name"                    ,None     ,None  ,True)
         ,("LENGTHKM"                      ,"LengthKM"                     ,"Double" ,None  ,False)
         ,("REACHCODE"                     ,"ReachCode"                    ,None     ,None  ,True)
         ,("FLOWDIR"                       ,"FlowDir"                      ,None     ,None  ,False)
         ,("WBAREACOMI"                    ,"WBAreaComID"                  ,"Long"   ,11    ,True)
         ,("FTYPE"                         ,"FType"                        ,None     ,None  ,True)
         ,("FCODE"                         ,"FCode"                        ,"Long"   ,5     ,True)
         ,("StreamLeve"                    ,"StreamLevel"                  ,"Long"   ,11    ,True)
         ,("StreamOrde"                    ,"StreamOrder"                  ,"Long"   ,11    ,True)
         ,("StreamCalc"                    ,"StreamCalc"                   ,"Long"   ,11    ,True)
         ,("FromNode"                      ,"FromNode"                     ,"Long"   ,11    ,True)
         ,("ToNode"                        ,"ToNode"                       ,"Long"   ,11    ,True)
         ,("Hydroseq"                      ,"Hydroseq"                     ,"Long"   ,11    ,True)
         ,("LevelPathI"                    ,"LevelPathID"                  ,"Long"   ,11    ,True)
         ,("Pathlength"                    ,"Pathlength"                   ,"Double" ,None  ,False)
         ,("TerminalPa"                    ,"TerminalPathID"               ,"Long"   ,11    ,True)
         ,("ArbolateSu"                    ,"ArbolateSum"                  ,"Double" ,None  ,False)
         ,("Divergence"                    ,"Divergence"                   ,"Short"  ,None  ,False)
         ,("StartFlag"                     ,"StartFlag"                    ,"Short"  ,None  ,False)
         ,("TerminalFl"                    ,"TerminalFlag"                 ,"Short"  ,None  ,False)
         ,("DnLevel"                       ,"DnLevel"                      ,"Short"  ,None  ,False)
         ,("UpLevelPat"                    ,"UpLevelPathID"                ,"Long"   ,11    ,True)
         ,("UpHydroseq"                    ,"UpHydroseq"                   ,"Long"   ,11    ,True)
         ,("DnLevelPat"                    ,"DnLevelPathID"                ,"Long"   ,11    ,True)
         ,("DnMinorHyd"                    ,"DnMinorHyd"                   ,"Long"   ,11    ,True)
         ,("DnDrainCou"                    ,"DnDrainCount"                 ,"Short"  ,None  ,False)
         ,("DnHydroseq"                    ,"DnHydroseq"                   ,"Long"   ,11    ,True)
         ,("FromMeas"                      ,"FMeasure"                     ,"Double" ,None  ,False)
         ,("ToMeas"                        ,"TMeasure"                     ,"Double" ,None  ,False)
         ,("RtnDiv"                        ,"RtnDiv"                       ,"Short"  ,None  ,False)
         ,("VPUIn"                         ,"VPUIn"                        ,"Short"  ,None  ,False)
         ,("VPUOut"                        ,"VPUOut"                       ,"Short"  ,None  ,False)
         ,("AreaSqKM"                      ,"AreaSqKM"                     ,"Double" ,None  ,False)
         ,("TotDASqKM"                     ,"TotDASqKM"                    ,"Double" ,None  ,False)
         ,("DivDASqKM"                     ,"DivDASqKM"                    ,"Double" ,None  ,False)
         ,("HWNodeSqKM"                    ,"HWNodeSqKM"                   ,"Double" ,None  ,False)
         ,("MAXELEVRAW"                    ,"MaxElevRaw"                   ,"Double" ,None  ,False)
         ,("MINELEVRAW"                    ,"MinElevRaw"                   ,"Double" ,None  ,False)
         ,("MAXELEVSMO"                    ,"MaxElevSMO"                   ,"Double" ,None  ,False)
         ,("MINELEVSMO"                    ,"MinElevSMO"                   ,"Double" ,None  ,False)
         ,("SLOPE"                         ,"Slope"                        ,"Double" ,None  ,False)
         ,("ELEVFIXED"                     ,"ElevFixed"                    ,None     ,None  ,False)
         ,("HWTYPE"                        ,"HWType"                       ,None     ,None  ,False)
         ,("SLOPELENKM"                    ,"SlopeLenKM"                   ,"Double" ,None  ,False)
         ,("Q0001A"                        ,"Q0001A"                       ,"Double" ,None  ,False)
         ,("V0001A"                        ,"V0001A"                       ,"Double" ,None  ,False)
         ,("Qincr0001A"                    ,"Qincr0001A"                   ,"Double" ,None  ,False)
         ,("Q0001B"                        ,"Q0001B"                       ,"Double" ,None  ,False)
         ,("V0001B"                        ,"V0001B"                       ,"Double" ,None  ,False)
         ,("Qincr0001B"                    ,"Qincr0001B"                   ,"Double" ,None  ,False)
         ,("Q0001C"                        ,"Q0001C"                       ,"Double" ,None  ,False)
         ,("V0001C"                        ,"V0001C"                       ,"Double" ,None  ,False)
         ,("Qincr0001C"                    ,"Qincr0001C"                   ,"Double" ,None  ,False)
         ,("Q0001D"                        ,"Q0001D"                       ,"Double" ,None  ,False)
         ,("V0001D"                        ,"V0001D"                       ,"Double" ,None  ,False)
         ,("Qincr0001D"                    ,"Qincr0001D"                   ,"Double" ,None  ,False)
         ,("Q0001E"                        ,"Q0001E"                       ,"Double" ,None  ,False)
         ,("V0001E"                        ,"V0001E"                       ,"Double" ,None  ,False)
         ,("Qincr0001E"                    ,"Qincr0001E"                   ,"Double" ,None  ,False)
         ,("Q0001F"                        ,"0001F"                        ,"Double" ,None  ,False)
         ,("Qincr0001F"                    ,"Qincr0001F"                   ,"Double" ,None  ,False)
         ,("ARQ0001NAV"                    ,"ARQ0001NAV"                   ,"Double" ,None  ,False)
         ,("TEMP0001"                      ,"TEMP0001"                     ,"Double" ,None  ,False)
         ,("PPT0001"                       ,"PPT0001"                      ,"Double" ,None  ,False)
         ,("PET0001"                       ,"PET0001"                      ,"Double" ,None  ,False)
         ,("QLOSS0001"                     ,"QLOSS0001"                    ,"Double" ,None  ,False)
         ,("QG0001ADJ"                     ,"QG0001ADJ"                    ,"Double" ,None  ,False)
         ,("QG0001NAV"                     ,"QG0001NAV"                    ,"Double" ,None  ,False)
         ,("LAT"                           ,"Lat"                          ,"Double" ,None  ,False)
         ,("Gageadj"                       ,"GageAdj"                      ,None     ,None  ,False)
         ,("avgqadj"                       ,"AvgQAdj"                      ,"Double" ,None  ,False)
         ,("SMGageID"                      ,"SMGageID"                     ,None     ,None  ,False)
         ,("SMgageq"                       ,"SMGageQ"                      ,"Double" ,None  ,False)
         ,("ETFRACT1"                      ,"ETFract1"                     ,"Double" ,None  ,False)
         ,("ETFRACT2"                      ,"ETFract2"                     ,"Double" ,None  ,False)
         ,("a"                             ,"a"                            ,"Double" ,None  ,False)
         ,("b"                             ,"b"                            ,"Double" ,None  ,False)
         ,("BCF"                           ,"BCF"                          ,"Double" ,None  ,False)
         ,("r2"                            ,"r2"                           ,"Double" ,None  ,False)
         ,("SER"                           ,"Ser"                          ,"Double" ,None  ,False)
         ,("NRef"                          ,"NRef"                         ,"Double" ,None  ,False)
         ,("gageseqp"                      ,"GageSeqP"                     ,"Double" ,None  ,False)
         ,("gageseq"                       ,"GageSeq"                      ,"Double" ,None  ,False)
         ,("RPUID"                         ,"RPUID"                        ,None     ,None  ,True)
      ];

   ##################################################################################################
   def nhdflowline_nonnetwork(self):
      
      return [ \
          ("COMID"                         ,"ComID"                        ,"Long"   ,11    ,True)
         ,("FDATE"                         ,"FDate"                        ,None     ,None  ,False)
         ,("RESOLUTION"                    ,"Resolution"                   ,None     ,None  ,False)
         ,("GNIS_ID"                       ,"GNIS_ID"                      ,None     ,None  ,True)
         ,("GNIS_NAME"                     ,"GNIS_Name"                    ,None     ,None  ,True)
         ,("LENGTHKM"                      ,"LengthKM"                     ,"Double" ,None  ,False)
         ,("REACHCODE"                     ,"ReachCode"                    ,None     ,None  ,True)
         ,("FLOWDIR"                       ,"FlowDir"                      ,None     ,None  ,False)
         ,("WBAREACOMI"                    ,"WBAreaComID"                  ,"Long"   ,11    ,True)
         ,("FTYPE"                         ,"FType"                        ,None     ,None  ,True)
         ,("FCODE"                         ,"FCode"                        ,"Long"   ,5     ,True)
      ];   
   
   ##################################################################################################
   def nhdwaterbody(self):
      
      return [ \
          ("COMID"                         ,"ComID"                        ,"Long"   ,11    ,True)
         ,("FDATE"                         ,"FDate"                        ,None     ,None  ,False)
         ,("RESOLUTION"                    ,"Resolution"                   ,None     ,None  ,False)
         ,("GNIS_ID"                       ,"GNIS_ID"                      ,None     ,None  ,True)
         ,("GNIS_NAME"                     ,"GNIS_Name"                    ,None     ,None  ,True)
         ,("AREASQKM"                      ,"AreaSQKM"                     ,"Double" ,None  ,False)
         ,("ELEVATION"                     ,"Elevation"                    ,"Double" ,None  ,False)
         ,("REACHCODE"                     ,"ReachCode"                    ,None     ,None  ,True)
         ,("FTYPE"                         ,"FType"                        ,None     ,None  ,True)
         ,("FCODE"                         ,"FCode"                        ,"Long"   ,5     ,True)
         ,("ONOFFNET"                      ,"OnOffNet"                     ,"Short"  ,None  ,True)
         ,("PurpCode"                      ,"PurpCode"                     ,None     ,None  ,False)
         ,("PurpDesc"                      ,"PurpDesc"                     ,None     ,None  ,False)
      ];
                
   ##################################################################################################
   def catchment(self):
      
      return [ \
          ("GRIDCODE"                      ,"GridCode"                     ,"Long"   ,11    ,True)
         ,("FEATUREID"                     ,"FeatureID"                    ,"Long"   ,11    ,True)
         ,("SOURCEFC"                      ,"SourceFC"                     ,None     ,None  ,True)
         ,("AreaSqKM"                      ,"AreaSqKM"                     ,"Double" ,None  ,False)
      ];
    
   ##################################################################################################
   def huc12(self):
      
      return [ \
          ("HUC_8"                         ,"HUC_8"                        ,None     ,None  ,True)
         ,("HUC_10"                        ,"HUC_10"                       ,None     ,None  ,True)
         ,("HUC_12"                        ,"HUC_12"                       ,None     ,None  ,True)
         ,("ACRES"                         ,"Acres"                        ,"Double" ,None  ,False)
         ,("NCONTRB_A"                     ,"NContrb_Area"                 ,"Double" ,None  ,False)
         ,("HU_10_GNIS"                    ,"HU_10_GNIS"                   ,None     ,None  ,False)
         ,("HU_12_GNIS"                    ,"HU_12_GNIS"                   ,None     ,None  ,False)
         ,("HU_10_DS"                      ,"HU_10_DS"                     ,None     ,None  ,False)
         ,("HU_10_NAME"                    ,"HU_10_Name"                   ,None     ,None  ,False)
         ,("HU_10_MOD"                     ,"HU_10_MOD"                    ,None     ,None  ,False)
         ,("HU_10_TYPE"                    ,"HU_10_Type"                   ,None     ,None  ,False)
         ,("HU_12_DS"                      ,"HU_12_DS"                     ,None     ,None  ,False)
         ,("HU_12_NAME"                    ,"HU_12_Name"                   ,None     ,None  ,False)
         ,("HU_12_MOD"                     ,"HU_12_MOD"                    ,None     ,None  ,False)
         ,("HU_12_TYPE"                    ,"HU_12_Type"                   ,None     ,None  ,False)
         ,("META_ID"                       ,"Meta_ID"                      ,None     ,None  ,False)
         ,("STATES"                        ,"States"                       ,None     ,None  ,False)
         ,("GAZ_ID"                        ,"GAZ_ID"                       ,"Long"   ,11    ,False)
         ,("WBD_Date"                      ,"WBD_Date"                     ,None     ,None  ,False)
         ,("VPUID"                         ,"VPUID"                        ,None     ,None  ,False)
         ,("HUC_2"                         ,"HUC_2"                        ,None     ,None  ,True)
         ,("HUC_4"                         ,"HUC_4"                        ,None     ,None  ,True)
         ,("HUC_6"                         ,"HUC_6"                        ,None     ,None  ,True)
      ];
      
class extract:
   """
   The main object for doing work with the geoprocessor.
   The calling code is expected to load the ESRI geoprocessor class
   """
   
   def __init__(self,target_ws=None):
      self.target_ws = target_ws;
         
   ################################################################################################## 
   def delete_table(self,table_name):
      
      if table_name == ".shp" or table_name == ".dbf":
         return;
         
      if arcpy.Exists(table_name):
         try:
            arcpy.Delete_management(table_name)
            
         except:
            sys.stderr.write("unable to delete " + table_name + "!");
            print arcpy.GetMessages(2)
            sys.exit(60)
            
   ################################################################################################## 
   def check_exists(self,ary_items_in):
   
      ary_items = [];
      for item in ary_items_in:
         if item is not None:
            ary_items.append(item);
      
      fcList = arcpy.ListFeatureClasses();
      
      if fcList is None or len(fcList) == 0:
         return -1;
      
      chk = 0;
      for fc in fcList:
         for item in ary_items:
            if fc.upper() == item.upper():
               chk += 1;
      
      tblList = arcpy.ListTables();
      for fc in tblList:
         for item in ary_items:
            if fc.upper() == item.upper():
               chk += 1;

      return abs(len(ary_items) - chk);
   
   ################################################################################################## 
   def create_container(
       self
      ,work_path
      ,container_name
      ,container_type = None
   ):
   
      if container_type is None:
         container_type = "FGDB";
         
      else:
         container_type = container_type.upper()
         
      if container_type == "FGDB":
         # Define and create new output filegeodatabase if needed
         if container_name[-4:] != ".gdb":
            container_name += ".gdb";
         
         if not arcpy.Exists(work_path + "\\" + container_name):
            try:
               arcpy.CreateFileGDB_management(
                  work_path,
                  container_name
               );
            except:
               print arcpy.GetMessages()
               raise;
      
      elif container_type == "GPKG":
         if container_name[-5:] != ".gpkg":
            container_name += ".gpkg";
         
         if not arcpy.Exists(work_path + "\\" + container_name):
            try:
               arcpy.gp.CreateSQLiteDatabase(
                   work_path + "\\" + container_name
                  , "GEOPACKAGE"
               );
            except:
               print arcpy.GetMessages()
               raise;
               
      elif container_type == "SHP" or container_type == "FOLDER":
         # Define and create new output folder to hold the shape files if required
         if not arcpy.Exists(work_path + "\\" + container_name):
            try:
               arcpy.CreateFolder_management(
                  work_path, 
                  container_name
               );
            except:
               print arcpy.GetMessages()
               raise;  
      
      else:
         sys.stderr.write("container types are FGDB, SHP, FOLDER or GPKG");
         sys.exit(60)
      
   ##################################################################################################
   def create_new_fieldmap(self,source_fc,map_array,fields_upper=False):

      try:
         fieldmappings = arcpy.CreateObject("FieldMappings")
         fieldmapstorage = arcpy.CreateObject("FieldMappings");
         
      except:
         print arcpy.GetMessages(2)
         sys.exit(60)
         
      #for (inputfield, outputfield, datatype, datalength, index_flag, ) in map_array:
      #   print inputfield, outputfield, datatype, datalength, index_flag;
      try:      
         fieldmappings.addTable(source_fc);
         fieldmapstorage.addTable(source_fc);
         
      except:
         print arcpy.GetMessages(2);
         raise;
         
      ary_inputs = [];
      for (inputfield, outputfield, datatype, datalength, index_flag) in map_array:
         ary_inputs.append(inputfield);
      
      fieldList = arcpy.ListFields(source_fc, "*", "ALL");      
      for actionfield in fieldList:
         
         if actionfield.name not in ary_inputs:
            if actionfield.name.upper() not in (
                'OBJECTID'
               ,'OBJECTID_1'
               ,'SE_SDO_ROWID'
               ,'SHAPE'
               ,'SHAPE.LEN'
               ,'SHAPE.LENGTH'
               ,'SHAPE.AREA'
               ,'SHAPE_LEN'
               ,'SHAPE_LENGTH'
               ,'SHAPE_AREA'
            ):
               try:
                  fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(actionfield.name))
               except:
                  print actionfield.name
                  print arcpy.GetMessages(2)
                  raise;
                  
      for (inputfield, outputfield, datatype, datalength, index_flag) in map_array:
         #print inputfield, outputfield, datatype, datalength, index_flag;
         
         try:
            fieldmap = fieldmappings.getFieldMap(fieldmappings.findFieldMapIndex(inputfield))
         except:
            print inputfield;
            raise;
         
         field = fieldmap.outputField
         if datatype is not None:
            field.type = datatype;
         if datalength is not None:
            field.length = datalength;
         
         if fields_upper is True:
            field.name = outputfield.upper();
            field.aliasName = outputfield.upper();
         else:
            field.name = outputfield;
            field.aliasName = outputfield.upper();
         
         fieldmap.outputField = field;
         
         if datatype is None or datatype == "Text":
            if datalength is not None:
               fieldmap.setStartTextPosition(0,0);
               fieldmap.setEndTextPosition(0,datalength-1);
         
         fieldmappings.replaceFieldMap(fieldmappings.findFieldMapIndex(inputfield), fieldmap)
               
      return fieldmappings
     
   ##################################################################################################
   def export_fc(self,source_fc,target_nm,str_sql,map_array,fields_upper=False,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("error, must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
      
      if map_array is not None:
         
         fieldmappings = self.create_new_fieldmap(
             source_fc
            ,map_array
            ,fields_upper
         );

         try:
            arcpy.FeatureClassToFeatureClass_conversion(
                source_fc
               ,target_ws
               ,target_nm
               ,str_sql
               ,fieldmappings
            );
            
         except:
            print arcpy.GetMessages()
            raise;
            
      else:
      
         try:
            arcpy.FeatureClassToFeatureClass_conversion(
                source_fc
               ,target_ws
               ,target_nm
               ,str_sql
            );
            
         except:
            print arcpy.GetMessages()
            raise;
      
   ##################################################################################################
   def export_tb(self,source_tb,target_nm,str_sql,map_array,fields_upper=False,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("error, must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      if map_array is not None:
         fieldmappings = self.create_new_fieldmap(
            source_tb,
            map_array,
            fields_upper
         );
         
         try:
            arcpy.TableToTable_conversion(
               source_tb,
               target_ws,
               target_nm,
               str_sql,
               fieldmappings
            );
         except:
            print arcpy.GetMessages()
            raise;
         
      else:
      
         try:
            arcpy.TableToTable_conversion(
               source_tb,
               target_ws,
               target_nm,
               str_sql
            );
            
         except:
            print arcpy.GetMessages(2)
            raise;
      
   ##################################################################################################
   def index_tb(self,target_nm,map_array,fields_upper=False,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("error, must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      arcpy.toolbox = "management";
      env.workspace = target_ws;

      for (inputfield, outputfield, datatype, datalength, index_flag) in map_array:
         
         if fields_upper is True:
            outputfield = outputfield.upper()
            
         if index_flag is True and target_nm[-4:] != ".dbf":
            try:
               # Create an attribute index for the few fields listed in command.
               arcpy.AddIndex_management(
                  target_nm, 
                  outputfield, 
                  outputfield + "_IDX"
               );

            except:
               if re.search("Attribute indexes cannot be created for fields with a length that is greater than 80.",arcpy.GetMessages(2)):
                  sys.stderr.write("Indexing " + outputfield + " skipped as field is too long for dBase indexes.\n");
               else:
                  sys.stderr.write("Indexing " + outputfield + " failed.\n");
                  print arcpy.GetMessages(2);
                  raise;
      
   ##################################################################################################
   def rebuild_spatial_index(self,target_nm,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("error, must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      fc = target_ws + "//" + target_nm;

      try:
         # Get the grid sizes from the tool, this is a string with 3 semi-colon seperated values (typically something like "1500; 0; 0") 
         indexgrids = arcpy.CalculateDefaultGridIndex_management(fc)
         indexgrid1 = indexgrids.split(";")[0]
         indexgrid2 = indexgrids.split(";")[1]
      
      except:
         print arcpy.getmessages();
         raise;
         
      try:
         # First remove the existing grid index
         arcpy.RemoveSpatialIndex_management(fc)
      
      except:
         print arcpy.getmessages();
         raise;
         
      try:
         # Now add the indexes calculated by the tool
         arcpy.AddSpatialIndex_management(fc,indexgrid1,indexgrid2)

      except:
         print arcpy.getmessages();
         raise;
      
   ##################################################################################################
   def project_fc_3785(self,target_nm,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("error, must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      arcpy.toolbox = "management";
      env.workspace = target_ws;
      
      cs = 'PROJCS["WGS_1984_Web_Mercator",GEOGCS["GCS_WGS_1984_Major_Auxiliary_Sphere",DATUM["D_WGS_1984_Major_Auxiliary_Sphere",SPHEROID["WGS_1984_Major_Auxiliary_Sphere",6378137.0,0.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],UNIT["Meter",1.0]]'
      
      try:
         arcpy.Project_management(
            env.workspace + "//" + target_nm, 
            target_nm + "_prjtmp", 
            cs, 
            "NAD_1983_To_WGS_1984_1;WGS_1984_Major_Auxiliary_Sphere_To_WGS_1984"
         );

      except:
         print arcpy.GetMessages(2)
         raise;
         
      arcpy.Delete_management(target_nm);
      arcpy.Rename_management(target_nm + "_prjtmp",target_nm);
      
   ##################################################################################################
   def project_fc(self,srid,target_nm,target_ws=None):
   
      if srid == "3785":
         self.project_fc_3785(target_nm,target_ws);
         
      elif srid == "3857":
         self.project_fc_3857(target_nm,target_ws);
      
      elif srid == "4326":
         self.project_fc_4326(target_nm,target_ws);
      
      else:
         sys.stderr.write("ERROR, unsupported SRID " + str(srid) + "!");
         sys.exit(-1)
               
   ##################################################################################################
   def project_fc_3857(self,target_nm,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      arcpy.toolbox = "management";
      env.workspace = target_ws;
      
      cs = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0],AUTHORITY["EPSG",3857]]'
      
      try:
         arcpy.Project_management(
             env.workspace + "//" + target_nm
            ,target_nm + "_prjtmp"
            ,cs
         );

      except:
         print arcpy.GetMessages(2)
         raise;
         
      arcpy.Delete_management(target_nm);
      arcpy.Rename_management(target_nm + "_prjtmp",target_nm);
      
   ##################################################################################################
   def project_fc_4326(self,target_nm,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("must provide target workspace for output");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      arcpy.toolbox = "management";
      env.workspace = target_ws;
      
      cs = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG",4326]]'
      
      try:
         arcpy.Project_management(
            env.workspace + "//" + target_nm, 
            target_nm + "_prjtmp", 
            cs, 
            "NAD_1983_To_WGS_1984_1"
         );

      except:
         print arcpy.GetMessages(2)
         raise;
         
      arcpy.Delete_management(target_nm);
      arcpy.Rename_management(target_nm + "_prjtmp",target_nm);
      
   ##################################################################################################
   def execute_immediate(self,str_sql,sp_title=None):
      if sp_title is None:
         sp_title = "stored procedure";         
      
      sys.stderr.write("Running " + sp_title + " on database...");
      
      try:
         sdeConn = arcpy.ArcSDESQLExecute(env.workspace);
         
      except:
         print " "
         print "workspace = " + str(env.workspace);
         print arcpy.GetMessages();
         raise;
   
      try:
         sdeReturn = sdeConn.execute(str_sql)
      except:
         sdeReturn = False
         raise;
      
      sys.stderr.write("DONE.\n");

      return sdeReturn;
      
   ##################################################################################################
   def create_dataset(self,dataset_name,sr=None,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("ERROR, must provide target workspace for output!");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      try:
         arcpy.CreateFeatureDataset_management(target_ws, dataset_name, sr);
         
      except:
         print " "
         print target_ws
         print dataset_name
         print arcpy.GetMessages(2);
         raise;
      
   ##################################################################################################
   def domain_exists(self,domain_name,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("ERROR, must provide target workspace for output!");
            sys.exit(-1)
         else:
            target_ws = self.target_ws;
            
      desc = arcpy.Describe(target_ws);
      for domain in desc.domains:
         if domain == domain_name:
            return True;
            
      return False;
      
   ##################################################################################################
   def assigndefaulttofield(self,target_table,target_field,default_value,subtype_code=None,target_ws=None):
      
      if target_ws is None:
         if self.target_ws is None:
            sys.stderr.write("ERROR, must provide target workspace for output!");
            sys.exit(-1)
         else:
            env.workspace = self.target_ws;
            
      try:
         arcpy.AssignDefaultToField_management(
            target_table,
            target_field,
            default_value,
            subtype_code
         );
      
      except:
         print target_table
         print target_field
         print arcpy.GetMessages(2);
         raise;

#####################################################################################################
# Step 10
# Verify arguments
#####################################################################################################
if len(sys.argv) == 1:
   usage();

try:
   opts,args = getopt.getopt(
       sys.argv[1:]
      ,"h"
      ,["help","input_fgdb=","in=","output_fgdb=","out="]
   );
   
except getopt.GetoptError:
   usage();

input_fgdb = None;
output_fgdb = None;
   
rc = 0;
for opt, arg in opts:
   if opt == "-h" or opt == "--help":
      usage();
   elif opt == "--input_fgdb" or opt == "--in":
      input_fgdb = arg;
   elif opt == "--output_fgdb" or opt == "--out":
      output_fgdb = arg;
      
if input_fgdb is None:
   sys.stderr.write("please provide input fgdb parameter\n");
   rc +=1;
   
if output_fgdb is None:
   sys.stderr.write("please provide output fgdb parameter\n");
   rc +=1;
   
if input_fgdb is not None and input_fgdb == output_fgdb:
   sys.stderr.write("error, input and output file geodatabase names cannot be the same\n");
   rc +=1;
   
if rc > 0:
   sys.stderr.write("use option --help for parameter details\n");
   sys.exit(1);
   
if input_fgdb[-4:] != ".gdb":
   input_fgdb += ".gdb";
   
if output_fgdb[-4:] != ".gdb":
   output_fgdb += ".gdb";
   
#####################################################################################################
# Step 20
# Verify source data exists and build scratch and output file geodatabases
#####################################################################################################
if not arcpy.Exists(input_fgdb):
   sys.stderr.write("error, could not find input geodatabase at " + input_fgdb);
   sys.exit(1);
   
if not arcpy.Exists(input_fgdb + "\\NHDSnapshot\\NHDFlowline_Network"):
   sys.stderr.write("error, could not find NHDFlowline_Network feature class at " + input_fgdb);
   sys.exit(1);
   
if arcpy.Exists(output_fgdb):
   arcpy.Delete_management(output_fgdb);
out_folder_path,out_name = os.path.split(output_fgdb);
arcpy.CreateFileGDB_management(out_folder_path,out_name);
   
scratch_fgdb = arcpy.CreateScratchName(
    "NHDPlus_Flattened_Scratch"
   ,".gdb"
   ,None
   ,arcpy.env.scratchFolder
);

scratch_folder_path,scratch_name = os.path.split(scratch_fgdb);
arcpy.CreateFileGDB_management(scratch_folder_path,scratch_name);

#####################################################################################################
# Step 30
# Initialize Feedback
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("Preparing to preprocess NHDPlus Flattened datasets\n");
sys.stdout.write("Input: " + input_fgdb + "\n");
sys.stdout.write("Output: " + output_fgdb + "\n");
sys.stdout.write("Scratch: " + scratch_fgdb + "\n");

start_time = time.time();
arcpy.env.outputZFlag = "Disabled";
arcpy.env.outputMFlag = "Disabled";
dzgp  = extract(scratch_fgdb);
dzmap = maps();

#####################################################################################################
# Step 40
# Count the incoming feature classes
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("1) Count the incoming records\n");
arcpy.env.overwriteOutput = True;

sys.stdout.write("  Counting NHDArea...");
arcpy.MakeTableView_management(input_fgdb + '\\NHDSnapshot\\NHDArea',"myTableView")
nhdarea_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(nhdarea_count) + "\n");

sys.stdout.write("  Counting NHDFlowline_Network...")
arcpy.MakeTableView_management(input_fgdb + '\\NHDSnapshot\\NHDFlowline_Network',"myTableView")
nhdflowline_network_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(nhdflowline_network_count) + "\n");

sys.stdout.write("  Counting NHDFlowline_NonNetwork...");
arcpy.MakeTableView_management(input_fgdb + '\\NHDSnapshot\\NHDFlowline_NonNetwork',"myTableView")
nhdflowline_nonnetwork_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(nhdflowline_nonnetwork_count) + "\n");

sys.stdout.write("  Counting NHDLine...");
arcpy.MakeTableView_management(input_fgdb + '\\NHDSnapshot\\NHDLine',"myTableView")
nhdline_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(nhdline_count) + "\n");

sys.stdout.write("  Counting NHDPoint...");
arcpy.MakeTableView_management(input_fgdb + '\\NHDSnapshot\\NHDPoint',"myTableView")
nhdpoint_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(nhdpoint_count) + "\n");

sys.stdout.write("  Counting NHDWaterbody...");
arcpy.MakeTableView_management(input_fgdb + '\\NHDSnapshot\\NHDWaterbody',"myTableView")
nhdwaterbody_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(nhdwaterbody_count) + "\n");

sys.stdout.write("  Counting CatchmentSP...");
arcpy.MakeTableView_management(input_fgdb + '\\NHDPlusCatchment\\CatchmentSP',"myTableView")
catchmentsp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(catchmentsp_count) + "\n");

sys.stdout.write("  Counting HUC12...");
arcpy.MakeTableView_management(input_fgdb + '\\WBDSnapshot\\HUC12',"myTableView")
huc12_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
sys.stdout.write(str(huc12_count) + "\n");

#####################################################################################################
# Step 50
# Copy feature classes from source to scratch removing Z and M values and altering fieldnames
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("2) Copy to scratch, kill M/Z, alter field names, remove feature datsets\n");

sys.stdout.write("  Copying NHDArea...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDSnapshot\\NHDArea'
   ,target_nm    = "NHDArea"
   ,str_sql      = None
   ,map_array    = dzmap.nhdarea()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDFlowline_Network...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDSnapshot\\NHDFlowline_Network'
   ,target_nm    = "NHDFlowline_Network"
   ,str_sql      = None
   ,map_array    = dzmap.nhdflowline_network()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDFlowline_NonNetwork...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDSnapshot\\NHDFlowline_NonNetwork'
   ,target_nm    = "NHDFlowline_NonNetwork"
   ,str_sql      = None
   ,map_array    = dzmap.nhdflowline_nonnetwork()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDLine...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDSnapshot\\NHDLine'
   ,target_nm    = "NHDLine"
   ,str_sql      = None
   ,map_array    = dzmap.nhdline()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDPoint...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDSnapshot\\NHDPoint'
   ,target_nm    = "NHDPoint"
   ,str_sql      = None
   ,map_array    = dzmap.nhdpoint()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDWaterbody...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDSnapshot\\NHDWaterbody'
   ,target_nm    = "NHDWaterbody"
   ,str_sql      = None
   ,map_array    = dzmap.nhdwaterbody()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying CatchmentSP...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\NHDPlusCatchment\\CatchmentSP'
   ,target_nm    = "CatchmentSP"
   ,str_sql      = None
   ,map_array    = dzmap.catchment()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying HUC12...");
dzgp.export_fc(
    source_fc    = input_fgdb + '\\WBDSnapshot\\HUC12'
   ,target_nm    = "HUC12"
   ,str_sql      = None
   ,map_array    = dzmap.huc12()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

#####################################################################################################
# Step 60
# Project the data to Web Mercator
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("3) Projecting to Web Mercator \n");

sys.stdout.write("  Projecting NHDArea...");
dzgp.project_fc_3857(
    target_nm    = "NHDArea"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Projecting NHDFlowline_Network...");
dzgp.project_fc_3857(
    target_nm    = "NHDFlowline_Network"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Projecting NHDFlowline_NonNetwork...");
dzgp.project_fc_3857(
    target_nm    = "NHDFlowline_NonNetwork"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Projecting NHDPoint...");
dzgp.project_fc_3857(
    target_nm    = "NHDPoint"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Projecting NHDWaterbody...");
dzgp.project_fc_3857(
    target_nm    = "NHDWaterbody"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Projecting CatchmentSP...");
dzgp.project_fc_3857(
    target_nm    = "CatchmentSP"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Projecting HUC12...");
dzgp.project_fc_3857(
    target_nm    = "HUC12"
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

#####################################################################################################
# Step 70
# Add Indexes 
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("4) Adding indexes \n");

sys.stdout.write("  Indexing NHDArea...");
dzgp.index_tb(
    target_nm    = "NHDArea"
   ,map_array    = dzmap.nhdarea()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Indexing NHDFlowline_Network...");
dzgp.index_tb(
    target_nm    = "NHDFlowline_Network"
   ,map_array    = dzmap.nhdflowline_network()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Indexing NHDFlowline_NonNetwork...");
dzgp.index_tb(
    target_nm    = "NHDFlowline_NonNetwork"
   ,map_array    = dzmap.nhdflowline_nonnetwork()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Indexing NHDPoint...");
dzgp.index_tb(
    target_nm    = "NHDPoint"
   ,map_array    = dzmap.nhdpoint()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Indexing NHDWaterbody...");
dzgp.index_tb(
    target_nm    = "NHDWaterbody"
   ,map_array    = dzmap.nhdwaterbody()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Indexing CatchmentSP...");
dzgp.index_tb(
    target_nm    = "CatchmentSP"
   ,map_array    = dzmap.catchment()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Indexing HUC12...");
dzgp.index_tb(
    target_nm    = "HUC12"
   ,map_array    = dzmap.huc12()
   ,target_ws    = scratch_fgdb
);
sys.stdout.write("DONE\n");

#####################################################################################################
# Step 80
# Copy to final fgdb
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("5) Copy into final fgdb \n");

sys.stdout.write("  Copying NHDArea...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\NHDArea'
   ,target_nm    = "NHDArea"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDFlowline_Network...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\NHDFlowline_Network'
   ,target_nm    = "NHDFlowline_Network"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDFlowline_NonNetwork...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\NHDFlowline_NonNetwork'
   ,target_nm    = "NHDFlowline_NonNetwork"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDLine...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\NHDLine'
   ,target_nm    = "NHDLine"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDPoint...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\NHDPoint'
   ,target_nm    = "NHDPoint"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying NHDWaterbody...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\NHDWaterbody'
   ,target_nm    = "NHDWaterbody"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying CatchmentSP...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\CatchmentSP'
   ,target_nm    = "CatchmentSP"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

sys.stdout.write("  Copying HUC12...");
dzgp.export_fc(
    source_fc    = scratch_fgdb + '\\HUC12'
   ,target_nm    = "HUC12"
   ,str_sql      = None
   ,map_array    = None
   ,target_ws    = output_fgdb
);
sys.stdout.write("DONE\n");

#####################################################################################################
# Step 90
# Check the final counts match
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("6) Check the final counts match\n");
arcpy.env.overwriteOutput = True;

sys.stdout.write("  Counting NHDArea...");
arcpy.MakeTableView_management(output_fgdb + '\\NHDArea',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == nhdarea_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting NHDFlowline_Network...")
arcpy.MakeTableView_management(output_fgdb + '\\NHDFlowline_Network',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == nhdflowline_network_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting NHDFlowline_NonNetwork...");
arcpy.MakeTableView_management(output_fgdb + '\\NHDFlowline_NonNetwork',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == nhdflowline_nonnetwork_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting NHDLine...");
arcpy.MakeTableView_management(output_fgdb + '\\NHDLine',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == nhdline_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting NHDPoint...");
arcpy.MakeTableView_management(output_fgdb + '\\NHDPoint',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == nhdpoint_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting NHDWaterbody...");
arcpy.MakeTableView_management(output_fgdb + '\\NHDWaterbody',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == nhdwaterbody_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting CatchmentSP...");
arcpy.MakeTableView_management(output_fgdb + '\\CatchmentSP',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == catchmentsp_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

sys.stdout.write("  Counting HUC12...");
arcpy.MakeTableView_management(output_fgdb + '\\HUC12',"myTableView")
temp_count = int(arcpy.GetCount_management("myTableView").getOutput(0))
if temp_count == huc12_count:
   sys.stdout.write("GOOD\n");
else:
   sys.stdout.write("MISMATCH!\n"); 

#####################################################################################################
# Step 100
# Cleaning up
#####################################################################################################
sys.stdout.write("\n");
sys.stdout.write("7) Clean up scratch space \n");
sys.stdout.write("  Scrubbing...");
arcpy.Delete_management(scratch_fgdb);
if os.path.exists(scratch_fgdb):
   arcpy.Delete_management(scratch_fgdb);
sys.stdout.write("DONE\n");

def timer(start,end):
   hours, rem = divmod(end-start, 3600);
   minutes, seconds = divmod(rem, 60);
   return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds);

sys.stdout.write("\n");   
sys.stdout.write("Elapsed Time: " + timer(start_time,time.time()) + "\n");
sys.stdout.write("\n");

