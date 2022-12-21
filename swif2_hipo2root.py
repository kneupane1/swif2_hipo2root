
from pathlib import Path
import argparse
import numpy as np
from tqdm import tqdm
import copy
import json


def file_lookup(input_path, total=20000):
    inputs = Path(input_path).rglob("dst.hipo")
    inps = []
    for inp in tqdm(inputs, total=total):
        num = str(inp).split('/')[-2].split("_")[-1]
        job = str(inp).split('/')[-4].split("_")[-1]
        inps.append({"local": f"{job}_{int(num):06d}_{inp.name}", "remote": str(inp)})
    if len(inps) < total:
        print(
            f"Warning: Only found {len(inps)} of {total} expected files!\nMaybe the run isn't done yet.\nCheck before submitting to swif.")
    inps = sorted(inps, key=lambda d: d['local']) 
    #for ins in inps:
    #    print(ins['local'])
    return inps


def input_to_output(out_path, i):
    outs = []
    print(len(input_files))
    for inp in input_files:
        name = inp['local'].split('.')[0]
        num = inp['remote'].split('/')[-2].split("_")[-1]
        job = inp['remote'].split('/')[-4].split("_")[-1]

        outs.append({"local": f"{name}.{out_file_type}",
                    "remote": f"{out_path}/{name}_{job}_{int(num):06d}.{out_file_type}"})

    return outs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='swif2 workflow generatror')
    parser.add_argument("--input",
                        help="Path to input files",
                        type=str,
                        required=True
                        )
    parser.add_argument("--output",
                        help="Path to output files",
                        type=str,
                        required=True
                        )
    parser.add_argument("--tag",
                        help="Tag for naiming output files",
                        type=str,
                        required=True
                        )
    parser.add_argument("--split",
                        help="Number of final merge files to create",
                        type=int,
                        required=False,
                        default=20
                        )
    args = parser.parse_args()

    input_path = args.input
    sim_num = input_path.split("_")[-1].split("/")[0]

    file_tag = args.tag

    workflow_header = {
        "name": f"hipo2root_sim_num_{sim_num}",
        "max_dispatched": 500,
    }

    _job = {
        # "name": "",
        "command": [
            f"{Path().absolute()}/hipo2root.sh"
        ],
        "batch_flags": [
            "--account=clas12",
            "--time=06:00:00",
            "--cpus-per-task=16",
            "--job-name=hipo2root"
        ],
        # "inputs": [],
        # "outputs": []
    }

    input_files = file_lookup(input_path)
    out_path = f"{args.output}/{sim_num}"
    Path(out_path).mkdir(exist_ok=True, parents=True)
    out_file_type = "root"

    jobs = []
    inputs = np.array_split(input_files, 20)
    for i, split_inputs in enumerate(inputs):
        job = copy.deepcopy(_job)
        # output_files = input_to_output(split_inputs, out_path, out_file_type)
        job['name'] = f"hipo2root_{sim_num}_batch_{i}"
        job["inputs"] = list(split_inputs)
        job["outputs"] = [{"local": "merged.root",
                           "remote": f'{out_path}/{file_tag}_{i:03d}.root'}]
        job["batch_flags"][-1] = f"--job-name=hipo2root_sim_{sim_num}_batch_{i}"
        jobs.append(job)

    workflow_header['jobs'] = jobs
    with open(f"clas12_hipo2root_{sim_num}.json", "w") as outfile:
        outfile.write(json.dumps(workflow_header))

    help_info = f"""

    To run using swif:

module load swif2
swif2 import -file clas12_hipo2root_{sim_num}.json
swif2 run hipo2root_sim_num_{sim_num}
swif2 list

Use: https://scicomp.jlab.org/scicomp/swif/active to check active workflows
    """
    print(help_info)
