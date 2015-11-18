{
    gROOT->ProcessLine(".x loadClasses.C");
    int eventNo = 3;
    MCReader(eventNo, "Cerenkov");
    MCReader(eventNo, "Transportation");
    MCReader(eventNo, "Attenuation");
    MCReader(eventNo, "G4FastSimulationManagerProcess");
}