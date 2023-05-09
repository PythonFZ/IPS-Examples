import ipsuite as ips


mapping = ips.geometry.BarycenterMapping(data=None)
thermostat = ips.calculators.LagevinThermostat(
    temperature=300, friction=0.01, time_step=0.5
)

with ips.Project(automatic_node_names=True) as project:
    mol = ips.configuration_generation.SmilesToAtoms(smiles="O")

    packmol = ips.configuration_generation.Packmol(
        data=[mol.atoms], count=[10], density=997
    )

    cp2k = ips.calculators.CP2KSinglePoint(
        data=packmol,
        cp2k_files=["GTH_BASIS_SETS", "GTH_POTENTIALS", "dftd3.dat"],
        cp2k_shell="cp2k_shell.psmp",
    )

    geopt = ips.calculators.ASEGeoOpt(
        model=cp2k,
        data=packmol.atoms,
        optimizer="BFGS",
        run_kwargs={"fmax": 0.1},
    )

    md = ips.calculators.ASEMD(
        model=cp2k,
        thermostat=thermostat,
        data=geopt.atoms,
        data_id=-1,
        sampling_rate=1,
        dump_rate=1,
        steps=250,
    )

    test_data = ips.configuration_selection.RandomSelection(data=md, n_configurations=50)
    val_data = ips.configuration_selection.RandomSelection(data=md, n_configurations=50, exclude_configurations=test_data.selected_configurations)
    train_data = ips.configuration_selection.RandomSelection(data=md, n_configurations=50, exclude_configurations=[test_data.selected_configurations, val_data.selected_configurations])

    model = ips.models.MACE(data=train_data, test_data=val_data)

    predictions = ips.analysis.Prediction(data=val_data, model=model)
    analysis = ips.analysis.PredictionMetrics(data=predictions)

    ml_md = ips.calculators.ASEMD(
        model=model,
        thermostat=thermostat,
        data=geopt.atoms,
        data_id=-1,
        sampling_rate=1,
        dump_rate=1,
        steps=5000,
    )

    dft_box_scale = ips.analysis.BoxScale(data=geopt.atoms, data_id=-1, mapping=mapping, start=0.9, stop=1.5, model=cp2k)
    ml_box_scale = ips.analysis.BoxScale(data=geopt.atoms, data_id=-1, mapping=mapping, start=0.9, stop=1.5, model=model)


project.run(repro=False)
