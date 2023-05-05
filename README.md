# MLeDNA

The pipeline generates the most optimal single or multiple primers that could facilitate the highest resolution of taxonomic identification, considering the given amplicon sequences.

# External Dependencies
[MAFFT](https://mafft.cbrc.jp/alignment/software/) (v7.505 or compatible)

# Install
Currently only support Linux. Please use conda to manage the environment.
```
$ conda create -n MLeDNA python=3.9
$ conda activate MLeDNA
$ git clone https://github.com/billzt/MLeDNA-cli.git
$ cd MLeDNA
$ python3 setup.py develop
$ mledna -h
```

# Test
## Default
```
$ cd test
$ mledna amplicon_fish85_primers34.tsv 
```
The result is:
```
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Primers
# 1: West_FishF1_COX1, resolve  85 species
# ###########
# Number of Unresolved Species under diff=1: 0
# ###########
# See MLeDNAResult/matrix.xlsx for details
```
The result indicates that the `West_FishF1_COX1` primer is best for the inputted 85 fishes, as **all** of them demonstrate amplicons with at least **1bp** variation under this primer.
## Adjust the threshold of differences in amplicons
```
$ mledna amplicon_fish85_primers34.tsv -d 8
```
The result is:
```
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Primers
# 1: Weigt_FISHCOI, resolve  83 species
# ###########
# Number of Unresolved Species under diff=8: 2
# ###########
# See MLeDNAResult/matrix.xlsx for details
```
Note: Since we did not change the default output directory, it would **reuse** the previous alignment results.

The result indicates that the `Weigt_FISHCOI` primer is best for the inputted 85 fishes, as **83** of them demonstrate amplicons with at least **8bp** variation under this primer. No additional primers could increase the distinguished species.

## Use a preferred primer
```
$ mledna amplicon_fish85_primers34.tsv -p Miya_MiFish_U_12S
```
The result is:
```
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Primers
# 1: Miya_MiFish_U_12S, resolve  79 species
# 2: West_FishF2_COX1, resolve additional 6 species
# ###########
# Number of Unresolved Species under diff=1: 0
# ###########
# See MLeDNAResult/matrix.xlsx for details
```

The result indicates that the best combination is `Miya_MiFish_U_12S + West_FishF2_COX1`.

## Just view certain primers provided by users. Do not recommend other primers.
```
$ rm -rf MLeDNAResult/
$ mledna amplicon_fish85_primers34.tsv -p Miya_MiFish_U_12S,Valentini_Teleo_12S -n 2
```
The result is:
```
# Sequence alignment: 0/2 primers finished
# Sequence alignment: 2/2 primers finished
# Step 2: Find Siblings for Each Target Species
# Tree analysis: 0/2 primers finished
# Tree analysis: 1/2 primers finished
# Tree analysis: 2/2 primers finished
# Step 3: Find Best Locus Combination
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Primers
# 1: Miya_MiFish_U_12S, resolve  79 species
# 2: Valentini_Teleo_12S, resolve additional 4 species
# ###########
# Number of Unresolved Species under diff=1: 2
# ###########
# See MLeDNAResult/matrix.xlsx for details
```
The result indicates that `Miya_MiFish_U_12S + Valentini_Teleo_12S` can distinguish 83 (79+4) out of 85 species. The remaining 2 species cannot be distinguished by them. Other primers were not calculated.

# Parameters
## Mandatory
a four-column-file in TSV format for amplicon sequences. Each line stands for an amplicon. Lines starting with `#` are ignored.
1. Primer Name or ID (only use alphabets, numbers and underscores)
2. Sequence Name or ID (only use alphabets, numbers and underscores)
3. Species Name or ID (only use alphabets, numbers and underscores)
4. Sequence

Multiple sequences for the same species is allowed.

| Primer Name  | Sequence Name | Species Name | Amplicons under this Primer |
| ------------- | ------------- | ------------- |------------- |
| p1  | seqid_1  | tax1 | `ACAAAGTTTAACCATGTTAAACAACTTATTAAAGA`
| p1  | seqid_1b  | tax1 | `ACAAAGTTTAACCATGCTAAACAACTTATTAAAGA`
| p1  | seqid_2  | tax2 | `ACCCAGTTTAACCATGCTAAACAACTTATTAAAGA`
| p2  | seqid_1  | tax1 | `CGCCTCTTGCATTCTACGTATAAGAGGTCCCGCCTG`
| p2  | seqid_2  | tax2 | `CGCCTCTTGCATTCTACGTATAAGATGTCCCGCCTG`


# Optional
```
  -h, --help            show this help message and exit
  -d THRESHOLD_DIFF, --threshold-diff THRESHOLD_DIFF
                        minimum DNA difference required for nearest siblings (default: 1)
  -p PRIMERS, --primers PRIMERS
                        preferred primers separated by comma. eg. primer1,primer2 (default: any)
  -n THRESHOLD_NUM, --threshold-num THRESHOLD_NUM
                        maximum number of selected primers. (default: 5)
  -t THREADS, --threads THREADS
                        number of CPUs (default: 4)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        directory for output (default: MLeDNAResult)
```




