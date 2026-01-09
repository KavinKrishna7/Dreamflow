function toggleTheme() {
    document.body.classList.toggle('light');
    document.body.classList.toggle('dark');
    const btn = document.querySelector('.theme-toggle');
    btn.textContent = document.body.classList.contains('light') ? '☀️' : '🌙';
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('loanForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const res = await fetch('/check', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await res.json();

            const resultDiv = document.getElementById('result');
            resultDiv.textContent = result.result;
            resultDiv.className = `result ${result.isEligible ? 'success' : 'fail'}`;
            resultDiv.classList.remove('hidden');

            document.getElementById('meterWrapper').classList.remove('hidden');
            document.getElementById('scoreValue').textContent = result.score + '%';
            document.getElementById('suggestion').textContent = result.suggestion;

            const angle = (result.score * 1.8) - 90;
            document.getElementById('needle').style.transform = `rotate(${angle}deg)`;

            const badge = document.getElementById('approvalBadge');
            badge.classList.toggle('hidden', !result.isEligible);

            document.getElementById('meterWrapper').scrollIntoView({ behavior: 'smooth' });

        } catch (err) {
            alert("Something went wrong. Please try again.");
        }
    });
});

