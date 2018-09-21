import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import h5py



def head_tail(vec) :
    """Affiche début et fin d'un vecteur."""
    chaine = '[ ' + str(vec[0]) + '   ' + str(vec[1]) + '   ' + str(vec[2])
    chaine += '   ...   '
    chaine += str(vec[-3]) + '   ' + str(vec[-2]) + '   ' + str(vec[-1]) + ' ]'

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
    Coordonnées, variables du système de N-S, tension de surface."""

    # -------------------------------------------------------------------------------------------------------
    # constructeur
    # -------------------------------------------------------------------------------------------------------
    def __init__(self, path_h5file) :
        """Constructeur. Lecture des fichiers h5"""
        # ---------------------------------------------------------------------------------------------------
        # pré-traitement
        # ---------------------------------------------------------------------------------------------------
        path_list = path_h5file.split('/')
        # nom du fichier h5 demandé par l'utilisateur
        self.user_h5 = path_list[-1]
        # suffixe pour noms des graphes
        self.suf = '-'.join([path_list[-3], path_list[-2]])
        # chemin d'accès aux données
        self.dir = '/'.join(path_list[0:-1])
        os.chdir(self.dir)
        # chemin d'accès aux graphes
        self.graphs = '/'.join(path_list[0:-4]) + '/graphs'

        # liste des fichier h5
        self.h5 = glob.glob('*.h5')
        # nombre de fichier h5
        self.nh5 = len(self.h5)

        # ensemble des données du fichier h5
        self.data = h5py.File(self.user_h5, 'r')
        # données concernant le fluide
        self.fluid = self.data['Fluid#0']

        # graphic parameters
        self.point_size = 5
        self.scale = 0.005
        self.scale2 = 0.05
        self.png = False

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
        file_name =  glob.glob('Solid_Kinematics*.csv')
        self.Pt = np.loadtxt(file_name[0], delimiter=',', skiprows=1)

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
        chaine += '\ny     : ' + head_tail(self.z)
        chaine += '\nvx    : ' + head_tail(self.vx)
        chaine += '\nvy    : ' + head_tail(self.vy)
        chaine += '\nvy    : ' + head_tail(self.vz)
        chaine += '\nP     : ' + head_tail(self.P)
        chaine += '\nkappa : ' + head_tail(self.kappa)
        chaine += '\nmvx   : ' + head_tail(self.mvx)
        chaine += '\nmvy   : ' + head_tail(self.mvy)
        chaine += '\nmvy   : ' + head_tail(self.mvz)
        chaine += '\nFTSx  : ' + head_tail(self.FTSx)
        chaine += '\nFTSy  : ' + head_tail(self.FTSy)
        chaine += '\nFTSy  : ' + head_tail(self.FTSz)
        chaine += '\nwGRPx : ' + head_tail(self.wGRPx)
        chaine += '\nwGRPy : ' + head_tail(self.wGRPy)
        chaine += '\nwGRPy : ' + head_tail(self.wGRPz)
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
        if len(np.shape(self.Pt)) == 1 :
            return(0, 0)
        #}
        tf = self.Pt[-1, 0]
        fig, ax = plt.subplots()
        ax.plot(self.Pt[:, 0], self.Pt[:, 24], label='Pression', linewidth=0.25)

        ax.set_xlim((0., tf))
        ax.set_xlabel('$t$ [s]')
        ax.set_ylabel('$P$ [Pa]')
        ax.set_title('Évolution de la pression')

        self.save_figure(fig, 'Pt')

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
        print('|         ', '|   min   ', '|  mean   ', '|   max   ', '|', sep='')
        print('|_________|_________|_________|_________|')
        print('|         |         |         |         |')
        print('| kappa   | %7.3f | %7.3f | %7.3f |' % (np.min(self.kappa[self.ic]), np.mean(self.kappa[self.ic]), np.max(self.kappa[self.ic])))
        print('|         |         |         |         |')
        print('| epsilon | %7.3f | %7.3f | %7.3f |' % (100*np.min(self.rel[self.ic]), 100*np.mean(self.rel[self.ic]), 100*np.max(self.rel[self.ic])))
        print('|_________|_________|_________|_________|')
    #}
#}