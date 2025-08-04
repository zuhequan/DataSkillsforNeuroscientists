import json
import yaml

metadata = {}

metadata["comment"] = (
    "Structured metadata file for the dataset used in the Gurnani and Silver 2021 paper."
)

metadata["reference"] = "Experiment from Gurnani and Silver 2021"

metadata["paper_title"] = (
    "Multidimensional population activity in an electrically coupled inhibitory circuit in the cerebellar cortex"
)
metadata["paper_authors"] = ["Harsha Gurnani", "R. Angus Silver"]
metadata["experimenter"] = "Harsha Gurnani"

metadata["experiment_description"] = (
    "This dataset was generated for the study 'Multidimensional population activity in an electrically coupled inhibitory circuit in the cerebellar cortex' by Gurnani and Silver in Neuron, 2021. It includes pre-processed two-photon imaging data and behavioural data from head-fixed awake mice exhibiting spontaneous whisking and locomotion on a cylindrical wheel."
)

metadata["institution"] = "University College London"
metadata["lab"] = "Silver Lab"


if __name__ == "__main__":
    metadata_json_file = "../data/metadata.json"
    with open(metadata_json_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print("Metadata saved to %s" % metadata_json_file)

    metadata_yaml_file = "../data/metadata.yaml"
    with open(metadata_yaml_file, "w") as f:
        yaml.dump(metadata, f, indent=4)
    print("Metadata saved to %s" % metadata_yaml_file)
