import optparse
from pyinteraseq_trimming import *
from pyinteraseq_mapping import *
from pytinteraseq_domains_definition import *
from pyinteraseq_genomefileparsing import *


parser = optparse.OptionParser(usage='python %prog pyinteraseq_main_inputcheck.py', version='1.0',)
parser.add_option('--readforward', action="store", dest="readforward", default=None,
                  help='Read dataset input forward')
parser.add_option('--readreverse', action="store", dest="readreverse", default=None,
                  help='Read dataset input reverse',)
parser.add_option('--readforwardtype', type='choice', choices=['fastq', 'fasta'], default=None,
                  help='Read dataset input forward')
parser.add_option('--readreversetype', type='choice', choices=['fastq', 'fasta'], default=None,
                  help='Read dataset input reverse')
parser.add_option('--sampletype', type='choice', choices=['genomic', 'selection', 'control'], default=None,
                  help='Select type of dataset')

primer_opts = optparse.OptionGroup(
    parser, 'Primers Options',
    'Options for primer sequence and trimming.',
    )
primer_opts.add_option('--primer5forward', action="store", dest="primer5forward", default=None,
                       help='Output folder.')
primer_opts.add_option('--primer3forward', action="store", dest="primer3forward", default=None,
                       help='Output ID.')
primer_opts.add_option('--primer5reverse', action="store", dest="primer5reverse", default=None,
                       help='Output folder.')
primer_opts.add_option('--primer3reverse', action="store", dest="primer3reverse", default=None,
                       help='Output ID.')
parser.add_option_group(primer_opts)

query_opts = optparse.OptionGroup(
    parser, 'Output Options',
    'Options for the output destionation and name.',
    )
query_opts.add_option('--outputfolder', action="store", dest="outputfolder", default=None,
                      help='Output folder.')
query_opts.add_option('--outputid', action="store", dest="outputid", default=None,
                      help='Output ID.')

parser.add_option_group(query_opts)

reference_opts = optparse.OptionGroup(
    parser, 'Primers Options',
    'Options for primer sequence and trimming.',
    )
reference_opts.add_option('--fastasequence', action="store", dest="fastasequence", default=None,
                          help='Genome sequence fasta file.(.fasta|.fna|.fa)')
reference_opts.add_option('--annotation', action="store", dest="annotation", default=None,
                          help='Annotation File(.gff|.bed)')
reference_opts.add_option('--chromosomename', action="store", dest="chromosomename", default=None,
                          help='Chromosome Name.(NC_XXXX)')
parser.add_option_group(reference_opts)

parser.add_option_group(query_opts)

reference_opts = optparse.OptionGroup(
    parser, 'Advanced Options',
    'Options for advanced analysis.',
    )
reference_opts.add_option('--minclonelength', action="store", dest="minclonelength", default='100',
                          help='Minumum clones length.')
reference_opts.add_option('--thread', action="store", dest="thread", default='1',
                          help='Number of thread.')
parser.add_option_group(reference_opts)

options, args = parser.parse_args()

if __name__ == '__main__':
    DictInfo = dict()
    if options.readreverse is not None:
        if (options.readforwardtype == "fastq") and (options.readreversetype == "fastq"):
            DictInfo.update({
                "LogFilePath": TrimmingPaired(optparseinstance=options).logfilecreation(),
                "CutadaptPath": TrimmingSingle(optparseinstance=options).cutadaptcheck(),
                "PickOtus": TrimmingSingle(optparseinstance=options).pickotuscheck(),
                "PickRepSeq": TrimmingSingle(optparseinstance=options).pickrepseqcheck(),
                "LogInfoAppended": TrimmingPaired(optparseinstance=options).inputinformationappen()
            })
    else:
        DictInfo.update({
            "LogFilePath": TrimmingSingle(optparseinstance=options).logfilecreation(),
            "CutadaptPath": TrimmingSingle(optparseinstance=options).cutadaptcheck(),
            "PickOtus": TrimmingSingle(optparseinstance=options).pickotuscheck(),
            "PickRepSeq": TrimmingSingle(optparseinstance=options).pickrepseqcheck(),
            "LogInfoAppended": TrimmingSingle(optparseinstance=options).inputinformationappen()
        })
    # Parsing input fasta file
    DictInfo["fasta"] = GenomeFile(optparseinstance=options).fastareference()
    # Parsing Input annotation file
    DictInfo["annotation"] = AnnotationFile(optparseinstance=options).annotationbuild()
    # Trimming steps for fastq input
    if options.readforwardtype == 'fastq':
        # Trimming paired end fastq
        if options.readreverse is not None:
            DictInfo["Trimmed5paired"] = TrimmingPaired(optparseinstance=options).trimming5paired()
        else:
            # Trimming Single-End fastq
            DictInfo["Trimmed5single"] = TrimmingSingle(optparseinstance=options).trimming5single()
    elif options.readforwardtype == 'fasta':
        # Trimming paired end fasta
        if options.readreverse is not None:
            DictInfo["Trimmed5paired"] = TrimmingPaired(optparseinstance=options).trimming5paired()
        else:
            # Trimming Single-End fasta
            DictInfo["Trimmed5single"] = TrimmingSingle(optparseinstance=options).trimming5single()