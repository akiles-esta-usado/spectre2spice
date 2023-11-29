# Spectre2Spice
This is a fork of [Spectre2Spice](https://codeberg.org/thommythomaso/spectre2spice).


## Description
Spectre2Spice is a standalone application to translate netlists from the Cadence Spectre Circuit Simulator format to SPICE.

## Usage
~~~sh
spectre2spice -h
~~~

## Installation

### Install in local environment

Recommended for development

~~~sh
make venv
~~~

Internally, it creates a virtual environment with `venv` and then installs it with `python3 -m pip install -e .`

Modifications in code will be reflected in the module. To activate it, execute:

~~~sh
. .venv/bin/activate
~~~

### Install in system

Not recommended until its finished.

~~~sh
python3 -m pip install --user .
~~~

Eventually we can put it into pypi.

## Example netlist
An example netlist is included to test Spectre2Spice.
Run the following command to start the translation:
~~~sh
spectre2spice example/ my_top.scs output/ tech_example/
~~~

With logging activated:
~~~sh
spectre2spice example/ my_top.scs output/ tech_example/ --log_path logs/
~~~

## Run the translated netlist
~~~sh
ngspice output/my_top.sp
~~~

Once ngspice is running type run the simulation like this:
~~~
op
~~~

With 
~~~
print all
~~~

the node voltages can be displayed. Expected is:
~~~
v_v0#branch = -8.90967e-05
v_v1#branch = 0.000000e+00
vd = 2.409033e+00
vdd = 3.300000e+00
vg = 2.000000e+00
~~~