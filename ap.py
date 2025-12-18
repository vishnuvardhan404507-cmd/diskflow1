from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def solve_disk(algo, head, tracks_str):
    try:
        tracks = [int(x.strip()) for x in tracks_str.split(',') if x.strip()]
    except: return [head], 0
    
    head, size = int(head), 200
    sequence = [head]
    
    if algo == "FCFS": sequence += tracks
    elif algo == "SSTF":
        temp = tracks.copy()
        curr = head
        while temp:
            closest = min(temp, key=lambda x: abs(x - curr))
            sequence.append(closest); temp.remove(closest); curr = closest
    elif algo in ["SCAN", "LOOK"]:
        tracks.sort()
        left = [x for x in tracks if x < head][::-1]
        right = [x for x in tracks if x >= head]
        sequence += left + ([0] if algo == "SCAN" else []) + right
    elif algo in ["CSCAN", "CLOOK"]:
        tracks.sort()
        right = [x for x in tracks if x >= head]
        left = [x for x in tracks if x < head]
        sequence += right + ([size - 1, 0] if algo == "CSCAN" else []) + left

    dist = sum(abs(sequence[i] - sequence[i+1]) for i in range(len(sequence)-1))
    return sequence, dist

@app.route('/')
def index(): return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    d = request.json
    s, ds = solve_disk(d['algo'], d['head'], d['tracks'])
    return jsonify({'sequence': s, 'distance': ds})

@app.route('/developers')
def developers(): return render_template('inf.html')

@app.route('/solutions')
def solutions(): return render_template('solutions.html')

if __name__ == '__main__': app.run(debug=True)