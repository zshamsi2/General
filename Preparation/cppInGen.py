import glob

for f in glob.glob('*.mdcrd'):
    a = f.split('/')[-1]
    name = a.strip('.mdcrd')
    filename = 'cpp_'+name+'.in'
    f = open(filename, 'w')
    f.write('parm NOP-SS.prmtop \n')
    f.write('trajin ' + name + '.mdcrd\n')
    f.write('strip :PA\n')
    f.write('strip :PC\n')
    f.write('strip :OL')
    f.write('strip :WAT')
    f.write('center origin')
    f.write('autoimage origin')
    f.write('trajout ' + name +'_strip.mdcrd\n')
    f.write('run \n')
    f.write('quit')

