
from pathlib import Path
import argparse
import numpy as np
from tqdm import tqdm
import copy
import json
from dataclasses import dataclass, asdict
from typing import Union, List, AnyStr


@dataclass
class swif2_file:
    local: Union[AnyStr, Path]
    remote: Union[AnyStr, Path]


@dataclass
class swif2_job:
    name: AnyStr
    command: List[AnyStr]
    batch_flags: List[AnyStr]
    inputs: List[swif2_file]
    outputs: List[swif2_file]


@dataclass
class swif2_workflow:
    name: AnyStr
    jobs: List[swif2_job]
    max_dispatched: int = 500


def file_lookup(input_path, out_path):
    out_path = Path(out_path)
    out_path.mkdir(exist_ok=True, parents=True)
    inputs = Path(input_path).rglob("*.hipo")
    all_files = []
    for inp in tqdm(inputs):
        linked_file = {}

        name = inp.name[:-5]
        out_name = f"{name}.root"

        linked_file["name"] = name
        linked_file["inputs"] = [swif2_file(local=inp.name, remote=f"{inp}")]
        linked_file["outputs"] = [swif2_file(local=out_name, remote=out_path/out_name)]
        all_files.append(linked_file)

    return all_files


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

    all_files = file_lookup(args.input, args.output)
    all_jobs = []
    for fls in all_files:
        here = Path().cwd().absolute()
        command = f"{ here / 'hipo2root_data.sh'} {fls['inputs'][0].local} {fls['outputs'][0].local}"
        all_jobs.append(
            swif2_job(
                name=f"convert_{fls['name']}",
                command=[command],
                batch_flags=[
                    "--account=clas12",
                    "--time=01:00:00",
                    "--cpus-per-task=1",
                    f"--job-name=convert_{fls['name']}"
                ],
                inputs=fls['inputs'],
                outputs=fls['outputs']
            )
        )

    workflow = swif2_workflow(name=f"convert_{args.tag}", jobs=all_jobs)
    with open(f"convert_{args.tag}.json", "w") as outfile:
        outfile.write(json.dumps(asdict(workflow), indent=4, default=str))

    help_info = f"""

    To run using swif:

module load swif2
swif2 import -file convert_{args.tag}.json
swif2 run convert_{args.tag}
swif2 list

Use: https://scicomp.jlab.org/scicomp/swif/active to check active workflows
    """
    print(help_info)
