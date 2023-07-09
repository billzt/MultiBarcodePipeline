# MultiBarcodePipeline

The pipeline generates the most optimal single or multiple barcodes that could reach the highest resolution of taxonomy identification, based on provided amplicon sequences.

# External Dependencies
[MAFFT](https://mafft.cbrc.jp/alignment/software/) (v7.505 or compatible)

# Install
Linux OS is required. Please use conda to manage the environment. If you do not have a device running Linux OS, or you just want to have a quick look, you can try the [Docker version](https://github.com/billzt/MultiBarcodePipeline/blob/main/Docker.md)
```
$ conda create -n MultiBarcode python=3.9
$ conda activate MultiBarcode
$ git clone https://github.com/billzt/MultiBarcodePipeline.git
$ cd MultiBarcodePipeline
$ python3 setup.py develop
$ multi-barcode -h
```

# Test
## Default
```
$ cd test
$ multi-barcode amplicon_fish85_primers34.tsv 
```
The result is:
```
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Barcodes
# 1: West_FishF1_COX1, resolve  85 species
# ###########
# Number of Unresolved Species under diff=1: 0
# ###########
# See MultiBarcodeResult/matrix.xlsx for details
```
The result indicates that the `West_FishF1_COX1` barcode is best for the inputted 85 fishes, as **all** of them demonstrate amplicons with at least **1bp** variation under this barcode.

## Adjust the threshold of differences in amplicons
```
$ multi-barcode amplicon_fish85_primers34.tsv -d 8
```
The result is:
```
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Barcodes
# 1: Weigt_FISHCOI, resolve  83 species
# ###########
# Number of Unresolved Species under diff=8: 2
# ###########
# See MultiBarcodeResult/matrix.xlsx for details
```
Tips: Since we have not changed the default output directory after the previous run, it would **reuse** the previous alignment results.

The result indicates that the `Weigt_FISHCOI` barcode is best for the inputted 85 fishes, as **83** of them demonstrate amplicons with at least **8bp** variation under this barcode. No additional barcodes could increase the number of distinguished species.

## Use a preferred barcode
```
$ multi-barcode amplicon_fish85_primers34.tsv -p Miya_MiFish_U_12S
```
The result is:
```
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Barcodes
# 1: Miya_MiFish_U_12S, resolve  79 species
# 2: West_FishF2_COX1, resolve additional 6 species
# ###########
# Number of Unresolved Species under diff=1: 0
# ###########
# See MultiBarcodeResult/matrix.xlsx for details
```

The result indicates that the best combination is `Miya_MiFish_U_12S + West_FishF2_COX1`.

## Just view certain barcodes provided by users. Do not recommend new barcodes.
```
$ rm -rf MultiBarcodeResult/
$ multi-barcode amplicon_fish85_primers34.tsv -p Miya_MiFish_U_12S,Valentini_Teleo_12S -n 2
```
The result is:
```
# Sequence alignment: 0/2 barcodes finished
# Sequence alignment: 2/2 barcodes finished
# Step 2: Find Siblings for Each Target Species
# Tree analysis: 0/2 barcodes finished
# Tree analysis: 1/2 barcodes finished
# Tree analysis: 2/2 barcodes finished
# Step 3: Find Best Combination
# Finished
# ###########
# Number of Species: 85
# ###########
# Selected Barcodes
# 1: Miya_MiFish_U_12S, resolve  79 species
# 2: Valentini_Teleo_12S, resolve additional 4 species
# ###########
# Number of Unresolved Species under diff=1: 2
# ###########
# See MultiBarcodeResult/matrix.xlsx for details
```
The result indicates that `Miya_MiFish_U_12S + Valentini_Teleo_12S` can distinguish 83 (79+4) out of the 85 species. The remaining 2 species cannot be distinguished by them. Other barcodes were not calculated.

# Parameters
## Mandatory
a four-column-file in TSV format for amplicon sequences. Each line stands for an amplicon. Lines starting with `#` are ignored.
1. Sequence Name or ID (only use alphabets, numbers and underscores)
2. Barcode Name or ID (only use alphabets, numbers and underscores)
3. Species Name or ID (only use alphabets, numbers and underscores)
4. Amplicon-region DNA sequence

Multiple sequences from the same species are acceptable to deal with intra-species variations and polymorphisms.

An example

| Sequence Name  | Barcode Name | Species Name | Amplicon Seq. under this Barcode |
| ------------- | ------------- | ------------- |------------- |
| seqid_1  | p1  | tax1 | `ACAAAGTTTAACCATGTTAAACAACTTATTAAAGA`
| seqid_1b | p1  | tax1 | `ACAAAGTTTAACCATGCTAAACAACTTATTAAAGA`
| seqid_2  | p1  | tax2 | `ACCCAGTTTAACCATGCTAAACAACTTATTAAAGA`
| seqid_1  | p2  | tax1 | `CGCCTCTTGCATTCTACGTATAAGAGGTCCCGCCTG`
| seqid_2  | p2 | tax2 | `CGCCTCTTGCATTCTACGTATAAGATGTCCCGCCTG`


# Optional
```
  -h, --help            show this help message and exit
  -d THRESHOLD_DIFF, --threshold-diff THRESHOLD_DIFF
                        minimum DNA difference required for most closely related species under the same barcode (default: 1)
  -p PREFER, --prefer PREFER
                        preferred barcodes, in order, separated by comma. eg. barcode1,barcode2 (default: any)
  -n THRESHOLD_NUM, --threshold-num THRESHOLD_NUM
                        maximum number of selected barcodes. (default: 5)
  -t THREADS, --threads THREADS
                        number of CPUs (default: 4)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        directory for output (default: MultiBarcodeResult)
```




