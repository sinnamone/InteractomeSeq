from output_message import *
import sys
import os
import datetime
import subprocess
from Bio import SeqIO


class InputCheck(object):
    def __init__(self, optparseinstance):
        # import instance with all input flag
        self.inputistance = optparseinstance
        #put all under this
        self.thread = self.inputistance.thread
        self.count = 0
        self.filelog = None
        self.cutadapt = ''
        self.cutadaptversion = ""
        self.cloneslength = self.inputistance.minclonelength
        # check for forward reads
        if self.inputistance.readforward is not None:
            self.readforward = self.inputistance.readforward
        else:
            sys.stdout.write(msg1)
            sys.exit(0)
        # check for reverse read and assign sequencing type dataset
        if self.inputistance.readreverse is not None:
            self.readreverse = self.inputistance.readreverse
            self.sequencingtype = 'Paired-End'
        else:
            self.sequencingtype = 'Single-End'
        # Check type of dataset
        if self.inputistance.readforwardtype is not None:
            self.readforwardtype = self.inputistance.readforwardtype
        else:
            sys.stdout.write(msg2)
            sys.exit(0)
        # Check type of dataset reverse
        if self.inputistance.readreverse is not None:
            if self.inputistance.readreversetype is not None:
                self.readreversetype = self.inputistance.readreversetype
            else:
                sys.stdout.write(msg3)
                sys.exit(0)
        # Check for Dataset typr
        if self.inputistance.sampletype is not None:
            self.sampletype = self.inputistance.sampletype
        else:
            sys.stdout.write(msg4)
            sys.exit(0)
        # Check primers
        if self.inputistance.primer3forward is not None:
            self.primer3forward = self.inputistance.primer3forward
        else:
            sys.stdout.write(msg5)
            sys.exit(0)
        if self.inputistance.primer5forward is not None:
            self.primer5forward = self.inputistance.primer5forward
        else:
            sys.stdout.write(msg6)
            sys.exit(0)
        if self.inputistance.readreverse is not None:
            if self.inputistance.primer3reverse is not None:
                self.primer3reverse = self.inputistance.primer3reverse
            else:
                sys.stdout.write(msg7)
                sys.exit(0)
        if self.inputistance.readreverse is not None:
            if self.inputistance.primer5reverse is not None:
                self.primer5reverse = self.inputistance.primer5reverse
            else:
                sys.stdout.write(msg8)
                sys.exit(0)
        # check output folder
        if self.inputistance.outputfolder is not None:
            if self.inputistance.outputfolder.endswith('/') is True:
                self.outputfolder = self.inputistance.outputfolder
            else:
                self.outputfolder = self.inputistance.outputfolder + '/'
        else:
            sys.stdout.write(msg9)
            sys.exit(0)
        # check output id
        if self.inputistance.outputid is not None:
            self.outputid = self.inputistance.outputid
        else:
            sys.stdout.write(msg10)
            sys.exit(0)
        # check fasta sequence
        if self.inputistance.fastasequence is not None:
            self.fastasequence = self.inputistance.fastasequence
        else:
            sys.stdout.write(msg11)
            sys.exit(0)
        # check annotation
        if self.inputistance.annotation is not None:
            self.annotation = self.inputistance.annotation
        else:
            sys.stdout.write(msg12)
            sys.exit(0)
        self.out = self.outputfolder+self.outputid
        self.awk = None
        self.pick_otus = None
        self.pick_rep_set = None
        self.samtools = None

    def logfilecreation(self):
        if os.access(self.outputfolder, os.W_OK) is True:
            self.filelog = open(self.outputfolder+self.outputid+".log", "w")
            self.filelog.close()
            return self.outputfolder+self.outputid+".log"
        else:
            sys.stdout.write(msg13)
            sys.exit(0)

    def cutadaptchech(self):
        try:
            self.cutadapt = subprocess.check_output(['which', 'cutadapt']).split('\n')[0]
        except subprocess.CalledProcessError:
            self.filelog.write(msg32)
            sys.exit(0)
        else:
            return self.cutadapt

    def pickotuscheck(self):
        try:
            self.pick_otus = subprocess.check_output(['which', 'pick_otus.py']).split('\n')[0]
        except subprocess.CalledProcessError:
            self.filelog.write(msg67)
            sys.exit(0)
        else:
            return self.pick_otus

    def pickrepseqcheck(self):
        try:
            self.pick_rep_set = subprocess.check_output(['which', 'pick_rep_set.py']).split('\n')[0]
        except subprocess.CalledProcessError:
            self.filelog.write(msg68)
            sys.exit(0)
        else:
            return self.pick_rep_set

    def samtoolscheck(self):
        try:
            self.samtools = subprocess.check_output(['which', 'samtools']).split('\n')[0]
        except subprocess.CalledProcessError:
            self.filelog.write(msg69)
            sys.exit(0)
        else:
            return self.samtools

    def awkcheck(self):
        try:
            self.awk = subprocess.check_output(['which', 'awk']).split('\n')[0]
        except subprocess.CalledProcessError:
            self.filelog.write(msg70)
            sys.exit(0)
        else:
            return self.awk

    def fastqcount(self, fastq, rtype):
        self.count = 0
        for record in SeqIO.parse(fastq, rtype):
            self.count = self.count + 1
        return str(self.count)

    def inputinformationappen(self):
        self.filelog = open(self.outputfolder + self.outputid + ".log", "a")
        self.filelog.write(datetime.datetime.now().ctime() + '\n')
        self.filelog.write(msg14)
        self.filelog.write(msg15+self.sequencingtype)
        if self.sequencingtype == 'Paired-End':
            self.filelog.write(msg17 + self.readforward)
            self.filelog.write(msg18 + self.readreverse)
            self.filelog.write(msg19 + self.readforwardtype)
            self.filelog.write(msg20 + self.readreversetype)
            self.filelog.write(msg21 + self.primer5forward)
            self.filelog.write(msg22 + self.primer3forward)
            self.filelog.write(msg23 + self.primer5reverse)
            self.filelog.write(msg24 + self.primer3reverse)
            self.filelog.write(msg47 + self.fastqcount(self.readforward, self.readforwardtype))
            self.filelog.write(msg48 + self.fastqcount(self.readreverse, self.readreversetype))
        else:
            self.filelog.write(msg28 + self.readforward)
            self.filelog.write(msg29 + self.readforwardtype)
            self.filelog.write(msg30 + self.primer5forward)
            self.filelog.write(msg31 + self.primer3forward)
            self.filelog.write(msg49 + self.fastqcount(self.readforward, self.readforwardtype))
        self.filelog.write(msg25 + self.outputid)
        self.filelog.write(msg26 + self.fastasequence)
        self.filelog.write(msg27 + self.annotation)
        self.filelog.write(msg33 + subprocess.check_output(['cutadapt', '--version']))
        self.filelog.write(subprocess.check_output(['pick_otus.py', '--version']))
        self.filelog.write(subprocess.check_output(['pick_rep_set.py', '--version']))
        self.filelog.write(msg0)
        self.filelog.close()
        return True
