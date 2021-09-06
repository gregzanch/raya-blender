# Raya (Blender Add-on)

This repository contains the source code for the Raya Blender Add-on. This Add-on was developed for Blender 2.93, although it's probably compatible with 2.80 or higher.

## Features

- Set Material parameters
  - Absorption coefficients - _Octave band 63-16000hz_
- Set Object parameters
  - Active - _Inactive objects are not included in solution_
  - Type
    - Reflector - _All reflecting surfaces (objects) are reflectors_
    - Source - _Where rays are emitted from_
    - Receiver - _Where the impulse response is recorded from_
- Set Solver parameters
  - Max Order - _maximum ray reflection order_
  - Ray Count - _total number of rays to trace_
- Export a raya file (.gltf)

## Installation

In Blender, Open the preferences (Edit > Preferences) and navigate to the `Add-ons` tab. Press `Install...` and then select the `Raya.zip` archive. After successful installation, make sure the Add-on is enabled (make sure the checkbox is checked).

See the [Blender manual](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons) for more detailed information.

## Usage

### Setting Material Parameters

In the materials tab, when a material is selected, there will be a `Material Parameters` section. This is where the material's absorption coefficients can be set.

![Material parameters figure](/doc/material-parameters.png)

### Setting Object Parameters

In the Raya UI Panel, when an object is selected, there will be an `Object Parameters` section. This is where the object's active state and type can be set.

![Object parameters figure](/doc/object-parameters.png)

#### Receiver Parameters

If the selected object is the `Receiver` type, a slider for the receiver radius appears. The receiver has a radius property because (currently) raya considers all receivers to be spherical; the actual geometry of the receiver is not considered.

![Object parameters figure](/doc/receiver-parameters.png)


### Setting Solver Parameters

In the Raya UI Panel, there will be a `Solver Parameters` section. This is where the solver's `max_order` and `ray_count` parameters can be set.

![Object parameters figure](/doc/solver-parameters.png)

### Exporting Raya File

In the Raya UI Panel, there will be an `Operations` section. This is where the file can be exported. 

1. Before exporting, press the `Apply All` button. This will make sure all of the Raya settings are applied.
2. Enter the desired export path in the `Export Path` field. NOTE: This needs to be an __absolute path__, and has to have the `.gltf` file extension.
3. Press the `Export` button.

![Object parameters figure](/doc/operations.png)

## Developing

The entire add-on is written in the `__init__.py` script. After modifying this file, either run the `package.sh` shell script:

```shell
sh ./package.sh
```

or create a directory called `Raya` and copy the `__init__.py` script into it. Then compress the `Raya` directory into a .zip file. NOTE: _The directory doesn't have to be named `Raya`_