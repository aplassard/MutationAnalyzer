import vcf
from mutation.models import Mutation
from patient.models import Patient,Patient_Mutation
import os,os.path
import gzip
import time

def handle_file_upload(f,d):
    if f.name.endswith('gz'):
        d+='.gz'
    with open(d,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def parse_vcf(file_name,experiment_id):
    out_name = '.'.join(file_name.split('.')[:-1])+'.out.vcf'
    print 'Path: %s' % os.path.abspath('.')
    if os.path.exists(file_name):
        print '** Found File %s **' % file_name
        call = "java -jar SNPomics.jar annot -i %s -o %s " %(file_name,out_name)
        print '** Running Call `%s` **' % call
        os.system(call)
        file_reader = open(out_name,'r')
    elif os.path.exists(file_name+'.gz'):
        call = "gunzip -c %s | java -jar SNPomics.jar annot --input-type vcf -i - -o %s " %(file_name+'.gz',out_name)
        print '** Running Call `%s` **' % call
        os.system(call)
        file_reader = open(out_name,'r')
    else:
        print '** Error!! File Not Found!! **'
        return
    print '** Starting database loading from file %s  **' % out_name
    vcf_reader = vcf.Reader(file_reader)
    patients = {}
    PMs = []
    all_muts = {}
    n = 0
    m = 1000
    o = 0
    for record in vcf_reader:
        if len(all_muts.keys()) > 10000:
            print 'Taking a Break from reading the VCF to load some mutations out of memory into the database'
            Mutation.objects.bulk_create(filter(lambda x: not x.id,all_muts.values()))
            print 'Reloading Mutations that did not have IDs',
            start = time.time()
            for key in all_muts.keys():
                if not all_muts[key].id:
                    mut = all_muts[key]
                    all_muts[key]=Mutation.objects.get(pos = mut.pos, ref = mut.ref, alt=mut.alt, chrom = mut.chrom)
            print 'and it took %s seconds' % (int(time.time()-start))
            start = time.time()
            for i in xrange(len(PMs)):
                mut = all_muts.get(PMs[i][1])
                PMs[i][0].mutation=mut
                PMs[i]=PMs[i][0]
            Patient_Mutation.objects.bulk_create(PMs)
            print 'Created %s Patient Mutations and this took %s seconds' % (len(PMs),int(time.time()-start))
            PMs = []
            all_muts = {}

        muts = {}
        o += 1
        for alt in record.ALT:
            try:
                mut = Mutation.objects.get(pos = record.POS,ref = record.REF, alt = str(alt), chrom = record.CHROM)
            except:
                mut = Mutation(pos = record.POS,ref = record.REF, alt = str(alt), chrom = record.CHROM)
                n += 1
                if n == m:
                    print 'Found %s new mutations out of %s thus far' % (n,o)
                    m += 1000
            muts[str(alt)]=str(mut)
            all_muts[str(mut)]=mut
        for sample in record.samples:
            if sample.is_variant:
                patient = patients.get(sample.sample)
                if not patient:
                    patient = Patient.objects.get(patient_name = sample.sample, experiment_id__exact = experiment_id)
                    patients[sample.sample] = patient
                for allele in sample.gt_bases.split(sample.gt_phase_char()):
                    mut = muts.get(allele)
                    if mut:
                        PMs.append((Patient_Mutation(patient = patient, is_homozygous = not sample.is_het),mut))
    Mutation.objects.bulk_create(filter(lambda x: not x.id,all_muts.values()))
    print 'Reloading Mutations that did not have IDs',
    n = 0
    start = time.time()
    for key in all_muts.keys():
        if not all_muts[key].id:
            mut = all_muts[key]
            all_muts[key]=Mutation.objects.get(pos = mut.pos, ref = mut.ref, alt=mut.alt, chrom = mut.chrom)
    print 'and it took %s seconds' % (int(time.time()-start))
    start = time.time()
    for i in xrange(len(PMs)):
        mut = all_muts.get(PMs[i][1])
        PMs[i][0].mutation=mut
        PMs[i]=PMs[i][0]
    Patient_Mutation.objects.bulk_create(PMs)
    print 'Created %s Patient Mutations and this took %s seconds' % (len(PMs),int(time.time()-start))
    print '** Done Parsing VCF File **'



