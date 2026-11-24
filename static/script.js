document.addEventListener('DOMContentLoaded', () => {
    const choices = document.querySelectorAll('.choice');
    const resultDiv = document.getElementById('result');
    const scoreDiv = document.getElementById('score');
    const favouriteDiv = document.getElementById('favourite');

    choices.forEach(choice => {
        choice.addEventListener('click', () => {
            const userChoice = choice.getAttribute('data-choice');
            fetch('/play', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ choice: userChoice }),
            })
            .then(response => response.json())
            .then(data => {
                const { user_choice, computer_choice, result,
                        user_score, computer_score, favourite } = data;
                resultDiv.innerHTML = `You chose ${user_choice}, computer chose ${computer_choice}. You ${result}!`;
                scoreDiv.innerHTML = `${user_score} : ${computer_score}`;
                favouriteDiv.innerHTML = favourite ? `Your favourite: ${favourite}` : '';

                resultDiv.classList.remove('win', 'lose', 'draw');
                void resultDiv.offsetWidth;
                resultDiv.classList.add(result);
            });
        });
    });
});