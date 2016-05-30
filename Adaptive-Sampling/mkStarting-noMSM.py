# Finding the position of one frame in the desired cluster
def findElementPosition(l, desCluster):
    flag = False
    n_trajs = len(l)
    for i in range(n_trajs):
            n_frames = l[i]
            for j in range(len(n_frames)):
                if l[i][j] == desCluster:
                        output = [i, j]
                        flag = True
                        break
            if flag:
                break
    return output
# i is the trajectory number, and j is the frame number

# finding the population of each cluster
def populationFind(l, myn_clusters):
    pop = []
    for clusterID in range(myn_clusters):
            sum = 0
            for i in range(len(l)):
                    c = l[i]
                    c2 = c.tolist()
                    sum = sum + c2.count(clusterID)
            pop.append([sum, clusterID])
    pop.sort()
    return pop
    
########################################################################################################################
# The function is using other functions, find the less populated clusters and write the information of the cluster and cluster centers, their corresponding trajectory name, frames and other information into a dictionary file, "lessPopClsInf.txt".
# "T" is the name of trajectories array, in the same order as it was given into the msmbuilder, "l is the cluster labels corresponding to each, "myn_clusters" is the number of clusters and "n_sample" is the number of samples which are desired for the new round
########################################################################################################################

def writeOPF_lessPop(l,T, myn_clusters, n_samples):
    import json
    OPF = []
    pop = populationFind(l, myn_clusters)
    for i in range(n_samples):
            clusterID = pop[i][1] # it's the i-th first in the population list
            pos = findElementPosition(l, clusterID)
            trj = int(pos[0])
            frm = int(pos[1])+1
            OPF.append({'population':pop[i][0],'cluster':pop[i][1], 'traj':T[trj], 'frame':frm})
            print int(pos[1])+1 , int(pos[1])
    json.dump(OPF, open("ClsInf.txt",'w'))
    return OPF
# d2 = json.load(open("text.txt"))

########################################################################################################################
# This function write the appropriate input for cpptraj for extraction of frames corresponding to least populated clusters,
# The information is read from 'lessPopClsInf.txt' (which is writen by writeOPF function)
# The naming of the trajectories should be in a special format, so the function would be able to extract the topology file 
# name from trajectory name (usually used for unstriped trajectories with different round of simulation)
########################################################################################################################
def CpptrajInGen():
    import json
    inf = json.load(open("ClsInf.txt"))
    n_samples = len(inf)
    for i in range(n_samples):
            trj = inf[i]['traj']
            # simRound indicates the simulation round, like MD1, MD2,.. as each round might have different way of naming
            r = trj.split('/')[1]
            simRound = r.split('-')[0]
            # trjN is the trajectory name, without its address
            trjN = trj.split('/')[-1]
            if simRound=='MD1':
                a = trjN.strip('D1.mdcrd')
                # topN is the topology name which can be found from the trajectory name
                topN = a.strip('M')
                # topAd indicates the topolgy file name plus its address
                topAd = 'rawTrj/MD1-rwTop/'+topN+'.top'
                    
            if simRound=='MD2':
                topN = trjN.split('_md')[0]
                topAd = 'rawTrj/MD2-rwTop/'+topN+'.top'
            
            if simRound=='MD3':
                topN = trjN.split('_md')[0]
                topAd = 'rawTrj/MD3-rwTop/'+topN+'.top'
            
            if simRound=='MD4':
                topN = trjN.split('_md')[0]
                topAd = 'rawTrj/MD4-rwTop/'+topN+'.top'
                
            print topN
            f = open('cppASample_' + str(i), 'w')
            f.write('parm ' + topAd + '\n')
            f.write('trajin ' + trj  + '\n')
            f.write('parmbox alpha 90 beta 90 gamma 90\n')
            f.write('trajout AS1_SampleR4_' + str(i) + '.rst restart onlyframes ' + str(inf[i]['frame']) +'\n')
            f.write('parmwrite out SampleR4_' + str(i) +'.prmtop \n')
            f.write('run \n')
            f.write('quit')
            f.close()

########################################################################################################################
# This function generates the Cpptraj input files for extracting frames corresponding to the least populated clusters,
# It is useful trajectories with common topology files ( usually for striped trajectories)
########################################################################################################################

def CpptrajInGen_commonTop(topFile):
    import json
    inf = json.load(open("ClsInf.txt"))
    n_samples = len(inf)
    for i in range(n_samples):
            f = open('ccpASample_' + str(i), 'w')
            f.write('parm ' + topFile + '\n')
            trj = inf[i]['traj']
                
            f.write('trajin ' + trj  + '\n')
                
            f.write('parmbox alpha 90 beta 90 gamma 90\n')
            f.write('trajout Sample_' + str(i) + '.rst restart onlyframes ' + str(inf[i]['frame']) +'\n')
            f.write('parmwrite out Sample_' + str(i) +'.prmtop \n')
            f.write('run \n')
            f.write('quit \n')
            f.close()
###########################################################################################################################
# make ClsInf for informaions of one frame for each cluster
###########################################################################################################################
def writeOPF_all(l,T, myn_clusters, n_samples):
    import json
    OPF = []
    for i in range(n_samples):
            pos = findElementPosition(l, i)
            trj = int(pos[0])
            frm = int(pos[1])+1
            OPF.append({'cluster':i, 'traj':T[trj], 'frame':frm})
            print int(pos[1])+1 , int(pos[1])
    json.dump(OPF, open("ClsInf.txt",'w'))
    return OPF
###########################################################################################################################
# 
###########################################################################################################################
#ds = dataset('trj/*.xtc', topology='system.pdb')
#n_samples = 10
#selection = MSM.draw_samples(clustered, n_samples)
#samples = utils.map_drawn_samples(selection, ds, top ='system.pdb')

# pipeline!!!
