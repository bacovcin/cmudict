"""Converts the CMUdict to include the Plotnik style vowels
   (Primarily derived from plotnik.py in JoFrhwld/FAVE)"""

# CMU phoneset (distinctive features) to Plotnik coding
MANNER = {'s': '1', 'a': '2', 'f': '3', 'n': '4', 'l': '5', 'r': '6'}
PLACE = {'l': '1', 'a': '4', 'p': '5', 'b': '2', 'd': '3', 'v': '6'}
VOICE = {'-': '1', '+': '2'}

# CMU phones
CONSONANTS = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M',
              'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z',
              'ZH']
VOWELS = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH',
          'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
SPECIAL = ['BR', 'CG', 'LS', 'LG', 'NS']


class Phone:
    """represents a CMU dict phoneme (label and distinctive features)"""
    # !!! not to be confused with class extractFormants.Phone !!!
    label = ''  # label
    vclass = ''  # vocalic (+ = vocalic, - = consonantal)
    vlng = ''  # vowel length (l = long, s = short, d = diphthong, a = ???, 0 = n/a)
    vheight = ''  # vowel height (1 = high, 2 = mid, 3 = low)
    vfront = ''  # vowel frontness (1 = front, 2 = central, 3 = back)
    vrnd = ''  # vowel roundness (+ = rounded, - = unrounded, 0 = n/a)
    ctype = ''  # manner of articulation (s = stop, a = affricate, f = fricative, n = nasal, l = lateral, r = glide, 0 = n/a)
    cplace = ''  # place of articulation (l = labial, b = labiodental, d = dental, a = apical, p = palatal, v = velar, 0 = n/a)
    cvox = ''  # consonant voicing (+ = voiced, - = unvoiced, 0 = n/a)


def read_phoneset(f):
    """reads the CMU phoneset (assigns distinctive features to each phoneme);
      returns it as dictionary object (taken from JoFrhwld/FAVE)"""
    lines = open(f, 'r').readlines()
    phoneset = {}
    for line in lines[1:]:  # leave out header line
        phone = Phone()
        line = line.rstrip('\n')
        sline = line.split()
        label = sline[0]  # phoneme label
        phone.label = label
        phone.vclass = sline[1]  # vocalic
        phone.vlng = sline[2]  # vowel length
        phone.vheight = sline[3]  # vowel height
        phone.vfront = sline[4]  # vowel frontness
        phone.vrnd = sline[5]  # vowel roundness
        phone.ctype = sline[6]  # consonants:  manner of articulation
        phone.cplace = sline[7]  # consonants:  place of articulation
        phone.cvox = sline[8]  # consonants:  voicing
        phoneset[label] = phone
    return phoneset

A2P = {'AA': 'o',
       'AE': 'ae',
       'AH': 'uh',
       'AO': 'oh',
       'AW': 'aw',
       'AY': 'ay',
       'EH': 'e',
       'ER': '*hr',
       'EY': 'ey',
       'IH': 'i',
       'IY': 'iy',
       'OW': 'ow',
       'OY': 'oy',
       'UH': 'u',
       'UW': 'uw'}
A2P_R = {'EH': 'e',
         'AE': 'ae',
         'IH': 'iyr',
         'IY': 'iyr',
         'EY': 'eyr',
         'AA': 'ahr',
         'AO': 'owr',
         'OW': 'owr',
         'UH': 'uwr',
         'UW': 'uwr',
         'AH': 'uh',
         'AW': 'aw',
         'AY': 'ay',
         'OY': 'oy'}

INGLIDERS = ['FATHER', 'FATHER', "FATHER'S", 'MA', "MA'S", 'PA',
             "PA'S", 'SPA', 'SPAS', "SPA'S", 'CHICAGO', "CHICAGO'S", 'PASTA',
             'BRA', 'BRAS', "BRA'S", 'UTAH', 'TACO', 'TACOS', "TACO'S",
             'GRANDFATHER', 'GRANDFATHERS', "GRANDFATHER'S", 'CALM', 'CALMER',
             'CALMEST', 'CALMING', 'CALMED', 'CALMS', 'PALM', 'PALMS', 'BALM',
             'BALMS', 'ALMOND', 'ALMONDS', 'LAGER', 'SALAMI', 'NIRVANA',
             'KARATE', 'AH']


