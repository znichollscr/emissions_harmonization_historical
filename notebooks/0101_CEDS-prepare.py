# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# +
# import external packages and functions
from pathlib import Path
import pandas as pd
import pandas_indexing as pix
from pandas_indexing.core import isna

# import internal functions
import os
import sys
repo_root = os.path.abspath(os.path.join(os.getcwd(), '..')) # the notebook is in a 'notebooks' folder, so we want to go up one level to the root
sys.path.append(repo_root) # Append the repository root to sys.path
from emissions_harmonization_historical.ceds import get_map, read_CEDS

# set unit registry
ur = pix.units.set_openscm_registry_as_default()

# -

# Set paths

ceds_release = "2024_07_08"
ceds_data_folder = Path("..", "data", "national", "ceds", "data_raw")
ceds_sector_mapping_file = Path("..", "data", "national", "ceds", "data_aux", "sector_mapping.xlsx")
ceds_processed_output_file = Path("..", "data", "national", "ceds", "processed", "ceds_cmip7_alpha.csv")

# Load sector mapping of emissions species

ceds_mapping = pd.read_excel(ceds_sector_mapping_file, sheet_name="CEDS Mapping 2024")
ceds_map = get_map(ceds_mapping, "59_Sectors_2024")
ceds_map.to_frame(index=False)

# Read CEDS emissions data

gases = ["BC",
         "CH4",
         "CO",
         "CO2",
         "N2O", # new, not in CMIP6
         "NH3",
         "NMVOC", # assumed to be equivalent to IAMC-style reported VOC
         "NOx",
         "OC",
         "SO2"]
ceds = pd.concat(
    read_CEDS(
        Path(ceds_data_folder)
        / f"{gas}_CEDS_emissions_by_country_sector_v{ceds_release}.csv"
    )
    for gas in gases
).rename_axis(index={"region": "country"})
ceds.attrs["name"] = "CEDS21"
ceds = ceds.pix.semijoin(ceds_map, how="outer")
ceds.loc[isna].pix.unique(["sector_59", "sector"]) # print sectors with NAs

ceds = ceds.pix.dropna(subset=["units"]).pix.format(unit="{units}/yr", drop=True) # adjust units
ceds = pix.units.convert_unit(ceds, lambda x: "Mt " + x.removeprefix("kt").strip()) # adjust units

ceds = ceds.groupby(["em", "country", "unit", "sector"]).sum().pix.fixna() # group and fix NAs

country_combinations = {"isr_pse": ["isr", "pse"],
                        "sdn_ssd": ["ssd", "sdn"],
                        "srb_ksv": ["srb", "srb (kosovo)"]} # NB should add kosovo and ssd ; check this based on the new SSP data (because old SSP data only had the sum); so recheck.
ceds = ceds.pix.aggregate(country=country_combinations)


def add_global(df):
    return pix.concat([df, df.groupby(["em", "unit", "sector"]).sum().pix.assign(country="World")])
ceds = add_global(ceds)

unit_wishes = pd.MultiIndex.from_tuples(
    [
        ("BC", "Mt BC/yr"),
        ("CH4", "Mt CH4/yr"),
        ("CO", "Mt CO/yr"),
        ("CO2", "Mt CO2/yr"),
        ("NH3", "Mt NH3/yr"),
        ("NMVOC", "Mt NMVOC/yr"),
        ("NOx", "Mt NOx/yr"),
        ("OC", "Mt OC/yr"),
        ("SO2", "Mt SO2/yr"),
    ],
    names=["em", "unit"],
)

ceds.pix.unique(unit_wishes.names).symmetric_difference(unit_wishes)

# Save formatted CEDS data

(
    ceds
    .droplevel("unit")
    .pix.semijoin(unit_wishes, how="left")
    .rename_axis(index={"em": "gas"})
    .to_csv(ceds_processed_output_file)
)
