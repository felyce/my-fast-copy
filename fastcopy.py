#!/usr/bin/python
# -*- coding: utf-8; mode: python-mode; -*-
# Last Change:2009/08/09 01:39:54.

import os, os.path

class fc_file(object):

    buf_size = 1024*1024

    def __init__(self, _name, _target):
        self.name = _name
        self.size = os.path.getsize( _name )
        self.bin = None
        self.abs_name = os.path.abspath(_name)
        self.basename = os.path.basename(_name)
        self.target_path = _target
        self.isOK = False

        self.__on_init()

    def __on_init(self):
        try:
            fp = open(self.name, 'rb', self.buf_size)
        except Exception, e:
            print e
        else:
            self.isOK = True
        finally:
            fp.close()

        

class FastCopy(object):

    BUF_SIZE = 1024*1024*100
    READ_BUFFER = 1024*1024*60

    def __init__(self, path, arg):
        self.file_list = []
        self.all_file_size = 0
        self.target_path = unicode(path).encode('utf-8')
        self.tooBigFile_list = []
        self.file_bin = {}

        self.__on_init(arg)


    def __on_init(self, _arg):
        for file in _arg:
            if os.path.isdir(file):
                continue

            self.file_list.append( os.path.abspath( file ) )


    def __regfile(self):
        print "Reading files.... size(%d)" % len(self.file_list)
        for file in self.file_list:
            size = os.path.getsize( file )
            basename = os.path.basename( file )

            if self.BUF_SIZE < size:
                self.tooBigFile_list.append( basename )
                self.file_list.remove( file )
                continue

            if self.BUF_SIZE < size + self.all_file_size:
                continue

            fp = open( file, 'rb' )
            try:
                self.file_bin[ basename ] = fp.read()
            except Exception, e:
                print 'Not %s is copy.' % file
                print e
                continue
            else:
                self.all_file_size += size
            finally:
                self.file_list.remove( file )
                fp.close()


    def __copy(self):
        print "Writing files... size(%d)" % len(self.file_bin)
        while self.file_bin:
            basename, binary = self.file_bin.popitem()
            new_path = os.path.join( self.target_path, basename )

            fp = open(new_path, 'w')
            try:
                fp.write(binary)
            except Exceptino, e:
                print e
                continue
                if os.exists(new_path):
                    os.remove(new_path)
            finally:
                fp.close()

        self.all_file_size = 0
                
    def __tooBigFileCopy(self):
        print "coping BIGFILE...size(%d)" % len(self.tooBigFile_list)
        for bigfile in self.tooBigFile_list:
            new_path = os.path.join( self.target_path, bigfile )
            
            rp = open( bigfile, 'rb' )
            wp = open( new_path, 'wb' )

            try:
                buff = rp.read(self.READ_BUFFER)

                while buff:
                    wp.write(buff)
                    buff = rp.read(self.READ_BUFFER)

            except Exception, e:
                print e
                if os.exists(new_path):
                    os.remove(new_path)
            finally:
                rp.close()
                wp.close()

    def run(self):
        while self.file_list:
            self.__regfile()
            self.__copy()
            
        self.__tooBigFileCopy()

        
def main():
    import sys
    import optparse

    usage = "usage: %prog [option] -t dir file1, file2, ..."
    parser = optparse.OptionParser(usage)
    parser.add_option('-d', '--directory',
                        action = "store",
                        dest = "target",
                        help = "to Copy Directory.")
    
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1 or not args or not options.target:
        parser.print_help()
        sys.exit(1)
    
    fc = FastCopy(options.target, args)
    fc.run()

if __name__ == '__main__':
	main()