def philadelphia_postconversion(lex, phones, prec, i, fol, curcode, phoneset):
    """Deals with Philadelphia specific complications"""
    vowel = phones[i].rstrip('012')
    stress = phones[i][-1]
    # 1. /aeh/ and /aey/:  tense and variable short-a
    phone = phones[i]
    if (curcode == 'ae' and
        phone == 'AE1' and
        lex not in ['AND', "AN'", 'AM', 'AN', 'THAN'] and
        phoneset[fol].ctype != 0):
        # /aeh/:  tense short-a

        # mad, bad, glad and derived forms
        if lex in ['MAD', 'BAD', 'GLAD', 'MADLY', 'BADLY', 'GLADLY', 'MADDER',
                   'BADDER', 'GLADDER', 'MADDEST', 'BADDEST', 'GLADDEST',
                   'MADNESS', 'GLADNESS', 'BADNESS', 'MADHOUSE']:
            return 'aeh'

        # /aey/:  variable short-a

        if lex in ['RAN', 'SWAM', 'BEGAN', 'CAN', 'FAMILY', 'FAMILIES',
                   "FAMILY'S", 'JANUARY', 'ANNUAL', 'ANNE', "ANNE'S", 'ANNIE',
                   "ANNIE'S", 'JOANNE', 'GAS', 'GASES', 'EXAM', 'EXAMS',
                   "EXAM'S", 'ALAS', 'ASPIRIN']:
            return 'aeBR'

        # following /l/
        if phones[i + 1] == 'L':
            return 'aeBR'

        # -SKV- words, e.g. "master", "rascal", "asterisk"
        if len(phones) >= i + 4:
            if (phones[i + 1] == 'S' and
                phones[i + 2] in ['P', 'T', 'K'] and
                phoneset[phones[i + 3].rstrip('012')].cvox == '0'):
                if lex[-3:] not in ["ING", "IN'"]:  # exclude final "-ing"/"-in'" words, e.g. "asking"
                    return 'aeBR'
        # following front nasals, voiceless fricatives
        if fol in ['M', 'N', 'S', 'TH', 'F']:
            # tensing consonants word-finally
            if phones[i + 2] == '#':
                if lex in ['MATH']:
                    return 'aeBR'
                return 'aeh'  # e.g. "man", "ham"
            # tensing consonants NOT word-finally
            else:
                # AE1 ['M', 'N', 'S', 'TH', 'F'] followed by another consonant
                # (e.g. "hand", "classroom")
                if ((phoneset[phones[i + 2].rstrip('012')].cvox != '0') and
                     lex not in ['CATHOLIC', 'CATHOLICS', 'CAMERA']):
                    return 'aeh'
                # AE1 ['M', 'N', 'S', 'TH', 'F'] followed by a vowel
                else:
                    # following suffixes -ing, -in', -es ("manning")
                    if len(phones) > i + 4:
                        a = phones[i + 2]
                        b = phones[i + 3]
                        ab = [a, b]
                        # print "Suffix for word %s is %s." % (trans, ab)
                        if (phones[i+4] == '#' and
                            ab in [['IH0', 'NG'],
                                   ['AH0', 'NG'],
                                   ['AH0', 'N'],
                                   ['AH0', 'Z']]):
                            return 'aeh'
                        # all other cases
                        else:
                            return 'aeBR'
                    else:
                        return 'aeBR'

    # convert dictionary entries to short-a for "-arry" words
    if curcode == 'e' and 'ARRY' in lex:
        if len(phones) >= i + 3:
            if (phones[i + 1] == 'R' and 
                phoneset[phones[i + 2].rstrip('012')].cvox == '0'):
                return 'aeBR'

    # random dictionary inaccuracies
    if curcode == 'o' and lex == 'MARIO':
        return 'ae'

    # 2. /e/
    if lex in ["CATCH", "KEPT"]:
        return 'e'

    # 3. /oh/
    if (vowel == 'AA' and 
        lex in ['LAW', 'LAWS', "LAW'S", 'LAWFUL', 'UNLAWFUL', 'DOG', 'DOGS',
                "DOG'S", 'DOGGED', 'ALL', "ALL'S", 'CALL', 'CALLS', "CALL'S",
                'CALLING', 'CALLED', 'FALL', 'FALLS', "FALL'S", 'FALLING'
                'AUDIENCE', 'AUDIENCES', "AUDIENCE'S", 'ON', 'ONTO', 'GONNA',
                'GONE', 'BOSTON', "BOSTON'S", 'AWFUL', 'AWFULLY', 'AWFULNESS',
                'AWKWARD', 'AWKWARDLY', 'AWKWARDNESS', 'AWESOME', 'AUGUST',
                'COUGH', 'COUGHS', 'COUGHED', 'COUGHING']):
        return 'oh'

    # 4. /o/
    if (vowel == 'AO' and 
        lex in ['CHOCOLATE', 'CHOCOLATES', "CHOCOLATE'S", 'WALLET', 'WALLETS',
                'WARRANT', 'WARRANTS', 'WATCH', 'WATCHES', 'WATCHED',
                'WATCHING', 'WANDER', 'WANDERS', 'WANDERED', 'WANDERING',
                'CONNIE', 'CATHOLICISM', 'WANT', 'WANTED', 'PONG', 'GONG',
                'KONG', 'FLORIDA', 'ORANGE', 'HORRIBLE', 'MAJORITY']):
        return 'o'

    if vowel == 'AE' and lex in ['LANZA', "LANZA'S"]:
        return 'o'

    # 5. /iw/
    if phone == "UW1":
        # UW1 preceded by /y/
        if phones[i - 1] == 'Y':
            return 'iw'
        # words spelled with "-ew", e.g. "threw", "new", "brew"
        if 'EW' in lex:
            return 'iw'
        # words spelled with "-u" after /t/, /d/, /n/, /l/, /s/, e.g.
        # "Tuesday", "nude", "duty", "new"
        if phones[i - 1] in ['T', 'D', 'N', 'L', 'S']:
            for t in ['TU', 'DU', 'NU', 'LU', 'SU']:  # make sure -u spelling is adjacent to consonant in orthography
                if t in lex:
                    return 'iw'

    # 6. /Tuw/
    if phone == "UW1" and lex in ['THROUGH']:
        return 'Tuw'

    # 7. front vowels before r
    if vowel in ['EH', 'AE'] and phones[i + 1] == 'R':
        if phones[i+2] == '#':  # word-final /r/
            return 'eyr'
        if len(phones) >= i + 2:
            if phoneset[phones[i + 2].rstrip('012')].cvox != '0':  # not word-final but also NOT intervocalic r
                return 'eyr'
    return curcode

