# Changelog for upcoming 1.0.1.rc1 release

## New Features

### General

- Limited taxa buttons in side panel to improve performance in data sets
with a large number of taxa (> 1000).

### Statistics

- Added character (nucleotide/residue) proportion for single genes plot.
This new plot can be viewed in absolute counts or proportion character
proportion.
- Added gene conservation plot for single genes.

## Improvements

### General

- Taxa information popup from the side panel are now dynamically fetched
and should be noticeable faster for large data sets.
- Added version option to all CLI interfaces via the "-v" or "--version"
options.

### Orthology

- Improved handling and sanity checking of input and output directories
for orthomcl_pipeline CLI interface.

### Statistics

- Automatic calculation of summary statistics has been disabled for
data sets with a large number of taxa (> 1000). Calculation of summary
statistics can still be triggered manually.

## Bug Fixes

### Orthology

- Fixed orthomcl_pipeline error when the input proteomes where not
properly sanitized (i.e., contain whitespace).

# Changelog for 1.0.0 release

## Bug fixes

### Process

- Improved recognition of Nexus interleave information [1.0.0rc1.dev1].

# Changelog for 1.0.0rc1 release

## New Features

## General

- Progressbar2 is now bundled with TriFusion to prevent import issues [0.5.3].
- Increased performance when updating app structures after loading alignment
files into TriFusion [0.5.13].

## Improvements

## General

- Added animation for dropdown menus [0.5.17].
- Increased efficiency of filechoosers when opening directories with
a great number of files [0.5.20].
- Improved item search in the main side panel [0.5.21].
- The order of partitions in the side panel and output files is now sorted
according to the starting position of the position [0.5.23].
- Added EPS, PS, JPEG and TIFF options as figure formats [0.5.33].

### Orthology

- Protein and nucleotide sequences exported by the Orthology module now have
the same header for each taxa. This makes it easier for downstream processing
of aligning concatenating, etc. [0.5.34].
- Added a backstage output file that makes the correspondance between the
unique headers of ortholog groups and their original header in the proteome
file [0.5.34].
- Added informative popups when comparing different group files with active
filters and/or excluded taxa [0.5.34].
- Added usearch and mcl checks before executing the orthomcl_pipeline [0.5.35].

### Process

- Refactored concatenation procedure increasing performance up to 29x in run
time [0.5.4].
- Added automatic recognition of "?" as missing data symbols, in addition to
"n" and "x" [0.5.5].
- Added option to invert selection of active Taxon/File buttons in the main
side panel [0.5.6].
- Greatly improved performance when importing partition scheme for large
alignments [0.5.7].
- Refactored Process backend to greatly improve performance of all operations,
mainly when dealing with many input alignments. [0.5.10].
- New output format dialog design that informs which formats are available for
main operations [0.5.11].
- Added check and warning when selecting output formats that are not valid
for the current main operation [0.5.11].
- Several minor UI improvements [0.5.12].
- Increased memory efficiency of Process execution [0.5.14].
- Output files are now correctly generated when non-contiguous partitions
are defined. These partitions are effectively merged before
writing the output files [0.5.23].
- Added error message when there are no output formats after ignoring
formats non-compliant with conversion/reverse concatenation [0.5.25].
- Added custom SNAPP output format extension [0.5.25].
- Added support for multiple sequence types (DNA and protein) for almost all
operations [0.5.30].
- Major improvement of the partition and substitution model setup in
certain output file formats (Nexus and Phylip) [0.5.30].
- Improved performance when toggling files/taxa on the side panel
[0.5.39].
- Improved performance on alignment reading for Unix operating systems
[0.5.40].

### Statistics

- Improved legend positioning [0.5.1].
- Homogenized axis labels and title aesthetic style across plots [0.5.1].
- Color maps are dynamically selected based on the number of categories,
resulting
in more distinguishable color palettes [0.5.1].
- Improved sliding window line plots. These line plots are now smoothed with
an interpolation,  allowing for a much better and fine grained color
transition [0.5.1].
- Improved dialogs and warnings for sliding window plots [0.5.27].

## Bug fixes

### General

- Fixed total data set information for taxon informative popup [0.5.16].
- Fixed text flickering for some informative popups [0.5.17].
- Fixed partition label update in side panel after merging or splitting [0.5.22].
- Fixed alignment counter for single partitions after splitting [0.5.23].
- Fixed occasional crash when canceling the loading of input files [0.5.31].
- Fixed removal of proteome files from selection in the side panel [0.5.33].

### Orthology

- Handled exception when orthology filters result in no data to be
plotted [0.5.6].
- Fixed import of some badly formatted group files in Orthology Explore
section [0.5.24].
- Fixed issue where the end of the orthology search operation would hold
indefinitely [0.5.28].
- Fixed minor issue with ortholog filter settings in explore section when
proteome files are loaded [0.5.29].
- Fixed issue where plots with no data would prevent the generation of a full
report [0.5.34].
- Fixed issues with orthomcl_pipeline that prevented the run from ending when
invalid input files were present in the input directory [0.5.35].

### Process

- Fixed 'ntax' parameter of NEXUS format when converting with custom active
taxa sets [0.5.2].
- Fixed issue when reverse concatenating directly from an incorrect partitions
file [0.5.8].
- Fixed issue when converting after specifying an output file for
concatenation. [0.5.11]
- Fixed missing informative popups for inactive files/taxa [0.5.15].
- Fixed several issues of the partition scheme when using custom file data sets
[0.5.18].
- Fixed issue with some Nexus badly formatted input files [0.5.19].
- Fixed several issues with partition and substitution model setup in Nexus
and Phylip output formats [0.5.30].
- Fixed issue with overwrite/skip/cancel when executing process operations
[0.5.32].
- Fixed issue with consensus using the first sequence method [0.5.37].
- Fixed issue preventing reverse concatenation from a single alignment
when multiple alignments were provided [0.5.38].
- Fixed issues with partitions when removing alignment files [0.5.38].

### Statistics

- Fixed color scheme for stacked bar plots that lumped together pairs
of categories [0.5.1].
- Fixed issue where removing taxa from the active taxa group would not
take effect on some operations of the Statistics module [0.5.36].