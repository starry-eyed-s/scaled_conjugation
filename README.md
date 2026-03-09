
Lexically-Scaled MaxEnt learning on Korean Irregular Verb/Adjective Conjugation
========================================================================================

This repository contains a modified implementation of the original Lexically-Scaled MaxEnt model (Hughto et al., 2019), updated to allow different priors on distinct morphological constituents. It also includes training-data generation code, toy datasets modeled after Korean regular and irregular verb/adjective conjugation, and empirical data extracted from the Korean Google Treebank Corpus.

* The code runs on Python 3.  
  `train.py` takes largely the same arguments as the original model, except that the user must now manually specify three separate lambda values:

    - LAMBDA1  
    - LAMBDA2 (for the stem or preceding morphological constituent)  
    - LAMBDA3 (for the suffix or succeeding morphological constituent)

  **Usage:**
  
    ```bash
    python3 train.py \
        METHOD NEG_WEIGHTS NEG_SCALES \
        LAMBDA1 LAMBDA2 LAMBDA3 \
        L2_PRIOR INIT_WEIGHT RAND_WEIGHTS \
        ETA EPOCHS TD_FILE LANGUAGE OUTPUT_DIR
    ```

* Training output file names now explicitly indicate the epoch, learning rate, and all three priors applied during generation, making it easier to track experimental settings.

## Organization

Training data and simulation outputs are organized into three folders corresponding to the experimental conditions:

* **Toy_balanced**: Statistically balanced toy dataset and simulation outputs for paradigms including -/t/- and -/s/-final conjugations.
* **Toy_imbalanced**: Statistically imbalanced toy dataset and simulation outputs for paradigms including -/p/-, -/t/-, and -/s/-final conjugations.
* **Google_Treebank**: Simulations based on fully empirical corpus data from the Korean Google Treebank Corpus, downloaded from https://github.com/emorynlp/ud-korean/tree/master/google


## Toy data

For the toy-data simulations, the data-generation script and the generated training `.tsv` files are stored in the `data` subfolder:

* `multi_suffix.py`
* Generated training files: `2suffix.tsv`, `4suffix.tsv`, `6suffix.tsv`, `8suffix.tsv`, `10suffix.tsv`

The toy stems and their ID-mapped versions are stored in:

* `toy_stems.json` (generated toy stems)
* `toy_stems_with_id.json` (stems with mapped morpheme IDs)


## Empirical data 

For the empirical condition, the extracted -p/-t/-s-final stem conjugation data are stored in `google_treebank.tsv`. The constituent stem and suffix morphemes are further organized and mapped onto distinct IDs in `stem_suffix_id_map.tsv`.

This organization allows us to track which stems or suffixes receive scale weights, since the weights are not cleanly partitioned by stem class or suffix type but are instead distributed across individual morphemes.

