#!/home/vmagda/.anaconda3/bin/python

# -----------------------------------------------------------------------------------------------------------
# Stage vmagda avril-septembre 2018.
#
# Données issues de simulations SPH-Flow en 3D.
# Programme de post-traitement pour évaluation de la qualité du modèle de tension de surface. S'adapte aux
# simulations sur un pas de temps et aux simulations évolutives. Lecture des fichiers h5 et des fichiers de
# type Solid_Kinematics.csv et Fluid_Conservation.csv.
#
# python --version
# Python 3.6.5 :: Anaconda, Inc.
#
# SYNOPSIS :
# ./main.py [path to]/TS_SPHFlow3D/data/tX/RdxX-dxX/bulle1.h5
#
# Respecter la structure du dossier TS_SPHFlow3D. Voir README.md à la racine de TS_SPHFlow3D.
# -----------------------------------------------------------------------------------------------------------

# python packages
import sys

# personnal sources
from plot import Particles



# -----------------------------------------------------------------------------------------------------------
# données
# -----------------------------------------------------------------------------------------------------------
path_to_h5 = sys.argv[1]
print('# ----------------------------------------------------')
print('#', path_to_h5)
print('# ----------------------------------------------------')
part = Particles(path_to_h5)



# -----------------------------------------------------------------------------------------------------------
# Graphes
# -----------------------------------------------------------------------------------------------------------
if part.evolutif :
    part.plot_P()
    part.plot_EC()
#}



# -----------------------------------------------------------------------------------------------------------
# Infos
# -----------------------------------------------------------------------------------------------------------
part.info_simu()





# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# plt.show()