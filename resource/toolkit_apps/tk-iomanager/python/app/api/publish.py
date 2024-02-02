
import os
import subprocess
import sgtk
from sgtk.platform.qt import QtCore, QtGui
#import tractor.api.author as author


class Publish:
    
    def __init__(self,model,row,parent=None):
        
        self.model = model
        self.row = row

        self._app = sgtk.platform.current_bundle()
        self._sg = self._app.shotgun
        self.project = self._app.context.project
        self.shot_name = self._get_model_data(2)
        self.seq_type = self._get_model_data(3)
        self.user = self._app.context.user

        self.create_seq()
        self.create_shot()
        self._get_version()
        self.create_copy_job()
        self.create_version()
        if self.seq_type == "org":
            self.update_shot_info()

        self.publish_to_shotgun()

        
    @property
    def seq_name(self):
        temp = self.shot_name.split("_")
        if len(temp) == 2:
            return temp[0]
        else:
            return temp[0]
    

    
    

    
    def create_seq(self):
        print "create seq"
        
        key = [
                ['project','is',self.project],
                ['code','is',self.seq_name]
                ]
        
        seq_ent = self._sg.find_one('Sequence',key)
        if seq_ent:
            self.seq_ent = seq_ent
            return
        desc = {
                'project' :self.project,
                'code' : self.seq_name
                }
        self.seq_ent = self._sg.create("Sequence",desc)
        return 


    def create_shot(self):
        print "create Shot"

        key = [
                ['project','is',self.project],
                ['sg_sequence','is',self.seq_ent],
                ['code','is',self.shot_name]
                ]

        shot_ent = self._sg.find_one('Shot',key)
        if shot_ent:
            self.shot_ent = shot_ent
            return
        desc = {
                'project' : self.project,
                'sg_sequence': self.seq_ent,
                'code' : self.shot_name
                }
        self.shot_ent = self._sg.create("Shot",desc)
        return 
        
    def update_shot_info(self):
        desc = {
                "sg_cut_in" : 1001,
                "sg_cut_out" : 1000+len(self.copy_file_list),
                "sg_cut_duration": len(self.copy_file_list),
                "sg_timecode_in": self._get_model_data(12),
                "sg_timecode_out": self._get_model_data(13),

               }

        self._sg.update("Shot",self.shot_ent['id'],desc)
    

    def create_copy_job(self):

        
        scan_path = self._get_model_data(4)
        file_ext = self._get_model_data(7)
        
        cmd = ["/bin/mkdir","-p"]
        
        cmd.append(self.plate_path)
        if not os.path.exists(self.plate_path):
            print "create plate dir"
            subprocess.call(cmd)

        for index in range(0,len(self.copy_file_list)):
            cmd = ["/bin/cp","-fv"]
            cmd.append(os.path.join(scan_path,self.copy_file_list[index]))
            cmd.append(os.path.join(self.plate_path,self.plate_file_name+"."+str(1000+index+1)+"."+file_ext))
            # print cmd
            subprocess.call(cmd)

    def create_version(self):
        
        file_ext = self._get_model_data(7)
        
        mov_path = os.path.join(self._app.sgtk.project_path,'seq',
                                self.seq_name,
                                self.shot_name,"plate",
                                self.plate_file_name+".mov")
        
        mov_name = self.plate_file_name+".mov"
        cmd = []
        cmd.append("ffmpeg")
        cmd.append('-y')
        cmd.append("-start_number")
        cmd.append("1001")
        cmd.append('-i')
        cmd.append(os.path.join(self.plate_path,self.plate_file_name+".%04d."+file_ext))
        cmd.append('-vcodec')
        cmd.append('libx264')
        cmd.append('-pix_fmt')
        cmd.append('yuv420p')
        cmd.append(mov_path)

        subprocess.call(cmd)
        # print 'create mov file'

        key = [
                ['entity','is',self.shot_ent],
                ['code','is',mov_name]
                ]
        if self._sg.find_one("Version",key):
            self.version_ent = self._sg.find_one("Version",key)
            return
        desc = {
                "project" : self.project,
                "code" : mov_name,
                "sg_status_list" : "rev",
                'entity' : self.shot_ent,
                "sg_path_to_movie" : mov_path,
               # "sg_version_type" : self.seq_type,
                }
        self.version_ent = self._sg.create("Version",desc)
        self._sg.upload('Version', self.version_ent['id'], mov_path, 'sg_uploaded_movie')
    
    @property
    def plate_file_name(self):
        temp = self.shot_name + "_"+self.seq_type+"_v%02d"%self.version
        return temp
    
    @property
    def copy_file_list(self):
        
        file_list = []

        start_index = self._get_model_data(14)
        end_index = self._get_model_data(15)
        pad = self._get_model_data(6)
        file_name  = self._get_model_data(5)
        file_ext = self._get_model_data(7)
        
        for i in range(int(start_index),int(end_index)+1):
            copy_file = file_name + "."+pad%i+"."+file_ext
            file_list.append(copy_file)
        
        return file_list




    
    def _get_model_data(self,col):

        index = self.model.createIndex(self.row,col)
        return self.model.data(index,QtCore.Qt.DisplayRole )

    def _get_version(self):
        key = [
                ['project','is',self.project],
                ['entity','is',self.shot_ent],
                ["published_file_type","is",self.published_file_type],
                ['name','is',self.version_file_name]
               ]
        published_ents = self._sg.find("PublishedFile",key,['version_number'])
        print published_ents
        if not published_ents:
            self.version = 1
        else:
            self.version = published_ents[-1]['version_number'] + 1
            
    
    @property
    def file_ext(self):
        return self._get_model_data(7)

    @property
    def published_file_type(self):
        if self.seq_type == "org":
            key  = [['code','is','Plate']]
            return self._sg.find_one("PublishedFileType",key,['id'])
        else:
            key  = [['code','is','Source']]
            return self._sg.find_one("PublishedFileType",key,['id'])

    @property
    def plate_path(self):
        
        temp = os.path.join(self._app.sgtk.project_path,'seq',self.seq_name,
               self.shot_name,"plate",self.seq_type,"v%03d"%self.version)
        return temp

    @property
    def plate_jpg_path(self):

        temp = os.path.join(self._app.sgtk.project_path,'seq',self.seq_name,
               self.shot_name,"plate",self.seq_type,"v%03d_jpg"%self.version)
        return temp

    @property
    def plate_file_name(self):
        temp = self.shot_name + "_"+self.seq_type+"_v%02d"%self.version
        return temp
    @property
    def version_file_name(self):
        temp = self.shot_name + "_"+self.seq_type
        return temp
    

    def publish_to_shotgun(self):
        
        context = sgtk.Context(self._app.tank,project = self.project,
                               entity = self.shot_ent,
                               step = None,
                               task = None,
                               user = self.user)

        file_ext = self._get_model_data(7)

        if self.seq_type == "org":
            published_type = "Plate"
        else:
            published_type = "Source"
            

        publish_data = {
            "tk": self._app.tank,
            "context": context,
            "path": os.path.join(self.plate_path,self.plate_file_name+".%04d."+file_ext),
            "name": self.version_file_name,
            "created_by": self.user,
            "version_number": self.version,
            #"thumbnail_path": item.get_thumbnail_as_path(),
            "published_file_type": published_type,
            #"dependency_paths": publish_dependencies
        }

        sgtk.util.register_publish(**publish_data)
        
#        QtGui.QMessageBox.information( None, 'Finished' , 'Finished to Publish' )

