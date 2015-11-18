{
    gROOT->ProcessLine(".x loadClasses.C");
    // MCReader("KE240MeV_AB20cm_veto_5x5gen.root", "mc.root", 0);
    // MCReader("KE450MeV_AB20cm.root", "check.root", 2, 244);
    MCReader("KE240MeV_AB20cm_veto_5x5gen.root", "check.root", 2, 329);
}