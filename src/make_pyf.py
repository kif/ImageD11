

import os, glob, shutil, numpy.f2py
import sys

head  = """
python module %s

usercode '''
#include "blobs.h"
'''
interface

usercode '''
/* This runs inside the init part of the module as it is after interface */
#define str(x) (#x)
PyDict_SetItemString(d,str(s_1)    ,PyInt_FromLong(s_1));
PyDict_SetItemString(d,str(s_I)    ,PyInt_FromLong(s_I));
PyDict_SetItemString(d,str(s_I2)   ,PyInt_FromLong(s_I2));
PyDict_SetItemString(d,str(s_fI)   ,PyInt_FromLong(s_fI));
PyDict_SetItemString(d,str(s_ffI)  ,PyInt_FromLong(s_ffI));
PyDict_SetItemString(d,str(s_sI)   ,PyInt_FromLong(s_sI));
PyDict_SetItemString(d,str(s_ssI)  ,PyInt_FromLong(s_ssI));
PyDict_SetItemString(d,str(s_sfI)  ,PyInt_FromLong(s_sfI));
PyDict_SetItemString(d,str(s_oI)   ,PyInt_FromLong(s_oI));
PyDict_SetItemString(d,str(s_ooI)  ,PyInt_FromLong(s_ooI));
PyDict_SetItemString(d,str(s_soI)  ,PyInt_FromLong(s_soI));
PyDict_SetItemString(d,str(s_foI)  ,PyInt_FromLong(s_foI));
PyDict_SetItemString(d,str(mx_I)   ,PyInt_FromLong(mx_I));
PyDict_SetItemString(d,str(mx_I_f) ,PyInt_FromLong(mx_I_f));
PyDict_SetItemString(d,str(mx_I_s) ,PyInt_FromLong(mx_I_s));
PyDict_SetItemString(d,str(mx_I_o) ,PyInt_FromLong(mx_I_o));
PyDict_SetItemString(d,str(bb_mx_f),PyInt_FromLong(bb_mx_f));
PyDict_SetItemString(d,str(bb_mx_s),PyInt_FromLong(bb_mx_s));
PyDict_SetItemString(d,str(bb_mx_o),PyInt_FromLong(bb_mx_o));
PyDict_SetItemString(d,str(bb_mn_f),PyInt_FromLong(bb_mn_f));
PyDict_SetItemString(d,str(bb_mn_s),PyInt_FromLong(bb_mn_s));
PyDict_SetItemString(d,str(bb_mn_o),PyInt_FromLong(bb_mn_o));

PyDict_SetItemString(d,str(avg_i),PyInt_FromLong(avg_i));
PyDict_SetItemString(d,str(f_raw),PyInt_FromLong(f_raw));
PyDict_SetItemString(d,str(s_raw),PyInt_FromLong(s_raw));
PyDict_SetItemString(d,str(f_cen),PyInt_FromLong(f_cen));
PyDict_SetItemString(d,str(s_cen),PyInt_FromLong(s_cen));
PyDict_SetItemString(d,str(o_raw),PyInt_FromLong(o_raw));
PyDict_SetItemString(d,str(m_ff),PyInt_FromLong(m_ff));
PyDict_SetItemString(d,str(m_ss),PyInt_FromLong(m_ss));
PyDict_SetItemString(d,str(m_oo),PyInt_FromLong(m_oo));
PyDict_SetItemString(d,str(m_sf),PyInt_FromLong(m_sf));
PyDict_SetItemString(d,str(m_so),PyInt_FromLong(m_so));
PyDict_SetItemString(d,str(m_fo),PyInt_FromLong(m_fo));
PyDict_SetItemString(d,str(dety),PyInt_FromLong(dety));
PyDict_SetItemString(d,str(detz),PyInt_FromLong(detz));

PyDict_SetItemString(d,str(NPROPERTY),PyInt_FromLong(NPROPERTY));

PyDict_SetItemString(d,str(s2D_1),PyInt_FromLong(s2D_1));
PyDict_SetItemString(d,str(s2D_I),PyInt_FromLong(s2D_I));
PyDict_SetItemString(d,str(s2D_fI),PyInt_FromLong(s2D_fI));
PyDict_SetItemString(d,str(s2D_sI),PyInt_FromLong(s2D_sI));
PyDict_SetItemString(d,str(s2D_ffI),PyInt_FromLong(s2D_ffI));
PyDict_SetItemString(d,str(s2D_sfI),PyInt_FromLong(s2D_sfI));
PyDict_SetItemString(d,str(s2D_ssI),PyInt_FromLong(s2D_ssI));
PyDict_SetItemString(d,str(s2D_bb_mx_f),PyInt_FromLong(s2D_bb_mx_f));
PyDict_SetItemString(d,str(s2D_bb_mx_s),PyInt_FromLong(s2D_bb_mx_s));
PyDict_SetItemString(d,str(s2D_bb_mn_f),PyInt_FromLong(s2D_bb_mn_f));
PyDict_SetItemString(d,str(s2D_bb_mn_s),PyInt_FromLong(s2D_bb_mn_s));
PyDict_SetItemString(d,str(NPROPERTY2D),PyInt_FromLong(NPROPERTY2D));
/* ends user code */
'''
end interface

interface
"""

