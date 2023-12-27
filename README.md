# metaswitch-sippswd-regsipbind
Python script that pulls SIP password and current UA strings from Registered SIP bindings via Metview Web API.

preload TNs in csv file, run scripts, output will be printed to output.csv in the same directory



## Using the tool
From the root directory

Install Requirements

```
pip3 install -r requirements.txt
```
Create a target list file, with a list of TNs that need to be searched

Example target list
```
TN
8125551234
8125554321
5055550000
5055551111
```

Call script and provide needed variables
```
python3 sippswd-regsipbind.py
```



Example Run
```
/metaswitch-sippswd-regsipbind$ python3 sippswd-regsipbind.py
MetaViewWeb Username:username
Password: 
MetaViewWeb Address:1.1.1.1
MetaViewWeb port:8087
MetaViewWeb version (example: 9.3):9.3
path to target list:target.csv
```

## Result
A file will be created, `output.csv` in the root directory, it will contain all sip passwords and UA strings

Example Output
```csv
DN,BGName,Pass_state,SIPPassword,Reg_UA1,Reg_UA2,Reg_UA3,Reg_UA4
8125551234,Example BG,bad pass,8125551234,Cisco/SPA525G2-7.6.2			
8125554321,Example BG,ok,C464133C5786,Cisco/SPA525G2-7.6.2			
5055550000,Example BG,bad_pass,password1,Cisco/SPA525G2-7.6.2			
5055551111,Example BG,bad_pass,123456789,Cisco/SPA525G2-7.6.2,Polycom/5.4.3.1014,PolycomVVX-VVX_411-UA/5.4.3.1014	
```