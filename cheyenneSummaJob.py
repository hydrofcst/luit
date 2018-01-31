
import os, shutil
import subprocess

# User-provided info
summaexe = '/glade/p/work/manab/fcast/summa/bin/summa.exe'
masterdir = '/glade/p/work/manab/fcast/PNW/'
summafilemanname = 'summa_fileManager.txt'
pbstemplatename = 'template_pbs.txt'
restartflag = '-r never'    #Options: [y,m,d,e,never]
logdname = 'log'
jobdname = 'joblists'
pbsdname = 'pbsscripts'

strtGRU = 1
endGRU = 11723
lenGRU = 10      #GRU Length of each run
numcores = 36       #Number of cores requested in each node



def concatDir(dname):
    '''
    Concatenates Master dir and another dname (directory name)
    '''
    filename = masterdir + dname
    return(filename)

def purgeDir(folder):
    '''
    Purges contents of a directory
    '''

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
            
def createJobs(strtGRU, endGRU, lenGRU):
    '''
    Creates a list of SUMMA jobs to be run
    '''
    runCommandList = []
    for num in range(strtGRU, endGRU, lenGRU):
        if (num + lenGRU < endGRU):
            runCommand = [summaexe, '-g', str(num), str(lenGRU), restartflag, '-m', 
                          summafileman, '>', os.path.join(logdir, str(num))]
            runCommand = " ".join(runCommand)
            runCommandList.append(runCommand)
        else:   #Ensuring that the last SUMMA job has correct length
            runCommand = [summaexe, '-g', str(num), str(endGRU-num+1), restartflag, '-m', summafileman]
            runCommand = " ".join(runCommand)
            runCommandList.append(runCommand)
    return(runCommandList)

def createFilenames(dir, prestring, ext):
    '''
    Creates names of joblists and pbsscripts
    '''
    listlen = numcores * lenGRU   #Number of jobs in each joblist
    listnum = endGRU//listlen + (endGRU % listlen > 0)  #Total number of joblists required
    listname = []

    for num in range(0, listnum):
        filename = os.path.join(dir, prestring + str(num))
        filename = filename + ext
        listname.append(filename)
    
    return(listname)

def writeJobLists(runCommandList, joblist, numcores):
    '''
    Write jobs to joblist text files
    '''
    for x,y in enumerate(range(0, len(runCommandList), numcores)):
        jobchunk = runCommandList[y : y + numcores]
        with open(joblist[x], 'w') as file_handler:
            for item in jobchunk:
                file_handler.write("{}\n".format(item))
                
def pbsScripts(joblist):
    '''
    Creates PBS scripts for each joblist
    '''
    for p in range(0, len(joblist)):
        with open(pbstemplate, "rt") as fin:
            with open(pbslist[p], "wt") as fout:
                for line in fin:
                    fout.write(line.replace('columbiaTest_NUMBER', 'PNW_SM_' + str(p)).
                               replace('JOBLIST', joblist[p]))

def submitCheyenne(pbslist):
    for count, value in enumerate(pbslist):
        subprocess.run(["qsub", value])


if __name__ == '__main__':
    logdir = concatDir(logdname)
    jobdir = concatDir(jobdname)
    pbsdir = concatDir(pbsdname)
    pbstemplate = concatDir(pbstemplatename)
    summafileman = concatDir(summafilemanname)

    purgeDir(logdir)
    purgeDir(jobdir)
    purgeDir(pbsdir)
    
    runCommandList = createJobs(strtGRU, endGRU, lenGRU)
    
    joblist = createFilenames(jobdir, 'summa_joblist_', '')
    pbslist = createFilenames(pbsdir, 'pbs_', '.sh')
    
    writeJobLists(runCommandList, joblist, numcores)
    pbsScripts(joblist)

submitCheyenne(pbslist)
