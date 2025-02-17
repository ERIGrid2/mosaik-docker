import subprocess
from strenum import StrEnum


class ProcessOutStreamDef(StrEnum):
    '''Enum for defining process output handle.'''
    STDOUT = 'STDOUT'
    STDERR = 'STDERR'


def execute( cmd, env = None ):
    '''
    Invoke and execute a subprocess.

    :param cmd: sequence of program arguments or else a single string or path-like object (see Python "subprocess" module).
    :return: None
    '''
    p = subprocess.Popen(
        cmd,
        env = env,
        #stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # Wait for process to terminate and retrieve return code.
    return_code = p.wait()

    if ( 0 != return_code ):
        raise Exception( p.stderr.read().decode( 'utf-8' )[:-1] )


def execute_and_capture_output( cmd, env = None, out_def = ProcessOutStreamDef.STDOUT ):
    '''
    Invoke and execute a subprocess.
    Output from the subprocess to stdout is captured and returned as string.

    :param cmd: sequence of program arguments or else a single string or path-like object (see Python "subprocess" module).
    :param env: dict of environment variables for executing the command
    :param out_def: specify if command's output from STDOUT or STDERR should be captured
    :return: subprocess output (str)
    '''
    p = subprocess.Popen(
        cmd,
        env = env,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    # Wait for process to terminate and retrieve return code.
    return_code = p.wait()

    # Check
    if ( 0 != return_code ):
        raise Exception( p.stderr.read().decode( 'utf-8' )[:-1] )

    p_out_def_options = {
        ProcessOutStreamDef.STDOUT: p.stdout,
        ProcessOutStreamDef.STDERR: p.stderr,
    }

    p_out = p_out_def_options[out_def]

    return p_out.read().decode( 'utf-8' )[:-1]



def execute_and_stream_output( cmd, out_stream, env = None, out_stream_def = ProcessOutStreamDef.STDOUT ):
    '''
    Invoke and execute a subprocess.
    Output from the process to stdout is sent line by line to the specified output stream.

    :param cmd: sequence of program arguments or else a single string or path-like object (see Python "subprocess" module).
    :param out_stream: output stream
    :param env: dict of environment variables for executing the command
    :param out_stream_def: specify if command's output from STDOUT or STDERR should be streamed
    :return: None
    '''
    p = subprocess.Popen(
        cmd,
        env = env,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    p_out_stream_def_options = {
        ProcessOutStreamDef.STDOUT: p.stdout,
        ProcessOutStreamDef.STDERR: p.stderr,
    }

    p_out_stream = p_out_stream_def_options[out_stream_def]

    # Read output line by line and display via output stream.
    while True:
        line = p_out_stream.readline()
        if not line: break
        out_stream( line.decode( 'utf-8' )[:-1] )

    # Wait for process to terminate and retrieve return code.
    return_code = p.wait()

    if ( 0 != return_code ):
        raise Exception( p.stderr.read().decode( 'utf-8' )[:-1] )
