#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstdio>

#include <RAT/Config.hh>
#include <RAT/DSReader.hh>
// #include <RAT/Processor.hh>
// #include <RAT/Log.hh>
#include <RAT/DS/Root.hh>
// #include <RAT/TrackNav.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCTrack.hh>
#include <RAT/DS/MCTrackStep.hh>

#include "TFile.h"
#include "TTree.h"
#include "TGraph2D.h"
#include "TString.h"

using namespace std;
using namespace RAT;

void MCReader(string inputFileName, string outputFileName="mc.root", int verbose=0, int showOne=-1)
{
    int tmpcode;
    cout << "start: " << flush; tmpcode = system("date");

    DSReader r(inputFileName.c_str());

    TFile f(outputFileName.c_str(), "recreate");

    map<string, int> volMap;
    volMap["unknown"] = 0;
    volMap["wbls1"] = 1;
    volMap["wbls2"] = 2;
    volMap["wbls3"] = 3;
    volMap["wbls4"] = 4;
    volMap["cuvette1"] = 5;
    volMap["cuvette2"] = 6;
    volMap["cuvette3"] = 7;
    volMap["cuvette4"] = 8;
    volMap["hodo1"] = 9;
    volMap["hodo2"] = 10;
    volMap["hodo3"] = 11;
    volMap["hodo4"] = 12;
    volMap["counter1"] = 13;
    volMap["counter2"] = 14;
    volMap["absorber"] = 15;
    volMap["air_box"] = 16;
    volMap["opSheet"] = 17;
    volMap["platform"] = 18;
    volMap["pmt"] = 19;
    volMap["veto"] = 20;
    volMap["veto_hole"] = 21;


    const int nVolume = 22;
    float gen_x, gen_y, gen_z;
    int gen_pdg;
    float dE[nVolume], dx[nVolume], energy[nVolume], t[nVolume];
    float e_dE[nVolume], e_dx[nVolume], e_energy[nVolume], e_t[nVolume];
    float p_dE[nVolume], p_dx[nVolume], p_energy[nVolume], p_t[nVolume];
    TTree *tree = new TTree("MC", "MC Info");
    tree->Branch("gen_x", &gen_x);
    tree->Branch("gen_y", &gen_y);
    tree->Branch("gen_z", &gen_z);
    tree->Branch("gen_pdg", &gen_pdg);
    tree->Branch("dE", dE, "dE[22]/F");
    tree->Branch("dx", dx, "dx[22]/F");
    tree->Branch("energy", energy, "energy[22]/F");
    tree->Branch("t", t, "t[22]/F");
    tree->Branch("e_dE", e_dE, "e_dE[22]/F");
    tree->Branch("e_dx", e_dx, "e_dx[22]/F");
    tree->Branch("e_energy", e_energy, "e_energy[22]/F");
    tree->Branch("e_t", e_t, "e_t[22]/F");
    tree->Branch("p_dE", p_dE, "p_dE[22]/F");
    tree->Branch("p_dx", p_dx, "p_dx[22]/F");
    tree->Branch("p_energy", p_energy, "p_energy[22]/F");
    tree->Branch("p_t", p_t, "p_t[22]/F");
    for (int i=0; i<nVolume; i++) {
        dE[i] = 0;
        dx[i] = 0;
        energy[i] = 0;
        t[i] = 0;
        e_dE[i] = 0;
        e_dx[i] = 0;
        e_energy[i] = 0;
        e_t[i] = 0;
        p_dE[i] = 0;
        p_dx[i] = 0;
        p_energy[i] = 0;
        p_t[i] = 0;
    }

    int nEntries = r.GetTotal();
    int startEntry = 0;
    int endEntry = nEntries;
    if (showOne>=0) { startEntry=showOne; endEntry=showOne+1; }
    for (int entry=startEntry; entry<endEntry; entry++) {
        DS::Root *ds = r.GetEvent(entry);
        DS::MC *mc = ds->GetMC();

        DS::MCParticle *particle = mc->GetMCParticle(0);
        gen_x = particle->GetPosition().X();
        gen_y = particle->GetPosition().Y();
        gen_z = particle->GetPosition().Z();
        gen_pdg = particle->GetPDGCode();


        int nTracks = mc->GetMCTrackCount();
        // cout << "total tracks: " << nTracks << endl;

        if (entry % 100 == 0) cout << "processing event " << entry << endl;

        // cout << "ds loaded: " << flush;  tmpcode = system("date");
        for (int i=0; i < nTracks; i++) {
            DS::MCTrack *track = mc->GetMCTrack(i);
            // if (i % 100000 == 0) cout << "processing track " << i << endl;
            int track_id = track->GetID();
            int track_pdg = track->GetPDGCode();
            float track_length = track->GetLength();
            int nSteps = track->GetMCTrackStepCount();

            // if (track_id!=1 && track_pdg==2212) {
            //     cout << "id: " << track_id << ", pdg: " << track_pdg << " " << track->GetParticleName()
            //          << ", length: " << track_length << ", steps: " << nSteps
            //          << ", mother: " << track->GetParentID() << endl;
            // }
            if (!(track_id == 1 || track_pdg == 11 || track_pdg == -11 || track_pdg == 2212)) continue; // only check primary proton, e+/-


            if (verbose>=1) {
                cout << "id: " << track_id << ", pdg: " << track_pdg << " " << track->GetParticleName()
                     << ", length: " << track_length << ", steps: " << nSteps
                     << ", mother: " << track->GetParentID() << endl;
            }

            float lastStepKE = track->GetMCTrackStep(0)->GetKE();
            for (int j=0; j < nSteps; j++) {
                DS::MCTrackStep *step = track->GetMCTrackStep(j);
                string volname = step->GetVolume();
                if (volname == "virtual_target" || volname == "world") continue;

                string process = step->GetProcess();
                float step_length = step->GetLength();
                float step_KE = step->GetKE();
                float step_dE = lastStepKE - step_KE;
                if (volname.find("opSheet")!=string::npos) { volname = "opSheet"; }
                else if (volname.find("pmt")!=string::npos) { volname = "pmt"; }

                int vol_id = volMap[volname];
                if (vol_id == 0) { cout << "unknown volume: " << volname << endl; exit(0); }
                if (track_id == 1) {  // for proton energy loss
                    dE[vol_id] += step_dE;
                    dx[vol_id] += step_length;
                    energy[vol_id] = step_KE; // this will record the KE in the last step of the volume.
                    t[vol_id] = step->GetGlobalTime(); // same as above
                }
                else if (track_pdg == 2212) {  // for secondary energy loss
                    p_dE[vol_id] += step_dE;
                    p_dx[vol_id] += step_length;
                    p_energy[vol_id] = step_KE; // this will record the KE in the last step of the volume.
                    p_t[vol_id] = step->GetGlobalTime(); // same as above
                }
                else {  // for secondary energy loss
                    e_dE[vol_id] += step_dE;
                    e_dx[vol_id] += step_length;
                    e_energy[vol_id] = step_KE; // this will record the KE in the last step of the volume.
                    e_t[vol_id] = step->GetGlobalTime(); // same as above
                }


                if (verbose>=2 && vol_id == 1) {
                    printf("  %15s %8.2f %8.2f %8.2f %15s", volname.c_str(), step_length, step_KE, step_dE, process.c_str());
                    cout << endl;
                }

                lastStepKE = step_KE;
            }

        }
        tree->Fill();

        for (int i=0; i<nVolume; i++) {
            dE[i] = 0;
            dx[i] = 0;
            energy[i] = 0;
            t[i] = 0;
            e_dE[i] = 0;
            e_dx[i] = 0;
            e_energy[i] = 0;
            e_t[i] = 0;
            p_dE[i] = 0;
            p_dx[i] = 0;
            p_energy[i] = 0;
            p_t[i] = 0;
        }
    }

    cout << "end processing: " << flush;  tmpcode = system("date");

    tree->Write();
    f.Close();
    cout << "ROOT file saved to " << outputFileName << endl;

}