tail = """
end interface
end python module _cImageD11
"""

def add_wrappers( pyf, csource ):
    """ reads a wrapper out of a C file which is delimited by:
    F2PY_WRAPPER_START and F2PY_WRAPPER_END """
    with open(csource, "r") as cfile:
        in_wrapper = False
        for line in cfile.readlines():
            if in_wrapper:
                if line.find("F2PY_WRAPPER_END") >= 0:
                    pyf.write("\n")
                    in_wrapper = False
                else:
                    pyf.write(line)
            else:
                if line.find("F2PY_WRAPPER_START") >= 0:
                    in_wrapper = True


def makepyf( pyfname, sources ):
    import os
    if pyfname.endswith('.pyf'):
        pyfname = pyfname[:-4]
    with open(pyfname+".pyf","w") as pyf:
        pyf.write(head%os.path.split(pyfname)[-1])
        for sfile in sources:
            add_wrappers(pyf, sfile)
        pyf.write(tail)


def write_docs( inp, outf ):
    """ One single block of !DOC per item, first word is key
    """
    with open(inp , "r") as pyf:
        fname = None
        docs = {}
        for line in pyf.readlines():
            if line.startswith("!DOC"):
                if fname is not None:
                    docs[fname] += line[5:]
                else:
                    words = line.split()
                    fname = words[1]
                    docs[fname] = " ".join(words[2:]) + "\n"
            else:
                fname = None
    with open(outf, "w") as docf:
        docf.write('\n"""Autogenerated from make_pyf.py Edit in %s please"""\n'%(inp))
        keys = list(docs.keys())
        keys.sort()
        for fname in keys:
            docf.write( '%s = """%s"""\n'%(fname, docs[fname]))
        docf.write("__all__ = [\n" + ",\n".join(['    "%s"'%(k) for k in keys ])+  "]")


for name in ['"c:\Program Files\LLVM\bin\clang-format" ',
             'clang-format-10',
             'clang-format' ]:
    if os.path.exists(name) or os.system(name+" -version")==0:
        CF = name + ' --style=file -i '
        break
else:
    print("clang-format was not found, please do not send to git!")
    CF = 'echo '


def clean(sources):
    """ Runs clang-format on all the C source files
    Breaks a lot of things but hopefully stops it looking bad
    """
    for fname in sources + glob.glob("*.h"):
        print("cleaning",fname)
        os.system(CF+fname)

if __name__ == "__main__":

    PYF = "_cImageD11.pyf"
    sources = [s for s in glob.glob("*.c") if s.find("module")<0 ]
    clean( sources )
    makepyf( PYF , sources ) 
    DOCF = os.path.join("..", "ImageD11", "cImageD11_docstrings.py")
    write_docs( PYF, DOCF )

