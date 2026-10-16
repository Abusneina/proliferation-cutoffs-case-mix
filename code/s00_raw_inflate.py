"""Recover a single deflated entry from a concatenated split zip by reading the local header
directly and inflating the raw stream; verifies CRC-32 and size against the central directory."""
import sys, struct, zlib, time
src, out = sys.argv[1], sys.argv[2]
name=b"GSE96058_gene_expression_3273_samples_and_136_replicates_transformed.csv/GSE96058_gene_expression_3273_samples_and_136_replicates_transformed.csv"
data=open(src,"rb")
buf=data.read(1<<20)
pos=-1; off=0
# locate local header for the csv entry
data.seek(0); chunk=b""; base=0
while True:
    blk=data.read(1<<24)
    if not blk: break
    chunk=chunk[-4096:]+blk; i=chunk.find(b"PK\x03\x04"+b"\x00"*0)
    j=chunk.find(name)
    if j>=0:
        k=chunk.rfind(b"PK\x03\x04",0,j); pos=base-len(chunk)+len(blk)+k; break
    base+=len(blk)
data.seek(pos); hdr=data.read(30)
sig,ver,flag,meth,mt,md,crc,csz,usz,nl,el=struct.unpack("<IHHHHHIIIHH",hdr)
data.seek(pos+30+nl+el); start=data.tell()
print(f"local header at {pos}, method={meth}, data starts {start}, flag={flag:#x}")
# expected crc/size from central directory (zip64 aware)
data.seek(0,2); size=data.tell(); data.seek(max(0,size-65536)); tail=data.read()
cd=tail.rfind(b"PK\x01\x02"+b"")
exp_crc=exp_usz=None
p=0
while True:
    p=tail.find(b"PK\x01\x02",p)
    if p<0: break
    (s,vm,vn,fl,me,t,d,cr,cs,us,fnl,exl,cml,dn,ia,ea,lho)=struct.unpack("<IHHHHHHIIIHHHHHII",tail[p:p+46])
    fn=tail[p+46:p+46+fnl]
    if fn==name:
        exp_crc=cr; exp_usz=us
        if us==0xFFFFFFFF:
            ex=tail[p+46+fnl:p+46+fnl+exl]; q=0
            while q<len(ex):
                hid,hl=struct.unpack("<HH",ex[q:q+4])
                if hid==1: exp_usz=struct.unpack("<Q",ex[q+4:q+12])[0]; break
                q+=4+hl
    p+=46
print(f"expected crc={exp_crc:#010x} size={exp_usz}")
data.seek(start); d=zlib.decompressobj(-15); crc=0; n=0; t0=time.time()
with open(out,"wb") as fo:
    while True:
        blk=data.read(1<<24)
        if not blk: break
        o=d.decompress(blk); fo.write(o); crc=zlib.crc32(o,crc); n+=len(o)
        if d.eof: break
        print(f"  inflated {n/1e9:.2f} GB  ({time.time()-t0:.0f}s)",flush=True)
print(f"done: {n} bytes, crc={crc:#010x}  ->  {'CRC OK' if crc==exp_crc else 'CRC MISMATCH'} / {'SIZE OK' if n==exp_usz else 'SIZE MISMATCH'}")
