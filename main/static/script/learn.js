

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
    let index = 0;
    let update = function () {
        if (index > words.length) return;
        // check if answer is correct, else return
        if (index !== 0 && !(reverse ? [words[index-1]['w']] : words[index-1]['t']).includes(answer.value)) return;
        // maybe add feedback for being correct / incorrect
        if (index < words.length) document.getElementById('vocab').innerHTML = (reverse ? words[index]['t'][0] : words[index]['w']);
        answer.value = '';
        index++;
    }
    answer.addEventListener('keydown', (event) => {
        if (event.keyCode !== 13) return;
        update();
    });
    update();
}