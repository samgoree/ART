ART

Categorizes files using adaptive resonance theory neural networks, based on an implementation at

http://mnemstudio.org/neural-networks-art1-example-1.htm

Usage: run ARTCategorizer.py [arg1]

where arg1 is the vigilance parameter

Reads input from standard input in the format of:

,label1,label2,label3,...

word1,percentage1,percentage2,percentage3,...

word2,percentage1,percentage2,percentage3,...

...

Prints output to stdout in the format of

word1,category

word2,category

...
