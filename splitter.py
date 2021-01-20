##############################################################
#splitter.py Splitt a File into less large file and undo that
#
#Author: hlvs-apps
#Licensed under Apache 2.0
##############################################################

import os
import glob
import argparse
import math
import textwrap


verbose=False

def split(src,out_dir,bytes_per_file,format,chars_per_step):
    printverbose('Starting Split Mode')
    string_for_out=''
    n_now=0
    file_number_now=0
    if(os.path.isfile(src)):
        printverbose(src+' is a File')
    else:
        print(src+' is not a File. Aborting.')
        return
    if(os.path.isdir(out_dir)):
        printverbose(out_dir+' is a Directory')
    else:
        print(out_dir+' is not a Directory. Aborting.')
        return
    #Get File size of Source, to Calculate Digits
    f_size=os.path.getsize(src)
    printverbose('File Size: '+str(f_size))
    aprox_files=math.ceil(f_size/bytes_per_file)
    printverbose('That means approx. '+str(aprox_files)+ ' Files.')
    diggits=math.ceil(len(str(aprox_files)))
    printverbose('That means we need '+str(diggits)+' Diggits.')
    file = open(src, 'r')
    try:
        while 1: 
            ch = file.read(chars_per_step)           
            if not ch:  
                break
            string_for_out+=ch
            n_now+=chars_per_step
            if n_now>=bytes_per_file:
                out_name=os.path.join(out_dir, str(file_number_now).zfill(diggits) + '.' + format)
                with open(out_name, 'w') as output:
                    printverbose('Writing File '+out_name)
                    output.write(string_for_out)
                string_for_out=''
                file_number_now+=1
                n_now=0
        if n_now!=0:
            out_name=os.path.join(out_dir, str(file_number_now).zfill(diggits) + '.' + format)
            with open(out_name, 'w') as output:
                printverbose('Writing File '+out_name)
                output.write(string_for_out)
    finally:
        file.close()
def printverbose(text):
    if(verbose==True):
        print(text)

def join_files_to_big_file(src_dir,out_file,format,max_size):
    printverbose("Start Joining")
    if(os.path.isdir(src_dir)):
        printverbose(src_dir+' is a Directory')
    else:
        print(src_dir+' is not a Directory. Aborting.')
        return
    with open(out_file,'w') as f:
        for filename in glob.glob(os.path.join(src_dir, '*.' + format)):
            current_size = f.tell()
            if (max_size!=-1):
                if(current_size>=max_size):
                    printverbose('current_size({})>=max_size({})  Aborting.'.format(current_size,max_size))
                    break
            with open(filename,'r') as actual_apend:
                printverbose("Add "+str(filename))
                f.write(actual_apend.read())

def main(src,out,join,format,size,max_size):
    if(join==True):
        join_files_to_big_file(src,out,format,max_size)
    else:
        split(src,out,size,format,math.ceil(size/100))
if __name__ == '__main__':
    nameofscrip=os.path.basename(__file__)
    parser = argparse.ArgumentParser(prog=nameofscrip,
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\
Example Usage:
  Splitting: python {} File.txt ./result/ -m s
  Joining: python {} ./result/ File2.txt -m j

WARNING: This Code only works with Files with one Character per Byte.
'''.format(nameofscrip,nameofscrip)))
    parser.add_argument('src', help='Source file or directory', type=str)
    parser.add_argument('out', help='Output file or directory', type=str)
    parser.add_argument('-m','--mode', dest='mode', help='"-m s" for splitting files, "-m j" for joining files, default is "-m s"', choices=['s','j'])
    parser.add_argument('-s','--size', dest='filesize', help='File Output Size for mode Split in Bytes, Default is 52428800 (50 MB)', type=int, default=52428800)
    parser.add_argument('-f','--format', dest='format', help='File Format for In and Output files. Example Usage: "-f txt" for .txt files. txt is default format',default='txt', type=str)
    parser.add_argument('--max-size', dest='maxsize', help='File Output Size for mode Join Mode in Bytes, Default is -1 (Original Size)',type=int, default=-1)
    parser.add_argument('-v','--verbose', dest='verbose', help='Show Verbose Information', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()
    verbose=args.verbose
    printverbose("Verbose Information is enabled")
    printverbose("Mode: "+str(args.mode))
    printverbose("Source: "+args.src)
    printverbose("Size: "+str(args.filesize))
    printverbose("Output: "+args.out)
    printverbose("Format: "+args.format)
    printverbose("Max Size: "+str(args.maxsize))
    if args.mode=='j':
        main(args.src,args.out,True,args.format,args.filesize,args.maxsize)
    elif args.mode=='s':
        main(args.src,args.out,False,args.format,args.filesize,args.maxsize)
    else:
        printverbose ("Warning: You didnt't set a mode. "+'Mode "-m s" is used instad. to learn more, call "python {} -h'.format(nameofscrip))
        main(args.src,args.out,False,args.format,args.filesize,args.maxsize)
