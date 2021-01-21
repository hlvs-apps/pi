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
import sys
from pathlib import Path

verbose=False
overide=False
aborted=False
def query_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def split(src,out_dir,bytes_per_file,format,chars_per_step):
    global aborted
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
    diggits=math.ceil(len(str(aprox_files-1)))
    printverbose('That means we need '+str(diggits)+' Diggits.')
    file = open(src, 'r')
    question_is_trogerd=False
    i=0
    while i < aprox_files:
        printverbose(str(i))
        printverbose("Checking: "+str(os.path.join(out_dir, str(i).zfill(diggits)+ '.' + format)))
        if Path(os.path.join(out_dir, str(i).zfill(diggits)+ '.' + format)).is_file():
            printverbose("Exists")
            if(overide==True):
                os.remove((str(os.path.join(out_dir, str(i).zfill(diggits)+ '.' + format))))
            else:
                if(query_yes_no("File {} does exist. Do you want to overide it?".format(str(os.path.join(out_dir, str(i).zfill(diggits)))))):
                    os.remove((str(os.path.join(out_dir, str(i).zfill(diggits)+ '.' + format))))
                    question_is_trogerd=True
                else:
                    print("Aborting.")
                    aborted=True
                    print("Note: you can also run {} -o to skip this questions.".format(os.path.basename(__file__)))
                    return
        i+=1
    if question_is_trogerd:
        print("Note: you can also run {} -o to skip this questions.".format(os.path.basename(__file__)))
    printverbose("Let's start")
    progressBar(0, prefix = 'Progress:', suffix = 'Complete', length = 50,total=aprox_files)
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
                progressBar(file_number_now, prefix = 'Progress:', suffix = 'Complete', length = 50,total=aprox_files)
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
def progressBar(state, total=10, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    # Progress Bar Printing Function
    percent = ("{0:." + str(decimals) + "f}").format(100 * (state / float(total)))
    filledLength = int(length * state // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
def join_files_to_big_file(src_dir,out_file,format,max_size):
    printverbose("Start Joining")
    global aborted
    if Path(out_file).is_file():
            printverbose("Exists")
            if(overide==True):
                os.remove(out_file)
            else:
                if(query_yes_no("File {} does exist. Do you want to overide it?".format(out_file))):
                    os.remove(out_file)
                    print("Note: you can also run {} -o to skip this questions.".format(os.path.basename(__file__)))
                else:
                    print("Aborting.")
                    aborted=True
                    print("Note: you can also run {} -o to skip this questions.".format(os.path.basename(__file__)))
                    return

    if(os.path.isdir(src_dir)):
        printverbose(src_dir+' is a Directory')
    else:
        print(src_dir+' is not a Directory. Aborting.')
        return
    progressBar(0, prefix = 'Progress:', suffix = 'Complete', length = 50,total=100)
    with open(out_file,'w') as f:
        list= glob.glob(os.path.join(src_dir, '*.' + format))
        lenall=len(list)
        i=1
        for filename in list:
            current_size = f.tell()
            if (max_size!=-1):
                if(current_size>=max_size):
                    printverbose('current_size({})>=max_size({})  Aborting.'.format(current_size,max_size))
                    break
            with open(filename,'r') as actual_apend:
                printverbose("Add "+str(filename))
                progressBar(i, prefix = 'Progress:', suffix = 'Complete', length = 50,total=lenall)
                f.write(actual_apend.read())
            i+=1

def main(src,out,join,format,size,max_size):
    if(join==True):
        join_files_to_big_file(src,out,format,max_size)
    else:
        split(src,out,size,format,math.ceil(size/100))
    if(aborted==False):
        progressBar(100, prefix = 'Progress:', suffix = 'Complete', length = 50,total=100)#Show 100%
        print("")
        print("")
        print("Done.")
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
    parser.add_argument('-o','--overide', dest='overide', help='Overide existing files. When set, you will not be asked if you want to overide the files', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()
    verbose=args.verbose
    overide=args.overide
    printverbose("Verbose Information is enabled")
    printverbose("Mode: "+str(args.mode))
    printverbose("Source: "+args.src)
    printverbose("Size: "+str(args.filesize))
    printverbose("Output: "+args.out)
    printverbose("Format: "+args.format)
    printverbose("Max Size: "+str(args.maxsize))
    printverbose("Overide: "+str(args.overide))
    if args.mode=='j':
        main(args.src,args.out,True,args.format,args.filesize,args.maxsize)
    elif args.mode=='s':
        main(args.src,args.out,False,args.format,args.filesize,args.maxsize)
    else:
        printverbose ("Warning: You didnt't set a mode. "+'Mode "-m s" is used instad. to learn more, call "python {} -h'.format(nameofscrip))
        main(args.src,args.out,False,args.format,args.filesize,args.maxsize)
