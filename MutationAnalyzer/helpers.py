import vcf
from mutation.models import Mutation

def parse_vcf(vcf_file):
    vcf_reader = vcf.Reader(open(vcf_file,'r'))
    for record in vcf_reader:
        for alt in record.ALT:
            m = Mutation(chrom = record.CHROM, pos = record.POS, ref = record.REF, alt = alt)
            print m,
            for sample in record.samples:
                print sample,
    print