def convert_vowel(ortho, phones,  prec, i, fol, phoneset):
    """Converts Arbabet vowel to plotnik notation"""
    phone = phones[i]
    vowel = phone.rstrip('012')
    stress = phone[-1]
    lex = ortho.upper()
    if fol == '#' and vowel in ['IY', 'EY', 'OW']:
        newvowel = vowel.lower()+'F'
    elif phoneset[fol].cvox == '-' and vowel == 'AY':
        newvowel = "ay0"
    elif vowel == 'AA' and lex in INGLIDERS:
        newvowel = "ah"
    elif vowel == 'UW' and phoneset[prec].cplace == 'a':
        newvowel = 'Tuw'
    elif vowel != 'ER' and phoneset[fol].ctype == 'r':
        newvowel = A2P_R[vowel]
    elif vowel == 'AH' and stress == '0':
        newvowel = "@"
    else:
        newvowel = A2P[vowel]
    return philadelphia_postconversion(lex=lex,
                                       phones=phones,
                                       prec=prec,
                                       i=i,
                                       fol=fol,
                                       curcode=newvowel,
                                       phoneset=phoneset)


def convert_phones(ortho, phones, phoneset):
    """For each phone determines if it is a vowel and converts it and maintains
    the consonants"""
    newphones = []
    for i in range(1, len(phones) - 1):
        phone = phones[i]
        if phone.rstrip('012') in VOWELS:
            vowel = convert_vowel(ortho=ortho,
                                  phones=phones,
                                  prec=phones[i - 1].rstrip('012'),
                                  i=i,
                                  fol=phones[i + 1].rstrip('012'),
                                  phoneset=phoneset)
            newphones.append(vowel+'.'+phone[-1])
        else:
            newphones.append(phone)
    return newphones


def convert_line(myline, phoneset):
    """Converts each line to include Plotnik style vowels"""
    sline = myline.rstrip().split()
    ortho = sline[0]
    phones = convert_phones(ortho, ['#'] + sline[1:] + ['#'], phoneset)
    return ortho + ' ' + ' '.join(phones) + '\n'


if __name__ == '__main__':
    phoneset = read_phoneset('cmu_phoneset.txt')
    infile = open('cmudict.dict')
    outfile = open('cmudict-plotnik.dict', 'w')
    for line in infile:
        outfile.write(convert_line(line, phoneset))
