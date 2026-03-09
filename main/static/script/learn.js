

function init(){
    const value = document.getElementById('select_mode').value;
    yeet_popup();
    switch(value) {
        case 'reverse':
            run_default(reverse=true);
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
        if (index !== 0 && answer.value !== words[index-1][reverse ? 'w' : 't']) return
        // maybe add feedback for being correct / incorrect
        if (index < words.length) document.getElementById('vocab').innerHTML = words[index][reverse ? 't' : 'w'];
        answer.value = '';
        index++;
    }
    answer.addEventListener('keydown', (event) => {
        if (event.keyCode !== 13) return;
        update();
    });
    update();
}