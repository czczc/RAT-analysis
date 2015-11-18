#!/bin/bash
echo "cp -r KE450MeV_AB0cm KE$1MeV_AB0cm; pushd KE$1MeV_AB0cm; sed -i 's/450/$1/' gen.mac; ./run.sh; popd"
