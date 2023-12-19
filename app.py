# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/minimize', methods=['POST'])
def minimize_dfa():
    data = request.get_json()
    num_states = len(data)
    num_alphabets = len(data[0])

    alphabet = []
    transition_table = []

    for i in range(1, num_alphabets + 1):
        alphabet.append(data[0][str(i)])

    for i in range(1, num_states):
        row = []
        for j in range(1, num_alphabets + 1):
            row.append(data[i][str(j)])
        transition_table.append(row)

    # Implement Hopcroft's algorithm for DFA minimization
    def hopcroft_minimization(alphabet, transition_table):
        # Step 1: Initialize partitions
        partitions = [set(range(num_states))]
        final_partitions = []

        # Step 2: Split states into initial partitions based on final and non-final states
        final_states = set()
        non_final_states = set()

        for state in range(num_states):
            if state in final_states:
                final_states.add(state)
            else:
                non_final_states.add(state)

        if final_states:
            partitions.append(final_states)
        if non_final_states:
            partitions.append(non_final_states)

        # Step 3: Refine partitions until no further refinement is possible
        while partitions != final_partitions:
            final_partitions = partitions.copy()
            partitions = []

            for partition in final_partitions:
                for symbol in alphabet:
                    split = False
                    new_partitions = []

                    for state in partition:
                        target_state = int(transition_table[state][alphabet.index(symbol)])

                        for index, new_partition in enumerate(new_partitions):
                            if target_state in new_partition:
                                new_partitions[index].add(state)
                                split = True
                                break

                        if not split:
                            new_partitions.append(set([state]))

                    if len(new_partitions) > 1:
                        partitions.extend(new_partitions)
                    else:
                        partitions.append(partition)

        return partitions

    # Perform DFA minimization using Hopcroft's algorithm
    minimized_partitions = hopcroft_minimization(alphabet, transition_table)

    # Return the minimized partitions as JSON response
    return jsonify(minimized_partitions)

if __name__ == '__main__':
    app.run(debug=True)
