# Use the Docker version

## Install Docker

Please refer to [Docker's manual page](https://docs.docker.com/get-docker/).

## Pull the image of MultiBarcodePipeline

```bash
docker pull taobioinfo/multibarcodepipeline:latest
```

## Run

```bash
# Get testing data from GitHub
git clone https://github.com/billzt/MultiBarcodePipeline.git
cd MultiBarcodePipeline/test

# run
# the parameter (TSV table) must be in relative path starting from the current working directory
docker run --rm --workdir=/home -v $(pwd):/home docker.io/taobioinfo/multibarcodepipeline amplicon_fish85_primers34.tsv
```

## Limitations

* Running speed is much slower than that on native Linux OS.
* Paths of the inputted TSV table must be in **relative path starting from the current working directory**. That is, `./amplicon_fish85_primers34.tsv` is OK, but `/home/user/data/amplicon_fish85_primers34.tsv` cannot be used.
