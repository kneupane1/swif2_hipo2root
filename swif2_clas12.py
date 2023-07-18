
from pathlib import Path
import argparse
import numpy as np
from tqdm import tqdm
import copy
import json


def file_lookup(input_path):
    inputs = Path(input_path).rglob("*.root")
    inps = [{"local": fl.name, "remote": fl.as_posix()} for fl in inputs]
    print(inps)
    return inps

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
    file_tag = args.tag

    workflow_header = {
        "name": f"clas12_ana_{args.tag}",
        "max_dispatched": 1,
    }

    job = {
        # "name": "",
        "command": [f"{Path().absolute()}/clas12.sh"],
        "batch_flags": [
            "--account=clas12",
            "--time=06:00:00",
            "--cpus-per-task=16",
        ],
    }

    input_files = file_lookup(input_path)
    out_path = f"{args.output}"
    Path(out_path).mkdir(exist_ok=True, parents=True)
    out_file_type = "csv"

    jobs = []
    job['name'] = f"clas12_ana_{args.tag}"
    job["inputs"] = list(input_files)
    job["outputs"] = [{"local": "clas12.csv",
                      "remote": f'{out_path}/clas12.csv'}]
    job["batch_flags"].append(f"--job-name=clas12_ana_{args.tag}")
    jobs.append(job)

    workflow_header['jobs'] = jobs
    with open(f"clas12_ana_{args.tag}.json", "w") as outfile:
        outfile.write(json.dumps(workflow_header, indent=4))

    help_info = f"""

    To run using swif:

module load swif2
swif2 import -file clas12_ana_{args.tag}.json
swif2 run clas12_ana_{args.tag}
swif2 list

Use: https://scicomp.jlab.org/scicomp/swif/active to check active workflows
    """
    print(help_info)
