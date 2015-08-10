import sys
import time
from blessings import Terminal


def slowprint(str_val, delay=0.15):
    str_val = str_val.strip()
    for i in str_val:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(delay)


def main():
    term = Terminal()
    letters_q = []
    i = 0
    while True:
        i += 1
        line = sys.stdin.readline()
        if len(line) == 0: continue
        if i%5 == True and "sync_idx" in line:
            sys.stdout.write('\n')
            slowprint('Acquiring Signal...', delay=.05)
        if "Sync" in line:
            sys.stdout.write('\n\t\t\t\t')
            print term.green
            slowprint('Acquired.',delay=0.2)
        if line[0] == '$':
            letters_q.append(line[1])
            if line[1] == '@':
                print term.green
                sys.stdout.write('\n\t\t\t\tintercept> ')
                sys.stdout.flush()
                
                slowprint(''.join(letters_q)[:-1], delay=0.05)
                letters_q = []
        elif line[0] == '@':
	    
            print term.white
            sys.stdout.write("%f" % time.time())
            slowprint("~] " + line[1:], delay=0.05)


if __name__ == "__main__":
    print 'hi'
    main()
