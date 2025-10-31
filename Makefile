.PHONY: run rig mesh rigmesh

run: rigmesh

rig:
	python main.py

mesh:
	python mesh.py

rigmesh:
	python rigmesh.py

