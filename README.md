# ctrlx-webserver

May 2024, DCEM Bosch Rexroth

Contact: Aria Malik Havidiansyah (ariamalik.havidiansyah@boschrexroth.de) and Raul Cruz Oliver (raul.cruz-oliver@boschrexroth.ch)

## Introduction

This repository contains the source code to build your own custom user interface based on a Python Flask webserver. The webserver communicates with the official ctrlX Motion app though the datalayer.

In the following image one can see an overview of the system topology. 

![alt text](docs/images/overview.png)

As presented in the image, the custom webserver is available through the port 5000. 

For complementary, we are showing that the basic web interface provided by ctrlX OS is available in the port 8443.

### Platform notes
This example has been developped for ctrlX OS 2.4, in which the official 2.4 version of the Motion App has been installed.

**NOTE:** In version 2.6 there would be substancial changes in the way metadata is managed, we will provide an example for this new ctrlX OS as soon at is available in a different branch in this repository. Stay tuned!

We assume the reader has access to the 2.4 ctrlX SDK and all the dependencies to build the python examples from such SDK are installed in the system in which this project is going to be compiled, if you are working in an the App-Build enviroment, the dependencies will be most likely installed in the system already. 

Apart from having such dependencies installed in the system (basically the datalayer and zmq packages, and of course snapcraft), this project is self contained and this repository can be cloned in any directory in your system and the automatic build scripts must run without errors.

## Files description

### Project README and LICENSE
- **README.md**
- **LICENSE**

### Snap build 
- **snap/snapcraft.yalm** : it contains the instructions to build the snap package
- **build-snap-amd64.sh** : it builds automatically the snap for amd64 platforms using snapcraft.
- **build-snap-arm64.sh** : it builds automatically the snap for arm64 platforms using snapcraft.

### Datalayer provider functionalities
- **datalayerProvider.py** : functionalities to create a datalayer node
- **app/my_provider_node.py\*** : implementation to create a datalayer node
- **metadata.cvs** : it contains the datalayer node metadata definition
- **mddb/\*** : it contains compiled datalayer node metadata

### Webserver backend
- **main.py** : it constaint the backend implementation

###  Webserver frontend
- **static/\*** : it contains javascript and css files
- **templates/index.html** : it constains the frontend implementation, with embedded javascript code

### Flatbuffers related 
- **flatbuffers\*** : it contains flatbuffer files (.fbs)
- **bfbs/\*** : it contains the binary files generated from flatbuffers files (.fbs)
- **motion/core/fbtypes\*** : it contains python libraries generated from flatbuffers files (.fbs) 
- **robot/core/fbtypes\*** : it contains python libraries generated from flatbuffers files (.fbs) 

### Automatic flatbuffers compiler
- **make-bfbs-pyfbs.sh** : it generates automatically binary files and python libraries from flatbuffers files (.fbs)
- **make-mddb.sh** : it generates automatically binary files 

### Compilation tools
- **bin/comm.datalayer/ubuntu22-gcc-x64/release/mddb_compiler** : tool to compile metadata files (.csv) into binary (.mddb)
- **bin/oss.flatbuffers/ubuntu22-gcc-x64/release/flatc** : tool to compile flatbuffer files (.fbs) into binary (.bfbs) and into pyhon libraries

### App manager and configuration
- **appdata/appdatacontrol.py** : functionalies to manage snap inside ctrlX OS
- **config/package-assets/ctrlx-webserver.package-manifest.json** : definitions to manage the snap inside ctrlX OS

### Documentation
- **docs/images\*** : images used in the README.md

### Python package setup files
- **setup.py**
- **setup.cfg**

### Other files
- **install-venv.sh** : automatically install the required packaged in virtual environment
- **requirements.txt** : dependenciies list that will be installed 
- **venv/\*** : it contains dependencies needed when working in a virtual environement
- **settings.py**


## Implementation information
This section contains practical information for custom implementations of datalayer nodes.

### Flatbuffers
Nodes in datalayer can be single basic datatypes such as float, string, integers, etc. or more complex data structures combining basic datatypes. 
One can define a custom data structure in the so-called flatbuffer. Flatbuffers are a technology developed by Google that automatically serilizes the data, allowing an efficient information flow.

we find three types of flatbuffer related files in ctrlX:
- **flatbuffers/xxx.fbs** : human language definition of the data stream
- **bfbs/xxx.bfbs** : compiled file generated from the .fbs. It contains the definition of the data stream. It is installed in ctrlX OS, so the data type is available.
- **xxx/xxx/fbtypes/xxx** : python libraries generated from the .fbs. It allows the use of the datatype in python programs.

If we are working with flatbuffers already defined by ctrlX, we can find the .bfbs and rhe python libraries in the official SDK. We suggest copying the required  pytho libraries, organised in folders in the sdk, directly to the project root. As an example, you can see what we did with the because theumotion/core/xxx. Note that you do not need the .bfbs because they are already installed in the ctrlX. 

If you want to work with a custom flatbuffer, you will need first to define it in the .fbs file, placing it in the "flatbuffers/" folder. Then, you need to generate the .bfbs and the python libraries. We have set up a .sh, called "make-bfbs-pyfbs.sh" that exposes the commands to do so, modify it for your needs. Once you execute those commands, you will get a .bfbs in the "/bfbs" directory, and python libraries in the root of the project. The /"bfbs/" will be dumped in the snap, and ctrlX OS will recognise the datatype.

#### .fbs file explanation

The .fbs file contains 3 main parts. Let's see those in the custom flatbuffer robotActualValues.fbs

```json
namespace robot.core.fbtypes;
```

This defines the structure for the python libraries that will be generated. The definition showed in the snipped will generate the python libraries inside a directory /motion/core/fbtypes. You can see other examples with the ctrlX already defined types

```json
/// actual values of the kinematics
table RobotActualValues {

  /// actual position
  actualPosX:double;

  actualPosY:double;
  
  actualPosZ:double;
}
```
This is the actual definition of the message and its name, in this case a concatenation of 3 double called RobotActualValues.

```json
root_type RobotActualValues;
```
This exposes the type name. For consistency, it is suggested to refer here with the flatbuffer definition gives in the previous part.

### Metadata
Nodes created in the datalayer might be complemented with metadata information. It specifies the data type of the information stored there, the access rights (read, write, etc.) among other features.

Until ctrlX OS 2.4, itself included, metadata is specified by the developper in a .csv file that must then be compiled using the process exposed in "./make-mddb.sh" into a binary file with extension .mddb. Modify the .sh file if needed. Such compiled file must be stored in a directory called "mddb", which is utimately dumped into the snap.

This above described procedure has been depreceated from ctrlX OS 2.6 onwards, where metadata will be directly specified in the node provider implementation. Stay tuned for an update of this project when this feature is available!

## Function Description
This is defined in the ctrlX Community post that can be found in the following [link](https://developer.community.boschrexroth.com/t5/ctrlX-Author-Team-Articles/SDK-Python-webserver-custom-User-Interface-for-Motion-App/ba-p/94933)





