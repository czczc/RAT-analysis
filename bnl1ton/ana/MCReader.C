#include <iostream>
#include <iomanip>
#include <fstream>

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

void print_vector(ostream& out, vector<float>& v, TString desc, bool end=false);


void MCReader(int eventNo, TString option){
    int tmpcode;

    cout << "start: " << flush; tmpcode = system("date");

    DSReader r("test3.root");
    DS::Root *ds = r.GetEvent(eventNo-3);
    cout << "ds loaded: " << flush;  tmpcode = system("date");

    DS::MC *mc = ds->GetMC();
    int size_mc = mc->GetMCTrackCount();
    cout << "total tracks: " << size_mc << endl;

    vector<float> xx, yy, zz, tt, ll, wlwl;

    for (int i=0; i < size_mc; i++) {
        DS::MCTrack *track = mc->GetMCTrack(i);
        if (i % 100000 == 0) cout << "processing track " << i << endl;
        if (! (track->GetParticleName() == "opticalphoton") ) continue;
        int size_step = track->GetMCTrackStepCount();
        for (int j=0; j < size_step; j++) {
            DS::MCTrackStep *step = track->GetMCTrackStep(j); // Copy over initial step
            if ( option == "Cerenkov" ||
                 option == "Transportation" ||
                 option == "Attenuation" ||
                 option == "G4FastSimulationManagerProcess"
                ) {
                if (! (step->GetProcess() == option) ) continue;
            }
            else { cout << "Sorry, option not recognized" << endl; }
            TVector3 vec = step->GetEndpoint();
            // if (vec.Mag()>10000) continue;
            xx.push_back(vec.X()); yy.push_back(vec.Y()); zz.push_back(vec.Z());
            tt.push_back(step->GetGlobalTime());
            ll.push_back(step->GetLength());
            wlwl.push_back(1240e-6/step->GetKE()); // nm

            TString name = step->GetProcess();
            if (! ( name == "Cerenkov" ||
                    name == "Transportation" ||
                    name == "Attenuation" ||
                    name == "G4FastSimulationManagerProcess")
                ) {
                cout << step->GetProcess() << endl;
            }

            // if (! (step->GetProcess() == "Cerenkov") ) {

            // }
        }
    }
    cout << "end processing: " << flush;  tmpcode = system("date");

    TString rootFileName = TString::Format("%i-%s.root", eventNo, option.Data());
    float x, y, z, t, l, wl;
    TTree *tree = new TTree("MCTrack", "MC Track Info");
    tree->Branch("x", &x);
    tree->Branch("y", &y);
    tree->Branch("z", &z);
    tree->Branch("t", &t);
    tree->Branch("l", &l);
    tree->Branch("wl", &wl);
    TFile f(rootFileName.Data(), "recreate");
    int size = xx.size();
    for (int i=0; i<size; i++) {
        x = xx[i]; y = yy[i]; z = zz[i]; t = tt[i]; wl = wlwl[i]; l = ll[i];
        tree->Fill();
    }
    tree->Write();
    // TGraph2D g(x.size(), &x[0], &y[0], &z[0]);
    // g.Write();
    f.Close();
    cout << "ROOT file saved to " << rootFileName << endl;

    // TrackNav nav(ds, true);
    // TrackCursor c = nav.Cursor(true);
    // cout << "track loaded: " << flush;  tmpcode = system("date");

    TString jsonFileName = TString::Format("%i-%s.json", eventNo, option.Data());
    ofstream out(jsonFileName.Data());

    out << fixed << setprecision(0);
    out << "{" << endl;
    print_vector(out, xx, "x");
    print_vector(out, yy, "y");
    print_vector(out, zz, "z");

    out << fixed << setprecision(1);
    print_vector(out, tt, "t");

    out << '"' << "type" << '"' << ":" << '"' << "MCTrack" << '"' << endl;
    out << "}" << endl;

    out.close();
    cout << "JSON file saved to " << jsonFileName << endl;


}

void print_vector(ostream& out, vector<float>& v, TString desc, bool end)
{
    int N = v.size();

    out << '"' << desc << '"' << ":[";
    for (int i=0; i<N; i++) {
        out << v[i];
        if (i!=N-1) {
            out << ",";
        }
    }
    out << "]";
    if (!end) out << ",";
    out << endl;
}