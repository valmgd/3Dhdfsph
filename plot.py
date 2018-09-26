# -----------------------------------------------------------------------------------------------------------
# Objet Particles.
#
# État du nuage de particules à un temps fixé.
# -----------------------------------------------------------------------------------------------------------



import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import h5py
from mpl_toolkits.mplot3d import Axes3D



def head_tail(vec) :
    """Affiche début et fin d'un vecteur."""
    chaine = '[ ' + '   '.join(vec[:3])
    chaine += '   ...   '
    chaine += '   '.join(vec[-3:]) + ' ]'

    return(chaine)
#}

def set_graph_style(fig, ax) :
    """Basic settings for graph."""
    ax.set_aspect('equal', 'datalim')
    ax.set_facecolor('lavender')

    ax.legend(loc='best', fontsize='x-large', fancybox=True, framealpha=0.5)
    ax.grid(color='gray', linestyle='--')

    fig.tight_layout()
#}

def norm(x, y, z) :
    """Norme euclidienne."""
    return(np.sqrt(x**2 + y**2 + z**2))
#}



class Particles :
    """Classe Particles.

    Coordonnées, variables du système de N-S, tension de surface, etc.
    Permet un post-traitement pour évaluer la qualité des simulations SPH-Flow, en particulier pour le
    terme de tension de surface.
    
    Lecture d'un fichier h5 à un temps donné. On peut créer une liste d'objets pour avoir l'évolution en
    temps.
    
    Lecture du fichier Solid_Kinematics.csv pour évolution de la pression d'une particule au cours du
    temps."""

    # -------------------------------------------------------------------------------------------------------
    # constructeur
    # -------------------------------------------------------------------------------------------------------
    def __init__(self, path_h5file) :
        """Constructeur. Lecture des fichiers h5.
        
        Synopsis :
        x = Particles('chemin/vers/fichier/bulleX.h5')"""
        # ---------------------------------------------------------------------------------------------------
        # pré-traitement
        # ---------------------------------------------------------------------------------------------------
        # chemin d'accès aux données
        self.dir = os.path.dirname(os.path.realpath(path_h5file))
        os.chdir(self.dir)
        dir_list = self.dir.split('/')
        # nom du fichier h5 demandé par l'utilisateur
        self.user_h5 = path_h5file.split('/')[-1]
        # graph name suffix based on directory structure
        self.suf = '-'.join([dir_list[-2], dir_list[-1]])
        # chemin d'accès aux graphes
        self.graphs = '/'.join(dir_list[0:-3]) + '/graphs'
        # liste des fichier h5
        self.h5 = glob.glob('*.h5')
        # nombre de fichier h5
        self.nh5 = len(self.h5)

        print('# data directory     :', self.dir)
        print('# h5 file name       :', self.user_h5)
        print('# graphs path        :', self.graphs)
        print('# graphs name suffix :', self.suf)

        # ensemble des données du fichier h5
        self.data = h5py.File(self.user_h5, 'r')
        # données concernant le fluide
        self.fluid = self.data['Fluid#0']

        # graphic parameters
        self.point_size = 5
        self.scale = 0.005
        self.scale2 = 0.05
        self.png = True

        # ---------------------------------------------------------------------------------------------------
        # lecture des données
        # ---------------------------------------------------------------------------------------------------
        # coordonnées des particules
        self.x = np.array(self.fluid['X'])
        self.y = np.array(self.fluid['Y'])
        self.z = np.array(self.fluid['Z'])
        self.n = len(self.x)
        # volume
        self.w = np.array(self.fluid['Volume'])
        # masse volumique
        # vitesse
        self.vx = np.array(self.fluid['VX'])
        self.vy = np.array(self.fluid['VY'])
        self.vz = np.array(self.fluid['VZ'])
        # pression
        self.P = np.array(self.fluid['P'])

        # courbure
        self.kappa = np.array(self.fluid['Curvature'])
        # quantité de mouvement
        self.mvx = np.array(self.fluid['mvx'])
        self.mvy = np.array(self.fluid['mvy'])
        self.mvz = np.array(self.fluid['mvz'])

        # tension de surface
        self.FTSx = np.array(self.fluid['FTSx'])
        self.FTSy = np.array(self.fluid['FTSy'])
        self.FTSz = np.array(self.fluid['FTSz'])
        # tension de surface volumique
        self.wFTSx = self.w * self.FTSx
        self.wFTSy = self.w * self.FTSy
        self.wFTSz = self.w * self.FTSz

        # gradient de pression volumique
        self.wGRPx = np.array(self.fluid['wGRPx'])
        self.wGRPy = np.array(self.fluid['wGRPy'])
        self.wGRPz = np.array(self.fluid['wGRPz'])
        # gradient de pression
        self.GRPx = self.wGRPx / self.w
        self.GRPy = self.wGRPy / self.w
        self.GRPz = self.wGRPz / self.w

        self.rel = norm( self.mvx , self.mvy , self.mvz ) / norm( self.wGRPx , self.wGRPy , self.wGRPz )

        # évolution de la pression particule centrale
        file_sk =  glob.glob('Solid_Kinematics*')
        # présence du fichier Solid_Kinematics* (booléen)
        self.has_sk = (len(file_sk) >= 1)
        if self.has_sk :
            file_sk = file_sk[0]
        #}

        file_fc = glob.glob('FluidConservation*')[0]
        if file_fc[-3:] == 'csv' :
            delim = ','
            skip = 1
        elif file_fc[-3:] == 'dat' :
            delim = '  '
            skip = 7
        #}

        self.fluid_conservation = np.loadtxt(file_fc, delimiter=delim, skiprows=skip)


        # simulation sur + de 1 pas de temps ? (booléen)
        self.evolutif = False

        if self.has_sk :
            self.solid_kinematics   = np.loadtxt(file_sk, delimiter=delim, skiprows=1)
            # simulation sur + de 1 pas de temps ? (booléen)
            self.evolutif = (len(np.shape(self.solid_kinematics)) == 2)
            if self.evolutif :
                self.time = self.solid_kinematics[:-5, 0]
                self.Pt = self.solid_kinematics[:-5, 24]
                self.EC = self.fluid_conservation[:-5, 3]
            #}
        #}

        # ---------------------------------------------------------------------------------------------------
        # post-traitement
        # ---------------------------------------------------------------------------------------------------
        # indices des points de la couronne (indices pour lesquels la courbure est non nulle)
        self.ic = [i for i, elt in enumerate(self.kappa) if elt > 1]
    #}

    # -------------------------------------------------------------------------------------------------------
    # représentation
    # -------------------------------------------------------------------------------------------------------
    def __repr__(self) :
        """Vecteurs lus dans les fichiers h5."""
        chaine  = 'Read from files :'
        chaine += '\nx     : ' + head_tail(self.x)
        chaine += '\ny     : ' + head_tail(self.y)
        chaine += '\nz     : ' + head_tail(self.z)
        chaine += '\nvx    : ' + head_tail(self.vx)
        chaine += '\nvy    : ' + head_tail(self.vy)
        chaine += '\nvz    : ' + head_tail(self.vz)
        chaine += '\nP     : ' + head_tail(self.P)
        chaine += '\nkappa : ' + head_tail(self.kappa)
        chaine += '\nmvx   : ' + head_tail(self.mvx)
        chaine += '\nmvy   : ' + head_tail(self.mvy)
        chaine += '\nmvz   : ' + head_tail(self.mvz)
        chaine += '\nFTSx  : ' + head_tail(self.FTSx)
        chaine += '\nFTSy  : ' + head_tail(self.FTSy)
        chaine += '\nFTSz  : ' + head_tail(self.FTSz)
        chaine += '\nwGRPx : ' + head_tail(self.wGRPx)
        chaine += '\nwGRPy : ' + head_tail(self.wGRPy)
        chaine += '\nwGRPz : ' + head_tail(self.wGRPz)
        chaine += '\nw     : ' + head_tail(self.w)

        return(chaine)
    #}

    # -------------------------------------------------------------------------------------------------------
    # save figure in pdf and png format
    # -------------------------------------------------------------------------------------------------------
    def save_figure(self, fig, fname) :
        """Enregistre un graphe en pdf et éventuellement png."""
        fig.savefig(self.graphs + '/' + fname + '_' + self.suf + '.pdf')

        if self.png :
            fig.savefig(self.graphs + '/' + fname + '_' + self.suf + '.png', dpi=500)
        #}
    #}

    # -------------------------------------------------------------------------------------------------------
    # plot évolution de la pression de la particule centrale
    # -------------------------------------------------------------------------------------------------------
    def plot_P(self) :
        """Plot l'évolution de la pression de la particule centrale au cours du temps."""

        tf = self.time[-1]
        fig, ax = plt.subplots()
        ax.plot(self.time, self.Pt, label='Pression', linewidth=0.25)

        ax.set_xlim((0., tf))
        # ax.set_ylim((min(self.Pt), max(self.Pt)))
        # ax.set_ylim((-50, 50))
        ax.set_xlabel('$t$ [s]')
        ax.set_ylabel('$P$ [Pa]')
        ax.set_title('Évolution de la pression')

        self.save_figure(fig, 'Pt')

        return(fig, ax)
    #}

    # -------------------------------------------------------------------------------------------------------
    # plot énergie cinétique
    # -------------------------------------------------------------------------------------------------------
    def plot_EC(self) :
        """Plot l'évolution de la pression de la particule centrale au cours du temps."""

        tf = self.time[-1]
        fig, ax = plt.subplots()
        ax.plot(self.time, self.EC, label='Pression', linewidth=1, c='orangered')

        ax.set_xlim((0., tf))
        ax.set_xlabel('$t$ [s]')
        ax.set_ylabel('$EC$')
        ax.set_title('Évolution de l\'énergie cinétique')

        self.save_figure(fig, 'EC')

        return(fig, ax)
    #}

    # -------------------------------------------------------------------------------------------------------
    # plot nuage de particules
    # -------------------------------------------------------------------------------------------------------
    def plot_part(self) :
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # ax.scatter(self.x, self.y, self.z)
        return(fig, ax)
    #}

    # -------------------------------------------------------------------------------------------------------
    # somme de la quantité de mouvement sur un quartier de la bulle
    # -------------------------------------------------------------------------------------------------------
    def quarter(self) :
        """Somme les vecteurs de quantité de mouvement sur un quartier de la bulle."""
        n = len(self.x)
        somme_x = somme_y = somme_z = 0.
        for i in range(0, n) :
            if self.x[i] >= 0 and self.y[i] >= 0 :
                somme_x += self.mvx[i]
                somme_y += self.mvy[i]
                somme_z += self.mvz[i]
            #}
        #}
        return(somme_x, somme_y, somme_z)
    #}

    # -------------------------------------------------------------------------------------------------------
    # Infos sur la simulation
    # -------------------------------------------------------------------------------------------------------
    def info_simu(self) :
        """Info diverses sur la simu."""
        # somme sur un quartier
        somme_x, somme_y, somme_z = self.quarter()
        print('Somme Dmv/Dt sur un quartier : [', somme_x, ',', somme_y, ',', somme_z, ']')

        # intervalle de pression
        Pmin = str(min(self.P[self.ic]))
        Pmax = str(max(self.P[self.ic]))
        print('Intervalle de pression       : [', Pmin, ',', Pmax, ']')

        # Courbure attendue
        print('Courbure attendue            :', 2 * (1 / (3*sum(self.w) / (4*np.pi))**(1/3)))

        # table de courbure et erreur relative
        print(' _______________________________________')
        print('|         |         |         |         |')
        print('|         |   min   |  mean   |   max   |')
        print('|_________|_________|_________|_________|')
        print('|         |         |         |         |')
        print('| kappa   | %7.3f | %7.3f | %7.3f |' % (np.min(self.kappa[self.ic]), np.mean(self.kappa[self.ic]), np.max(self.kappa[self.ic])))
        print('|         |         |         |         |')
        print('| epsilon | %7.3f | %7.3f | %7.3f |' % (100*np.min(self.rel[self.ic]), 100*np.mean(self.rel[self.ic]), 100*np.max(self.rel[self.ic])))
        print('|_________|_________|_________|_________|')
    #}
#}