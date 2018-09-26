#!/home/vmagda/.anaconda3/bin/python

# -----------------------------------------------------------------------------------------------------------
#
#
#         .d8888b.  8888888b.       888           888  .d888       .d8888b.  8888888b.  888    888 
#        d88P  Y88b 888  "Y88b      888           888 d88P"       d88P  Y88b 888   Y88b 888    888 
#             .d88P 888    888      888           888 888         Y88b.      888    888 888    888 
#            8888"  888    888      88888b.   .d88888 888888       "Y888b.   888   d88P 8888888888 
#             "Y8b. 888    888      888 "88b d88" 888 888             "Y88b. 8888888P"  888    888 
#        888    888 888    888      888  888 888  888 888               "888 888        888    888 
#        Y88b  d88P 888  .d88P      888  888 Y88b 888 888         Y88b  d88P 888        888    888 
#         "Y8888P"  8888888P"       888  888  "Y88888 888          "Y8888P"  888        888    888 
#
#
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
# ./main.py path/to/bulleX.h5
# Penser à adapter le Shebang ligne 1.
#
# /!\ Respecter la structure du dossier TS_SPHFlow3D. Voir README.md à la racine de TS_SPHFlow3D.
# -----------------------------------------------------------------------------------------------------------

# python packages
import sys
import numpy as np
import matplotlib.pyplot as plt

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