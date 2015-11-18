#!/usr/bin/env python

import pandas as pd
from numpy import random
import matplotlib.pyplot as plt
import sys #only needed to determine Python version number
import pylab

def main():
    # filename = r'results.txt'
    # filename = r'results_0cm.txt'
    filename = r'results_10cm.txt'
    df = pd.read_csv(filename, delim_whitespace=True)
    print df
    fig = plt.figure()
    # fig.suptitle('dE/dx [Absorber = 20 cm]', fontsize=14, fontweight='bold')
    fig.suptitle('dE/dx [Absorber = 10 cm]', fontsize=14, fontweight='bold')
    # fig.suptitle('dE/dx [No Absorber]', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Beam Proton Energy [MeV]')
    ax.set_ylabel('dE/dx [MeV/cm]')

    s1 = df.loc[df['volume'] == 'wbls1']
    s2 = df.loc[df['volume'] == 'wbls2']
    s3 = df.loc[df['volume'] == 'wbls3']
    s4 = df.loc[df['volume'] == 'wbls4']

    ax.plot(s1['initE'], s1['dEdx'], '-o', label='wbls1')
    ax.plot(s2['initE'], s2['dEdx'], '-o', label='wbls2')
    ax.plot(s3['initE'], s3['dEdx'], '-o', label='wbls3')
    ax.plot(s4['initE'], s4['dEdx'], '-o', label='wbls4')

    ax.legend()
    ax.set_xlim([200,475])
    plt.grid()

    # fig.savefig('1.png')
    # fig.savefig('E_0cm.png')
    fig.savefig('E_10cm.png')
    return df

def absorber():
    # filename = r'results.txt'
    # filename = r'results_0cm.txt'
    filename = r'results_240MeV.txt'
    df = pd.read_csv(filename, delim_whitespace=True)
    print df
    fig = plt.figure()
    # fig.suptitle('dE/dx [Absorber = 20 cm]', fontsize=14, fontweight='bold')
    fig.suptitle('dE/dx [Proton Energy = 240 MeV]', fontsize=14, fontweight='bold')
    # fig.suptitle('dE/dx [No Absorber]', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('HDPE Absorber Thickness [cm]')
    ax.set_ylabel('dE/dx [MeV/cm]')

    s1 = df.loc[df['volume'] == 'wbls1']
    s2 = df.loc[df['volume'] == 'wbls2']
    s3 = df.loc[df['volume'] == 'wbls3']
    s4 = df.loc[df['volume'] == 'wbls4']

    ax.plot(s1['absL'], s1['dEdx'], '-o', label='wbls1')
    ax.plot(s2['absL'], s2['dEdx'], '-o', label='wbls2')
    ax.plot(s3['absL'], s3['dEdx'], '-o', label='wbls3')
    ax.plot(s4['absL'], s4['dEdx'], '-o', label='wbls4')

    ax.legend(loc=2)
    ax.set_xlim([-0.2,26])
    plt.grid()

    # fig.savefig('1.png')
    # fig.savefig('E_0cm.png')
    fig.savefig('Abs_240MeV.png')
    return df

def eff():
    # filename = r'results.txt'
    # filename = r'results_0cm.txt'
    filename = r'eff_20cm.txt'
    df = pd.read_csv(filename, delim_whitespace=True)
    print df
    fig = plt.figure()
    fig.suptitle('Efficency [Absorber = 20 cm]', fontsize=14, fontweight='bold')
    # fig.suptitle('dE/dx [Proton Energy = 240 MeV]', fontsize=14, fontweight='bold')
    # fig.suptitle('dE/dx [No Absorber]', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Beam Proton Energy [MeV]')
    ax.set_ylabel('Trigger Efficency')

    s1 = df.loc[df['Trigger'] == 'H1+H2+H3+H4']
    s2 = df.loc[df['Trigger'] == 'H1+H2']
    s3 = df.loc[df['Trigger'] == 'H1+H2+H3']
    s4 = df.loc[df['Trigger'] == 'C1/(H1+H2+H3)']
    s5 = df.loc[df['Trigger'] == '(C1+C2)/(H1+H2+H3)']
    s6 = df.loc[df['Trigger'] == '(C1+C2+C3)/(H1+H2+H3)']
    s7 = df.loc[df['Trigger'] == '(C1+C2+C3+C4)/(H1+H2+H3)']

    ax.plot(s2['E'], s2['eff'], '-o', label='H1+H2')
    ax.plot(s3['E'], s3['eff'], '-o', label='H1+H2+H3')
    ax.plot(s1['E'], s1['eff'], '-o', label='H1+H2+H3+H4')
    # ax.plot(s4['E'], s4['eff'].multiply(s3['eff']), '-o', label='C1+H1+H2+H3')
    # ax.plot(s5['E'], s5['eff'].multiply(s3['eff']), '-o', label='C1+C2+H1+H2+H3')
    # ax.plot(s6['E'], s6['eff'].multiply(s3['eff']), '-o', label='C1+C2+C3+H1+H2+H3')
    # ax.plot(s7['E'], s7['eff'].multiply(s3['eff']), '-o', label='C1+C2+C3+C4+H1+H2+H3')

    ax.legend(loc=0)
    ax.set_xlim([200, 475])
    plt.grid()

    # fig.savefig('1.png')
    # fig.savefig('E_0cm.png')
    fig.savefig('eff_20cm.png')
    return df

if __name__ == "__main__":
    # df = main()
    # df = absorber()
    df = eff()