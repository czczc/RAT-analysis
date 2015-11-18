// volMap["unknown"] = 0;
// volMap["wbls1"] = 1;
// volMap["wbls2"] = 2;
// volMap["wbls3"] = 3;
// volMap["wbls4"] = 4;
// volMap["cuvette1"] = 5;
// volMap["cuvette2"] = 6;
// volMap["cuvette3"] = 7;
// volMap["cuvette4"] = 8;
// volMap["hodo1"] = 9;
// volMap["hodo2"] = 10;
// volMap["hodo3"] = 11;
// volMap["hodo4"] = 12;
// volMap["counter1"] = 13;
// volMap["counter2"] = 14;
// volMap["absorber"] = 15;
// volMap["air_box"] = 16;
// volMap["opSheet"] = 17;
// volMap["platform"] = 18;
// volMap["pmt"] = 19;

void ana(TString filename)
{
    // TString filename = "../gen/KE400MeV_AB20cm/mc.root";
    eff(filename);
    loss(filename);
}

void loss(TString filename)
{
    TFile *f = new TFile(filename.Data());
    TTree *t = (TTree*)f->Get("MC");

    int nTotal = t->GetEntries();
    TCanvas *c1 = new TCanvas();
    TH1F *h;

    TString H1H2H3 = "dE[9]>0.01 && dE[10]>0.01 && dE[11]>0.01";

    const int nVol = 16;
    string name[nVol]   = {"wbls1", "wbls2", "wbls3", "wbls4", "cuvette1", "cuvette2", "cuvette3", "cuvette4", "H1", "H2", "H3", "H4", "A1", "A2", "absorber", "air"};
    int index[nVol]     = {      1,       2,       3,       4,          5,          6,          7,          8,    9,   10,   11,   12,   13,   14,         15,    16};
    float mpv_min[nVol] = {      1,       1,       1,       1,        0.5,        0.5,        0.5,        0.5,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,        0.1,   0.1};
    float mpv_max[nVol] = {     10,      10,      10,      12,         10,         10,         10,         10,   10,   10,   10,   10,   10,   10,        100,    10};

    printf("\n%s\n", filename.Data());
    printf("-----------------------------------------\n");
    printf("%10s %6s %6s %6s %6s\n", "volume", "E[MeV]", "dE[MeV]", "dx[cm]", "dE/dx[MeV/cm]");
    printf("-----------------------------------------\n");

    for (int i=0; i<nVol; i++) {
        TString draw = TString::Format("dE[%i]>>h(10000,0,100)", index[i]);
        // cout << draw << endl;
        t->Draw(draw.Data(), H1H2H3);
        h = (TH1F*)gDirectory->FindObject("h");
        float mpv_dE = findMPV(h, mpv_min[i], mpv_max[i]);
        float mean_dE = findMean(h, mpv_min[i], mpv_max[i]);

        TString draw = TString::Format("energy[%i]>>h(100000,0,1000)", index[i]);
        t->Draw(draw.Data(), H1H2H3);
        h = (TH1F*)gDirectory->FindObject("h");
        float mpv_energy = findMPV(h, 10, 1000);
        float mean_energy = findMean(h, 10, 1000);

        TString draw = TString::Format("dx[%i]>>h(10000,0,1000)", index[i]);
        // cout << draw << endl;
        t->Draw(draw.Data(), H1H2H3);
        h = (TH1F*)gDirectory->FindObject("h");
        float mpv_dx = findMPV(h, 1, 1000)/10.;
        float mean_dx = findMean(h, 1, 1000)/10.;

        TString draw = TString::Format("dE[%i]/dx[%i]*10>>h(1200,0,12)", index[i], index[i]);
        // cout << draw << endl;
        t->Draw(draw.Data(), H1H2H3);
        h = (TH1F*)gDirectory->FindObject("h");
        float mpv_dEdx = findMPV(h, 0.1, 12);
        float mean_dEdx = findMean(h, 0.1, 12);

        printf("%10s %6.2f %6.2f %6.2f %6.2f\n", name[i].c_str(), mean_energy, mean_dE, mean_dx, mean_dEdx);
    }
    cout << "done" << endl;
}

float findMPV(TH1F* h, float start, float end)
{
    float max = 0;
    int startBin = start / h->GetBinWidth(1);
    int endBin = end / h->GetBinWidth(1);
    float maxBin = startBin;

    for (int i=startBin; i<=endBin; i++) {
        float val = h->GetBinContent(i);
        if (val>max) {
            max = val;
            maxBin = i;
        }
    }
    return h->GetBinLowEdge(maxBin);
}

float findMean(TH1F* h, float start, float end)
{
    h->GetXaxis()->SetRangeUser(start, end);
    return h->GetMean();
}

void eff(TString filename)
{
    TFile *f = new TFile(filename);
    TTree *t = (TTree*)f->Get("MC");

    int nTotal = t->GetEntries();

    TH1F *h;
    int n, nT3;
    TCanvas *c1 = new TCanvas();

    printf("--------------------- \n");
    printf("%12s %6s\n", "Trigger", "eff.");
    printf("--------------------- \n");

    TString H1 = "dE[9]>0.01";
    t->Draw("dE[1]>>h", H1);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%12s %6.3f\n", "H1", float(n)/nTotal);

    TString H1H2 = H1 + " && dE[10]>0.01";
    t->Draw("dE[1]>>h", H1H2);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%12s %6.3f\n", "H1+H2", float(n)/nTotal);

    TString H1H2H3 = H1H2 + " && dE[11]>0.01";
    t->Draw("dE[1]>>h", H1H2H3);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    nT3 = n;
    printf("%12s %6.3f\n", "H1+H2+H3", float(n)/nTotal);

    TString H1H2H3H4 = H1H2H3 + " && dE[12]>0.01";
    t->Draw("dE[1]>>h", H1H2H3H4);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%12s %6.3f\n", "H1+H2+H3+H4", float(n)/nTotal);

    printf("------------------------------------------- \n");

    printf("%27s %6s\n", "Cell Hit Under Trigger", "eff.");
    printf("------------------------------------------- \n");

    TString H1H2H3C1 = H1H2H3 + " && dE[1]>0.01";
    t->Draw("dE[1]>>h", H1H2H3C1);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%27s %6.3f\n", "C1/(H1+H2+H3)", float(n)/nT3);

    TString H1H2H3C1C2 = H1H2H3C1 + " && dE[2]>0.01";
    t->Draw("dE[1]>>h", H1H2H3C1C2);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%27s %6.3f\n", "(C1+C2)/(H1+H2+H3)", float(n)/nT3);

    TString H1H2H3C1C2C3 = H1H2H3C1C2 + " && dE[3]>0.01";
    t->Draw("dE[1]>>h", H1H2H3C1C2C3);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%27s %6.3f\n", "(C1+C2+C3)/(H1+H2+H3)", float(n)/nT3);

    TString H1H2H3C1C2C3C4 = H1H2H3C1C2C3 + " && dE[4]>0.01";
    t->Draw("dE[1]>>h", H1H2H3C1C2C3C4);
    h = (TH1F*)gDirectory->FindObject("h");
    n = h->GetEntries();
    printf("%27s %6.3f\n", "(C1+C2+C3+C4)/(H1+H2+H3)", float(n)/nT3);
}