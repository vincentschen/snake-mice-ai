echo "TEST NOTE: Preliminary test of everything..."
python game.py -s greedy -n 1 -q
python game.py -s oracle -n 1 -q
python game.py -s expectimax -n 1 -d 2 -e a -q
python game.py -s expectimax -n 1 -d 2 -e b -q
python game.py -s expectimax -n 1 -d 2 -e c -q
python game.py -s minimax -n 1 -d 2 -e b -q
python game.py -s alphabeta -n 1 -d 2 -e b -q
echo "DONE!"