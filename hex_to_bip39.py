# "KztFe4CmMZWeEhbB3oZd1VzzViHak8iqvEmf15RSmrHaW7oLTgEw"
# 1N3feJzxzvSsthqzNYeBk3Mp8xeqYrUSDj

import md5
import errno
import sys
import getpass
import third_party.ianoxley.base58 as base58

WORDLIST_DIR    = "third_party/bip39_wordlist"
WORDLIST_EN     = "english.txt"
WORDLIST_EN_MD5 = "2a80fc2c95f3a4b0a5769764df251820"
WORDLIST_COUNT  = 2048

def init_words(wordlist_file, wordlist_md5):
    strings = []
    try:
        with open(wordlist_file) as f:
            strings = f.readlines()
        strings = [x.strip() for x in strings]
    except IOError as e:
        msg = "Unable to load wordlist file \"%s\"" % wordlist_file
        if e.errno == errno.ENOENT:
            print msg, "- file does not exist"
        elif e.errno == errno.EACCES:
            print msg, "- file cannot be opened"
        else:
            print msg, "- error ", e.errno
        return []
    # Verify word count
    if len(strings) != WORDLIST_COUNT:
        print "Wordlist file \"%s\" appears to be corrupted" % wordlist_file
        return []
    # Verify MD5
    m = md5.new()
    for s in strings:
        m.update(s)
    if m.hexdigest() != wordlist_md5:
        print "Wordlist file \"%s\" appears to be corrupted" % wordlist_file
        return []
    return strings

def encode(s, words):
    encoded = []
    while s > 0:
        encoded += [words[s % len(words)]]
        s /= len(words)
    return encoded

def decode(w, words):
    decoded = 0L
    lookup = {k: v for v, k in enumerate(words)}
    while w != []:
        decoded *= len(words)
        decoded += lookup[w.pop()]
    return decoded

def print_words(words):
    for i in range(0,len(words)):
        print "%02d: %-20s" % (i+1, words[i])

def main():
    words = init_words(WORDLIST_DIR + "/" + WORDLIST_EN, WORDLIST_EN_MD5)
    if words == []:
        return -1
    print " === BITCOIN PRIVATE KEY TO WORDLIST CONVERSION UTILITY === "
    print ""
    print " IMPORTANT NOTE:"
    print ""
    print "    Before using this utility with a live private key, ensure the"
    print "    following steps have been taken:"
    print "    1) Disconnect from the internet."
    print "    2) Make sure that you are alone, on a machine that you own, in a private"
    print "       place (i.e. somewhere no-one can see your screen)"
    print "    3) Do NOT store the output of this program in a file on an internet-"
    print "       capable machine. Remember that even deleting the file is not enough"
    print "       to remove the key completely from disk."
    print ""
    print "    For the paranoid:"
    print "    1) Only run this application on a system that has never been, and never"
    print "       will be, attached to the internet."
    print "    2) Boot into a secure memory-only OS, such as Tails"
    print "    3) Do not print the output of this program, as most modern printers contain"
    print "       non-volatile storage and can connect to the internet."
    print "    4) When coping by hand onto paper, make sure that pen imprints do not"
    print "       transfer to pages below."
    print ""
    print "    THE AUTHOR OF THIS APPLICATION CAN ACCEPT NO LIABILITY IF DATA HAS BEEN"
    print "    COMPROMISED. USE THIS APPLICATION AT YOUR OWN RISK."
    print ""
    raw_input("PRESS ENTER TO AGREE AND PROCEED")
    keytype = -1
    while keytype < '1' or keytype > '3':
        print "Please enter the input key type:"
        print "  1. Base58   (Contains all upper- and lower-case characters as well as digits)"
        print "  2. Hex      (Only contains digits and the characters A-F)"
        print "  3. Wordlist (A series of English words)"
        keytype = raw_input("> ")
    if keytype == '1':
        key = 0
        while key <= 0:
           inkey = raw_input("Please enter the private key: ")
           inkey = inkey.strip()
           try:
              key = base58.decode(inkey)
           except:
              print "Bad BASE58 Key!"
              key = 0
    if keytype == '2':
        key = 0
        while key <= 0:
           inkey = raw_input("Please enter the private key: ")
           inkey = inkey.strip()
           try:
              key = int(inkey, 16)
           except:
              print "Bad HEX Key!"
              key = 0
    if keytype == '3':
        phrase = []
        while phrase == []:
            word = None
            lookup = {k: v for v, k in enumerate(words)}
            while word == None:
                word = raw_input("Word %02d: (BLANK for END): " % (len(phrase) + 1))
                if word == "":
                    break
                else:
                    if word.lower() in lookup:
                        phrase += [word.lower()]
                        word = None
                    else:
                        print "Bad word, try again."
                        word = None
    print "VERIFY that the key you entered is correct"
    print ""
    if keytype == '1':
        print "*** %s ***" % base58.encode(key)
    elif keytype == '2':
        print "*** %s ***" % hex(key)
    else:
        print_words(phrase)
    print ""
    raw_input("Press ENTER to confirm, or CTRL+C to cancel")
    
    if keytype == '1' or keytype == '2':
        print "The following is the wordlist that corresponds to this private key:"
        print_words(encode(key, words))
    else:
        print "The following is the private key that corresponds to the wordlist just entered:"
        print ""
        print "*** %s ***" % base58.encode(decode(phrase, words))
    print ""
    print "If this is your first time encoding/decoding, it is recommended that you run this"
    print "utility again in reverse in order to verify this data."
    print ""
    raw_input("Please copy this information somewhere private. Press ENTER once done.")
    print "Complete!"
    return 0
        
if __name__ == '__main__':
  main()
