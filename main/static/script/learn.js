

function init(){
    const value = document.getElementById('select_mode').value;
    yeet_popup();
    switch(value) {
        case 'reverse':
            run_default(reverse=true);
            break;
        default:
            run_default();
    }
}

function run_default(reverse=false) {
    const answer = document.getElementById('answer');
    const input = document.getElementById('input');
    const count = document.getElementById('count');
    count.innerHTML = '0';
    document.getElementById('total').innerHTML = words.length;
    let index = 0;
    let value = 1;
    let update = function () {
        if (index > words.length) return;
        // check if answer is correct, else return
        if (index !== 0) {
            word = reverse ? [words[index-1]['w']] : words[index-1]['t']
            if (!word.includes(answer.value)) {
                value = 0;
                if (input.querySelector('#idk-button') == null) {
                    let idk_button = document.createElement('button');
                    idk_button.id = 'idk-button';
                    idk_button.innerHTML = "I don't know";
                    idk_button.addEventListener('click', () => {
                        input.removeChild(idk_button);
                        let p = document.createElement('p');
                        let ok_button = document.createElement('button');
                        p.innerHTML = "'" + document.getElementById('vocab').innerHTML + "' means '" + word[0] + "'!";
                        ok_button.innerHTML = 'proceed';
                        ok_button.addEventListener('click', () => { yeet_popup(); answer.value = word[0]; update(); });
                        popup([p, ok_button], enable_close=false);
                    });
                    input.appendChild(idk_button);
                }
                feedback(correct=false);
                return;
            }
            count.innerHTML = parseInt(count.innerHTML) + value;
            if (input.querySelector('#idk-button') != null) input.removeChild(document.getElementById('idk-button'));
            feedback();
        }
        // maybe add feedback for being correct / incorrect
        if (index < words.length) {
            document.getElementById('vocab').innerHTML = (reverse ? words[index]['t'][0] : words[index]['w']);
            note = words[index][reverse ? 'note-t' : 'note'];
            document.getElementById('notes').innerHTML = note ? note : '';
        }
        else { // when the thing is done
            answer.disabled = 'true';
            let title = document.createElement('h3');
            let text = document.createElement('p');
            title.innerHTML = 'You did it!';
            text.innerHTML = 'You managed to get ' + count.innerHTML + ' out of ' + words.length + ' words right!';
            popup([title, text]);
        }
        value = 1;
        answer.value = '';
        index++;
    }
    answer.addEventListener('keydown', (event) => {
        if (event.keyCode !== 13) return;
        update();
    });
    update();
}

function feedback(correct=true) {
    label = document.getElementById('input');
    label.classList.remove(correct ? 'incorrect' : 'correct');
    label.classList.add(correct ? 'correct' : 'incorrect');
    setTimeout(() => { label.classList.remove(correct ? 'correct' : 'incorrect'); }, correct ? 300 : 1000);
}