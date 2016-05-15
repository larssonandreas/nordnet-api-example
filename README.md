# Description
Example client for connecting to the Nordnet API using Python 3.5 with the Crypto package using PKCS1_v1_5 and
PublicKey encryption modules. The client is intended for demo and educational purposes but could be altered to
be used for other purposes if needed.

Comments has been added in order to give breif guidance on what each section of the code does, however it is not
inteneded to be a "learn-to-program"-tutorial and prior coding experience is adviced.

The example code has (**on purpose**) been keept simple and scaled down in order to keep it to the bare essentiasl and
therefor it **DOES NOT** include any **exception/error handling** or logging.

# Up and running
The following steps needs to be completed in order to get the integration up and running.
* Step 1: Getting a developer account
 * Step 2: Install code dependencies and run the provided code

### Setting up the required accounts
Register an account with the Nordnet API developer programme to setup a username and password to be used with the code.
https://api.test.nordnet.se/

### Installation
```
1. Download the example code
2. Add your credentials to the crednetials.json file
3. run main.py
```

# Usage
In order to run the example and se the resulting output simply run.
```
python main.py
```

# Troubleshooting
The Crypto package has known troubles when running on python 3.5 when it comes to finiding the right internal modules.
If the pycrypto is installed using pip the package Crypto can on some ocasions yeild an error like "missing pacakge" or
similar.
```
ImportError: No module named Crypto.Cipher'
```
In order to solve this problem simply re-install the package with easy_install
```
pip uninstall pycrypto
easy_install pycrypto
```
# Warranty and Liability
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY.

# Keywords
* Python 3.5
* Nordnet
* Nordnet-API
* Crypto.Cipher import PKCS1_v1_5
* Crypto.PublicKey