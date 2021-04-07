# Library Requirement
```python
pip3 install bitarray
pip3 install ecdsa
pip3 install pycryptodome
```

# How to install library offline on Pi
```
1) Download the library folder
2) Copy those files to Pi
    scp *tar.gz pi@192.168.1:
3) Go to your pi ssh and install them
    pip3 install bitarray.tar.gz
    pip3 install ecdsa.tar.gz
    pip3 install pycryptodome.tar.gz
```

# Fixing up ECDSA issue
The main problem of install ECDSA library is the non-existence of SEP128r1 curve which is required to generate 16 bytes key. The main reason is because the curve is not secure enough, hence there's no need to install that curve with the main library. But given this protocol description, we have to add that curve back to the library.

## On Computer
```
cd ~
git clone https://github.com/tlsfuzzer/python-ecdsa
sudo cp ~/python-ecdsa/src/ecdsa/*.py /usr/lib/python3/dist-packages/ecdsa
```

## On Pi
On Computer terminal
```
scp -r ~/python-ecdsa/src/ecdsa pi@192.168.4.1:~
```

Then on Pi terminal
```
sudo mv ~/ecdsa /usr/lib/python3/dist-packages/
```

