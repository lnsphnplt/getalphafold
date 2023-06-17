import os
import urllib.request


def checkurl(url):
    urlok = True
    try:
        a = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print(f'Error code: {e.code}')
        urlok = False
    return urlok


def checkversion(name, i, setversion, versions):
    while setversion==0 and len(versions)>0:
        version = versions.pop()
        urlstem = 'https://alphafold.ebi.ac.uk/files/'
        affile = f'AF-{name}-F{i}-model_v{version}.pdb'
        url = urlstem+affile
        urlok = checkurl(url)
        if urlok:
            print(f'set version {version}')
            setversion = version
            return version
            #break 
    print(f'could not find alphafold model for uniprot {name}')



def checkfragments(name, setversion):
    big = False
    urlstem = 'https://alphafold.ebi.ac.uk/files/'
    f1 = checkurl(urlstem+f'AF-{name}-F1-model_v{setversion}.pdb')
    f2 = checkurl(urlstem+f'AF-{name}-F2-model_v{setversion}.pdb')
    if f1 and f2:
        print(f'Found multiple fragements for uniprot {name}')
        big = True
    return big

def getpdb(name, i, setversion, outdir):
    urlstem = 'https://alphafold.ebi.ac.uk/files/'
    affile = f'AF-{name}-F{i}-model_v{setversion}.pdb'
    url = urlstem+affile
    pathout = os.path.join(outdir, affile)
    urllib.request.urlretrieve(url, pathout)
    

def executefct():
    name = str(input('Enter Uniprot identifier:'))
    print(f'Uniprot identifier: {name}')
    version = int(input('Enter model version: \n if not possible will return most recently published model'))
    print(f'Model version: {version}')
    path = str(input('Enter absolute path to storage location of pdb file:'))
    print(f'Absolute path to storage location of pdb file: {path}')
    print('! If nonexistent will store in current working directory')
    print('! If model consists of several fragments will make directory')


    name = name.upper()
    i = 1
    affile = f'AF-{name}-F{i}-model_v{version}.pdb'
    urlstem = 'https://alphafold.ebi.ac.uk/files/'
    url = urlstem+affile


    setversion = 0
    versions = [1, 2, 3, 4, 5]
    versions = [v for v in versions if v != version]

    if checkurl(url):
        setversion = version
    else:
        print(f'Could not find model_v{version}, will search for different version')
        setversion = checkversion(name, 1, setversion, versions)
        

    outdir = os.getcwd()
    if os.path.isdir(path):
        outdir = path

    big = checkfragments(setversion)
    if big:
        outdir = os.path.join(outdir, f'AF-{name}-Fx-model_v{setversion}')
        os.makedirs(outdir)
        print('Created new directory: '+outdir)


    for i in range(100):
        try:
            getpdb(name, i , setversion, outdir)
        except:
            if i>2:
                n = i-1
                print(f'stored {n} fragments')
            break



if __name__ == '__main__':
    executefct()


