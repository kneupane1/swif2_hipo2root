# swif2_hipo2root
Using JLab swif2 to run a conversion and merging of hipo files to root files

### Usage
```
usage: swif2 workflow generatror [-h] --input INPUT --output OUTPUT --tag TAG [--split SPLIT]

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Path to input files
  --output OUTPUT  Path to output files
  --tag TAG        Tag for naiming output files
  --split SPLIT    Number of final merge files to create
```

### Example
```
python swif2_hipo2root.py --input /volatile/clas12/osg2/kneupane/job_5402 --output /volatile/clas12/users/tylern/merged_hipo --tag sim_name_type_settings
```
