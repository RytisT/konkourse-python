find -name '*.jpg' | # find jpegs
gawk 'BEGIN{ a=1 }{ printf "mv %s %04d.jpg\n", $0, a++ }' | # build mv command
bash # run that command
