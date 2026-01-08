document.getElementById("loanForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = Object.fromEntries(new FormData(e.target));

  const res = await fetch("/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();

  document.getElementById("result").textContent = result.result;
  document.getElementById("score").textContent = result.score + "%";
  document.getElementById("suggestion").textContent = result.suggestion;

  const angle = result.score * 1.8 - 90;
  document.getElementById("needle").style.transform = `rotate(${angle}deg)`;

  const badge = document.getElementById("approval");
  if (result.isEligible) badge.classList.remove("hidden");
  else badge.classList.add("hidden");
});
