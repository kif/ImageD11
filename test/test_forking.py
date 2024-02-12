
# There is a problem of forking / multiprocessing.
# There are no imports here!

# Each function is intended to run in a subprocess


def run_test_fun(function, env=None):
    """ Runs a function in a subprocess, returns the output """
    import sys
    from subprocess import PIPE, Popen
    args = [ sys.executable, __file__, function]
    proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, env=env)
    stdout, stderr = proc.communicate(  )
    return stdout, stderr


def omp_call(N=1024):
    """ returns the number of threads in use for an example call using openmp """
    import ImageD11.cImageD11
    import numpy as np
    dat = np.full((N,N), 101, dtype=np.uint16)
    drk = np.full((N,N), 100, dtype=np.float32)
    cor = np.empty((N,N), dtype=np.float32)
    ImageD11.cImageD11.uint16_to_float_darksub( cor.ravel(), drk.ravel(), dat.ravel() )
    threads_avail = ImageD11.cImageD11.cores_available()
    threads_used = ImageD11.cImageD11.cimaged11_omp_get_max_threads()
    return threads_avail, threads_used


def should_warn_on_fork_in_parent():
    """ This is the problem case, we want a warning """
    import multiprocessing
    try:
        multiprocessing.set_start_method('fork')
    except AttributeError:
        pass
    threads_avail, threads_used = omp_call()
    assert threads_avail == threads_used, 'not threaded?'
        
def test_should_warn_on_fork_in_parent():
    """ this is called by py.test to run the previous function """
    stdout, stderr = run_test_fun( "should_warn_on_fork_in_parent" )
    import sys
    if sys.version_info[0] > 2:
        assert stderr.find(b'please use forkserver or spawn for multiprocessing') > 0
    else:
        assert stderr.find('python2') != -1

    
def should_warn_on_fork_in_child():
    """ This is a problem case, we want a warning """
    import multiprocessing
    try:
        multiprocessing.set_start_method('fork')
    except AttributeError:
        pass
    p = multiprocessing.Pool(2)
    for threads_avail, threads_used in p.map(omp_call, (1024,1024)):
        assert threads_used == 1, 'failed to set omp threads == 1 for child'
        
def test_should_warn_on_fork_in_child():
    stdout, stderr = run_test_fun( "should_warn_on_fork_in_child" )
    import sys
    if sys.version_info[0] > 2:
        assert stderr.find(b'please use forkserver or spawn for multiprocessing') > 0
    else:
        assert stderr.find('python2') != -1
    
    
def threads_in_child_no_warn():
    """ This is a working case, we do not want a warning """
    import multiprocessing
    try:
        multiprocessing.set_start_method('forkserver')
    except AttributeError:
        pass
    p = multiprocessing.Pool(2)
    for threads_avail, threads_used in p.map(omp_call, (1024,1024)):
        if threads_avail>=3:
            assert threads_used == 3, 'failed to set omp threads == 3 %d for child'%(threads_used)

def test_threads_in_child_no_warn():
    import sys, os
    env = os.environ.copy()
    env['OMP_NUM_THREADS']='3'
    stdout, stderr = run_test_fun( "threads_in_child_no_warn",env=env)
    if sys.version_info[0] > 2:
        assert len(stderr)==0
    else:
        # python2....
        assert stderr.find('python2') != -1
    
    
                    
if __name__=="__main__":
    import sys
    try:
        result = globals()[sys.argv[1]]()
    except Exception as e:
        print(e)
        raise