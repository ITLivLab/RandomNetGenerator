import random
import graphviz as gv

from flask import Flask, request, Response, jsonify
from functools import wraps
import os

app = Flask(__name__)

profile_dir = "profiles/"
profiles = os.listdir(profile_dir)
nmap_profiles = {}

for aprofile in profiles:
    #nmap_profiles[aprofile] = open(profile_dir + aprofile).read().replace("\r\n", "<br />").replace("\n", "<br />")
    nmap_profiles[aprofile] = open(profile_dir + aprofile).read()

def graph_gen():
        g1 = gv.Graph(format='svg')
        g1.node('INTERNET',style='filled',color='blue',fontcolor='white')
        switches = []
        computers = []

        for i in range(0,random.randrange(2, 8, 2)):
                #print "Switch " + str(i)
                switches.append(i)
                g1.node('Switch ' + str(i), shape='box',style='filled',color='lightblue')

        #print ""
        for i in range(0,random.randrange(5, 15)):
                #print "Computer " + str(i)
                compname = str(i) + " " + random.choice(profiles)
                computers.append(compname)
                g1.node('Computer ' + compname, shape='square',style='filled')

        #print ""
        internet = random.choice(switches)
        for sw1 in switches:
                sw2 = random.choice(switches)
                if sw1 != sw2:
                        if random.randrange(0,20) == 13:
                                #print "Connecting HUB " + str(sw1) + " to " + str(sw2)
                                g1.edge('Switch ' + str(sw1), 'Switch ' + str(sw2))
                        else:
                                #print "Connecting " + str(sw1) + " to " + str(sw2)
                                g1.edge('Switch ' + str(sw1), 'Switch ' + str(sw2))

        #print ""
        for comp1 in computers:
                sw1 = random.choice(switches)
                #print "Connecting Computer " + str(comp1) + " to Switch " + str(sw1)
                g1.edge('Computer '+comp1, 'Switch ' +str(sw1))

        #print ""
        #print str(internet) + " is connected to the internet"
        g1.edge('Switch ' + str(internet), 'INTERNET')

        return g1.pipe()


@app.route('/')
def network():
    return "<!DOCTYPE html> <html> <body>" + graph_gen() + "<br /> <h1> SAVE THIS PAGE!! <br /> TO VIEW COMPUTER PROFILES GO TO /profile/FILENAME.txt </h1>" + "</body> </html>"

@app.route('/profile/<name>')
def ret_profile(name):
    return "<!DOCTYPE html> <html> <body> <pre>" + nmap_profiles[name] + "</pre> </body> </html>"

if __name__ == "__main__":
    #app.debug = True
    app.run(host="0.0.0.0", port=80)

