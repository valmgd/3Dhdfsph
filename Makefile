# Chemin vers Dossier TS_SPHFLow3D
DIR = ~

.PHONY : current
current :
	./main.py $(DIR)/TS_SPHFlow3D/data/tX/RdxX-dxX/bulle1.h5

.PHONY : all
all :
	# un pas de temps
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx02_11-dx0_00050/bulle1.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx02_50-dx0_00050/bulle1.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx03_00-dx0_00050/bulle1.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx04_00-dx0_00050/bulle1.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx06_00-dx0_00033/bulle1.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx08_00-dx0_00025/bulle1.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_0s/Rdx10_00-dx0_00020/bulle1.h5

	# évolution d'une bulle à l'équilibre
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_5s/Rdx02_11-dx0_00050/bulle50.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_5s/Rdx02_50-dx0_00050/bulle50.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_5s/Rdx03_00-dx0_00050/bulle50.h5

	# évolution d'un cube
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_5c/Rdx03_00-dx0_00050/bulle88.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_5c/Rdx04_00-dx0_00050/bulle85.h5
	./main.py $(DIR)/TS_SPHFlow3D/data/t0_5c/Rdx04_00-dx0_00025/bulle500.h5

.PHONY : open
open :
	vim main.py plot.py Makefile