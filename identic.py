


import os
import argparse
import hashlib

parser= argparse.ArgumentParser()
parser.add_argument("-d", action="store_true", default=False ) #parser argument control -d flag
parser.add_argument("-f", action="store_true", default=False ) #parser argument control -f flag
parser.add_argument("-n", action="store_true", default=False ) #parser argument control -n flag
parser.add_argument("-c", action="store_true", default=False ) #parser argument control -c flag
parser.add_argument("-cn", action="store_true", default=False ) #parser argument control -cn flag
parser.add_argument("-s", action="store_true", default=False ) #parser argument control -s flag
parser.add_argument('input',action='store',nargs='*',default=os.getcwd()) #parser argument take directory as an input
args=parser.parse_args()


givendirectory=[]                        # decide defaultdir or givendir and if it is default put it in a list 
if isinstance(args.input, list):
    
    givendirectory=args.input
else:
    givendirectory.append(args.input)  






                                         
def descending(y):               #sort the dictionary in descending order
    l=list(y.items())
    l.sort(reverse=True)         #sort in descending order
    dict1=dict(l)                # convert the list in dictionary 

    return dict1 









files1={}             #dictionary of files whose contents duplicates
filesname1={}        #dictionary of files whose names duplicates 
filesize={}           #dictionary of files whose sizes duplicates
dirs1={}           #dictionary of directory whose contents duplicates
dirsname1={}       #dictionary of directory whose names duplicates
dirsize={}          #dictionary of directory whose sizes duplicates

 
def findlisthash(path):             #finds sha256 value of content of afile
    filename = path
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
    
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
            
        return sha256_hash.hexdigest()

def hash_dir(dir_path):              #finds sha256 value of a directory content
    hashes = []
    for path, dirs, files in os.walk(dir_path):
        for file in files: 
            
            hashes.append(findlistname(findlisthash(os.path.join(path, file))))  # find content hash of a file
        for dir in dirs: 
            hashes.append(hash_dir(os.path.join(path, dir)))   #call recursively the same function for dirs in dir  
        break 
    
    y=sorted(hashes) #sort hashes
    x=''.join(y)   #combine hashes
    
    return (hashlib.sha256(x.encode('utf-8')).hexdigest())


def findlistname(namelist):         #finds sha256 value of a file name
    return (hashlib.sha256(namelist.encode('utf-8')).hexdigest())


def finddirname(dir_path):         #finds sha256 value of a directory name. It includes subdirectory names and subfile names
    hash=[]
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            hash.append(findlistname(file)) #finds sha256 value of a file name
              
        for dir in dirs:
        
            hash.append(findlistname(dir))
            finddirname(os.path.join(root, dir))    #call recursively the same funtion for dirs in dir
    
    
    if hash==[]:
        base=os.path.basename(dir_path)         #if it is empty directory append hash the name of the directory only
        
        return findlistname(base) 
    else:    
        base=os.path.basename(dir_path)
        hash.append(findlistname(base))
        y=sorted(hash)
    
        x=''.join(y)
        
        return hashlib.sha256(x.encode('utf-8')).hexdigest()




def get_file_size_in_bytes(file_path):        #finds size of  a file

    size = os.path.getsize(file_path)
    return size



def get_dir_size_in_bytes(start_path):          #finds size of  a directory
    total_size = 0
    
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return  str(total_size)



for dirss in givendirectory:
    for root, dirs, files in os.walk(dirss):  #os.walk in current directory
        
        for filenames in files:
            files1[os.path.join(root,filenames)]=findlisthash(os.path.join(root,filenames))     #fill out files1 with key: filenames in files, value: hash value of the file 
            filesname1[os.path.join(root,filenames)]=findlistname(filenames)  #fill out filesname1 with key: path of files, value: hash value of the file name 
            

        
        for dirnames in dirs:
            dirs1[os.path.join(root, dirnames)]=hash_dir(os.path.join(root, dirnames)) #fill out dirs1 with key: dirnames in dirs, value: hash value of the file 
            dirsname1[os.path.join(root, dirnames)]=finddirname(os.path.join(root, dirnames))#fill out dirss1 with key: path in dirs, value: hash value of the directory names
            
            

    
