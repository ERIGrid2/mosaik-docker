import subprocess


def execute( cmd ):
    '''
    Invoke and execute a subprocess.

    :param cmd: sequence of program arguments or else a single string or path-like object (see Python "subprocess" module).
    :return: None
    '''
    p = subprocess.Popen(
        cmd,
        #stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # Wait for process to terminate and retrieve return code.
    return_code = p.wait()

    if ( 0 != return_code ):
        raise Exception( p.stderr.read().decode( 'utf-8' )[:-1] )


def execute_and_capture_output( cmd ):
    '''
    Invoke and execute a subprocess.
    Output from the subprocess to stdout is captured and returned as string.

    :param cmd: sequence of program arguments or else a single string or path-like object (see Python "subprocess" module).
    :return: subprocess output to stdout (str)
    '''
    p = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # Wait for process to terminate and retrieve return code.
    return_code = p.wait()

    # Check
    if ( 0 != return_code ):
        raise Exception( p.stderr.read().decode( 'utf-8' )[:-1] )

    return p.stdout.read().decode( 'utf-8' )[:-1]



def execute_and_stream_output( cmd, out_stream ):
    '''
    Invoke and execute a subprocess.
    Output from the process to stdout is sent line by line to the specified output stream.

    :param cmd: sequence of program arguments or else a single string or path-like object (see Python "subprocess" module).
    :param out_stream: output stream
    :return: None
    '''
    p = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # Read output line by line and display via output stream.
    while True:
        line = p.stdout.readline()
        if not line: break
        out_stream( line.decode( 'utf-8' )[:-1] )

    # Wait for process to terminate and retrieve return code.
    return_code = p.wait()

    if ( 0 != return_code ):
        raise Exception( p.stderr.read().decode( 'utf-8' )[:-1] )