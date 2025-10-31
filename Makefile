.PHONY: run rig mesh rigmesh

run: rigmesh

rig:
	python rig.py

mesh:
	python mesh.py

rigmesh:
	python rigmesh.py

