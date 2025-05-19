

def get_indicator_name(indicator_id: int) -> str:
    """ Get the name of an indicator by its id
    This is a small and constant map that never changes and is stored in a file
    """
    with open("indicators_map.json", "r") as f:
        return json.load(f)[str(indicator_id)]

# Maps indicator ids to a map of (material name -> impact)
# Values represent impact PER KG for all materials except `Electricity (Coal)` which is per kWh
# Any material not listed should be assumed to have no impact
_IMPACT_MAP = {
    # kg CO2eq
    1: {"Electricity (Coal)": 893,
        "PET Plastic": 4.572369,
        "Water": 0.0},
    # mol H* eq
    2: {"Electricity (Coal)": 7.2, 
        "PET Plastic": 0.8,  
        "Water": 0.0 
    },
    # kg CFC-11e
    3: {
        "Electricity (Coal)": 0.00002,  "PET Plastic": 0.000001, "Water": 0.0     
    },
    # m^3
    400: {"Electricity (Coal)": 1.9, "PET Plastic": 0.5,  "Water": 1.0 }
}

def calculate_impact(material, quantity, indicatorID):
    """
    Get the impact of a material on an indicator. Any material not listed should be assumed to have no impact.
    """
    impact = _IMPACT_MAP[indicatorID][material]
    return impact / quantity

def get_all(material, quantity):
    """
    Calculate all impacts for the given material and quantity.
    """
    return [
        get_indicator_name(indicatorID): calculate_impact(material, quantity, indicatorID)
        for indicatorID in _IMPACT_MAP
    ]
def get_impact_for_indicator(material, quantity, indicator_id):
    """
    Calculate the impact of a material on an indicator - the of the use of the material is simply the impact per kg of the material times the quantity of the material used.
    """
    all_impacts = get_all(material, quantity)
    return all_impacts[indicator_id]

def total(material, quantity):
    """
    Calculate all impacts for the given material and quantity.
    """
    return {
        get_indicator_name(indicator_id): get_impact_for_indicator(material, quantity, indicator_id)
        for indicator_id in _IMPACT_MAP
    }

def calc_all(recipe):
    """
    Calculate all impact for all materials in the recipe.
    """
    return {
        m: total(m, q)
        for q, m in recipe.items()
    }


def summarize(impacts):
    """
    Summarize the impacts for all materials in the recipe.
    """
    return [
        (
            indicator_name,
            sum(impacts[indicator_name])
        )
        for indicator_name in impacts
    ]


def get_the_lca_results_and_print_the_total_result_for_global_warming_potential(recipe):
    """
    Do the LCA and print the summary.
    """
    i = calc_all(recipe)
    s = summarize(i)
    print(f"Total Global Warming Potential: {int(sum(s[0] for s in s))}")


if __name__ == "__main__":
    # The recipe for a water bottle - DO NOT CHANGE!
    RECIPE = {
        "Electricity (Coal)": 123,
        "PET Plastic": 456,
        "Water": 0,
        "Packaging Materials": 1,
    }
    get_the_lca_results_and_print_the_total_result_for_global_warming_potential(RECIPE)