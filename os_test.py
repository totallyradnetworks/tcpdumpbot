import subprocess, os, time
import signal, psutil
dump_pid = ''


def run_process():    
    global dump_pid
    p = subprocess.Popen(['tcpdump', '-i', 'eth1'], stdout=subprocess.PIPE)
    dump_pid = p.pid
    #dump_ppid = os.getppid()
    #psu = psutil.Process(dump_pid)
    #child_psu = psu.children()
    #print('PSUTIL PID & NAME: %s %s' % (psu.pid, psu.name))
    #print('PSUTIL CHILD PID & NAME: %s ' % (child_psu))
    print('OS. Version of Process spawned with PID of: %s ' % (p.pid))
    #subprocess.run(create_string(), shell=True)

def kill_process():
    global dump_pid
    #psu = psutil.Process(dump_pid)
    os.system("kill %s" % (dump_pid))
    #subprocess.check_call(['sudo', 'kill', str(dump_pid)])
    print('Process %s Killed.' % dump_pid)
    #child_psu = psu.children(recursive=True)

run_process()
time.sleep(10)
kill_process()