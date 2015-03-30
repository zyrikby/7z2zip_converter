import os, shutil, random
import zipfile, subprocess
from multiprocessing import JoinableQueue, Pool, Process


class Converter_7z2zip():
    SHOW_EXTRACT_COMMAND_OUTPUT = False
    
    def _create_tmp_unpack_folder(self, file_path):
        head, tail = os.path.split(file_path)
        tmp_dir = os.path.join(head, "unpack-%d" % (random.randint(0, 10000)))
        os.makedirs(tmp_dir)
        return tmp_dir
    
    
    def __init__(self, input_filepath, output_filepath, threads_num = 4):
        try:
            import zlib
            self._compression = zipfile.ZIP_DEFLATED
        except:
            while True:
                user_input = raw_input('Module zlib to compress files is not installed. Proceed conversion without compressing (y/n)?: ')
                if user_input.capitalize() == 'YES' or user_input.capitalize() == 'Y':
                    self._compression = zipfile.ZIP_STORED
                    break
                elif user_input.capitalize() == 'NO' or user_input.capitalize() == 'N':
                    print "Exiting!!!"
                    exit(1)
        
        self.input_filepath = os.path.abspath(input_filepath)
        self.output_filepath = os.path.abspath(output_filepath)
        
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)
        
        self._threads_num = threads_num
        
    
    def convert(self):
        tmp_unpack_path = self._create_tmp_unpack_folder(self.output_filepath)
        
        header, files_attrs = self._get_archive_metadata()
        file_list = [attrs["Path"] for attrs in files_attrs if attrs["Attributes"] == "....A"]
        
        files_input_queue = JoinableQueue(200)
        files_processed_queue = JoinableQueue(200)
        
        extractor_processes = Pool(self._threads_num, self._extract_files, (files_input_queue, files_processed_queue, tmp_unpack_path))
        archiver_process = Process(target=self._archive_files, args = (files_processed_queue, tmp_unpack_path))
        archiver_process.start()
        
        for archived_file in file_list:
            files_input_queue.put(archived_file)
        
        
        files_input_queue.join()
        for i in xrange(self._threads_num):
            files_input_queue.put(None)
        extractor_processes.close()
        extractor_processes.join()
        
        files_processed_queue.join()
        files_processed_queue.put(None)
        archiver_process.join()
    
        shutil.rmtree(tmp_unpack_path, True)
        
    
    
    def _get_archive_metadata(self):
        output = subprocess.check_output(['7z', 'l', '-slt', self.input_filepath])
        header = {}
        files_attrs = []
        
        lines = output.split('\n')
        
        header_begin = False
        body_begin = False
        f_attrs = {}
        for line in lines:
            if line.strip() == "--":
                header_begin = True
                continue
            elif line.strip() == '----------':
                header_begin = False
                body_begin = True
                continue
            
            if header_begin:
                if line.strip() == '':
                    continue
                attrs_list = [x.strip() for x in line.split('=')]
                header[attrs_list[0]] = attrs_list[1]
                continue
            
            
            if body_begin:
                if line.strip() == '':
                    if len(f_attrs) != 0:
                        files_attrs.append(f_attrs.copy())
                        f_attrs.clear()
                    continue
                
                f_attrs_list = [x.strip() for x in line.split('=')]
                f_attrs[f_attrs_list[0]] = f_attrs_list[1]
                continue
                 
        return header, files_attrs
    
    
    def _extract_files(self, q_in, q_res, tmp_unpack_path):
        OUTPUT = None
        if not self.SHOW_EXTRACT_COMMAND_OUTPUT:
            OUTPUT = open(os.devnull, 'w')
            
        try:
            while True:
                file_name_to_extract = q_in.get()
                if file_name_to_extract is None:
                    print "No files to extract anymore!"
                    q_in.task_done()
                    break
                ret_code = subprocess.call(['7z', 'x', '-o%s' % tmp_unpack_path, self.input_filepath, file_name_to_extract], stdout=OUTPUT)
                if ret_code == 0:
                    q_res.put(file_name_to_extract)
                    q_in.task_done()
                    print "File [%s] extracted from the archive!" % file_name_to_extract
                else:
                    print "Error while extracting file: %s" % file_name_to_extract
                    q_in.task_done()
        finally:
            if OUTPUT:
                OUTPUT.close()
                

    def _archive_files(self, q, tmp_unpack_path):
        with zipfile.ZipFile(self.output_filepath, 'a', self._compression, True) as z_file:
            file_counter = 0
            while True:
                file_counter += 1
                file_name_to_archive = q.get()
                if file_name_to_archive is None:
                    print "No files to archive anymore!"
                    q.task_done()
                    break
                file_full_path = os.path.join(tmp_unpack_path, file_name_to_archive)
                z_file.write(file_full_path, file_name_to_archive)
                os.remove(file_full_path)
                q.task_done()
                print "%dth file [%s] is added to the archive!" % (file_counter, file_name_to_archive)
