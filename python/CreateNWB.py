from datetime import datetime

from dateutil.tz import tzlocal
import pynwb
import platform
import hdmf
from LoadMatData import load_mat_file

from WriteMetadata import metadata


hdmf_ver = "v%s" % hdmf.__version__


def create_nwb_file(original_experiment_id):
    """
    Create an NWB file based on the metadata and data from the Gurnani and Silver 2021 paper.
    """
    print("Creating NWB file for experiment ID: %s" % original_experiment_id)

    mat_file = f"../data/{original_experiment_id}.mat"

    id, _, ymd, h, m, s = original_experiment_id.split("_")

    session_start_time = datetime(
        2000 + int(ymd[:2]),
        int(ymd[2:4]),
        int(ymd[4:6]),
        int(h),
        int(m),
        int(s),
        tzinfo=tzlocal(),
    )
    create_date = datetime.now(tz=tzlocal())

    nwb_file_info = (
        "NWB file based on data from %s, created with pynwb v%s (hdmf %s), Python v%s"
        % (
            metadata["paper_title"],
            pynwb.__version__,
            hdmf_ver,
            platform.python_version(),
        )
    )

    nwbfile = pynwb.NWBFile(
        session_description=metadata["reference"],
        identifier=original_experiment_id,
        session_start_time=session_start_time,
        file_create_date=create_date,
        notes=nwb_file_info,
        experimenter=metadata["experimenter"],
        experiment_description=metadata["experiment_description"],
        institution=metadata["institution"],
        lab=metadata["lab"],
    )

    # Load the .mat file
    (
        neuron_df_f_data,
        neuron_times,
        speed,
        whisker_motion_index,
        state,
        pca_dff,
        puff_events,
    ) = load_mat_file(mat_file)

    recorded_data = {
        "Wheel speed": speed,
        "Whisker Motion Index": whisker_motion_index,
        "State": state,
    }

    for key, value in recorded_data.items():
        print(f"Adding recorded data: {key} with shape {value.shape}")
        ts = pynwb.TimeSeries(
            name=key, data=value[1], unit="??", timestamps=value[0] / 1000
        )
        nwbfile.add_acquisition(ts)

    for i in range(len(neuron_df_f_data)):
        neuron_id = i + 1
        print("Adding neuron data %i" % neuron_id)
        data = neuron_df_f_data[i]

        timestamps = [t for t in neuron_times[i] / 1000]  # Convert to seconds

        ts = pynwb.TimeSeries(
            "Neuron %i fluorescence" % neuron_id, data, "seconds", timestamps=timestamps
        )

        nwbfile.add_acquisition(ts)

    nwb_file_name = "Gurnani2021.nwb"

    print("Saving NWB file: \n%s" % nwbfile)
    io = pynwb.NWBHDF5IO(nwb_file_name, mode="w")

    print("Written: %s" % nwb_file_name)

    io.write(nwbfile)
    io.close()

    return nwb_file_name


if __name__ == "__main__":
    original_experiment_id = "FL90__180316_15_20_48"
    nwb_file_name = create_nwb_file(original_experiment_id)
    print("NWB file created: %s" % nwb_file_name)
