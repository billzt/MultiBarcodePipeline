# Use the Docker version

## Install Docker

Please refer to [Docker's manual page](https://docs.docker.com/get-docker/).

## Pull the image of MiFish

```bash
docker pull taobioinfo/multibarcodepipeline:latest
```

Old versions are also [available](https://hub.docker.com/repository/docker/taobioinfo/multibarcodepipeline/tags), though not recommended.

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