if args.cn :   #if  -cn is given 
    

    if args.d:        #if -d is given
        new_dict3 = {}
        for pair in dirsname1.items():          # find dublicate hash values, combine them and put another dictionary
            if pair[1] not in new_dict3.keys():
                new_dict3[pair[1]] = []

            new_dict3[pair[1]].append(pair[0])  

        print("\t")    
        list4=[]

        for k,v in new_dict3.items():            # put dublicate directory names to a list
            if (len(v)>1):
                list4.append(sorted(v))
        new_dict = {}
        for pair in dirs1.items():                 # find dublicate hash values, combine them and put another dictionary
            if pair[1] not in new_dict.keys():
                new_dict[pair[1]] = []

            new_dict[pair[1]].append(pair[0])

        
         
        list1=[]
        for k,v in new_dict.items():    # put dublicate directory contents to a list
        
            if (len(v)>1):
                list1.append(sorted(v)) 
        
        list9=[]
        
        for items in list1:
            
            for ite in list4:            # if there is common dublicate dirname and dir contents put them to a list 
                if(all(x in items for x in ite)):
                    list9.append(ite) 
                elif(all(x in ite for x in items)):
                    list9.append(items) 

        for items in list9:
                    
                for i in items:
                        
                        if(args.s):    #if -s flag is given 
                           print(i,"\t", get_dir_size_in_bytes(i))     #print dirpaths and sizes
                        else:         
                           print(i)          #print dirpaths
                        
                print("\t")     
     

        

    else:                           #follow the same steps in -cn -d for -cn -f or -cn
        new_dict3 = {}
        for pair in filesname1.items():
            if pair[1] not in new_dict3.keys():
                new_dict3[pair[1]] = []

            new_dict3[pair[1]].append(pair[0])  

           
        list4=[]

        for k,v in new_dict3.items():
            if (len(v)>1):
                list4.append(sorted(v))
        new_dict = {}
        for pair in files1.items():
            if pair[1] not in new_dict.keys():
                new_dict[pair[1]] = []

            new_dict[pair[1]].append(pair[0])

        
        print("\t")  
        list1=[]
        for k,v in new_dict.items():
        
            if (len(v)>1):
                list1.append(sorted(v)) 
        
        list9=[]
        
        for items in list1:
            
            for ite in list4: 
                if(all(x in items for x in ite)):
                    list9.append(ite) 
                elif(all(x in ite for x in items)):
                    list9.append(items) 

        for items in list9:
                    
                for i in items:
                        
                        if(args.s):
                           print(i,"\t", get_file_size_in_bytes(i))
                        else:
                           print(i)
                        
                print("\t")     


 
        
                            
elif args.n:    #if -n is given         
    
    if args.d:      #if -d is given                                         
        new_dict3 = {}                     # find dublicate hash values, combine them and put another dictionary
        for pair in dirsname1.items(): 
            if pair[1] not in new_dict3.keys():
                new_dict3[pair[1]] = []

            new_dict3[pair[1]].append(pair[0])  

        
        print("\t")
        list4=[]

        for k,v in new_dict3.items():  # put dublicate directory names to a list
            if (len(v)>1):
                list4.append(sorted(v))
                
        for items in sorted(list4):
                    
                    for i in items:
                        
                        
                        print(i)
                        
                            
                    print("\t")    
    else:                                #follow the same steps in -n -d for -n -f or -n       
        new_dict3 = {}
        for pair in filesname1.items():
            if pair[1] not in new_dict3.keys():
                new_dict3[pair[1]] = []

            new_dict3[pair[1]].append(pair[0])  



        print("\t")
        list4=[]

        for k,v in new_dict3.items():
            if (len(v)>1):
                list4.append(sorted(v))
                
        for items in sorted(list4):
                    
                    for i in items:
                        
                        
                        print(i)
                    print("\t")               
                                    
                        
                        
                                                                

else:                #follow the same steps in -n for -c or default value(nothing)
    
                    
                        


    if args.d:
        new_dict1 = {}
        for pair in dirs1.items():
            if pair[1] not in new_dict1.keys():
                new_dict1[pair[1]] = []

            new_dict1[pair[1]].append(pair[0])  

        print("\t")
        list2=[]

        for k,v in new_dict1.items():
            if (len(v)>1):
                
                list2.append(sorted(v))
        for items in sorted(list2):
                    for i in items:
                        
                        if(args.s):
                            
                            print(i,"\t", get_dir_size_in_bytes(i))
                        else:
                            print(i)
                        
                    print("\t")    
                        
    else:
        new_dict = {}
        for pair in files1.items():
            if pair[1] not in new_dict.keys():
                new_dict[pair[1]] = []

            new_dict[pair[1]].append(pair[0])


        print("\t")
        list1=[]
        for k,v in new_dict.items():
        
            if (len(v)>1):
                list1.append(sorted(v))
            
        for items in sorted(list1):
                for i in items:
                        
                        if(args.s):
                            print(i,"\t", get_file_size_in_bytes(i))
                        else:
                            print(i)
                        
                        
                print("\t")             
                                                            
                            



                        
                        


                        


