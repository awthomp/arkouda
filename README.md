# arkouda
arkouda python/chapel package

 * requires chapel 1.19.0
 * requires llvm version of Chapel parser to support HDF5 I/O
 * requires zeromq version >= 4.2.5, tested with 4.2.5 and 4.3.1
 * requires python 3.6 or greater
```bash
# it should be simple to get things going on a mac�
brew install chapel # needs to change because of HDF5 I/O which needs a build with export CHPL_LLVM=llvm
brew install python3
brew install zeromq
pip3 install numpy
pip3 install pandas
pip3 install jupyter
```
 * setup your CHPL_HOME env variable and source $CHPL_HOME/util/setchplenv.bash
 * compile arkouda_server.chpl
 * don't forget the --fast flag on the compile line
 * need to use the -senableParScan config param on the compile line
 * you may also need to use -I to find zmq.h and -L to find libzmq.a
```bash
chpl --fast -senableParScan arkouda_server.chpl
```
```bash
chpl --ccflags=-Wno-incompatible-pointer-types --cache-remote --fast -senableParScan arkouda_server.chpl
```
 * startup the arkouda_server
 * defaults to port 5555
```bash
./arkouda_server
```
 * config var on the commandline
  * --v=true/false to turn on/off verbose messages from server
  * --ServerPort=5555
 * or you could run it this way if you don't want as many messages
and a different port to be used
```bash
./arkouda_server --ServerPort=5555 --v=false
```
 * in the same directory in a different terminal window
 * run the ak_test.py python3 program
 * this program just does a couple things and calls shutdown for the server
 * edit the server and port in the script to something other than the
default if you ran the server on a different server or port
```bash
./ak_test.py
```
or
```bash
python3 ak_test.py
```
 * This also works fine from a jupyter notebook
 * there is an included Jupyter notebook called test_arkouda.ipynb

### Naming conventions for code

#### Python3
 * camelCase for variable names
```python
printThreshold = 100
```
 * names with underscores for functions
```python
def print_it(x):
    print(x)
```
#### Chapel
 * camelCase for variable names and procedures
```chapel
var aX: [{0..#s}] real;
proc printIt(x) {
     writeln(x);
}
````
 * CamelCase for Class names
 ```chapel
 class Foo: FooParent
 {}
 ```
 