# :coding: utf-8

import os
import sys
import urllib
import shutil
import datetime

sys.path.append("/westworld/inhouse/tool/rez-packages/XlsxWriter/1.2.3/platform-linux/arch-x86_64/lib/python2.7/site-packages")
import xlsxwriter

import shotgun_api3

SG = shotgun_api3.Shotgun(
    'https://west.shotgunstudio.com',
    'ami_main',
    'etlehurtsogGstfjxzxz2?lzd'
)

PYTHON3 = sys.version_info[0] == 3
if not PYTHON3:
    reload(sys)
    sys.setdefaultencoding("utf-8")


class CreateXlsxFile( ):
    def __init__( self, sa, input_path ):
        self.input_path   = str(input_path)
        self.project      = sa.params['project_name']
        self.project_id   = sa.params['project_id']
        self.entity_type  = sa.params['entity_type']
        self.selected_id  = sa.params['selected_ids'].split(',')
        self.col_name     = sa.params['column_display_names']
        self.col_code     = sa.params['cols']
        self.thumb_folder = self.input_path + os.path.sep + '.thumbnail'
        now               = datetime.datetime.now()
        self.xlsx_path    = self.input_path + os.path.sep + sa.params['entity_type'] +'_' + now.strftime('%Y%m%d_%H%M%S') + '.xlsx'
        self.create_xlsx()

    def create_xlsx( self ):
        ''' find thumbnail col '''
        thumb_col  = self.col_name.index('Thumbnail')

        ''' write xlsx file '''
        with xlsxwriter.Workbook( self.xlsx_path ) as workbook:
            worksheet = workbook.add_worksheet( self.entity_type )  
            ''' header format'''    
            header  = workbook.add_format( {'bold' :1 } )
            header.set_align( 'center' )
            header.set_align( 'vcenter' )
            header.set_bg_color( 'green' )
            header.set_font_size( 14 )

            ''' write xlsx header '''
            for col_idx, col in enumerate( self.col_name ):
                worksheet.write( 0, col_idx, col, header )
                # alph = string.uppercase[i]
                if col_idx == thumb_col:
                    worksheet.set_column( col_idx, col_idx, 70 )
                    # worksheet.set_column( '{0}:{0}'.format( alph ), 25 )
                else:
                    worksheet.set_column( col_idx, col_idx, 25 )
                    # worksheet.set_column( '{0}:{0}'.format( alph ), 25 )
            ''' get field info & download thumbnails '''
            field_info = self.get_field_info()
            ''' write field data '''
            for row_idx, row in enumerate( self.selected_id ):
                for col_idx, col in enumerate( self.col_code ):
                    info = field_info[row_idx][col]
                    if col == 'image':
                        thumb_img = os.path.join( self.thumb_folder, row + '.jpg' )
                        if os.path.exists( thumb_img ):
                            worksheet.insert_image( row_idx + 1, col_idx, thumb_img )
                            worksheet.set_row( row_idx + 1, 200)
                    else:
                        if info and PYTHON3 :
                                if isinstance( info, str ):
                                    worksheet.write( row_idx + 1 , col_idx, info )
                                elif isinstance( info, datetime.datetime ):
                                    time_info = info.strftime( "%Y/%m/%d, %H:%M:%S" )
                                    worksheet.write( row_idx + 1 , col_idx, time_info )
                                elif isinstance( info, int ):
                                    worksheet.write( row_idx + 1 , col_idx, str(info) )
                                elif 'name' in info:
                                    worksheet.write( row_idx + 1 , col_idx, info['name'] )
                        elif info and not PYTHON3:
                                if isinstance( info, basestring ):
                                    worksheet.write( row_idx + 1 , col_idx, info )
                                elif isinstance( info, datetime.datetime ):
                                    time_info = info.strftime( "%Y/%m/%d, %H:%M:%S" )
                                    worksheet.write( row_idx + 1 , col_idx, time_info )
                                elif isinstance( info, int ):
                                    worksheet.write( row_idx + 1 , col_idx, str(info) )
                                elif 'name' in info:
                                    worksheet.write( row_idx + 1 , col_idx, info['name'].encode("utf-8") )

    def get_field_info( self ):
        field_info = []
        if not os.path.exists( self.thumb_folder ):
            os.makedirs( self.thumb_folder )
        for id in self.selected_id :
            shotgrid_info = SG.find_one( self.entity_type, [ ['project.Project.name', 'is', self.project ], [ 'id', 'is', int(id) ]] , self.col_code ) 
            print('#'*50)         
            print( id )
            print( shotgrid_info )
            print( self.col_code )
            print('#'*50)         
            if shotgrid_info['image']:
                thumb_img = os.path.join( self.thumb_folder, id + '.jpg' )
                urllib.urlretrieve( shotgrid_info['image'], thumb_img )

            # Shot_Colorspace
            # Query 형태의 Entity는 SG에서 기본적으로 제공해주지 않음
            # Published File <-> Link의 정보를 이용해서 가져오기
            if 'sg_shot_colorspace' in self.col_code and 'sg_published_files' in self.col_code :
                for pub_file in shotgrid_info['sg_published_files']:
                    pub_file_info = SG.find_one( 'PublishedFile', [ ['id', 'is', int( pub_file['id'] )]] , [ 'sg_colorspace', 'published_file_type' ])
                    if pub_file_info['published_file_type']['name'] == 'Plate' :
                        shotgrid_info['sg_shot_colorspace'] = pub_file_info['sg_colorspace']

            # Attachment entity
            # Query 형태의 Entity는 SG에서 기본적으로 제공해주지 않음
            # 연결 된 쿼리에서 파악 후 정보를 넣어줌
            if self.entity_type == 'Attachment':
                if 'sg_shot_code' not in self.col_code:
                    message_box('Error', u'"Shot Code" 필드 정보를 추가해주세요.')

                elif 'sg_shot_code' in self.col_code:   
                    note_filters = [
                        ['project', 'is', {'type': 'Project', 'id': int(self.project_id), 'name': self.project}],
                        ['id', 'is', shotgrid_info['attachment_links'][0]['id']]
                    ]

                    note_fields = ['note_links', 'content']
                    
                    note_info = SG.find_one('Note', note_filters, note_fields)

                    if note_info is not None:
                        if 'sg_shot_code' in self.col_code:
                            shotgrid_info['sg_shot_code'] = [link['name'] for link in note_info['note_links'] if link['type'] == 'Shot'][0]
                        
                        if 'sg_version_name' in self.col_code:
                            shotgrid_info['sg_version_name'] = [link['name'] for link in note_info['note_links'] if link['type'] == 'Version'][0]

                        if 'sg_note_for_file' in self.col_code:
                            shotgrid_info['sg_note_for_file'] = note_info['content']

                        version_filters = [
                            ['project', 'is', {'type': 'Project', 'id': int(self.project_id), 'name': self.project}],
                            ['id', 'is', [link['id'] for link in note_info['note_links'] if link['type'] == 'Version']]
                        ]

                        version_fields = ['sg_status_list', 'user']

                        version_info = SG.find_one('Version', version_filters, version_fields)

                        if 'sg_artist' in self.col_code:
                            shotgrid_info['sg_artist'] = version_info['user']['name']
                        
                        if 'sg_version_status' in self.col_code:
                            shotgrid_info['sg_version_status'] = version_info['sg_status_list']
                    
                    else:
                        message_box('Info', u'"Note"가 정보가 필요합니다.')

            # 리스트 형태 -> 텍스트 형태로 대체
            for col in self.col_code:
                if shotgrid_info[col] and isinstance( shotgrid_info[col], list ):
                    tmp_list = ""
                    print('-'*50)
                    print(self.col_code)
                    for data in shotgrid_info[col]:
                        tmp_list += '\n'
                        tmp_list += (data['name'])
                        print( data['name'])
                    shotgrid_info[col] = tmp_list
                    print('-'*50)

            # 위의 리스트 -> 텍스트형식 변환으로 인해 필요 없어짐
            # # entity_type이 Attachment인 경우
            # if self.entity_type == 'Attachment' and shotgrid_info['attachment_links']:
            #     if shotgrid_info['attachment_links'][0]['type'] == 'Note':
            #         note_id   = shotgrid_info['attachment_links'][0]['id']
            #         note_info = SG.find_one( 'Note', [[ 'project.Project.name', 'is', self.project ],[ 'id', 'is', int(note_id) ]], ['note_links', 'content'] ) 
            #         shotgrid_info['sg_note_for_file'] = note_info['content'] 
            #         print('-'*40)
            #         print(note_info)
            #         print('-'*40)
            #         # Shot Code, Version Name, Version Status, Note for File, Artist
            #         # sg_shot_code, sg_version_name, sg_version_status, sg_note_for_file, sg_artist
            #         # shot        , version        , version          , note            , version
            #         for info in note_info['note_links']:
            #             if info['type'] == 'Version' :
            #                 version_info = SG.find_one( 'Version', [ ['project.Project.name', 'is', self.project ], [ 'code', 'is', info['name'] ]], [ 'user', 'sg_status_list' ]  ) 
            #                 shotgrid_info['sg_version_name'] = info['name']
            #                 shotgrid_info['sg_version_status'] = version_info['sg_status_list']
            #                 shotgrid_info['sg_artist'] = version_info['user']
            #             elif info['type'] == 'Shot' :
            #                 shotgrid_info['sg_shot_code'] = info['name']
            #     # elif shotgrid_info['attachment_links'][0]['type'] == 'Shot'\
            #     #         shotgrid_info['attachment_links'][0]['type'] == 'Version':
            #     shotgrid_info['attachment_links'] = shotgrid_info['attachment_links'][0]['name']
            field_info.append( shotgrid_info )   
        return field_info

    def del_thumbnail( self ):
        shutil.rmtree( self.thumb_folder )

def message_box(message_type, message ):
    from PyQt4.QtGui import QMessageBox
    if message_type == 'Error':
        QMessageBox.critical( None, message_type , message )

    elif message_type == 'Info':
        QMessageBox.information( None, message_type , message )