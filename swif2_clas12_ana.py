
from pathlib import Path
import argparse
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


def file_lookup(input_path, out_path, number_files=10):
    out_path = Path(out_path)
    out_path.mkdir(exist_ok=True, parents=True)
    inputs = Path(input_path).rglob("*.root")
    all_files = []
    for i, inp in enumerate(inputs):
        linked_file = {}
        out_name = f"out_{inp.name}.root"

        linked_file["name"] = inp.name
        linked_file["inputs"] = [swif2_file(local=inp.name, remote=f"{inp}")]
        linked_file["outputs"] = [swif2_file(local="out.root", remote=out_path/out_name)]
        all_files.append(linked_file)
        if i > 10:
            break

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
    parser.add_argument("--test",
                        help="Number of final merge files to create",
                        type=bool,
                        required=False,
                        default=False
                        )
    args = parser.parse_args()

    all_files = file_lookup(args.input, args.output, 10 if args.test else 100_000_000)
    all_jobs = []
    for fls in all_files:
        here = Path().cwd().absolute()
        command = f"{ here / 'hipo2root_ana.sh'}"
        all_jobs.append(
            swif2_job(
                name=f"convert_{fls['name']}",
                command=[command],
                batch_flags=[
                    "--account=clas12",
                    "--time=01:00:00",
                    "--cpus-per-task=1",
                    f"--job-name=convert_{fls['name']}",
                    "--mem-per-cpu=8192"
                ],
                inputs=fls['inputs'],
                outputs=fls['outputs']
            )
        )

    workflow_json_name = f"analysis_{args.tag}"
    workflow = swif2_workflow(name=workflow_json_name, jobs=all_jobs)
    with open(f"{workflow_json_name}.json", "w") as outfile:
        outfile.write(json.dumps(asdict(workflow), indent=4, default=str))

    help_info = f"""

    To run using swif:

module load swif2
swif2 import -file {workflow_json_name}.json
swif2 run {workflow_json_name}
swif2 list

Use: https://scicomp.jlab.org/scicomp/swif/active to check active workflows
    """
    print(help_info)
