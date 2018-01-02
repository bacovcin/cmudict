This is a fork of the cmudict that converts the vowels to the Philadelphia System vowel codes introduced by Bill Labov.

The conversion code (convert\_dict.py and cmu\_phoneset) is derived from scripts that are part of [the FAVE project](https://github.com/JoFrhwld/FAVE).

The output of the file is cmudict-plotnik.dict. The only difference from cmudict.dict is that all of the vowel phones have been replaced with the Labovian vowel codes (e.g., iyC, e). Stress information has been retained after the new vowel codes. The vowel codes and the stress code (0, 1, 2) are now separated by a full stop.
